from django.urls import path
from . import views

app_name = 't_ressource_humaine' 
# User asked for app name 't_ressource_humaine'. 
# Standard django practice is app_name = package name usually, but 't_rh' is shorter for templates.
# HOWEVER, there is ALREADY an app 't_rh'. This will cause namespace collision if I use 't_rh'.
# I MUST change app_name to 't_ressource_humaine' or 'rh_formateurs'.
# Given the user context, I should stick to 't_ressource_humaine' to avoid conflict with existing 't_rh'.
# But in views.py I used 't_rh:contrat_list'. I need to fix views.py in the next step or this file.
# I will set app_name='t_ressource_humaine' here and UPDATE views.py.

urlpatterns = [
    path('contrats/', views.ContratListView.as_view(), name='contrat_list'),
    path('contrats/create/', views.ContratCreateView.as_view(), name='contrat_create'),
    path('contrats/<int:pk>/update/', views.ContratUpdateView.as_view(), name='contrat_update'),
    path('contrats/<int:pk>/print/', views.ContratDetailView.as_view(), name='contrat_print'),
    path('contrats/<int:contrat_id>/rubriques/', views.manage_rubriques_contrat, name='manage_rubriques_contrat'),
    
    path('contrats/<int:contrat_id>/generer-paie/', views.generer_paie, name='generer_paie'),
    path('fiches/', views.FichePaieListView.as_view(), name='fiche_paie_list'),
    path('fiches/<int:pk>/', views.FichePaieDetailView.as_view(), name='fiche_paie_detail'),
    path('fiches/<int:pk>/modifier/', views.modifier_paie, name='modifier_paie'),
    path('fiches/<int:pk>/supprimer/', views.supprimer_paie, name='supprimer_paie'),
    
    path('rubriques/', views.RubriqueListView.as_view(), name='rubrique_list'),
    path('rubriques/ajouter/', views.RubriqueCreateView.as_view(), name='rubrique_create'),
    path('rubriques/<int:pk>/modifier/', views.RubriqueUpdateView.as_view(), name='rubrique_update'),
    path('rubriques/<int:pk>/supprimer/', views.RubriqueDeleteView.as_view(), name='rubrique_delete'),

    path('config/', views.config_paie, name='config_paie'),
    path('select-entreprise/', views.select_entreprise_paie, name='select_entreprise_paie'),
]
