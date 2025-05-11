# -*- coding: utf-8 -*-


from collections.abc import Iterable
from typing import cast

from flask import current_app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from marshmallow import Schema
from marshmallow import fields

from .bp import bp
from ..utils import validate_json_arguments
from ...api import APIArgumentError
from ...api import APIException
from ...api import APIResult
from ...api import AccountNotFound
from ...api import DisabledAccount
from ...api import GetAccounts
from ...api import LoginSuccess
from ...api import LogoutSuccess
from ...api import RequestSuccess
from ...api import Unauthorized
from ...api import WrongUsernameOrPassword
from ...api import api
from ...extensions import db
from ...extensions import jwt_redis_blocklist
from ...models.auth import Role
from ...models.auth import User
from ...permission import PERMISSIONS
from ...permission import passed_permissions
from ...permission import permissions_required


class UserLoginSchema(Schema):
    username = fields.String(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False)


@bp.route("/login", methods=["POST"])
@api
def login() -> APIResult:
    data = validate_json_arguments(UserLoginSchema)
    user = User.query.filter_by(username=data["username"]).first()

    if (user is None) or (not user.verify_password(data["password"])):
        return WrongUsernameOrPassword()

    if not user.active:
        return DisabledAccount()

    access_token = create_access_token(identity=user.id)
    return LoginSuccess(access_token=access_token)


@bp.route("/logout", methods=["POST"])
@jwt_required()  # type: ignore[misc]
@api
def logout() -> APIResult:
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])
    return LogoutSuccess()


@bp.route("/whoami", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
def whoami() -> APIResult:
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return Unauthorized()
    return GetAccounts(
        accounts=[dict(id=user.id, username=user.username, roles=[r.name for r in user.roles], active=user.active)])


class AccountsFilterSchema(Schema):
    username = fields.String(allow_none=True)
    active = fields.Boolean(allow_none=True)
    roles = fields.List(fields.String(allow_none=False), allow_none=True)


@bp.route("/accounts", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.ACCOUNT.GET])
def get_accounts() -> APIResult:
    data = validate_json_arguments(AccountsFilterSchema, optional=True)

    accounts: list[User]
    if not data:
        accounts = User.query.all()
    else:
        query = User.query
        if data.get("username") is not None:
            query = query.filter(User.username.like(f"%{data['username']}%"))
        if data.get("active") is not None:
            query = query.filter(User.active == data["active"])
        if data.get("roles") is not None:
            query = query.filter(User.roles.any(Role.name.in_(data["roles"])))
        accounts = query.all()

    return GetAccounts(accounts=[
        dict(id=v.id, username=v.username, roles=[r.name for r in cast(Iterable[Role], v.roles)], active=v.active) for v
        in accounts])


@bp.route("/accounts/<int:account_id>", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.ACCOUNT.GET])
def get_account(account_id: int) -> APIResult:
    account = User.query.filter_by(id=account_id).first()
    if account is None:
        return AccountNotFound()
    return GetAccounts(
        accounts=[dict(id=v.id, username=v.username, roles=[r.name for r in v.roles], active=v.active) for v in
                  [account]])


class UserCreateSchema(Schema):
    username = fields.String(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False)

    roles = fields.List(fields.String(allow_none=False), required=True, allow_none=False)
    active = fields.Boolean(required=True, allow_none=False)


def validation_username(username: str) -> None:
    messages: list[str] = []
    if len(username) < 3:
        messages.append("username must be at least 3 characters long")
    if len(username) > 16:
        messages.append("username must be at most 16 characters long")
    # if not re.match(r"^[a-zA-Z0-9_]+$", username):
    #     messages.append("username must contain only letters, numbers, and underscores")

    if messages:
        raise APIException(APIArgumentError(arguments={"username": messages}))


def validation_password(password: str) -> None:
    messages: list[str] = []
    if len(password) < 6:
        messages.append("password must be at least 6 characters long")
    if len(password) > 16:
        messages.append("password must be at most 16 characters long")
    # if not re.search(r"[a-z]", password):
    #     messages.append("password must contain at least one lowercase letter")
    # if not re.search(r"[A-Z]", password):
    #     messages.append("password must contain at least one uppercase letter")
    # if not re.search(r"[0-9]", password):
    #     messages.append("password must contain at least one digit")
    # if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
    #     messages.append("password must contain at least one special character")

    if messages:
        raise APIException(APIArgumentError(arguments={"password": messages}))


@bp.route("/accounts", methods=["POST"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.ACCOUNT.CREATE])
def create_account() -> APIResult:
    data = validate_json_arguments(UserCreateSchema)
    validation_username(data["username"])
    validation_password(data["password"])

    if User.query.filter_by(username=data["username"]).first() is not None:
        return APIArgumentError(arguments={"username": ["username already exists"]})

    for role_name in data["roles"]:
        role = Role.query.filter_by(name=role_name).first()
        if role is None:
            return APIArgumentError(arguments={"roles": ["role not found"]})

    user = User.create(**data)
    user.active = data["active"]
    db.session.add(user)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return RequestSuccess()


class UserUpdateSchema(Schema):
    username = fields.String(allow_none=True)
    password = fields.String(allow_none=True)

    roles = fields.List(fields.String(allow_none=False), allow_none=True)
    active = fields.Boolean(allow_none=True)


class UserUpdateSelfPasswordSchema(Schema):
    password = fields.String(allow_none=False)


@bp.route("/accounts/<int:account_id>", methods=["PUT"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.ACCOUNT.UPDATE, PERMISSIONS.ACCOUNT.UPDATE_SELF_PASSWORD, ], strategy=any)
def update_account(account_id: int) -> APIResult:
    user: User | None = User.query.filter_by(id=account_id).first()

    if user is None:
        return AccountNotFound()

    fully_permission = PERMISSIONS.ACCOUNT.UPDATE in passed_permissions
    data = validate_json_arguments(UserUpdateSchema if fully_permission else UserUpdateSelfPasswordSchema)

    if data.get("username") is not None:
        validation_username(data["username"])
        user.username = data["username"]
    if data.get("password") is not None:
        validation_password(data["password"])
        user.password = data["password"]
    if data.get("roles") is not None:
        new_roles = []
        for role_name in data["roles"]:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                return APIArgumentError(arguments={"roles": ["role not found"]})
            new_roles.append(role)
        user.roles = new_roles  # type: ignore[assignment]
    if data.get("active") is not None:
        user.active = data["active"]

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return RequestSuccess()


@bp.route("/accounts/<int:account_id>", methods=["DELETE"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.ACCOUNT.DELETE])
def delete_account(account_id: int) -> APIResult:
    user = User.query.filter_by(id=account_id).first()
    if user is None:
        return AccountNotFound()
    db.session.delete(user)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return RequestSuccess()
