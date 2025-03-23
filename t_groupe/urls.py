from django.contrib import admin
from django.urls import path
from .views import *

app_name="t_groupe"

urlpatterns = [

    path('nouveau-groupe/', NewGroupe, name="nouveaugroupe"),
    path('liste-des-groupes/', ListeGroupe, name="listegroupes"),
    path('details-groupe/<int:pk>/', detailsGroupe, name="detailsgroupe"),
    path('mise-à-jour/<int:pk>/', UpdateGroupe, name="UpdateGroupe"),
    path('supprimer-groupe/<int:pk>/', deleteGroupe, name="deletegroupe"),
    path('brouilon/<int:pk>/', makeGroupeBrouillon, name="makeGroupeBrouillon"),
    path('valider-groupe/<int:pk>/',validateGroupe, name="validateGroupe"),
]
