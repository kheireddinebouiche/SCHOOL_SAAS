from django.contrib import admin
from django.urls import path
from .views import *
from .f_views.prospects import *
from .f_views.prinscrits import *

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
    path('ApiLoadFormation', ApiLoadFormation, name="ApiLoadFormation"),
    path('details-prospect/<int:pk>/', DetailsProspect, name="DetailsProspect"),

    path('ApiLoadSpecialite', ApiLoadSpecialite, name="ApiLoadSpecialite"), 
    path('ApiLoadProspectDetails', ApiLoadProspectDetails, name="ApiLoadProspectDetails"),
    path('ApiUpdatePropectDetails', ApiUpdatePropectDetails, name="ApiUpdatePropectDetails"),
    path('ApiUpdateProspectEtsDetails', ApiUpdateProspectEtsDetails, name="ApiUpdateProspectEtsDetails"),


    ########################################## Gestion des notes ###################################################
    path('ApiLoadNote', ApiLoadNote, name="ApiLoadNote"),
    path('ApiStoreNote', ApiStoreNote, name="ApiStoreNote"),
    path('ApiDeleteNote', ApiDeleteNote, name="ApiDeleteNote"),
    path('ApiUpdateNote', ApiUpdateNote, name="ApiUpdateNote"),
    ########################################## !Gestion des notes###################################################

    ########################################## Fiche des voeux###################################################
    path('ApiLoadFicheVoeuxProspect', ApiLoadFicheVoeuxProspect, name="ApiLoadFicheVoeuxProspect"),
    ########################################## Fiche des voeux###################################################
    

    path('ApiLoadProspectPerosnalInfos', ApiLoadProspectPerosnalInfos, name="ApiLoadProspectPerosnalInfos"),

    path('ApiLoadProspectRendezVous', ApiLoadProspectRendezVous, name="ApiLoadProspectRendezVous"),
    path('ApiLoadRendezVousDetails', ApiLoadRendezVousDetails, name="ApiLoadRendezVousDetails"),

    path('ApiStoreRappel', ApiStoreRappel, name="ApiStoreRappel"),
    path('ApiDeleteRappel', ApiDeleteRappel, name="ApiDeleteRappel"),
    path('ApiValidateProspect', ApiValidateProspect, name="ApiValidateProspect"),
    path('ApiUpdateRappel', ApiUpdateRappel, name="ApiUpdateRappel"),

    path('liste-des-preinscrits/', ListeDesPrinscrits, name="ListeDesPrinscrits"),
    path('ApiLoadPrinscrits', ApiLoadPrinscrits, name="ApiLoadPrinscrits"),

    path('ApiCheckStatutProspect', ApiCheckStatutProspect, name="ApiCheckStatutProspect"),


    path('details-preinscrit/<int:pk>/', DetailsPrinscrit, name="DetailsPrinscrit"),

    path('ApiLoadFormationAndSpecialite', ApiLoadFormationAndSpecialite, name="ApiLoadFormationAndSpecialite"),

    path('ApiLoadFormation', ApiLoadFormation , name="ApiLoadFormation"),
    path('ApiLoadSpecialite', ApiLoadSpecialite, name="ApiLoadSpecialite"),
    path('ApiUpdateVoeux', ApiUpdateVoeux, name="ApiUpdateVoeux"),

    ################################################### Gestion des pre inscrits ##########################################################

    path('ApiLoadPreinscrisPerosnalInfos', ApiLoadPreinscrisPerosnalInfos, name="ApiLoadPreinscrisPerosnalInfos"),
    path('ApiLoadPreinscritRendezVous', ApiLoadPreinscritRendezVous, name="ApiLoadPreinscritRendezVous"),
    path('ApiLoadNotePr', ApiLoadNotePr, name="ApiLoadNotePr"),
    path('ApiCheckHasCompletedProfile', ApiCheckHasCompletedProfile, name="ApiCheckHasCompletedProfile"),
    path('ApiCheckCompletedDoc', ApiCheckCompletedDoc, name="ApiCheckCompletedDoc"),
    path('ApiUpdatePreinscritInfos', ApiUpdatePreinscritInfos, name="ApiUpdatePreinscritInfos"),
    path('ApiLoadRequiredDocs', ApiLoadRequiredDocs, name="ApiLoadRequiredDocs"),
    path('add_document', add_document, name="add_document"),
    path('LoadPresinscritDocs', LoadPresinscritDocs, name="LoadPresinscritDocs"),
    path("DeleteDocumentPreinscrit",DeleteDocumentPreinscrit,name="DeleteDocumentPreinscrit"),
    path('ApiStoreNotePreinscrit', ApiStoreNotePreinscrit, name="ApiStoreNotePreinscrit"),
    ################################################### Gestion des pre inscrits ##########################################################
   
]
