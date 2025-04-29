import os
from datetime import timedelta


class Config:
    SSL_CERTIFICATE = os.path.join(os.path.dirname(__file__), '..', 'certs', 'server.crt')
    SSL_PRIVATE_KEY = os.path.join(os.path.dirname(__file__), '..', 'certs', 'server.key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_SECURE = True
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_TOKEN_LOCATION = ["cookies"]
    # noinspection SpellCheckingInspection
    JWT_COOKIE_SAMESITE = "None"
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
