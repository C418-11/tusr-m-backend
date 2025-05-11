# -*- coding: utf-8 -*-


import sys
import traceback

from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import redis

db = SQLAlchemy()
jwt = JWTManager()
jwt_redis_blocklist = redis.StrictRedis(
    host="127.0.0.1",
    decode_responses=True
)
try:
    jwt_redis_blocklist.ping()
except redis.exceptions.ConnectionError:
    traceback.print_exc()
    print("Redis 连接失败，请检查 Redis 服务是否启动")
    sys.exit(1)

__all__ = (
    "db",
    "jwt",
    "jwt_redis_blocklist",
)
