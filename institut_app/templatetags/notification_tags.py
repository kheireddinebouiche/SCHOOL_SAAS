
from django import template
from institut_app.models import Notification

register = template.Library()

@register.simple_tag(takes_context=True)
def get_unread_notifications(context):
    request = context['request']
    if request.user.is_authenticated:
        return Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5]
    return []

@register.simple_tag(takes_context=True)
def get_recent_notifications(context):
    request = context['request']
    if request.user.is_authenticated:
        return Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    return []

@register.simple_tag(takes_context=True)
def get_unread_notification_count(context):
    request = context['request']
    if request.user.is_authenticated:
        return Notification.objects.filter(user=request.user, is_read=False).count()
    return 0
