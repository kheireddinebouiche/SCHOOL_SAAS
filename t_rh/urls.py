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
    path('ApiListeServices', ApiListeServices, name="ApiListeServices"),
    path('ApiAddService', ApiAddService, name="ApiAddService"),
    path('ApiGetService', ApiGetService, name="ApiGetService"),
    path('ApiUpdateService', ApiUpdateService, name="ApiUpdateService"),
    path('ApiDeleteService', ApiDeleteService, name="ApiDeleteService"),

    path('nouveau-article-contrat/',NouveauArticleContrat, name="nouveau_article_contrat"),
    path('liste-articles-contrat/',listeArticlesContrat, name="liste_articles_contrat"),
    path('types-contrat/', listeTypeContrat, name="listeTypeContrat"),
    path('ApiListeTypeContrat', ApiListeTypeContrat, name="ApiListeTypeContrat"),
    path('ApiAddTypeContrat', ApiAddTypeContrat, name="ApiAddTypeContrat"),
    path('ApiUpdateTypeContrat', ApiUpdateTypeContrat, name="ApiUpdateTypeContrat"),
    path('ApiDeleteTypeContrat', ApiDeleteTypeContrat, name="ApiDeleteTypeContrat"),
    path('clauses-type-contrat/standard/<int:pk>/', ClausesTypeContrat, name="ClausesTypeContrat"),
    path('ApiGetClauseStandardOfType', ApiGetClauseStandardOfType, name="ApiGetClauseStandardOfType"),
    path('ApiAddNewClause', ApiAddNewClause, name="ApiAddNewClause"),
    path('ApiDeleteClause', ApiDeleteClause, name="ApiDeleteClause"),
    path('ApiUpdateClause', ApiUpdateClause, name="ApiUpdateClause"),

    path('categories-contrat/', ListeCategorieContrat, name="ListeCategorieContrat"),
    path('ApiListCategorie', ApiListCategorie, name="ApiListCategorie"),
    path('ApiGetDefaultValueForContrat', ApiGetDefaultValueForContrat, name="ApiGetDefaultValueForContrat"),
    path('ApiApiAddCategorieContrat', ApiAddCategorieContrat, name="ApiApiAddCategorieContrat"),
    path('details-catagories/<int:pk>/',detailsCategorie, name="detailsCategorie"),
    path('ApiGetListeTypeContratByCategorie', ApiGetListeTypeContratByCategorie, name="ApiGetListeTypeContratByCategorie"),

    path('ApiGetCategorieContrat', ApiGetCategorieContrat, name="ApiGetCategorieContrat"),
    path('ApiGetTypeContrat', ApiGetTypeContrat, name="ApiGetTypeContrat"),

    path('ApiCreateContrat', ApiCreateContrat, name="ApiCreateContrat"),

    path('liste-des-postes/', ListeDesPostes , name="ListeDesPostes"),
    path('ApiAddPoste', ApiAddPoste, name="ApiAddPoste"),
    path('ApiListePostes', ApiListePostes, name="ApiListePostes"),
    path('ApiGetListContratForEmploye', ApiGetListContratForEmploye, name="ApiGetListContratForEmploye"),
    path('mise-a-jours-poste/<int:pk>/',UpdatePoste, name="updatePoste"),

    path('ApiGetEntite', ApiGetEntite, name="ApiGetEntite"),

    path('contrat_temp/',view_contrat, name="view_contrat"),
]
