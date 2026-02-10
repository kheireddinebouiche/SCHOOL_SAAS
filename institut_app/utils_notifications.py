
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification, UserModuleRole
from django.contrib.auth import get_user_model

def send_notification_to_user(user, message, link=None):
    """
    Sends a notification to a specific user.
    """
    Notification.objects.create(user=user, message=message, link=link)
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "send_notification",
                "message": message,
            }
        )

def send_notification_to_role(role_name, message, link=None):
    """
    Sends a notification to all users who have the specified role name.
    """
    users = get_user_model().objects.filter(module_roles__role__name=role_name).distinct()
    for user in users:
        send_notification_to_user(user, message, link)

def send_notification_to_module_level(module_name, role_levels, message, link=None):
    """
    Sends a notification to users who have a specific role level in a specific module.
    role_levels: list of integers (e.g. [2, 3] for Supervisor, Manager)
    """
    users = get_user_model().objects.filter(
        module_roles__module__name=module_name, 
        module_roles__role__level__in=role_levels
    ).distinct()
    
    for user in users:
        send_notification_to_user(user, message, link)
