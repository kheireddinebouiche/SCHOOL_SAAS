from django import template
from institut_app.permissions.utils import user_can

register = template.Library()

@register.simple_tag(takes_context=True)
def user_can_access(context, module, permission=None, role=None):
    request = context['request']
    return user_can(
        request.user,
        module,
        permission,
        roles=[role] if role else None,
    )

@register.simple_tag
def has_submenu_access(user, module_code, submenu_code):
    if user.is_superuser:
        return True
    from institut_app.models import UserSubMenuAccess
    return UserSubMenuAccess.objects.filter(
        user=user,
        module_code=module_code,
        submenu_code=submenu_code,
        is_active=True
    ).exists()
