# -*- coding: utf-8 -*-


from typing import Any
from datetime import date

from sqlalchemy import Column
from sqlalchemy import Date


# noinspection PyPep8Naming
def DateCol(**kwargs: Any) -> Column[date]:
    return Column(Date, **kwargs)


# noinspection PyPep8Naming
def NullableDateCol(**kwargs: Any) -> Column[date]:
    return DateCol(nullable=True, **kwargs)


__all__ = (
    "DateCol",
    "NullableDateCol",
)
