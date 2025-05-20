# -*- coding: utf-8 -*-


from datetime import date
from typing import Any

from sqlalchemy import Column
from sqlalchemy import Date

from ..utils import ColumnDescriptor


class DateCol(ColumnDescriptor[Column[date]]):
    def create_column(self) -> Column[date]:
        return Column(Date, **self.kwargs)


# noinspection PyPep8Naming
def NullableDateCol(**kwargs: Any) -> DateCol:
    return DateCol(nullable=True, **kwargs)


__all__ = (
    "DateCol",
    "NullableDateCol",
)
