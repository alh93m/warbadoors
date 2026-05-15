from functools import wraps
from typing import Callable, Iterable

from django.http import HttpRequest, HttpResponseForbidden
from rest_framework.permissions import BasePermission

from accounts.models import User


def _user_has_role(user: User | None, roles: Iterable[str]) -> bool:
    """Return True if the user matches one of the given role identifiers.

    The function is intentionally permissive with anonymous users (returns False).
    Use central helpers to avoid role checks scattered across views.
    """
    if not user or not getattr(user, 'is_authenticated', False):
        return False
    return any(user.role == r for r in roles) or user.is_superuser


def role_required(roles: Iterable[str]):
    """Decorator for Django function views to require one of the specified roles.

    Example:
        @role_required(['sales_manager', 'sales_rep'])
        def view(request): ...
    """

    def decorator(view_func: Callable):
        @wraps(view_func)
        def _wrapped(request: HttpRequest, *args, **kwargs):
            if _user_has_role(getattr(request, 'user', None), roles):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden('Insufficient role permissions')

        return _wrapped

    return decorator


class IsInRole(BasePermission):
    """DRF permission class that allows access only to users in given roles.

    Usage in a viewset:
        permission_classes = [IsInRole]
        extra_kwargs = {'roles': ['accountant']}

    For flexibility, views should define `required_roles = ['role1','role2']`.
    """

    def has_permission(self, request, view):
        roles = getattr(view, 'required_roles', None)
        if roles is None:
            # No roles specified -> fallback to authenticated only
            return bool(request.user and request.user.is_authenticated)
        return _user_has_role(getattr(request, 'user', None), roles)
"""DRF permission hooks aligned with accounts.User roles."""

from rest_framework import permissions


class IsRole(permissions.BasePermission):
    """Allow only users whose role is in ``allowed_roles`` (or superuser)."""

    allowed_roles = ()

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        role = getattr(user, 'role', None)
        return role in self.allowed_roles


class IsInventoryManager(IsRole):
    allowed_roles = ('inventory_manager', 'admin')


class IsSalesRepresentative(IsRole):
    allowed_roles = ('sales_rep', 'admin')


class IsAdministrator(IsRole):
    allowed_roles = ('admin',)


class IsCustomerOrReadOnly(permissions.BasePermission):
    """Staff roles can write; customers read-only on unsafe methods."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        role = getattr(user, 'role', None)
        return role in ('admin', 'inventory_manager', 'sales_rep')
