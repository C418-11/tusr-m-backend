# -*- coding: utf-8 -*-


from typing import Any
from typing import overload

from flask_sqlalchemy.model import Model
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer


# noinspection PyPep8Naming
def IdCol() -> Column[int]:
    """
    创建主键ID列

    :return: 整数类型的主键列
    :rtype: Column[Integer]
    """
    return Column(Integer, primary_key=True)


# noinspection PyPep8Naming
@overload  # type: ignore[misc]
def ForeignKeyCol(foreign_key: str | type[Model], *, nullable: bool = False) -> Column[int]:
    # noinspection SpellCheckingInspection
    """
    创建外键列

    .. hint::
       当传入的 ``foreign_key`` 为模型时，会自动处理为 ``model.__tablename__ + ".id"``

    :param foreign_key: 外键列关联的列名
    :type foreign_key: str | type[Model]
    :param nullable: 是否允许为空
    :type nullable: bool

    :return: 外键列对象
    :rtype: Column[Integer]
    """


# noinspection PyPep8Naming
def ForeignKeyCol(foreign_key: str | type[Model], **kwargs: Any) -> Column[int]:
    if not isinstance(foreign_key, str):
        # noinspection SpellCheckingInspection
        foreign_key = f"{getattr(foreign_key, "__tablename__")}.id"
    return Column(Integer, ForeignKey(foreign_key), **kwargs)


# noinspection PyPep8Naming
def NullableForeignKeyCol(foreign_key: str | type[Model]) -> Column[int]:
    return ForeignKeyCol(foreign_key, nullable=True)


__all__ = (
    "IdCol",
    "ForeignKeyCol",
    "NullableForeignKeyCol",
)
