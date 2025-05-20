# -*- coding: utf-8 -*-
from typing import Any

from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer

from ..utils import ColumnDescriptor


class IntCol(ColumnDescriptor[Column[int]]):
    def create_column(self) -> Column[int]:
        return Column(Integer, **self.kwargs)


class FloatCol(ColumnDescriptor[Column[float]]):
    def create_column(self) -> Column[float]:
        return Column(Float, **self.kwargs)


# noinspection PyPep8Naming
def NullableFloatCol(**kwargs: Any) -> FloatCol:
    return FloatCol(nullable=True, **kwargs)


__all__ = (
    "IntCol",
    "FloatCol",
    "NullableFloatCol",
)
