
from django import template
from associe_app.models import SaaSNotification

register = template.Library()

@register.simple_tag(takes_context=True)
def get_unread_saas_notifications(context):
    request = context['request']
    if request.user.is_authenticated:
        return SaaSNotification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5]
    return []

@register.simple_tag(takes_context=True)
def get_recent_saas_notifications(context):
    request = context['request']
    if request.user.is_authenticated:
        return SaaSNotification.objects.filter(user=request.user).order_by('-created_at')[:10]
    return []

@register.simple_tag(takes_context=True)
def get_unread_saas_notification_count(context):
    request = context['request']
    if request.user.is_authenticated:
        return SaaSNotification.objects.filter(user=request.user, is_read=False).count()
    return 0
