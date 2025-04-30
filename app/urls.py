from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('institut_app.urls',namespace='institut_app')),
    path('rh/',include('t_rh.urls',namespace='t_rh')),
    path('crm/',include('t_crm.urls',namespace='t_crm')),
    path('pedagogie/',include('t_formations.urls',namespace='t_formations')),
    path('scolartie/groupes/',include('t_groupe.urls',namespace='t_groupe')),
    path('comptabilite/tresorerie/',include('t_tresorerie.urls',namespace='t_tresorerie')),
    path('scolarite/etudiants/', include('t_etudiants.urls', namespace='t_etudiants')),
    path('examens/', include('t_exam.urls', namespace="t_exam")),
    
]
