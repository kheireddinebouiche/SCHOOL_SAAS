
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification, UserModuleRole
from django.contrib.auth import get_user_model

from django.db import connection

def send_notification_to_user(user, message, link=None, extra_data=None):
    """
    Sends a notification to a specific user.
    """
    schema_name = connection.schema_name
    
    if schema_name == 'public':
        from associe_app.models import SaaSNotification
        notif = SaaSNotification.objects.create(user=user, message=message, link=link)
    else:
        notif = Notification.objects.create(user=user, message=message, link=link)

    channel_layer = get_channel_layer()
    if channel_layer:
        group_name = f"{schema_name}_user_{user.id}"
        print(f"DEBUG NOTIF: Sending to group {group_name}: {message}")
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "message": message,
                "link": link,
                "id": notif.id,
                "extra_data": extra_data
            }
        )

def send_notification_to_role(role_name, message, link=None):
    """
    Sends a notification to all users who have the specified role name, and to superusers.
    """
    from django.db.models import Q
    users = get_user_model().objects.filter(
        Q(module_roles__role__name=role_name) | Q(is_superuser=True)
    ).distinct()
    for user in users:
        send_notification_to_user(user, message, link)

def send_notification_to_module_level(module_name, role_levels, message, link=None):
    """
    Sends a notification to users who have a specific role level in a specific module, and to superusers.
    role_levels: list of integers (e.g. [2, 3] for Supervisor, Manager)
    """
    from django.db.models import Q
    users = get_user_model().objects.filter(
        Q(module_roles__module__name=module_name, module_roles__role__level__in=role_levels) |
        Q(is_superuser=True)
    ).distinct()
    
    for user in users:
        send_notification_to_user(user, message, link)
