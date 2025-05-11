# -*- coding: utf-8 -*-


from typing import Any
from typing import overload

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql.base import NO_ARG
# noinspection PyProtectedMember
from sqlalchemy.sql.base import _NoArg

from ..extensions import db


# noinspection PyPep8Naming
def IdCol() -> Column[Integer]:
    """
    创建主键ID列

    :return: 整数类型的主键列
    :rtype: Column[Integer]
    """
    return db.Column(db.Integer, primary_key=True)  # type: ignore[no-any-return]


# noinspection PyPep8Naming
def IntCol() -> Column[Integer]:
    """
    创建整数列

    :return: 整数列对象
    :rtype: Column[Integer]
    """
    return db.Column(db.Integer)  # type: ignore[no-any-return]


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def StrCol(
        length: int,
        *,
        nullable: bool = False,
        unique: bool = False,
        index: bool = False
) -> Column[String]:
    """
    创建可变长度字符串列

    :param length: 字符串最大长度（必须为正整数）
    :type length: int
    :param nullable: 是否允许空值
    :type nullable: bool
    :param unique: 是否唯一约束
    :type unique: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 字符串类型列对象
    :rtype: Column[String]

    :raise ValueError: 当length参数小于等于0时抛出
    """


# noinspection PyPep8Naming
def StrCol(length: int, **kwargs: Any) -> Column[String]:
    if length <= 0:
        raise ValueError(f"length must be positive, got {length}")
    return db.Column(db.String(length), **kwargs)  # type: ignore[no-any-return]


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def Str64Col(*, nullable: bool = False, unique: bool = False, index: bool = False) -> Column[String]:
    """
    创建固定长度64的字符串列快捷方法

    :param nullable: 是否允许空值
    :type nullable: bool
    :param unique: 是否唯一约束
    :type unique: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 64字符长度字符串列
    :rtype: Column[String]
    """


# noinspection PyPep8Naming
def Str64Col(**kwargs: Any) -> Column[String]:
    return StrCol(64, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def UniqueStr64Col(*, nullable: bool = False, index: bool = False) -> Column[String]:
    """
    创建唯一约束的64长度字符列快捷方法

    :param nullable: 是否允许空值
    :type nullable: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 带唯一约束的64长度字符列
    :rtype: Column[String]
    """


# noinspection PyPep8Naming
def UniqueStr64Col(**kwargs: Any) -> Column[String]:
    return Str64Col(unique=True, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def NullableStr64Col(*, unique: bool = False, index: bool = False) -> Column[String]:
    """
    创建可空64长度字符列快捷方法

    :param unique: 是否唯一约束
    :type unique: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 可空64长度字符列
    :rtype: Column[String]
    """


# noinspection PyPep8Naming
def NullableStr64Col(**kwargs: Any) -> Column[String]:
    return Str64Col(nullable=True, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def Str128Col(*, nullable: bool = False, unique: bool = False, index: bool = False) -> Column[String]:
    """
    创建固定长度128的字符串列快捷方法

    :param nullable: 是否允许空值
    :type nullable: bool
    :param unique: 是否唯一约束
    :type unique: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 128字符长度字符串列
    :rtype: Column[String]
    """


# noinspection PyPep8Naming
def Str128Col(**kwargs: Any) -> Column[String]:
    return StrCol(128, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def BoolCol(*, default: bool | _NoArg = NO_ARG, nullable: bool = False) -> Column[Boolean]:
    """
    创建布尔类型列

    :param default: 默认布尔值
    :type default: bool | _NoArg
    :param nullable: 是否允许空值
    :type nullable: bool

    :return: 布尔类型列对象
    :rtype: Column[Boolean]
    """


# noinspection PyPep8Naming
def BoolCol(**kwargs: Any) -> Column[Boolean]:
    return db.Column(db.Boolean, **kwargs)  # type: ignore[no-any-return]


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def NullableBoolCol(*, default: bool | _NoArg = NO_ARG) -> Column[Boolean]:
    """
    创建可空布尔类型列

    :param default: 默认布尔值
    :type default: bool | _NoArg

    :return: 可空布尔类型列对象
    :rtype: Column[Boolean]
    """


# noinspection PyPep8Naming
def NullableBoolCol(**kwargs: Any) -> Column[Boolean]:
    return BoolCol(nullable=True, **kwargs)


# noinspection PyPep8Naming
def DateCol(**kwargs: Any) -> Column[Date]:
    return db.Column(db.Date, **kwargs)  # type: ignore[no-any-return]


__all__ = (
    "IdCol",
    "IntCol",
    "StrCol",
    "Str64Col",
    "UniqueStr64Col",
    "NullableStr64Col",
    "Str128Col",
    "BoolCol",
    "NullableBoolCol",
    "DateCol",
)
