from django.urls import path
from .views import *
from .f_views.echeancier import *
from .f_views.preinscrit_paiements import *
from .f_views.echeancier_special import *
from .f_views.suivie_echeancier import *
from .f_views.paiements import *
from .f_views.rembourssement import *

app_name="t_tresorerie"

urlpatterns = [

    path('attentes-de-paiements/', AttentesPaiements, name="attentes_de_paiements"),
    path('ApiListeDemandePaiement', ApiListeDemandePaiement, name="ApiListeDemandePaiement"),
    path('ApiDeleteDemandePaiement', ApiDeleteDemandePaiement, name="ApiDeleteDemandePaiement"),

    path('ApiGetDetailsDemandePaiement', ApiGetDetailsDemandePaiement, name="ApiGetDetailsDemandePaiement"),

    path('details-paiement-request/<int:pk>/',PageDetailsDemandePaiement, name="PageDetailsDemandePaiement"),

    path('configuration/' , PageConfigPaiementSeuil, name="PageConfigPaiementSeuil"),
    path('ApiListSeuilPaiement', ApiListSeuilPaiement, name="ApiListSeuilPaiement"),

    path('ApiListeSpecialite', ApiListeSpecialite, name="ApiListeSpecialite"),
    path('ApiAddNewSeuil', ApiAddNewSeuil, name="ApiAddNewSeuil"),
    path('ApiDeleteSeuil', ApiDeleteSeuil, name="ApiDeleteSeuil"),
    path('ApiGetRequestPaiementsLine', ApiGetRequestPaiementsLine, name="ApiGetRequestPaiementsLine"),

    path('ApiListPaiementDone', ApiListPaiementDone, name="ApiListPaiementDone"),
    path('ApiStorePaiement', ApiStorePaiement, name="ApiStorePaiement"),
    path('ApiDeletePaiement', ApiDeletePaiement, name="ApiDeletePaiement"),

    path('ApiDetailsReceivedPaiement', ApiDetailsReceivedPaiement, name="ApiDetailsReceivedPaiement"),

    path('remboursements/', PageRemboursement , name="PageRemboursement"),
    path('ApiSetRembourssement', ApiSetRembourssement, name="ApiSetRembourssement"),


    path('modeles-echeancier/', ListeModelEcheancier, name="ListeModelEcheancier"),
    path('ApiLoadModelEcheancier', ApiLoadModelEcheancier, name="ApiLoadModelEcheancier"),
    path('ApiLoadFormations', ApiLoadFormations, name="ApiLoadFormations"),

    path('ApiLoadEcheancierDetails', ApiLoadEcheancierDetails, name="ApiLoadEcheancierDetails"),
    path('ApiSaveEcheancier', ApiSaveEcheancier, name="ApiSaveEcheancier"),
    path('ApiUpdateEcheancier', ApiUpdateEcheancier, name="ApiUpdateEcheancier"),
    path('ApiSetEcheancierDefault', ApiSetEcheancierDefault, name="ApiSetEcheancierDefault"),
    path('ApiSaveModeleEcheancier', ApiSaveModeleEcheancier, name="ApiSaveModeleEcheancier"),
    path('ApiLoadModeleEcheancierDetails', ApiLoadModeleEcheancierDetails, name="ApiLoadModeleEcheancierDetails"),
    path('ApiUpdateModeleEcheancier', ApiUpdateModeleEcheancier, name="ApiUpdateModeleEcheancier"),

    path('configuration-des-echeancier/', CreeEcheancier, name="CreeEcheancier"),
    path('echeanciers-configures/', ListeEcheanciersConfigures, name="ListeEcheanciersConfigures"),
    path('ApiLoadEcheanciersConfigures', ApiLoadEcheanciersConfigures, name="ApiLoadEcheanciersConfigures"),
    path('echeancier-appliquer/',echeancierAppliquer, name="echeancierAppliquer"),

    path('ApiLoadPromo', ApiLoadPromo, name="ApiLoadPromo"),

    path('ApiGetPaiementRequestDetails', ApiGetPaiementRequestDetails, name="ApiGetPaiementRequestDetails"),
    

    
    path("echeanciers-specials/",ListeEcheancierSpecial, name="ListeEcheancierSpecial"),
    path('ApiListEcheancierSpecial', ApiListEcheancierSpecial, name="ApiListEcheancierSpecial"),
    path('ApiApproveEcheancierSpecial', ApiApproveEcheancierSpecial, name="ApiApproveEcheancierSpecial"),
    path('ApiRejectEcheancierSpecial', ApiRejectEcheancierSpecial, name="ApiRejectEcheancierSpecial"),
    path('ApiStoreEcheancierSpecial', ApiStoreEcheancierSpecial, name="ApiStoreEcheancierSpecial"),

    path('ApiApplyRemiseToPaiement', ApiApplyRemiseToPaiement, name="ApiApplyRemiseToPaiement"),
    path('ApiStoreClientPaiement', ApiStoreClientPaiement, name="ApiStoreClientPaiement"),
    
    path('ApiDeletePaiement', ApiDeletePaiement, name="ApiDeletePaiement"),
    path("ApiApplyEcheancierSpecial", ApiApplyEcheancierSpecial, name="ApiApplyEcheancierSpecial"),


    path('ApiConfirmInscription', ApiConfirmInscription, name="ApiConfirmInscription"),
    path('ApiRequestRefundPaiement', ApiRequestRefundPaiement, name="ApiRequestRefundPaiement"),
    path('ApiLoadRefundData', ApiLoadRefundData, name="ApiLoadRefundData"),
    path('ApiLoadRefundDetails', ApiLoadRefundDetails, name="ApiLoadRefundDetails"),

    path('ApiAccepteRembourssement', ApiAccepteRembourssement, name="ApiAccepteRembourssement"),
    path('ApiRejectRembourssement', ApiRejectRembourssement, name="ApiRejectRembourssement"),

    path('suivie-des-echeanciers/', SuivieEcheancier, name="SuivieEcheancier"),
    path('ApiLoadConvertedProspects', ApiLoadConvertedProspects, name="ApiLoadConvertedProspects"),

    path('details-suivie-echeancier/<int:pk>/', DetailsEcheancierClient, name="DetailsEcheancierClient"),

    path('liste-des-paiements/', ListeDesPaiements, name="ListeDesPaiements"),
    path('ApiListePaiements', ApiListePaiements, name="ApiListePaiements"),

    path('ApiGetLunchedSpec', ApiGetLunchedSpec, name="ApiGetLunchedSpec"),

    path('ApiGetClientEcheancier', ApiGetClientEcheancier, name="ApiGetClientEcheancier"),

    path('ApiSaveRefundOperation', ApiSaveRefundOperation, name="ApiSaveRefundOperation"),
    path('ApiStats', ApiStats, name="ApiStats"),
    path('ApiShowRefundTraiteResult', ApiShowRefundTraiteResult, name="ApiShowRefundTraiteResult"),

    path('liste-des-rembourssements/', listeDesRembourssement, name="listeDesRembourssement"),
    path('ApiLoadRemboursements/', ApiLoadRemboursements, name="ApiLoadRemboursements"),

    path('ApiCheckEcheancierState', ApiCheckEcheancierState, name="ApiCheckEcheancierState"),
    path('ApiCheckStateModel', ApiCheckStateModel, name="ApiCheckStateModel"),

    path('ApiGetEntrepriseDetails', ApiGetEntrepriseDetails, name="ApiGetEntrepriseDetails"),

    path('ApiCheckForPayments', ApiCheckForPayments, name="ApiCheckForPayments"),

]