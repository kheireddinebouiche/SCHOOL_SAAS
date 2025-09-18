from django.urls import path
from .views import *
from .f_views.echeancier import *
from .f_views.preinscrit_paiements import *
from .f_views.echeancier_special import *

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



    
]