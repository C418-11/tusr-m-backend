# -*- coding: utf-8 -*-


from flask_jwt_extended import jwt_required
from marshmallow import Schema
from marshmallow import fields

from .bp import bp
from ..utils import validate_json_arguments
from ...api import APIArgumentError
from ...api import APIResult
from ...api import GetRoles
from ...api import RequestSuccess
from ...api import api
from ...extensions import db
from ...models.auth import Permission
from ...models.auth import Role
from ...permission import PERMISSIONS
from ...permission import permissions_required


class RolesFilterSchema(Schema):
    name = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    permissions = fields.List(fields.String(allow_none=False), allow_none=True)


@bp.route("/roles", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.ROLE.GET])
def get_roles() -> APIResult:
    data = validate_json_arguments(RolesFilterSchema, optional=True)

    roles: list[Role]
    if not data:
        roles = Role.query.all()
    else:
        query = Role.query
        if data.get("name") is not None:
            query = query.filter(Role.name.like(f"%{data['name']}%"))
        if data.get("description") is not None:
            query = query.filter(Role.description.like(f"%{data['description']}%"))
        if data.get("permissions") is not None:
            query = query.filter(Role.permissions.any(Permission.name.in_(data["permissions"])))
        roles = query.all()

    return GetRoles(roles=[dict(id=v.id, name=v.name, description=v.description) for v in roles])


class RoleCreateSchema(Schema):
    name = fields.String(required=True, allow_none=False)
    description = fields.String(required=True, allow_none=False)
    permissions = fields.List(fields.String(required=True, allow_none=False), required=True, allow_none=False)


@bp.route("/roles", methods=["POST"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.ROLE.CREATE])
def create_role() -> APIResult:
    data = validate_json_arguments(RoleCreateSchema)

    if Role.query.filter_by(name=data["name"]).first() is not None:
        return APIArgumentError(arguments={"name": ["name already exists"]})

    for permission_name in data["permissions"]:
        permission = Permission.query.filter_by(name=permission_name).first()
        if permission is None:
            return APIArgumentError(arguments={"permissions": ["permission not found"]})

    role = Role.create(**data)
    db.session.add(role)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return RequestSuccess()
