from django.contrib import admin
from django.urls import path
from .views import *
from .f_views.formateurs import *
from .f_views.double_diplomation import *

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

    ### Gestion de la double diplomation
    path('formation/double-diplomation/liste/',PageAssociation, name="PageAssociation"),
    path('ApiLoadFormations', ApiLoadFormations, name="ApiLoadFormations"),
    path('ApiLoadSpecialites',ApiLoadSpecialites, name="ApiLoadSpecialites"),
    path('ApiSaveDouble', ApiSaveDouble, name="ApiSaveDouble"),
    path('ApiLoadDoubleDiplomation', ApiLoadDoubleDiplomation, name="ApiLoadDoubleDiplomation"),
    path('ApiDeleteDoubleDiplomation', ApiDeleteDoubleDiplomation, name="ApiDeleteDoubleDiplomation"),
    path('ApiLoadSelestDoubleDiplomation', ApiLoadSelestDoubleDiplomation, name="ApiLoadSelestDoubleDiplomation"),
    path('ApiUpdateDoubleDiplomation', ApiUpdateDoubleDiplomation, name="ApiUpdateDoubleDiplomation"),

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
    path('ApiDeleteCoursRepartition',ApiDeleteCoursRepartition, name="ApiDeleteCoursRepartition"),
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
    path('get_module_details_with_teachers/', get_module_details_with_teachers, name="get_module_details_with_teachers"),

    path('liste-institut/',ListeDesInstituts, name="ListeDesInstituts"),

    path('ApiGetPartenaireSync', ApiGetPartenaireSync, name="ApiGetPartenaireSync"),
    path('ApiSyncPartenaire', ApiSyncPartenaire, name="ApiSyncPartenaire"),
    path('mise-a-jour-partenaire/<int:pk>/',UpdatePartenaire, name="UpdatePartenaire"),

    path('ApiLoadDocuments', ApiLoadDocuments , name="ApiLoadDocuments"),
    path('ApiAddDocument', ApiAddDocument, name="ApiAddDocument"),
    path('ApiDeleteDoc', ApiDeleteDoc, name="ApiDeleteDoc"),

    path('ApiLoadSpecForPartenaire', ApiLoadSpecForPartenaire, name="ApiLoadSpecForPartenaire"),

    # URL pour enregistrer les documents d'impression sélectionnés
    path('formation/<int:pk>/save-print-documents/', save_print_documents, name="save_print_documents"),
    # URL pour récupérer les documents d'impression sélectionnés
    path('formation/<int:pk>/get-print-documents/', get_print_documents, name="get_print_documents"),
    path('ApiLoadDocumentTemplate', ApiLoadDocumentTemplate, name="ApiLoadDocumentTemplate"),

    ### TRAITEMENT DES FORMATEURS ###
    path('formateurs/liste/',PageFormateurs, name="PageFormateurs"),
    path('create_formateur/', create_formateur, name="create_formateur"),
    path('update_formateur/', update_formateur, name="update_formateur"),
    path('delete_formateur/', delete_formateur, name="delete_formateur"),
    path('ApiGetFormateurs/', ApiGetFormateurs, name="ApiGetFormateurs"),
    path('assign_trainers_to_module/', assign_trainers_to_module, name="assign_trainers_to_module"),
    path('load_module_teachers/', load_module_teachers, name="load_module_teachers"),
    path('remove_trainer_from_module/', remove_trainer_from_module, name="remove_trainer_from_module"),
    path('update_module_details/', update_module_details, name="update_module_details"),
    path('validate_module/', validate_module, name="validate_module"),
    path('create_availability', create_availability, name="create_availability"),
    path('get_availability', get_availability, name="get_availability"),
    path('delete_availability', delete_availability, name="delete_availability"),


    path('ApiGetSpecialitesFromCombinaison',ApiGetSpecialitesFromCombinaison ,name="ApiGetSpecialitesFromCombinaison"),
]
