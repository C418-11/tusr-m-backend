# -*- coding: utf-8 -*-


from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer

from ..utils import ColumnDescriptor


class IntCol(ColumnDescriptor[Column[int]]):
    def create_column(self):
        return Column(Integer, **self.kwargs)


class FloatCol(ColumnDescriptor[Column[float]]):
    def create_column(self):
        return Column(Float, **self.kwargs)


# noinspection PyPep8Naming
def NullableFloatCol(**kwargs) -> FloatCol:
    return FloatCol(**kwargs)


__all__ = (
    "IntCol",
    "FloatCol",
    "NullableFloatCol",
)
