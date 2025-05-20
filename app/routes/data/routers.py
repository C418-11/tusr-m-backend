# -*- coding: utf-8 -*-


from dataclasses import dataclass

from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_sqlalchemy.model import Model

from ... import BaseModel
from ...api import APIResult
from ...api import GetTables
from ...api import api
from ...models.data import SchoolClass
from ...permission import PERMISSIONS
from ...permission import permissions_required

bp = Blueprint("data", __name__)


@dataclass
class DataTable:
    table: type[Model]


DATA_TABLES: list[DataTable] = [
    DataTable(SchoolClass),
]


@bp.route("/tables", methods=["GET"])
@jwt_required()  # type: ignore[misc]
@api
@permissions_required([PERMISSIONS.TABLE.LIST])
def get_table() -> APIResult:
    return GetTables(tables=BaseModel.get_columns_info())


__all__ = (
    "bp",
)
