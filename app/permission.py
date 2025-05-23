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

    class ROLE(StrEnum):
        CREATE = "auth/roles/create"
        GET = "auth/roles/get"
        DELETE = "auth/roles/delete"

    class ACCOUNT(StrEnum):
        CREATE = "auth/accounts/create"
        GET = "auth/accounts/get"
        LIST = "auth/accounts/list"
        DELETE = "auth/accounts/delete"
        UPDATE = "auth/accounts/update"
        UPDATE_SELF_PASSWORD = "auth/accounts/update/self_password"

    class TABLE(StrEnum):
        GET = "data/tables/get"
        LIST = "data/tables/list"

    class DATA(StrEnum):
        GET = "data/get"
        LIST = "data/list"
        CREATE = "data/create"
        UPDATE = "data/update"
        DELETE = "data/delete"


def verify_permissions_in_request(
        permission_names: Collection[str],
        *,
        strategy: Callable[[Iterable[Any]], bool],
        check_active: bool = True,
) -> bool:
    """
    检查权限需求

    :param permission_names: 权限名
    :type permission_names: list[str]
    :param strategy: 权限检查策略
    :type strategy: Callable[[Iterable[Any]], bool]
    :param check_active: 是否检查账户是否激活
    :type check_active: bool
    """

    me: User | None = current_user
    permission_names = set(permission_names)

    if me is None:
        _requested_permissions = {name: False for name in permission_names}
        _passed_permissions = set()
        _missing_permissions = permission_names
        _account_active = False
    else:
        _requested_permissions = {name: me.has_permission(name) for name in permission_names}
        _passed_permissions = set(filter(lambda name: _requested_permissions[name], permission_names))
        _missing_permissions = _requested_permissions.keys() - _passed_permissions
        _account_active = me.active  # type: ignore[assignment]

    g._requested_permissions = _requested_permissions
    g._passed_permissions = list(_passed_permissions)
    g._missing_permissions = list(_missing_permissions)
    g._account_active = _account_active

    return not any((
            me is None,
            check_active and not _account_active,
            not strategy(_requested_permissions.values()),
    ))


def permissions_required[C: Callable[..., APIResult]](
        permission_names: Collection[str],
        *,
        strategy: Callable[[Iterable[Any]], bool] = all,
        check_active: bool = True,
) -> Callable[[C], C]:
    """
    检查权限需求

    :param permission_names: 权限名
    :type permission_names: list[str]
    :param strategy: 权限检查策略
    :type strategy: Callable[[Iterable[Any]], bool]
    :param check_active: 是否检查账户是否激活
    :type check_active: bool
    """

    def wrapper(func: C) -> C:
        @decorator  # type: ignore[misc]
        def inner(wrapped: C, _instance: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
            if not verify_permissions_in_request(permission_names, strategy=strategy, check_active=check_active):
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


def get_account_active() -> bool:
    """
    获取账户是否激活

    :return: 账户是否激活
    :rtype: bool
    """

    active = g.get("_account_active")
    if active is None:
        raise RuntimeError(CONTEXT_NOT_VALID_ERROR_MSG)
    return cast(bool, active)


requested_permissions = LocalProxy(get_requested_permissions)
missing_permissions = LocalProxy(get_missing_permissions)
passed_permissions = LocalProxy(get_passed_permissions)
account_active = LocalProxy(get_account_active)

__all__ = (
    "PERMISSIONS",

    "verify_permissions_in_request",
    "permissions_required",

    "get_requested_permissions",
    "get_missing_permissions",
    "get_passed_permissions",
    "get_account_active",

    "requested_permissions",
    "missing_permissions",
    "passed_permissions",
    "account_active",
)
