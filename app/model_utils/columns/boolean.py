# -*- coding: utf-8 -*-


from typing import Any
from typing import overload

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy.sql.base import NO_ARG
# noinspection PyProtectedMember
from sqlalchemy.sql.base import _NoArg


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def BoolCol(*, default: bool | _NoArg = NO_ARG, nullable: bool = False) -> Column[bool]:
    """
    创建布尔类型列

    :param default: 默认布尔值
    :type default: bool | _NoArg
    :param nullable: 是否允许空值
    :type nullable: bool

    :return: 布尔类型列对象
    :rtype: Column[bool]
    """


# noinspection PyPep8Naming
def BoolCol(**kwargs: Any) -> Column[bool]:
    return Column(Boolean, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def NullableBoolCol(*, default: bool | _NoArg = NO_ARG) -> Column[bool]:
    """
    创建可空布尔类型列

    :param default: 默认布尔值
    :type default: bool | _NoArg

    :return: 可空布尔类型列对象
    :rtype: Column[bool]
    """


# noinspection PyPep8Naming
def NullableBoolCol(**kwargs: Any) -> Column[bool]:
    return BoolCol(nullable=True, **kwargs)


__all__ = (
    "BoolCol",
    "NullableBoolCol",
)
