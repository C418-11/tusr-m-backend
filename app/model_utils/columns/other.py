# -*- coding: utf-8 -*-


from typing import Any

from flask_sqlalchemy.model import Model
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from ..utils import ColumnDescriptor


class IdCol(ColumnDescriptor[Column[int]]):
    def create_column(self) -> Column[int]:
        return Column(Integer, primary_key=True, **self.kwargs)


class ForeignKeyCol(ColumnDescriptor[Column[int]]):
    def __init__(self, foreign_key: str | type[Model], **kwargs: Any) -> None:
        if not isinstance(foreign_key, str):
            # noinspection SpellCheckingInspection
            foreign_key = f"{getattr(foreign_key, "__tablename__")}.id"
        self.foreign_key = foreign_key
        super().__init__(**kwargs)

    def create_column(self) -> Column[int]:
        return Column(Integer, ForeignKey(self.foreign_key), **self.kwargs)


# noinspection PyPep8Naming
def NullableForeignKeyCol(foreign_key: str | type[Model]) -> ForeignKeyCol:
    return ForeignKeyCol(foreign_key, nullable=True)


__all__ = (
    "IdCol",
    "ForeignKeyCol",
    "NullableForeignKeyCol",
)
