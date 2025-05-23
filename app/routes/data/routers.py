# -*- coding: utf-8 -*-


from flask import Blueprint
from flask_jwt_extended import jwt_required

from ...api import DataTableNotFound
from ...api import GetRows
from ...api import GetTables
from ...api import RequestSuccess
from ...api import api
from ...model_utils import BaseModel
from ...model_utils.utils import ColumnInfo
from ...models.data import EDITABLE_TABLE_NAMES
from ...permission import PERMISSIONS
from ...permission import permissions_required

bp = Blueprint("data", __name__)

COLUMN_INFO: dict[str, dict[str, ColumnInfo]] = BaseModel.get_columns_info()  # type: ignore[assignment]
NAME2TABLE: dict[str, type[BaseModel]] = BaseModel.name2table()


LIMIT_VISIBILITY = False


@bp.route("/tables", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.TABLE.LIST, PERMISSIONS.TABLE.GET])
def get_tables() -> GetTables:
    return GetTables(tables={k: COLUMN_INFO[k] for k in EDITABLE_TABLE_NAMES})


@bp.route("/tables/<string:table_name>", methods=["GET"])
@jwt_required()
@api
@permissions_required([PERMISSIONS.TABLE.GET])
def get_table(table_name: str) -> GetTables | DataTableNotFound:
    if LIMIT_VISIBILITY and table_name not in EDITABLE_TABLE_NAMES:
        return DataTableNotFound()
    return GetTables(tables={table_name: COLUMN_INFO[table_name]})


@bp.route("/tables/<string:table_name>/rows/<int:offset>/<int:limit>", methods=["GET"])
@jwt_required()
@api
@permissions_required([PERMISSIONS.DATA.GET])
def get_rows(table_name: str, offset: int, limit: int) -> GetRows | DataTableNotFound:  # todo perm limit
    if LIMIT_VISIBILITY and table_name not in EDITABLE_TABLE_NAMES:
        return DataTableNotFound()
    query = NAME2TABLE[table_name].query
    rows = [row.to_dict() for row in query.offset(offset).limit(limit).all()]
    return GetRows(rows=rows)


@bp.route("/tables/<string:table_name>/rows", methods=["POST"])
@jwt_required()
@api
@permissions_required([PERMISSIONS.DATA.CREATE])
def create_row(table_name: str) -> RequestSuccess | DataTableNotFound:
    if LIMIT_VISIBILITY and table_name not in EDITABLE_TABLE_NAMES:
        return DataTableNotFound()
    table = NAME2TABLE[table_name]
    return RequestSuccess()


__all__ = (
    "bp",
)
