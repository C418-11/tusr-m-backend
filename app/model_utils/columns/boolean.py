# -*- coding: utf-8 -*-


from typing import Any

from sqlalchemy import Boolean
from sqlalchemy import Column

from ..utils import ColumnDescriptor


class BoolCol(ColumnDescriptor[Column[bool]]):
    def create_column(self):
        return Column(Boolean, **self.kwargs)


# noinspection PyPep8Naming
def NullableBoolCol(**kwargs: Any) -> BoolCol:
    return BoolCol(nullable=True, **kwargs)


__all__ = (
    "BoolCol",
    "NullableBoolCol",
)
