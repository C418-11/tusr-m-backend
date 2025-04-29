# -*- coding: utf-8 -*-


from collections.abc import Callable, Collection
from collections.abc import Iterable
from enum import StrEnum
from typing import Any
from typing import cast

from flask import g
from flask_jwt_extended import current_user
from werkzeug.local import LocalProxy
from wrapt import decorator  # type: ignore[import-untyped]

from .api import APIResult
from .api import PermissionDenied
from .models.auth import User


class PERMISSIONS:
    class PERMISSION(StrEnum):
        GET = "auth/permissions/get"

    class ACCOUNT(StrEnum):
        CREATE = "auth/accounts/create"
        GET = "auth/accounts/get"
        DELETE = "auth/accounts/delete"

    class ROLE(StrEnum):
        CREATE = "auth/roles/create"
        GET = "auth/roles/get"
        DELETE = "auth/roles/delete"


def verify_permissions_in_request(
        permission_names: Collection[str],
        *,
        strategy: Callable[[Iterable[bool]], bool] = all,
) -> bool:
    """
    检查权限需求

    :param permission_names: 权限名
    :type permission_names: list[str]
    :param strategy: 权限检查策略
    :type strategy: Callable[[Iterable[bool]], bool]
    """

    me: User | None = current_user
    permission_names = set(permission_names)

    if me is None:
        _requested_permissions = {name: False for name in permission_names}
        _passed_permissions = set()
        _missing_permissions = permission_names
    else:
        _requested_permissions = {name: me.has_permission(name) for name in permission_names}
        _passed_permissions = set(filter(lambda name: _requested_permissions[name], permission_names))
        _missing_permissions = _requested_permissions.keys() - _passed_permissions

    g._requested_permissions = _requested_permissions
    g._passed_permissions = list(_passed_permissions)
    g._missing_permissions = list(_missing_permissions)

    if me is None or (not strategy(_requested_permissions.values())):
        return False
    return True


def permissions_required[C: Callable[..., APIResult]](
        permission_names: Collection[str],
        *,
        strategy: Callable[[Iterable[bool]], bool] = all,
) -> Callable[[C], C]:
    """
    检查权限需求

    :param permission_names: 权限名
    :type permission_names: list[str]
    :param strategy: 权限检查策略
    :type strategy: Callable[[Iterable[bool]], bool]
    """

    def wrapper(func: C) -> C:
        @decorator  # type: ignore[misc]
        def inner(wrapped: C, _instance: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
            nonlocal permission_names, strategy
            if not verify_permissions_in_request(permission_names, strategy=strategy):
                return PermissionDenied(missing_permissions=get_missing_permissions())

            return wrapped(*args, **kwargs)

        return cast(C, inner(func))

    return wrapper


CONTEXT_NOT_VALID_ERROR_MSG = (
    "You must call `@permissions_required` or `verify_permissions_in_request`"
    "before using this method"
)


def get_requested_permissions() -> dict[str, bool]:
    """
    获取已请求权限

    :return: 已请求权限
    :rtype: dict[str, bool]
    """

    permissions = g.get("_requested_permissions")
    if permissions is None:
        raise RuntimeError(CONTEXT_NOT_VALID_ERROR_MSG)
    return cast(dict[str, bool], permissions)


def get_missing_permissions() -> list[str]:
    """
    获取未通过权限

    :return: 未通过权限
    :rtype: list[str]
    """

    permissions = g.get("_missing_permissions")
    if permissions is None:
        raise RuntimeError(CONTEXT_NOT_VALID_ERROR_MSG)
    return cast(list[str], permissions)


def get_passed_permissions() -> list[str]:
    """
    获取已通过权限

    :return: 已通过权限
    :rtype: list[str]
    """

    permissions = g.get("_passed_permissions")
    if permissions is None:
        raise RuntimeError(CONTEXT_NOT_VALID_ERROR_MSG)
    return cast(list[str], permissions)


requested_permissions = LocalProxy(get_requested_permissions)
missing_permissions = LocalProxy(get_missing_permissions)
passed_permissions = LocalProxy(get_passed_permissions)

__all__ = (
    "PERMISSIONS",
    "permissions_required",
    "get_passed_permissions",
    "passed_permissions",
)
