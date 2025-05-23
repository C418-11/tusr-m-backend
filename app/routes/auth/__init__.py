# -*- coding: utf-8 -*-


import importlib
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any
from typing import cast

from flask import Flask
from flask import Response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies

from .bp import bp
from ...api import APIResult
from ...api import Unauthorized
from ...api import api
from ...extensions import jwt
from ...extensions import jwt_redis_blocklist
from ...models.auth import User


importlib.import_module(".account", __package__)
importlib.import_module(".permission", __package__)
importlib.import_module(".role", __package__)


def initialize_hooks(app: Flask) -> None:  # noqa: C901 (too complex)
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(_jwt_header: dict[str, Any], jwt_payload: dict[str, Any]) -> bool:
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None

    @jwt.user_identity_loader
    def user_identity_lookup(user: User | int | str) -> str:
        if isinstance(user, User):
            return str(user.id)
        return str(user)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header: dict[str, Any], jwt_data: dict[str, Any]) -> User | None:
        identity = jwt_data["sub"]
        return cast(User | None, User.query.filter_by(id=identity).one_or_none())

    @jwt.user_lookup_error_loader
    @api
    def user_lookup_error_callback(*_: Any) -> APIResult:
        return Unauthorized()

    @app.after_request
    def refresh_expiring_jwts[R: Response](response: R) -> R:
        try:
            jwt_info = get_jwt()
        except RuntimeError:
            return response
        if not jwt_info:
            return response

        exp_timestamp = jwt_info["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response


def initialize_setup() -> None:
    from ...extensions import db
    from ...models.auth import Permission
    from ...permission import PERMISSIONS
    from ...models.auth import Role

    print("正在初始化身份验证系统")
    print()

    # 创建权限
    for name, desc in {
        PERMISSIONS.ACCOUNT.CREATE: "创建账户",
        PERMISSIONS.ACCOUNT.GET: "获取账户",
        PERMISSIONS.ACCOUNT.LIST: "获取账户列表",
        PERMISSIONS.ACCOUNT.UPDATE: "更新账户信息",
        PERMISSIONS.ACCOUNT.UPDATE_SELF_PASSWORD: "更新自身密码",  # todo 待实装前端
        PERMISSIONS.ACCOUNT.DELETE: "删除账户",
        PERMISSIONS.ROLE.GET: "获取角色",
        PERMISSIONS.ROLE.CREATE: "创建角色",
        PERMISSIONS.ROLE.DELETE: "删除角色",
        PERMISSIONS.PERMISSION.GET: "获取权限",
        PERMISSIONS.TABLE.GET: "获取数据表",
        PERMISSIONS.TABLE.LIST: "获取数据表列表",
        PERMISSIONS.DATA.GET: "获取数据",
        PERMISSIONS.DATA.LIST: "获取数据列表",
        PERMISSIONS.DATA.CREATE: "创建数据",
        PERMISSIONS.DATA.UPDATE: "更新数据",
        PERMISSIONS.DATA.DELETE: "删除数据",
    }.items():
        print(f"创建权限：{name}")
        # noinspection SpellCheckingInspection
        db.session.add(Permission(name=name, description=desc))
        db.session.commit()

    print()

    # 创建角色
    for name, (desc, permissions) in {
        "admin": ("管理员", [
            PERMISSIONS.ACCOUNT.GET,
            PERMISSIONS.ACCOUNT.LIST,
            PERMISSIONS.ACCOUNT.CREATE,
            PERMISSIONS.ACCOUNT.DELETE,
            PERMISSIONS.ACCOUNT.UPDATE,
            PERMISSIONS.ACCOUNT.UPDATE_SELF_PASSWORD,
            PERMISSIONS.ROLE.GET,
            PERMISSIONS.ROLE.CREATE,
            PERMISSIONS.ROLE.DELETE,
            PERMISSIONS.PERMISSION.GET,
            PERMISSIONS.TABLE.GET,
            PERMISSIONS.TABLE.LIST,
            PERMISSIONS.DATA.GET,
            PERMISSIONS.DATA.LIST,
            PERMISSIONS.DATA.CREATE,
            PERMISSIONS.DATA.UPDATE,
            PERMISSIONS.DATA.DELETE,
        ]),
        "user": ("用户", [
            PERMISSIONS.ACCOUNT.UPDATE_SELF_PASSWORD,
        ])
    }.items():
        print(f"创建角色：{name}")
        db.session.add(Role.create(name=name, description=desc, permissions=cast(list[str], permissions)))
        db.session.commit()

    print()

    # 创建用户
    for name, (password, roles) in {
        "admin": ("admin", ["admin"]),
        "user": ("user", ["user"]),
    }.items():
        print(f"创建用户：{name}")
        db.session.add(User.create(username=name, password=password, roles=roles))
        db.session.commit()

    print()
    print("身份验证系统初始化完成")


__all__ = ("bp", "initialize_hooks", "initialize_setup")
