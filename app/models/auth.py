# -*- coding: utf-8 -*-


from collections.abc import Iterable
from typing import Never
from typing import Optional
from typing import Self
from typing import cast

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from ..model_utils import BaseModel
from ..model_utils import BoolCol
from ..model_utils import DynamicMany2Many
from ..model_utils import IdCol
from ..model_utils import SecondaryTable
from ..model_utils import Str128Col
from ..model_utils import UniqueStr64Col

# 用户-角色关联表（多对多）
user_roles = SecondaryTable(
    "user_roles",
    user_id="users.id",
    role_id="roles.id"
)

# 角色-权限关联表（多对多）
role_permissions = SecondaryTable(
    "role_permissions",
    role_id="roles.id",
    permission_id="permissions.id"
)


class User(BaseModel):
    """
    用户模型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "users"
    id = IdCol()
    username = UniqueStr64Col(index=True)
    password_hash = Str128Col()
    active = BoolCol(default=True)

    # 关联角色（多对多）
    roles = DynamicMany2Many("Role", user_roles, "users")

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
        self.password_hash = generate_password_hash(password)  # type: ignore[assignment]

    def verify_password(self, password: str) -> bool:
        """
        验证密码

        :param password: 密码
        :type password: str

        :return: 密码是否正确
        :rtype: bool
        """
        return check_password_hash(self.password_hash, password)  # type: ignore[arg-type]

    def has_permission(self, permission_name: str) -> bool:
        """
        检查用户是否拥有权限

        :param permission_name: 权限名
        :type permission_name: str

        :return: 是否拥有该权限
        :rtype: bool
        """
        return any(role.has_permission(permission_name) for role in cast(Iterable[Role], self.roles))


class Role(BaseModel):
    """
    角色模型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "roles"

    id = IdCol()
    name = UniqueStr64Col()
    description = Str128Col()

    # 关联用户（多对多）
    users = DynamicMany2Many("User", user_roles, "roles")
    # 关联权限（多对多）
    permissions = DynamicMany2Many("Permission", role_permissions, "roles")

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


class Permission(BaseModel):
    """
    权限模型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "permissions"

    id = IdCol()
    name = UniqueStr64Col()
    description = Str128Col()

    # 关联角色（多对多）
    roles = DynamicMany2Many("Role", role_permissions, "permissions")


__all__ = (
    "User",
    "Role",
    "Permission",
)
