# -*- coding: utf-8 -*-


from typing import Any

from sqlalchemy import Column
from sqlalchemy import String

from app.model_utils.utils import ColumnDescriptor


class StrCol(ColumnDescriptor[Column[str]]):
    def __init__(self, length: int, **kwargs: Any):
        self.length = length
        super().__init__(**kwargs)

    def create_column(self) -> Column[str]:
        if self.length <= 0:
            raise ValueError(f"length must be positive, got {self.length}")
        return Column(String(self.length), **self.kwargs)


# noinspection PyPep8Naming
def Str32Col(**kwargs: Any) -> StrCol:
    return StrCol(32, **kwargs)


# noinspection PyPep8Naming
def NullableStr32Col(**kwargs: Any) -> StrCol:
    return StrCol(32, nullable=True, **kwargs)


# noinspection PyPep8Naming
def Str64Col(**kwargs: Any) -> StrCol:
    return StrCol(64, **kwargs)


# noinspection PyPep8Naming
def UniqueStr64Col(**kwargs: Any) -> StrCol:
    return Str64Col(unique=True, **kwargs)


# noinspection PyPep8Naming
def NullableStr64Col(**kwargs: Any) -> StrCol:
    return Str64Col(nullable=True, **kwargs)


# noinspection PyPep8Naming
def Str128Col(**kwargs: Any) -> StrCol:
    return StrCol(128, **kwargs)


# noinspection PyPep8Naming
def NullableStr128Col(**kwargs: Any) -> StrCol:
    return Str128Col(nullable=True, **kwargs)


# noinspection PyPep8Naming
def Str256Col(**kwargs: Any) -> StrCol:
    return StrCol(256, **kwargs)


# noinspection PyPep8Naming
def NullableStr256Col(**kwargs: Any) -> StrCol:
    return Str256Col(nullable=True, **kwargs)


__all__ = (
    "StrCol",
    "Str32Col",
    "NullableStr32Col",
    "Str64Col",
    "UniqueStr64Col",
    "NullableStr64Col",
    "Str128Col",
    "NullableStr128Col",
    "Str256Col",
    "NullableStr256Col",
)
