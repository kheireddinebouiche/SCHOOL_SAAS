from django.urls import path
from . import views

app_name = "t_documents_maker"

urlpatterns = [
    path('', views.editor_home, name='editor_home'),
    path('templates/', views.template_list, name='template_list'),
    path('create/', views.create_template, name='create_template'),
    path('edit/<int:template_id>/', views.edit_template, name='edit_template'),
    path('save/', views.save_template, name='save_template'),
    path('load/<int:template_id>/', views.load_template, name='load_template'),
    path('delete/<int:template_id>/', views.delete_template, name='delete_template'),
    path('variables/', views.list_variables, name='list_variables'),
    path('export/<int:template_id>/', views.export_template, name='export_template'),
    path('generate/<int:template_id>/', views.generate_document, name='generate_document'),
]
