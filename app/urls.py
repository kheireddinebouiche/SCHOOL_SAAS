from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('institut_app.urls',namespace='institut_app')),
    path('rh/',include('t_rh.urls',namespace='t_rh')),
    path('crm/',include('t_crm.urls',namespace='t_crm')),
    path('pedagogie/',include('t_formations.urls',namespace='t_formations')),
    path('scolarite/groupes/',include('t_groupe.urls',namespace='t_groupe')),
    path('comptabilite/tresorerie/',include('t_tresorerie.urls',namespace='t_tresorerie')),
    path('scolarite/etudiants/', include('t_etudiants.urls', namespace='t_etudiants')),
    path('emploie-du-temps/', include('t_timetable.urls', namespace="t_timetable")),
    path('examens/', include('t_exam.urls', namespace="t_exam")),
    path('conseil/', include('t_conseil.urls', namespace='t_conseil')),
    path('remises/', include('t_remise.urls', namespace='t_remise')),
    path('editeur/', include('t_documents_maker.urls', namespace="t_documents_maker")),
    path('editeur-documents/', include('pdf_editor.urls', namespace="pdf_editor")),
    
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

