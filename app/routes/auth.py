# -*- coding: utf-8 -*-


from collections.abc import Iterable
from collections.abc import Mapping
from collections.abc import Sequence
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any
from typing import cast

from flask import Blueprint
from flask import Flask
from flask import Response
from flask import current_app
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from marshmallow import Schema
from marshmallow import ValidationError
from marshmallow import fields

from ..api import APIArgumentError
from ..api import APIResult
from ..api import AccountNotFound
from ..api import GetAccounts
from ..api import GetPermissions
from ..api import GetRoles
from ..api import LoginSuccess
from ..api import LogoutSuccess
from ..api import RequestSuccess
from ..api import Unauthorized
from ..api import WrongUsernameOrPassword
from ..api import api
from ..extensions import db
from ..extensions import jwt
from ..extensions import jwt_redis_blocklist
from ..models.auth import Permission
from ..models.auth import Role
from ..models.auth import User
from ..permission import PERMISSIONS
from ..permission import permissions_required


class UserLoginSchema(Schema):
    username = fields.String(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False)


bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
@api
def login() -> APIResult:
    schema = UserLoginSchema()
    try:
        data = schema.load(cast(Mapping[str, Any] | Sequence[Mapping[str, Any]], request.json))
    except ValidationError as e:
        return APIArgumentError(arguments=e.messages)
    user = User.query.filter_by(username=data["username"]).first()

    if (user is None) or (not user.verify_password(data["password"])) or (not user.active):
        return WrongUsernameOrPassword()
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
    return GetAccounts(accounts=[
        dict(id=user.id, username=user.username, roles=[r.name for r in user.roles], active=user.active)
    ])


@bp.route("/accounts", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.ACCOUNT.GET])
def get_accounts() -> APIResult:
    accounts: list[User] = User.query.all()
    return GetAccounts(accounts=[
        dict(
            id=v.id,
            username=v.username,
            roles=[
                r.name for r in cast(Iterable[Role], v.roles)
            ],
            active=v.active
        ) for v in accounts
    ])


@bp.route("/accounts/<int:account_id>", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.ACCOUNT.GET])
def get_account(account_id: int) -> APIResult:
    account = User.query.filter_by(id=account_id).first()
    if account is None:
        return AccountNotFound()
    return GetAccounts(accounts=[
        dict(id=v.id, username=v.username, roles=[r.name for r in v.roles], active=v.active) for v in [account]
    ])


class UserCreateSchema(Schema):
    username = fields.String(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False)

    roles = fields.List(fields.String(required=True, allow_none=False), required=True, allow_none=False)
    active = fields.Boolean(required=True, allow_none=False)


@bp.route("/accounts", methods=["POST"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.ACCOUNT.CREATE])
def create_account() -> APIResult:
    schema = UserCreateSchema()
    try:
        data = schema.load(cast(Mapping[str, Any] | Sequence[Mapping[str, Any]], request.json))
    except ValidationError as e:
        return APIArgumentError(arguments=e.messages)

    if User.query.filter_by(username=data["username"]).first() is not None:
        return APIArgumentError(arguments={'username': ['username already exists']})

    user = User.create(
        username=data["username"],
        password=data["password"],
        roles=data["roles"],
    )
    user.active = data["active"]
    db.session.add(user)
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


@bp.route("/roles", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.ROLE.GET])
def get_roles() -> APIResult:
    roles: list[Role] = Role.query.all()
    return GetRoles(roles=[
        dict(id=v.id, name=v.name, description=v.description) for v in roles
    ])


@bp.route("/permissions", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.PERMISSION.GET])
def get_permissions() -> APIResult:
    permissions: list[Permission] = Permission.query.all()
    return GetPermissions(permissions=[
        dict(id=v.id, name=v.name, description=v.description) for v in permissions
    ])


def initialize_hooks(app: Flask) -> None:
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(_jwt_header: dict[str, Any], jwt_payload: dict[str, Any]) -> bool:
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None

    @jwt.user_identity_loader
    def user_identity_lookup(user: User | int | str) -> str:
        if isinstance(user, User):
            return str(user.id)
        return str(user)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header: dict[str, Any], jwt_data: dict[str, Any]) -> User | None:
        identity = jwt_data["sub"]
        return cast(User | None, User.query.filter_by(id=identity).one_or_none())

    @jwt.user_lookup_error_loader
    @api
    def user_lookup_error_callback(*_: Any) -> APIResult:
        return Unauthorized()

    @app.after_request
    def refresh_expiring_jwts[R: Response](response: R) -> R:
        try:
            jwt_info = get_jwt()
        except RuntimeError:
            return response
        if not jwt_info:
            return response

        exp_timestamp = jwt_info["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response


__all__ = (
    "bp",
    "initialize_hooks",
)
