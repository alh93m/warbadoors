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
