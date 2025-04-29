# -*- coding: utf-8 -*-


from typing import cast

from flask import Flask
from flask_cors import CORS

from . import api
from .config import Config
from .extensions import db
from .extensions import jwt
from .models.auth import Permission
from .models.auth import Role
from .models.auth import User
from .permission import PERMISSIONS
from .routes import auth


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(
        app,
        origins=[
            "http://localhost:*",
            "http://127.0.0.1:*",
            "https://localhost:*",
            "https://127.0.0.1:*",
        ],
        supports_credentials=True,
    )

    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)

    api.initialize_hooks(app)
    auth.initialize_hooks(app)

    app.register_blueprint(auth.bp, url_prefix="/auth")

    # 添加初始化命令
    @app.cli.command("init")
    def init() -> None:
        """初始化应用程序"""
        init_auth()

    return app


def init_auth() -> None:
    db.create_all()
    print("数据库表已创建")

    # 创建权限
    for name, desc in {
        PERMISSIONS.ACCOUNT.CREATE: "创建账户",
        PERMISSIONS.ACCOUNT.GET: "获取账户",
        PERMISSIONS.ACCOUNT.DELETE: "删除账户",
        PERMISSIONS.ROLE.GET: "获取角色",
        PERMISSIONS.ROLE.CREATE: "创建角色",
        PERMISSIONS.ROLE.DELETE: "删除角色",
        PERMISSIONS.PERMISSION.GET: "获取权限",
    }.items():
        print(f"创建权限：{name}")
        # noinspection SpellCheckingInspection
        db.session.add(Permission(name=name, description=desc))
    db.session.commit()

    # 创建角色
    for name, (desc, permissions) in {
        "admin": ("管理员", [
            PERMISSIONS.ACCOUNT.GET,
            PERMISSIONS.ACCOUNT.CREATE,
            PERMISSIONS.ACCOUNT.DELETE,
            PERMISSIONS.ROLE.GET,
            PERMISSIONS.ROLE.CREATE,
            PERMISSIONS.ROLE.DELETE,
            PERMISSIONS.PERMISSION.GET,
        ]),
    }.items():
        print(f"创建角色：{name}")
        db.session.add(Role.create(name=name, description=desc, permissions=cast(list[str], permissions)))
    db.session.commit()

    # 创建用户
    db.session.add(User.create(username="admin", password="admin", roles=["admin"]))
    db.session.commit()
    print("管理员用户已创建")
