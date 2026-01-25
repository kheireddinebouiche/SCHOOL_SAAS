from django.urls import path
from . import views

app_name = 't_stage'

urlpatterns = [
    path('', views.stage_dashboard, name='stage_dashboard'),
    path('list/', views.list_stages, name='list_stages'),
    path('launch/', views.launch_stage, name='launch_stage'),
    path('edit/<int:stage_id>/', views.edit_stage, name='edit_stage'),
    path('ajax/students-by-group/', views.ajax_get_students_by_group, name='ajax_get_students_by_group'),
    path('focus-group/<int:pk>/', views.focus_group_detail, name='focus_group_detail'),
    path('focus-groups/', views.list_focus_groups, name='list_focus_groups'),
    path('focus-group/create/', views.create_focus_group, name='create_focus_group'),
    path('focus-group/<int:fg_id>/add-seance/', views.add_seance, name='add_seance'),
    path('focus-group/<int:fg_id>/print-sessions/', views.print_sessions, name='print_sessions'),
    path('stage/<int:stage_id>/presentation/', views.progressive_presentation_form, name='presentation_form'),
    path('presentation/delete/<int:pk>/', views.delete_presentation, name='delete_presentation'),
    path('council/', views.validation_council, name='validation_council'),
    path('council/quick-decision/', views.quick_decision, name='quick_decision'),
    path('council/<int:pk>/', views.council_detail, name='council_detail'),
]
