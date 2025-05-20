# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from sqlalchemy import Column
from sqlalchemy.sql.schema import ScalarElementColumnDefault

from ..extensions import db


@dataclass(kw_only=True)
class ColumnInfo:
    type: str

    primary_key: bool
    unique: bool
    nullable: bool
    default: Any

    length: Optional[int]


class ColumnDescriptor[C: Column[Any]](ABC):
    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    def __get__(self, instance: Any, owner: Any) -> C:
        raise AttributeError("This attribute is not accessible")

    @abstractmethod
    def create_column(self) -> C:
        """
        生成具体的 SQLAlchemy Column
        """


class BaseModel(db.Model):  # type: ignore[misc, name-defined]
    __abstract__ = True
    _columns_registry: dict[str, dict[str, ColumnInfo]] = {}

    @classmethod
    def register_column[C: Column[Any]](cls, name: str, descriptor: ColumnDescriptor[C], column: C) -> None:
        # 提取字段信息
        cls._columns_registry.setdefault(cls.__tablename__, {})[name] = ColumnInfo(
            type=str(column.type),

            primary_key=column.primary_key,
            unique=bool(column.unique),
            nullable=bool(column.nullable),
            default=column.default.arg if isinstance(column.default, ScalarElementColumnDefault) else None,

            length=getattr(descriptor, "length", None),
        )

    @classmethod
    def get_columns_info(cls) -> dict[str, ColumnInfo] | dict[str, dict[str, ColumnInfo]]:
        """获取字段信息"""
        # noinspection SpellCheckingInspection
        if not hasattr(cls, "__tablename__"):
            return cls._columns_registry
        return cls._columns_registry[cls.__tablename__]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        # 遍历子类属性，将字段信息注册到类级别字段注册表中
        for name, attr in cls.__dict__.items():
            if isinstance(attr, ColumnDescriptor):
                column = attr.create_column()
                cls.register_column(name, attr, column)
                setattr(cls, name, column)
        super().__init_subclass__(**kwargs)


__all__ = (
    "ColumnInfo",
    "BaseModel",
    "ColumnDescriptor",
)
