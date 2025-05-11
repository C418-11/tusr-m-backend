# -*- coding: utf-8 -*-


from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

from flask_sqlalchemy.model import Model
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy.orm import RelationshipProperty

from ..extensions import db


# noinspection PyPep8Naming
def DynamicMany(model: str | type[Model], back_populates: str, **kwargs: Any) -> RelationshipProperty[Any]:
    """
    创建动态加载的单向关系属性

    用于“一对多”的“一”方，动态加载多个对象

    :param model: 关联的模型类名
    :type model: str
    :param back_populates: 反向引用属性名
    :type back_populates: str
    :param kwargs: 其他relationship配置参数
    :type kwargs: Any

    :return: 动态加载的关系属性对象
    :rtype: RelationshipProperty
    """
    if not isinstance(model, str):
        model = model.__name__
    return db.relationship(
        model,
        back_populates=back_populates,
        lazy="dynamic",
        **kwargs
    )


@dataclass
class RelationshipWithFK:
    """
    包含外键的关系属性
    """
    relationship: RelationshipProperty[Any]
    """
    关系属性
    """
    foreign_key: Column[Integer]
    """
    外键列
    """

    def __iter__(self) -> Iterator[Any]:
        yield self.relationship
        yield self.foreign_key


# noinspection PyPep8Naming
def BelongsTo(
        model: str | type[Model],
        back_populates: str,
        *,
        foreign_key: str,
        nullable: bool = False,
        **kwargs: Any,
) -> RelationshipWithFK:
    """
    创建多对一关系属性及外键列

    用于“多对一”的“多”方，定义外键并关联到目标模型

    .. note::
       当传入的 ``model`` 参数为 ``type[Model]`` 时，传入的外键应省略表名
       例如 ``foreign_key="tables.id"`` 应改为 ``foreign_key=".id"``
       保留点符号以提高可读性

    :param model: 关联的模型类名
    :type model: str
    :param back_populates: 反向引用属性名
    :type back_populates: str
    :param foreign_key: 外键路径字符串
    :type foreign_key: str
    :param nullable: 外键是否允许为空
    :type nullable: bool
    :param kwargs: 其他relationship配置参数
    :type kwargs: Any

    :return: 包含关系属性和外键列的元组对象
    :rtype: RelationshipWithFK
    """
    if not isinstance(model, str):
        # noinspection SpellCheckingInspection
        if (tb_name := getattr(model, "__tablename__", None)) is not None:
            foreign_key = f"{tb_name}.{foreign_key.strip(".")}"
        model = model.__name__

    relationship = db.relationship(
        model,
        back_populates=back_populates,
        **kwargs
    )
    foreign_key = db.Column(
        db.Integer,
        db.ForeignKey(foreign_key),
        nullable=nullable,
    )
    return RelationshipWithFK(relationship, foreign_key)


# noinspection PyPep8Naming
def DynamicMany2Many(model: str | type[Model], secondary: Table, back_populates: str) -> RelationshipProperty[Any]:
    """
    创建动态加载的多对多关系属性

    :param model: 关联的模型类名
    :type model: str
    :param secondary: 关联的中间表
    :type secondary: Table
    :param back_populates: 反向引用属性名
    :type back_populates: str

    :return: 包含动态关系属性的元组对象
    :rtype: RelationshipProperty[Any]
    """
    if not isinstance(model, str):
        model = model.__name__
    return db.relationship(
        model,
        secondary=secondary,
        back_populates=back_populates,
        lazy="dynamic",
    )


__all__ = (
    "DynamicMany",
    "BelongsTo",
    "DynamicMany2Many",
)
