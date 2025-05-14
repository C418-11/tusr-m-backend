# -*- coding: utf-8 -*-


from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer


# noinspection PyPep8Naming
def IntCol() -> Column[int]:
    """
    创建整数列

    :return: 整数列对象
    :rtype: Column[Integer]
    """
    return Column(Integer)


# noinspection PyPep8Naming
def FloatCol() -> Column[float]:
    """
    创建浮点数列

    :return: 浮点数列对象
    :rtype: Column[float]
    """
    return Column(Float)


# noinspection PyPep8Naming
def NullableFloatCol() -> Column[float]:
    """
    创建可为空的浮点数列

    :return: 可为空的浮点数列对象
    :rtype: Column[float]
    """
    return Column(Float, nullable=True)


__all__ = (
    "IntCol",
    "FloatCol",
    "NullableFloatCol",
)
