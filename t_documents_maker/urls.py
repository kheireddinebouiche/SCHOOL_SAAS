from django.urls import path
from . import views

app_name = 'document_manager'

urlpatterns = [
    path('', views.template_list, name='template_list'),
    path('editor/<int:template_id>/', views.template_editor, name='template_editor'),
    path('editor/', views.template_editor, name='template_new'),
    path('delete/<int:template_id>/', views.template_delete, name='template_delete'),
    path('ajax/save/', views.save_template, name='save_template'),
    path('ajax/preview/', views.preview_template, name='preview_template'),
    path('generate/', views.generate_pdf, name='generate_pdf'),
    path('pdf/<int:document_id>/download/', views.download_pdf, name='download_pdf'),
    path('documents/', views.document_list, name='document_list'),
]
