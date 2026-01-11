from django import template
from t_communication.models import Message

register = template.Library()

@register.simple_tag(takes_context=True)
def get_unread_messages(context):
    request = context['request']
    if request.user.is_authenticated:
        return Message.objects.filter(receiver=request.user, is_read=False).order_by('-timestamp')[:5]
    return []

@register.simple_tag(takes_context=True)
def get_unread_message_count(context):
    request = context['request']
    if request.user.is_authenticated:
        return Message.objects.filter(receiver=request.user, is_read=False).count()
    return 0
