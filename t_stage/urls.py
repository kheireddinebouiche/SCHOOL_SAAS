from django.urls import path
from . import views

app_name = 't_stage'

urlpatterns = [
    path('', views.stage_dashboard, name='stage_dashboard'),
    path('list/', views.list_stages, name='list_stages'),
    path('<int:stage_id>/', views.stage_detail, name='stage_detail'),
    path('<int:stage_id>/print/', views.print_stage_document, name='print_stage_document'),
    path('launch/', views.launch_stage, name='launch_stage'),
    path('edit/<int:stage_id>/', views.edit_stage, name='edit_stage'),
    path('delete/<int:stage_id>/', views.delete_stage, name='delete_stage'),
    path('ajax/students-by-group/', views.ajax_get_students_by_group, name='ajax_get_students_by_group'),
    path('focus-group/<int:pk>/', views.focus_group_detail, name='focus_group_detail'),
    path('focus-groups/', views.list_focus_groups, name='list_focus_groups'),
    path('focus-group/create/', views.create_focus_group, name='create_focus_group'),
    path('focus-group/<int:fg_id>/add-seance/', views.add_seance, name='add_seance'),
    path('seance/delete/<int:seance_id>/', views.delete_seance, name='delete_seance'),
    path('focus-group/<int:fg_id>/print-sessions/', views.print_sessions, name='print_sessions'),
    path('stage/<int:stage_id>/presentation/', views.progressive_presentation_form, name='presentation_form'),
    path('presentation/delete/<int:pk>/', views.delete_presentation, name='delete_presentation'),
    path('council/', views.validation_council, name='validation_council'),
    path('council/close/<int:pk>/', views.close_council, name='close_council'),
    path('council/quick-decision/', views.quick_decision, name='quick_decision'),
    path('council/<int:pk>/', views.council_detail, name='council_detail'),
    
    # Examens Finaux
    path('examens-finaux/', views.list_groupes_examens_finaux, name='list_groupes_examens_finaux'),
    path('examens-finaux/<int:groupe_id>/toggle-concerne/', views.toggle_concerne_examen, name='toggle_concerne_examen'),
    path('examens-finaux/<int:groupe_id>/saisie/', views.saisie_notes_examen_final, name='saisie_notes_examen_final'),
    path('examens-finaux/<int:groupe_id>/bulletins/', views.bulletins_examen_final, name='bulletins_examen_final'),
]
