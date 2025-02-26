from django.contrib import admin
from django.urls import path
from .views import *

app_name="t_crm"

urlpatterns = [
    
    path('nouveau-visiteur/',nouveauVisiteur, name="nouveau_visiteur"),
    path('liste-des-visiteurs/',listeVisiteurs, name="liste_visiteurs"),
    path('details-visiteur/<int:pk>/',detailsVisiteur, name="details_visiteur"),

    path('ApiGetSpecialite',ApiGetSpecialite,name="ApiGetSpecialite"),
    
]
