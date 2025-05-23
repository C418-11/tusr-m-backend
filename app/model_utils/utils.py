# -*- coding: utf-8 -*-


from abc import abstractmethod
from abc import ABC
from dataclasses import dataclass
from typing import Self
from typing import Any
from typing import Optional

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
    foreign_key: str | None

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
    _name2table: dict[str, type[Self]] = {}

    @classmethod
    def register_column[C: Column[Any]](cls, name: str, descriptor: ColumnDescriptor[C], column: C) -> None:
        assert len(column.foreign_keys) < 2, column.foreign_keys
        # 提取字段信息
        cls._name2table[cls.__tablename__] = cls
        cls._columns_registry.setdefault(cls.__tablename__, {})[name] = ColumnInfo(
            type=str(column.type),

            primary_key=column.primary_key,
            unique=bool(column.unique),
            nullable=bool(column.nullable),
            default=column.default.arg if isinstance(column.default, ScalarElementColumnDefault) else None,
            foreign_key=[fk.target_fullname for fk in column.foreign_keys][0] if column.foreign_keys else None,

            length=getattr(descriptor, "length", None),
        )

    @classmethod
    def get_columns_info(cls) -> dict[str, ColumnInfo] | dict[str, dict[str, ColumnInfo]]:
        """获取字段信息"""
        # noinspection SpellCheckingInspection
        if not hasattr(cls, "__tablename__"):
            return cls._columns_registry
        return cls._columns_registry[cls.__tablename__]

    @classmethod
    def name2table(cls, name: Optional[str] = None) -> type[Self] | dict[str, type[Self]]:
        if name is None:
            return cls._name2table
        return cls._name2table[name]

    def to_dict(self) -> dict[str, Any]:
        dct = {}
        for name in self.get_columns_info().keys():
            dct[name] = getattr(self, name)
        return dct

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
