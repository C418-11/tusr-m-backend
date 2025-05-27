# -*- coding: utf-8 -*-


import ast
import re

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from ...api import APIArgumentError
from ...api import DataTableNotFound
from ...api import GetRows
from ...api import GetTables
from ...api import RequestSuccess
from ...api import api
from ...extensions import db
from ...model_utils import BaseModel
from ...model_utils.utils import ColumnInfo
from ...models.data import EDITABLE_TABLE_NAMES
from ...permission import PERMISSIONS
from ...permission import permissions_required

bp = Blueprint("data", __name__)

COLUMN_INFO: dict[str, dict[str, ColumnInfo]] = BaseModel.get_columns_info()  # type: ignore[assignment]
NAME2TABLE: dict[str, type[BaseModel]] = BaseModel.name2table()  # type: ignore[assignment]

LIMIT_VISIBILITY = False


@bp.route("/tables", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.TABLE.LIST, PERMISSIONS.TABLE.GET])
def get_tables() -> GetTables:
    return GetTables(tables={k: COLUMN_INFO[k] for k in EDITABLE_TABLE_NAMES})


@bp.route("/tables/<string:table_name>", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.TABLE.GET])
def get_table(table_name: str) -> GetTables | DataTableNotFound:
    if LIMIT_VISIBILITY and table_name not in EDITABLE_TABLE_NAMES:
        return DataTableNotFound()
    return GetTables(tables={table_name: COLUMN_INFO[table_name]})


@bp.route("/tables/<string:table_name>/rows/<int:offset>/<int:limit>", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.DATA.GET])
def get_rows(table_name: str, offset: int, limit: int) -> GetRows | DataTableNotFound:  # todo perm limit
    if LIMIT_VISIBILITY and table_name not in EDITABLE_TABLE_NAMES:
        return DataTableNotFound()
    query = NAME2TABLE[table_name].query
    rows = [row.to_dict() for row in query.offset(offset).limit(limit).all()]
    return GetRows(rows=rows)


@bp.route("/tables/<string:table_name>/rows", methods=["POST"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.DATA.CREATE])
def create_row(table_name: str) -> RequestSuccess | DataTableNotFound | APIArgumentError:
    if LIMIT_VISIBILITY and table_name not in EDITABLE_TABLE_NAMES:
        return DataTableNotFound()

    table = NAME2TABLE[table_name]

    if not isinstance(request.json, dict):
        return APIArgumentError(arguments={"_schema": ["Invalid input type."]})

    try:
        obj = table(**{k: request.json[k] for k in request.json.keys() - {"id"}})
    except TypeError as err:
        if match := re.match(r"'(.*)' is an invalid keyword argument for ", str(err)):
            return APIArgumentError(arguments={match.group(1): ["invalid argument"]})
        raise

    db.session.add(obj)

    try:
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        if match := re.search(r"UNIQUE constraint failed: [^.]*\.(.*)", str(err)):
            params: str = re.search(r"\[parameters: (.*)]", str(err)).group(1)
            params_obj: tuple[str, ...] = ast.literal_eval(params)
            return APIArgumentError(
                arguments={match.group(1): [f"unique constraint failed: {param}"] for param in params_obj}
            )
        raise
    except Exception:
        db.session.rollback()
        raise
    return RequestSuccess()


@bp.route("/tables/<string:table_name>/rows/<int:row_id>", methods=["DELETE"])
@jwt_required()
@api
@permissions_required([PERMISSIONS.DATA.DELETE])
def delete_row(table_name: str, row_id: int) -> RequestSuccess | DataTableNotFound:
    if LIMIT_VISIBILITY and table_name not in EDITABLE_TABLE_NAMES:
        return DataTableNotFound()

    table = NAME2TABLE[table_name]
    obj = table.query.get(row_id)
    if obj is None:
        return DataTableNotFound()

    db.session.delete(obj)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return RequestSuccess()


__all__ = (
    "bp",
)
