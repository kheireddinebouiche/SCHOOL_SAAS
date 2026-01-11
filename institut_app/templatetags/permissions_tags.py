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
