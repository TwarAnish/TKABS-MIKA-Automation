# accounts/utils.py
from accounts.models import UserModulePermission


def has_module_permission(user, module_code: str, permission_code: str) -> bool:
    """
    Basic check: does user have this exact permission code in the module?
    Superuser always returns True.
    """
    if not user or not user.is_authenticated:
        return False

    if user.role == 'superuser':
        return True

    return UserModulePermission.objects.filter(
        user=user,
        module__code__iexact=module_code,
        permission__code__iexact=permission_code,
        is_active=True
    ).exists()