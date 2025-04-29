# -*- coding: utf-8 -*-


from collections.abc import Iterable
from typing import Never
from typing import Optional
from typing import Self
from typing import cast

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from ..extensions import db

# 用户-角色关联表（多对多）
user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"))
)

# 角色-权限关联表（多对多）
role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"))
)


class User(db.Model):  # type: ignore[misc, name-defined]
    """
    用户模型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=True)

    # 关联角色（多对多）
    roles = db.relationship("Role",
                            secondary=user_roles,
                            backref=db.backref("users", lazy="dynamic"))

    @classmethod
    def create(cls, username: str, password: str, roles: Optional[list[str]] = None, active: bool = True) -> Self:
        """
        创建用户

        :param username: 用户名
        :type username: str
        :param password: 密码
        :type password: str
        :param roles: 用户所属角色
        :type roles: Optional[list[str]]
        :param active: 启用账户
        :type active: bool

        :return: 用户对象
        :rtype: Self
        """
        if roles is None:
            roles = []
        else:
            roles = [Role.query.filter_by(name=name).first() for name in roles]
        user = cls(username=username, roles=roles, active=active)
        user.password = password  # type: ignore[assignment]
        return user

    @property
    def password(self) -> Never:
        """
        设置密码 （只写）
        """
        raise Exception("password is not a readable attribute")

    @password.setter
    def password(self, password: str) -> None:
        """
        设置密码

        :param password: 密码
        :type password: str
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """
        验证密码

        :param password: 密码
        :type password: str

        :return: 密码是否正确
        :rtype: bool
        """
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_name: str) -> bool:
        """
        检查用户是否拥有权限

        :param permission_name: 权限名
        :type permission_name: str

        :return: 是否拥有该权限
        :rtype: bool
        """
        return any(role.has_permission(permission_name) for role in cast(Iterable[Role], self.roles))


class Role(db.Model):  # type: ignore[misc, name-defined]
    """
    角色模型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))

    # 关联权限（多对多）
    permissions = db.relationship("Permission",
                                  secondary=role_permissions,
                                  backref=db.backref("roles", lazy="dynamic"))

    @classmethod
    def create(cls, name: str, description: str, permissions: Optional[list[str]] = None) -> Self:
        """
        创建角色

        :param name: 角色名
        :type name: str
        :param description: 描述
        :type name: str
        :param permissions: 角色所拥有的权限
        :type permissions: Optional[list[str]]

        :return: 角色对象
        :rtype: Self
        """
        if permissions is None:
            permissions = []
        else:
            permissions = [Permission.query.filter_by(name=perm).first() for perm in permissions]

        return cls(name=name, description=description, permissions=permissions)

    def has_permission(self, permission_name: str) -> bool:
        """
        角色是否拥有该权限

        :param permission_name: 权限名
        :type permission_name: str

        :return: 是否拥有该权限
        :rtype: bool
        """
        return any(permission.name == permission_name for permission in cast(Iterable[Permission], self.permissions))


class Permission(db.Model):  # type: ignore[misc, name-defined]
    """
    权限模型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))


__all__ = (
    "User",
    "Role",
    "Permission",
)
