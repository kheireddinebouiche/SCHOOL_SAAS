from ..models import UserModuleRole

def user_can(user, module_name, permission=None, roles=None):
    """
    Vérifie si un utilisateur peut accéder à une fonctionnalité d'un module
    """

    if not user.is_authenticated:
        return False

    try:
        umr = UserModuleRole.objects.select_related(
            'role', 'module'
        ).get(
            user=user,
            module__name=module_name,
            module__is_active=True,
            role__is_active=True
        )
    except UserModuleRole.DoesNotExist:
        return False

    # Permission du module
    if permission and not umr.has_permission(permission):
        return False

    # Rôles explicites
    if roles and umr.role.name not in roles:
        return False

    return True