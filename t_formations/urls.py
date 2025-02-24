from django.contrib import admin
from django.urls import path
from .views import *

app_name="t_formations"

urlpatterns = [

    path('nouvelle-formation/', addFormation, name="addFormation"),
    path('nouvelle-specialite/', addSpecialite, name="addSpecialite"),
    path('liste-des-formation/', listFormations, name="listFormations"),
    path('liste-des-specialitees/',listSpecialites, name="listSpecialites"),
    path('details-formations/<int:pk>/', detailFormation, name="detailFormation"),


    path('nouveau-partenaire/', AddPartenaire, name="addPartenaire"),
    path('liste-partenaires/', ListeDesPartenaires, name="listPartenaires"),
    path('details-partenaire/<int:pk>/', detailsPartenaire, name="detailsPartenaire"),
    path('supprimer-partenaire/<int:pk>/', deletePartenaire, name="deletePartenaire"),
]
