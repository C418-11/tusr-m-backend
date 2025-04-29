# -*- coding: utf-8 -*-


"""
状态码规则

阅读顺序：从右往左

第一位：请求状态

1. 请求成功
2. 请求异常

第二位：状态类别

1. API接口相关
2. 身份验证相关
"""

import dataclasses
from dataclasses import dataclass
from dataclasses import field
from http import HTTPStatus
from typing import Any, Optional, overload
from typing import Callable
from typing import cast
from typing import override

from flask import Flask
from flask import Response
from flask import jsonify
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from werkzeug.exceptions import HTTPException
from wrapt import decorator  # type: ignore[import-untyped]

from .extensions import jwt


@dataclass(kw_only=True)
class APIResult:
    code: int
    message: str

    @property
    def ignore_fields(self) -> tuple[str, ...]:
        return (
            HTTP_CODE_ATTR,
        )

    def build_response(self) -> Response:
        json = dataclasses.asdict(self)
        for f in self.ignore_fields:
            if f in json:
                del json[f]
        return jsonify(json)


API_CODES: dict[int, str] = {}
HTTP_2_API: dict[int, int] = {}


def register[C: APIResult](cls: type[C]) -> type[C]:
    API_CODES[cls.code] = cls.message
    if hasattr(cls, HTTP_CODE_ATTR):
        HTTP_2_API[getattr(cls, HTTP_CODE_ATTR)] = cls.code
    return cls


@overload
def d[D](default: D, /) -> D:
    ...


@overload
def d[D](*, default_factory: Callable[[], D]) -> D:
    ...


def d[D](default: Optional[D] = None, /, *, default_factory: Optional[Callable[[], D]] = None) -> D:
    if default_factory is not None:
        return field(default_factory=default_factory)
    if default is not None:
        return field(default=default)
    raise RuntimeError("default or default_factory must be specified")


HTTP_CODE_ATTR = "http_code"


@register
@dataclass(kw_only=True)
class RequestSuccess(APIResult):
    code: int = d(111)
    message: str = d("Request Success")


@register
@dataclass(kw_only=True)
class LoginSuccess(APIResult):
    code: int = d(121)
    message: str = d("Login Success")
    access_token: str

    @property
    def ignore_fields(self) -> tuple[str, ...]:
        return super().ignore_fields + ("access_token",)

    @override
    def build_response(self) -> Response:
        response = super().build_response()
        set_access_cookies(response, self.access_token)
        return response


@register
@dataclass(kw_only=True)
class LogoutSuccess(APIResult):
    code: int = d(221)
    message: str = d("Logout Success")

    @override
    def build_response(self) -> Response:
        response = super().build_response()
        unset_jwt_cookies(response)
        return response


@register
@dataclass(kw_only=True)
class GetAccounts(APIResult):
    code: int = d(321)
    message: str = d("Get Accounts Success")
    accounts: list[dict[str, Any]]


@register
@dataclass(kw_only=True)
class GetRoles(APIResult):
    code: int = d(421)
    message: str = d("Get Roles Success")
    roles: list[dict[str, Any]]


@dataclass(kw_only=True)
class GetPermissions(APIResult):
    code: int = d(421)
    message: str = d("Get Permissions Success")
    permissions: list[dict[str, Any]]


@register
@dataclass(kw_only=True)
class APINotFound(APIResult):
    code: int = d(112)
    message: str = d("API Not Found")
    http_code: int = d(HTTPStatus.NOT_FOUND)


@register
@dataclass(kw_only=True)
class WrongMethod(APIResult):
    code: int = d(212)
    message: str = d("Wrong Method")
    http_code: int = d(HTTPStatus.METHOD_NOT_ALLOWED)


@register
@dataclass(kw_only=True)
class APIInternalError(APIResult):
    code: int = d(312)
    message: str = d("API Internal Error")
    http_code: int = d(HTTPStatus.INTERNAL_SERVER_ERROR)


@register
@dataclass(kw_only=True)
class APIArgumentError(APIResult):
    code: int = d(412)
    message: str = d("API Argument Error")
    http_code: int = d(HTTPStatus.BAD_REQUEST)
    arguments: list[str] | dict[str, list[str]]


@register
@dataclass(kw_only=True)
class Unauthorized(APIResult):
    code: int = d(122)
    message: str = d("Unauthorized")
    http_code: int = d(HTTPStatus.UNAUTHORIZED)


@register
@dataclass(kw_only=True)
class PermissionDenied(APIResult):
    code: int = d(222)
    message: str = d("Permission Denied")
    http_code: int = d(HTTPStatus.FORBIDDEN)
    # noinspection PyDataclass
    missing_permissions: list[str] = d(default_factory=list)


@register
@dataclass(kw_only=True)
class AccountNotFound(APIResult):
    code: int = d(322)
    message: str = d("Account Not Found")


@register
@dataclass(kw_only=True)
class WrongUsernameOrPassword(APIResult):
    code: int = d(422)
    message: str = d("Wrong Username or Password")


class APIException(Exception):
    def __init__(self, result: APIResult) -> None:
        self.result = result


def api(func: Callable[..., APIResult]) -> Callable[..., Response | tuple[Response, int]]:
    @decorator  # type: ignore[misc]
    def wrapper(wrapped: Callable[..., Any], _instance: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
        try:
            api_result = wrapped(*args, **kwargs)
        except APIException as err:
            api_result = err.result

        if not isinstance(api_result, APIResult):
            raise RuntimeError(f"APIResult expected, got {api_result!r}")

        ext_return: list[Any] = []
        if hasattr(api_result, HTTP_CODE_ATTR):
            ext_return.append(getattr(api_result, HTTP_CODE_ATTR))

        response = api_result.build_response()
        if ext_return:
            return response, *ext_return

        return response

    return cast(Callable[..., Any], wrapper(func))


def initialize_hooks(app: Flask) -> None:
    @jwt.expired_token_loader
    @jwt.unauthorized_loader
    @api
    def unauthorized_callback(*_: Any) -> APIResult:
        return Unauthorized()

    @app.errorhandler(HTTPException)
    def handle(e: HTTPException) -> tuple[Response, int] | Response:
        api_code = None if e.code is None else HTTP_2_API.get(e.code)
        code, message = (None, e.description) if api_code is None else (api_code, API_CODES[api_code])

        if e.code is None:
            return jsonify(code=code, message=message)
        return jsonify(code=code, message=message), e.code


__all__ = (
    "APIResult",

    "API_CODES",
    "HTTP_2_API",

    "RequestSuccess",
    "LoginSuccess",
    "LogoutSuccess",
    "GetAccounts",
    "GetRoles",
    "GetPermissions",

    "APINotFound",
    "WrongMethod",
    "APIInternalError",
    "APIArgumentError",

    "Unauthorized",
    "PermissionDenied",
    "AccountNotFound",
    "WrongUsernameOrPassword",

    "APIException",

    "api",
    "initialize_hooks",
)
