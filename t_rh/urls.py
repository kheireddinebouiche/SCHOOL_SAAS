from django.contrib import admin
from django.urls import path,include
from .views import *

app_name="t_rh"

urlpatterns = [
    
    path('liste-employes/',listeEmployes, name="liste_employes"),
    path('nouveau-employe/',nouveauEmploye, name="nouveau_employe"),
    path('details-employe/<int:pk>/', detailsEmploye, name="detailsEmploye"),
    path('mise-a-jours/<int:pk>/',updateEmploye,name="updateEmploye"),

    path('nouveau-service/',nouveauService, name="nouveau_service"),
    path('liste-services/',listeServices, name="liste_services"),

    path('nouveau-article-contrat/',NouveauArticleContrat, name="nouveau_article_contrat"),
    path('liste-articles-contrat/',listeArticlesContrat, name="liste_articles_contrat"),
    
]
