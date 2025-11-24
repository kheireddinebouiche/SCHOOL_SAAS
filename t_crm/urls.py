from django.contrib import admin
from django.urls import path
from .views import *
from .f_views.prospects import *
from .f_views.prinscrits import *
from .f_views.derogations import *
from .f_views.reminder import *
from .f_views.entreprise_prospect import *
from .f_views.secondwishe import *
from .f_views.remise import *
from.f_views.counter import *

app_name="t_crm"

urlpatterns = [
    
    path('nouveau-visiteur/',nouveauVisiteur, name="nouveau_visiteur"),
    path('liste-des-visiteurs/',listeVisiteurs, name="liste_visiteurs"),
    path('ApiListeVisiteurs',ApiListeVisiteurs, name="ApiListeVisiteurs"),
    path('details-visiteur/<int:pk>/',detailsVisiteur, name="details_visiteur"),
    path('mise-a-jours/<int:pk>/', updateVisiteur, name="updateVisiteur"),
    path('delete-visiteur/', supprimerVisiteur, name="supprimer_visiteur"),

    path('ApiGetSpecialite',ApiGetSpecialite,name="ApiGetSpecialite"),
    path('ApiGETDemandeInscription', ApiGETDemandeInscription,name="ApiGETDemandeInscription"),
    path('ApiAddNewDemandeInscription',ApiAddNewDemandeInscription,name='ApiAddNewDemandeInscription'),
    path('liste-demande-inscription/', ListeDemandeInscription, name="ListeDemandeInscription"),
    path('ApiGetListeDemandeInscription', ApiGetListeDemandeInscription, name="ApiGetListeDemandeInscription"),
    path('ApiGetGrideDemandeInscription', ApiGetGrideDemandeInscription, name="ApiGetGrideDemandeInscription"),
    
    
    path('ApiConfirmDemandeInscription', ApiConfirmDemandeInscription, name="ApiConfirmDemandeInscription"),
    path('ApiAnnulerDemandeInscription', ApiAnnulerDemandeInscription, name="ApiAnnulerDemandeInscription"),
    path('ApiRemoveDemandeInscription', ApiRemoveDemandeInscription, name="ApiRemoveDemandeInscription"),

    path('filter_visiteur', filter_visiteur, name="filter_visiteur"),

    path('inscription-particulier/', InscriptionParticulier, name="inscription_particulier"),
    path('inscription-entreprise/', InscriptionEntreprise, name="inscription_entreprise"),
    path('liste-des-prospects/',ListeDesProspects, name="ListeDesProspects"),
    path('ApiLoadProspects',ApiLoadProspects, name="ApiLoadProspects" ),
    path('ApiDeleteProspect', ApiDeleteProspect, name="ApiDeleteProspect"),
    path('ApiFilterProspect', ApiFilterProspect, name="ApiFilterProspect"),
    path('ApiFilterPrinscrit', ApiFilterPrinscrit, name="ApiFilterPrinscrit"),
    path('ApiLoadFormation', ApiLoadFormation, name="ApiLoadFormation"),
    path('details-prospect/<int:pk>/', DetailsProspect, name="DetailsProspect"),
    path('ApiLoadPromos', ApiLoadPromos, name="ApiLoadPromos"),
    #path('ApiLoadSpecialite', ApiLoadSpecialite, name="ApiLoadSpecialite"), 
    path('ApiLoadProspectDetails', ApiLoadProspectDetails, name="ApiLoadProspectDetails"),
    path('ApiUpdatePropectDetails', ApiUpdatePropectDetails, name="ApiUpdatePropectDetails"),
    path('ApiUpdateProspectEtsDetails', ApiUpdateProspectEtsDetails, name="ApiUpdateProspectEtsDetails"),
    path('ApiCreateDoubleDiplomation', ApiCreateDoubleDiplomation, name="ApiCreateDoubleDiplomation"),


    ########################################## Gestion des notes ###################################################
    path('ApiLoadNote', ApiLoadNote, name="ApiLoadNote"),
    path('ApiStoreNote', ApiStoreNote, name="ApiStoreNote"),
    path('ApiDeleteNote', ApiDeleteNote, name="ApiDeleteNote"),
    path('ApiUpdateNote', ApiUpdateNote, name="ApiUpdateNote"),
    ########################################## !Gestion des notes###################################################

    ########################################## Fiche des voeux###################################################
    path('ApiLoadFicheVoeuxProspect', ApiLoadFicheVoeuxProspect, name="ApiLoadFicheVoeuxProspect"),
    path('ApiLoadFicheVoeuxDoubleProspect',ApiLoadFicheVoeuxDoubleProspect, name="ApiLoadFicheVoeuxDoubleProspect"),
    path('ApiConfirmeDoubleDiplome', ApiConfirmeDoubleDiplome, name="ApiConfirmeDoubleDiplome"),
    path('ApiLoadDoubleDiplomations', ApiLoadDoubleDiplomations, name="ApiLoadDoubleDiplomations"),
    path('ApiLoadDoubleSpecialite', ApiLoadDoubleSpecialite, name="ApiLoadDoubleSpecialite"),
    path('ApiUpdateDoubleVoeux',ApiUpdateDoubleVoeux, name="ApiUpdateDoubleVoeux"),
    path('ApiChangeToStandardCursus', ApiChangeToStandardCursus, name="ApiChangeToStandardCursus"),
    ########################################## Fiche des voeux###################################################
    

    path('ApiLoadProspectPerosnalInfos', ApiLoadProspectPerosnalInfos, name="ApiLoadProspectPerosnalInfos"),

    path('ApiLoadProspectRendezVous', ApiLoadProspectRendezVous, name="ApiLoadProspectRendezVous"),
    path('ApiLoadRendezVousDetails', ApiLoadRendezVousDetails, name="ApiLoadRendezVousDetails"),

    path('ApiStoreRappel', ApiStoreRappel, name="ApiStoreRappel"),
    path('ApiDeleteRappel', ApiDeleteRappel, name="ApiDeleteRappel"),
    path('ApiValidateProspect', ApiValidateProspect, name="ApiValidateProspect"),
    path('ApiValidateProspectDouble', ApiValidateProspectDouble, name="ApiValidateProspectDouble"),
    path('ApiUpdateRappel', ApiUpdateRappel, name="ApiUpdateRappel"),

    path('liste-des-preinscrits/', ListeDesPrinscrits, name="ListeDesPrinscrits"),
    path('ApiLoadPrinscrits', ApiLoadPrinscrits, name="ApiLoadPrinscrits"),
    path('ApiLoadPreinscritDoubleVoeux', ApiLoadPreinscritDoubleVoeux, name="ApiLoadPreinscritDoubleVoeux"),
    path('ApiCheckStatutProspect', ApiCheckStatutProspect, name="ApiCheckStatutProspect"),


    path('details-preinscrit/<int:pk>/', DetailsPrinscrit, name="DetailsPrinscrit"),

    path('ApiLoadFormationAndSpecialite', ApiLoadFormationAndSpecialite, name="ApiLoadFormationAndSpecialite"),

    #path('ApiLoadFormation', ApiLoadFormation , name="ApiLoadFormation"),
    path('ApiLoadSpecialite', ApiLoadSpecialite, name="ApiLoadSpecialite"),
    path('ApiLoadSpecialiteProspect', ApiLoadSpecialiteProspect, name="ApiLoadSpecialiteProspect"),
    path('ApiUpdateVoeux', ApiUpdateVoeux, name="ApiUpdateVoeux"),

    path('ApiCheckIfVoeuxExiste', ApiCheckIfVoeuxExiste, name="ApiCheckIfVoeuxExiste"),
    path('ApiCheckIfVoeuxDoubleExiste', ApiCheckIfVoeuxDoubleExiste, name="ApiCheckIfVoeuxDoubleExiste"),

    path('ApiUpdateProspectData', ApiUpdateProspectData, name="ApiUpdateProspectData"),
    path('ApiCreateVoeux', ApiCreateVoeux, name="ApiCreateVoeux"),

    ################################################### Gestion des pre inscrits ##########################################################

    path('ApiLoadPreinscrisPerosnalInfos', ApiLoadPreinscrisPerosnalInfos, name="ApiLoadPreinscrisPerosnalInfos"),
    path('ApiLoadPreinscritRendezVous', ApiLoadPreinscritRendezVous, name="ApiLoadPreinscritRendezVous"),
    path('ApiLoadNotePr', ApiLoadNotePr, name="ApiLoadNotePr"),
    path('ApiCheckHasCompletedProfile', ApiCheckHasCompletedProfile, name="ApiCheckHasCompletedProfile"),
    path('ApiCheckCompletedDoc', ApiCheckCompletedDoc, name="ApiCheckCompletedDoc"),
    path('ApiUpdatePreinscritInfos', ApiUpdatePreinscritInfos, name="ApiUpdatePreinscritInfos"),
    path('ApiLoadRequiredDocs', ApiLoadRequiredDocs, name="ApiLoadRequiredDocs"),

    path('add_document', add_document, name="add_document"),
    path('add_document_double', add_document_double, name="add_document_double"),
    
    path('LoadPresinscritDocs', LoadPresinscritDocs, name="LoadPresinscritDocs"),

    path("DeleteDocumentPreinscrit",DeleteDocumentPreinscrit,name="DeleteDocumentPreinscrit"),
    path('ApiStoreNotePreinscrit', ApiStoreNotePreinscrit, name="ApiStoreNotePreinscrit"),
    
    path('check_all_required_docs', check_all_required_docs, name="check_all_required_docs"),
    path('check_all_required_doc_double', check_all_required_doc_double, name="check_all_required_doc_double"),

    path('ApiStoreRappelPreinscrit', ApiStoreRappelPreinscrit, name="ApiStoreRappelPreinscrit"),
    ################################################### Gestion des dérogations ##########################################################
    
    path('ApiGetDossierDetails', ApiGetDossierDetails, name="ApiGetDossierDetails"),
    path('ApiGetDossierDetailsDouble',ApiGetDossierDetailsDouble, name="ApiGetDossierDetailsDouble"),
    
    path('liste-derogations/', liste_derogations, name="liste_derogations"),
    path('ApiLoadDerogation/', LoadDerogations, name="ApiLoadDerogation"),
    path('ApiCheckDerogationStatus', ApiCheckDerogationStatus, name="ApiCheckDerogationStatus"),
    path('ApiStoreDerogation', ApiStoreDerogation, name="ApiStoreDerogation"),
    path('ApiGetDerogationDetails', ApiGetDerogationDetails, name="ApiGetDerogationDetails"),
    path('ApiTraiteDerogation', ApiTraiteDerogation, name="ApiTraiteDerogation"),
    ################################################### Gestion des dérogations ##########################################################

    path('suivie-des-dossiers/', prospects_incomplets_view, name="prospects_incomplets_view"),

    path('ApiValidateRemider', ApiValidateRemider, name="ApiValidateRemider"),
    path('ApiArchiveReminder', ApiArchiveReminder, name="ApiArchiveReminder"),  

    path('ApiLoadEntrepriseProspectInfo', ApiLoadEntrepriseProspectInfo, name="ApiLoadEntrepriseProspectInfo"),
    path('ApiUpdateEntrepriseData', ApiUpdateEntrepriseData, name="ApiUpdateEntrepriseData"),
    path('ApiUpdateContactInfo', ApiUpdateContactInfo , name="ApiUpdateContactInfo"),

    path('get_crm_counters', get_crm_counters, name="get_crm_counters"),
    path('increment_crm_counter', increment_crm_counter, name="increment_crm_counter"),
    path('get_activity_history', get_activity_history, name="get_activity_history"),

    path('ApiListeSecondWishes', ApiListeSecondWishes, name="ApiListeSecondWishes"),
    path('ApiStoreSecondWish', ApiStoreSecondWish, name="ApiStoreSecondWish"),
    path('ApiDeleteSecondWish', ApiDeleteSecondWish, name="ApiDeleteSecondWish"),
    path('ApiCountFormationSupplementaire', ApiCountFormationSupplementaire, name="ApiCountFormationSupplementaire"),
    path('ApiConfirmeSecondWish', ApiConfirmeSecondWish, name="ApiConfirmeSecondWish"),

    path('gestion-des-reductions/', ListeRemiseApplique, name="ListeRemiseApplique"),
    path('AipLoadRemise', AipLoadRemise, name="AipLoadRemise"),

    path('ApiLoadProspectParticulier', ApiLoadProspectParticulier, name="ApiLoadProspectParticulier"),
    path('ApiStoreApplicedReduction', ApiStoreApplicedReduction, name="ApiStoreApplicedReduction"), 
    path('ApiloadRemiseAppliquer', ApiloadRemiseAppliquer, name="ApiloadRemiseAppliquer"),
    path('ApiLoadRemiseAppliquerDetails', ApiLoadRemiseAppliquerDetails, name="ApiLoadRemiseAppliquerDetails"),

    path('ApiValidatePreinscrit', ApiValidatePreinscrit, name="ApiValidatePreinscrit"),

    path('ApiGeneratePaiementRequest', ApiGeneratePaiementRequest, name="ApiGeneratePaiementRequest"),

    path('ApiLoadFinancialData', ApiLoadFinancialData, name="ApiLoadFinancialData"),

    path('ApiGetReductionDetails', ApiGetReductionDetails, name="ApiGetReductionDetails"),

    path('ApiActivateRemiseAppliquer', ApiActivateRemiseAppliquer, name="ApiActivateRemiseAppliquer"),
    
]
