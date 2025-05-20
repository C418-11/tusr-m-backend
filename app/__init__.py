# -*- coding: utf-8 -*-


from flask import Flask
from flask_cors import CORS

from . import api
from .config import Config
from .extensions import db
from .extensions import jwt
from .routes import auth
from .routes import data


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
    data.initialize_hooks(app)

    app.register_blueprint(auth.bp, url_prefix="/api/auth")
    app.register_blueprint(data.bp, url_prefix="/api/data")

    # 添加初始化命令
    @app.cli.command("init")
    def init() -> None:
        """初始化应用程序"""

        print("正在初始化应用程序")
        for setup in [
            create_all_with_progress,
            auth.initialize_setup,
            data.initialize_setup,
        ]:
            print()
            setup()
        print()
        print("应用程序初始化完成")

    return app


def create_all_with_progress() -> None:
    print("正在创建数据库")
    print()

    for key in db.metadatas:
        metadata, engine = db.metadatas[key], db.engines[key]
        for table in metadata.sorted_tables:
            print(f"正在创建表： {table.name}")
            table.create(bind=engine, checkfirst=True)

    print()
    print("数据库创建完成")
