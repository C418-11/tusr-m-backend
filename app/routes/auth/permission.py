# -*- coding: utf-8 -*-


from flask_jwt_extended import jwt_required
from marshmallow import Schema
from marshmallow import fields

from .bp import bp
from ..utils import JSONLike
from ..utils import validate_json_arguments
from ...api import APIResult
from ...api import GetPermissions
from ...api import api
from ...models.auth import Permission
from ...permission import PERMISSIONS
from ...permission import permissions_required


class PermissionsFilterSchema(Schema):
    name: str = fields.String(allow_none=True)  # type: ignore[assignment]
    description: str = fields.String(allow_none=True)  # type: ignore[assignment]


@bp.route("/permissions", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.PERMISSION.GET])
def get_permissions() -> APIResult:
    data: JSONLike = validate_json_arguments(PermissionsFilterSchema, optional=True)

    permissions: list[Permission]
    if data:
        query = Permission.query
        if data.get("name") is not None:
            query = query.filter(Permission.name.like(f"%{data['name']}%"))
        if data.get("description") is not None:
            query = query.filter(Permission.description.like(f"%{data['description']}%"))
        permissions = query.all()
        return GetPermissions(permissions=[dict(id=v.id, name=v.name, description=v.description) for v in permissions])

    permissions = Permission.query.all()
    return GetPermissions(permissions=[dict(id=v.id, name=v.name, description=v.description) for v in permissions])
