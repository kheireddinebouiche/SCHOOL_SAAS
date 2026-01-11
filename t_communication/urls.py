from django.urls import path
from . import views

app_name = 't_communication'

urlpatterns = [
    # Calendar URLs
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/reminders/', views.reminder_api_list, name='reminder_api_list'),
    path('api/reminders/create/', views.reminder_api_create, name='reminder_api_create'),
    path('api/reminders/<int:pk>/update/', views.reminder_api_update, name='reminder_api_update'),
    path('api/reminders/<int:pk>/delete/', views.reminder_api_delete, name='reminder_api_delete'),
    
    # Messaging URLs
    path('messages/', views.messages_view, name='messages'),
    path('messages/<int:user_id>/', views.conversation_view, name='conversation'),
    path('messages/group/<int:group_id>/', views.group_conversation_view, name='group_conversation'),
    path('api/messages/send/', views.send_message_api, name='send_message_api'),
    path('api/groups/create/', views.create_group_api, name='create_group_api'),
]
