from django.contrib import admin
from django.urls import path
from .views import *

app_name="t_formations"

urlpatterns = [

    path('formations/nouvelle-formation/', addFormation, name="addFormation"),
    path('ApiCheckIfFormationCompleted', ApiCheckIfFormationCompleted, name="ApiCheckIfFormationCompleted"),
    path('ApiListeFormation', ApiListeFormation, name="ApiListeFormation"),
    path('ApiListeSpecialiteByFormation', ApiListeSpecialiteByFormation, name="ApiListeSpecialiteByFormation"),
    path('specialites/nouvelle-specialite/', addSpecialite, name="addSpecialite"),
    path('formations/liste-des-formation/', listFormations, name="listFormations"),
    path('specialites/liste-des-specialitees/',listSpecialites, name="listSpecialites"),
    path('ApigetFormationSync', ApigetFormationSync, name="ApigetFormationSync"),
    path('ApiSyncFormation',ApiSyncFormation, name="ApiSyncFormation"),
    path('ApiSyncUpdateFormation', ApiSyncUpdateFormation, name="ApiSyncUpdateFormation"),
    path('ApiCheckFormationState', ApiCheckFormationState, name="ApiCheckFormationState"),

    path('formations/modification/<int:pk>/', updateFormation, name="updateFormation"),
    
    path('specialites/details-specialite/<int:pk>/', detailSpecialite, name="detailSpecialite"),
    path('formations/details-formations/<int:pk>/', detailFormation, name="detailFormation"),
    path('supprimer-specialite/<int:pk>/', deleteSpecialite, name="deleteSpecialite"),
    path('specilaites/modification-specialite/<int:pk>/', updateSpecialite, name="updateSpecialite"),


    path('nouveau-partenaire/', AddPartenaire, name="addPartenaire"),
    path('liste-partenaires/', ListeDesPartenaires, name="listPartenaires"),
    path('details-partenaire/<int:pk>/', detailsPartenaire, name="detailsPartenaire"),
    path('supprimer-partenaire/<int:pk>/', deletePartenaire, name="deletePartenaire"),

    path('apigetmodules',ApiGetSpecialiteModule, name="ApiGeSpecialitetModules"),
    path('ApiGetRepartitionModule', ApiGetRepartitionModule, name="ApiGetRepartitionModule"),
    path('ApiAffectModuleSemestre', ApiAffectModuleSemestre, name="ApiAffectModuleSemestre"),
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

    path('modules/liste-des-modules/', PageListeModules, name="PageListeModules"),
    path('ApiGetModules', ApiGetModules, name="ApiGetModules"),
    path('ApiGetModuleDetails', ApiGetModuleDetails, name="ApiGetModuleDetails"),

    path('liste-institut/',ListeDesInstituts, name="ListeDesInstituts"),

    path('ApiGetPartenaireSync', ApiGetPartenaireSync, name="ApiGetPartenaireSync"),
    path('ApiSyncPartenaire', ApiSyncPartenaire, name="ApiSyncPartenaire"),
    path('mise-a-jour-partenaire<int:pk>/',UpdatePartenaire, name="UpdatePartenaire"),

]
