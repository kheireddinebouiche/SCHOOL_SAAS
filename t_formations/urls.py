from django.contrib import admin
from django.urls import path
from .views import *

app_name="t_formations"

urlpatterns = [

    path('formations/nouvelle-formation/', addFormation, name="addFormation"),
    path('specialites/nouvelle-specialite/', addSpecialite, name="addSpecialite"),
    path('formations/liste-des-formation/', listFormations, name="listFormations"),
    path('specialites/liste-des-specialitees/',listSpecialites, name="listSpecialites"),
    
    path('specialites/details-specialite/<int:pk>/', detailSpecialite, name="detailSpecialite"),
    path('formations/details-formations/<int:pk>/', detailFormation, name="detailFormation"),
    path('supprimer-specialite/<int:pk>/', deleteSpecialite, name="deleteSpecialite"),
    path('specilaites/modification-specialite/<int:pk>/', updateSpecialite, name="updateSpecialite"),


    path('nouveau-partenaire/', AddPartenaire, name="addPartenaire"),
    path('liste-partenaires/', ListeDesPartenaires, name="listPartenaires"),
    path('details-partenaire/<int:pk>/', detailsPartenaire, name="detailsPartenaire"),
    path('supprimer-partenaire/<int:pk>/', deletePartenaire, name="deletePartenaire"),

    path('apigetmodules',ApiGetSpecialiteModule, name="ApiGeSpecialitetModules"),
    path('deleteModule',deleteModule,name="deletemodule"),
    path('ApiAddModule', ApiAddModule, name="ApiAddModule"),
    path('ApiUpdateModule', ApiUpdateModule, name="ApiUpdateModule"),

    path('archive-modules/' , archiveModule, name="archiveModule"),
    path('ApiGetModuleDetails', ApiGetModuleDetails, name="ApiGetModuleDetails"),
    path('archiveFormation' , archiveFormation, name="archiveFormation"),
    
    path('promos/nouvelle-promotion/',AddPromo, name="AddPromo"),
    path('promos/liste-des-promotions/',listPromos, name="listPromos"),
    path('ApiListePromos',ApiListePromos,name="ApiListePromos"),
    path('ApiGetPromo',ApiGetPromo,name="ApiGetPromo"),
    path('ApiUpdatePromo',ApiUpdatePromo,name="ApiUpdatePromo"),
    path('ApiActivatePromo', ApiActivatePromo, name="ApiActivatePromo"),
    path('ApiDeletePromo',ApiDeletePromo,name="ApiDeletePromo"),

]
