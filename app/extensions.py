# -*- coding: utf-8 -*-


from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import redis

db = SQLAlchemy()
jwt = JWTManager()
jwt_redis_blocklist = redis.StrictRedis(
    host="127.0.0.1",
    decode_responses=True
)
jwt_redis_blocklist.ping()

__all__ = (
    "db",
    "jwt",
    "jwt_redis_blocklist",
)
