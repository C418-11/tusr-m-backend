# -*- coding: utf-8 -*-


from typing import Any
from typing import overload

from sqlalchemy import Column
from sqlalchemy import String


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def StrCol(
        length: int,
        *,
        nullable: bool = False,
        unique: bool = False,
        index: bool = False
) -> Column[str]:
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
    :rtype: Column[str]

    :raise ValueError: 当length参数小于等于0时抛出
    """


# noinspection PyPep8Naming
def StrCol(length: int, **kwargs: Any) -> Column[str]:
    if length <= 0:
        raise ValueError(f"length must be positive, got {length}")
    return Column(String(length), **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def Str32Col(*, nullable: bool = False, unique: bool = False, index: bool = False) -> Column[str]:
    """
    创建固定长度32的字符串列快捷方法

    :param nullable: 是否允许空值
    :type nullable: bool
    :param unique: 是否唯一约束
    :type unique: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 32字符长度字符串列
    :rtype: Column[str]
    """


# noinspection PyPep8Naming
def Str32Col(**kwargs: Any) -> Column[str]:
    return StrCol(32, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def NullableStr32Col(*, unique: bool = False, index: bool = False) -> Column[str]:
    """
    创建允许为空的固定长度32的字符串列快捷方法

    :param unique: 是否唯一约束
    :type unique: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 32字符长度字符串列
    :rtype: Column[str]
    """


# noinspection PyPep8Naming
def NullableStr32Col(**kwargs: Any) -> Column[str]:
    return StrCol(32, nullable=True, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def Str64Col(*, nullable: bool = False, unique: bool = False, index: bool = False) -> Column[str]:
    """
    创建固定长度64的字符串列快捷方法

    :param nullable: 是否允许空值
    :type nullable: bool
    :param unique: 是否唯一约束
    :type unique: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 64字符长度字符串列
    :rtype: Column[str]
    """


# noinspection PyPep8Naming
def Str64Col(**kwargs: Any) -> Column[str]:
    return StrCol(64, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def UniqueStr64Col(*, nullable: bool = False, index: bool = False) -> Column[str]:
    """
    创建唯一约束的64长度字符列快捷方法

    :param nullable: 是否允许空值
    :type nullable: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 带唯一约束的64长度字符列
    :rtype: Column[str]
    """


# noinspection PyPep8Naming
def UniqueStr64Col(**kwargs: Any) -> Column[str]:
    return Str64Col(unique=True, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def NullableStr64Col(*, unique: bool = False, index: bool = False) -> Column[str]:
    """
    创建可空64长度字符列快捷方法

    :param unique: 是否唯一约束
    :type unique: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 可空64长度字符列
    :rtype: Column[str]
    """


# noinspection PyPep8Naming
def NullableStr64Col(**kwargs: Any) -> Column[str]:
    return Str64Col(nullable=True, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def Str128Col(*, nullable: bool = False, unique: bool = False, index: bool = False) -> Column[str]:
    """
    创建固定长度128的字符串列快捷方法

    :param nullable: 是否允许空值
    :type nullable: bool
    :param unique: 是否唯一约束
    :type unique: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 128字符长度字符串列
    :rtype: Column[str]
    """


# noinspection PyPep8Naming
def Str128Col(**kwargs: Any) -> Column[str]:
    return StrCol(128, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def NullableStr128Col(*, unique: bool = False, index: bool = False) -> Column[str]:
    """
    创建可空128长度字符列快捷方法

    :param unique: 是否唯一约束
    :type unique: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 可空128长度字符列
    :rtype: Column[str]
    """


# noinspection PyPep8Naming
def NullableStr128Col(**kwargs: Any) -> Column[str]:
    return Str128Col(nullable=True, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def Str256Col(*, nullable: bool = False, unique: bool = False, index: bool = False) -> Column[str]:
    """
    创建固定长度256的字符串列快捷方法

    :param nullable: 是否允许空值
    :type nullable: bool
    :param unique: 是否唯一约束
    :type unique: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 256字符长度字符串列
    :rtype: Column[str]
    """


# noinspection PyPep8Naming
def Str256Col(**kwargs: Any) -> Column[str]:
    return StrCol(256, **kwargs)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def NullableStr256Col(*, unique: bool = False, index: bool = False) -> Column[str]:
    """
    创建可空256长度字符列快捷方法

    :param unique: 是否唯一约束
    :type unique: bool
    :param index: 是否创建索引
    :type index: bool

    :return: 可空256长度字符列
    :rtype: Column[str]
    """


# noinspection PyPep8Naming
def NullableStr256Col(**kwargs: Any) -> Column[str]:
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
