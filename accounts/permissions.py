# permissions.py (create this file in accounts app)
from rest_framework import permissions

class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'superuser'

class IsAdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'superuser']

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.role in ['admin', 'superuser']
# accounts/permissions.py
from rest_framework import permissions

from .utils import has_module_permission


class ModuleViewPermission(permissions.BasePermission):
    module = None 

    def has_permission(self, request, view):
        if self.module is None:
            raise ValueError("ModuleViewPermission requires .module to be set")

        # If module is a string, wrap it in a list to keep logic consistent
        modules_to_check = [self.module] if isinstance(self.module, str) else self.module

        # Check if user has permission for ANY of the modules in the list
        for mod_code in modules_to_check:
            if (
                has_module_permission(request.user, mod_code, "VIEW") or
                has_module_permission(request.user, mod_code, "PREPARER") or
                has_module_permission(request.user, mod_code, "APPROVER") or
                has_module_permission(request.user, mod_code, "ADMIN")
            ):
                return True
        
        return False

class ModulePreparePermission(permissions.BasePermission):
    """
    Can create / edit / prepare in the module
    Allowed: PREPARER + ADMIN
    """
    module = None

    def has_permission(self, request, view):
        if self.module is None:
            raise ValueError("ModulePreparePermission requires .module to be set")

        return (
            has_module_permission(request.user, self.module, "PREPARER") or
            has_module_permission(request.user, self.module, "ADMIN")
        )


class ModuleApprovePermission(permissions.BasePermission):
    """
    Can approve items in the module
    - ADMIN: full access (no department restriction)
    - APPROVER: only own department (user.department == obj.department)
    """
    module = None

    def has_permission(self, request, view):
        if self.module is None:
            raise ValueError("ModuleApprovePermission requires .module to be set")

        return (
            has_module_permission(request.user, self.module, "APPROVER") or
            has_module_permission(request.user, self.module, "ADMIN")
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Superuser → always allowed
        if user.role == 'superuser':
            return True

        # Admin → full access, ignore department
        if has_module_permission(user, self.module, "ADMIN"):
            return True

        # Approver → check department match
        if not has_module_permission(user, self.module, "APPROVER"):
            return False

        # Get target department from the object
        target_dept = getattr(obj, 'department', None)
        if target_dept is None:
            return False  # safety: no department → cannot approve

        # Get user's department
        user_dept = user.department
        if user_dept is None:
            return False  # user has no department → cannot approve

        # Must match exactly
        return target_dept == user_dept


class ModuleAdminPermission(permissions.BasePermission):
    """
    Full admin rights in the module
    Allowed: ADMIN only
    """
    module = None

    def has_permission(self, request, view):
        if self.module is None:
            raise ValueError("ModuleAdminPermission requires .module to be set")

        return has_module_permission(request.user, self.module, "ADMIN")