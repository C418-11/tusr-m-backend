# -*- coding: utf-8 -*-


from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint

from ..extensions import db


# noinspection PyPep8Naming
def SecondaryTable(name: str, **col2fk: str) -> Table:
    """
    创建多对多关联表，并自动添加联合唯一约束

    :param name: 表名称
    :type name: str
    :param col2fk: 列名到外键的映射
    :type col2fk: str

    :return: 生成整数类型外键列的关联表对象，联合唯一约束
    :rtype: Table
    """
    return db.Table(
        name,
        *(
            Column(cname, Integer, ForeignKey(fk))
            for cname, fk in col2fk.items()
        ),
        UniqueConstraint(
            *col2fk.keys(),  # 所有列名作为联合唯一键
            name=f"uq_{name}_columns"
        ),
    )


__all__ = (
    "SecondaryTable",
)
