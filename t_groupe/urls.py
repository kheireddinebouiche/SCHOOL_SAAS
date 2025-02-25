from django.contrib import admin
from django.urls import path
from .views import *

app_name="t_groupe"

urlpatterns = [

    path('nouveau-groupe/', NewGroupe, name="nouveaugroupe"),
    path('liste-des-groupes/', ListeGroupe, name="listegroupes"),
    path('details-groupe/<int:pk>/', detailsGroupe, name="detailsgroupe"),
    path('supprimer-groupe/<int:pk>/', deleteGroupe, name="deletegroupe"),
]
