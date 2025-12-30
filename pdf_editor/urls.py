from django.urls import path
from . import views

app_name = 'pdf_editor'

urlpatterns = [
    # Main list view
    path('', views.TemplateListView.as_view(), name='template-list'),

    # Template creation - two-step process
    path('create/', views.TemplateCreateBasicView.as_view(), name='template-create'),
    path('create/full/', views.TemplateCreateView.as_view(), name='template-create-full'),

    # Document generation - These need to come before the general slug pattern
    path('<slug:slug>/generate/', views.DocumentGenerationView.as_view(), name='document-generate'),
    path('document/<int:pk>/preview/', views.DocumentPreviewView.as_view(), name='document-preview'),
    path('document/<int:pk>/export/', views.DocumentExportView.as_view(), name='document-export'),
    path('document/<int:pk>/print/', views.DocumentPrintView.as_view(), name='document-print'),

    # Template operations - These should come after document generation to avoid conflicts
    path('<slug:slug>/edit/', views.TemplateUpdateView.as_view(), name='template-update'),
    path('<slug:slug>/delete/', views.TemplateDeleteView.as_view(), name='template-delete'),
    path('<slug:slug>/', views.TemplateDetailView.as_view(), name='template-detail'),
]
