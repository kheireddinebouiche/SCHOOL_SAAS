from django.urls import path
from .views import *
from .f_views.echeancier import *
from .f_views.preinscrit_paiements import *
from .f_views.echeancier_special import *
from .f_views.suivie_echeancier import *
from .f_views.paiements import *
from .f_views.rembourssement import *
from .f_views.depenses import *
from .f_views.fournisseurs import *
from .f_views.caisse import *
from .f_views.plan_comptable import *

app_name="t_tresorerie"

urlpatterns = [

    path('attentes-de-paiements/', AttentesPaiements, name="attentes_de_paiements"),
    path('ApiListeDemandePaiement', ApiListeDemandePaiement, name="ApiListeDemandePaiement"),
    path('ApiDeleteDemandePaiement', ApiDeleteDemandePaiement, name="ApiDeleteDemandePaiement"),

    path('ApiGetDetailsDemandePaiement', ApiGetDetailsDemandePaiement, name="ApiGetDetailsDemandePaiement"),
    path('ApiGetDetailsDemandePaiementDouble', ApiGetDetailsDemandePaiementDouble, name="ApiGetDetailsDemandePaiementDouble"),

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
    path("ApiLoadDoubleFormation", ApiLoadDoubleFormation, name="ApiLoadDoubleFormation"),

    path('ApiLoadPromo', ApiLoadPromo, name="ApiLoadPromo"),

    path('ApiGetPaiementRequestDetails', ApiGetPaiementRequestDetails, name="ApiGetPaiementRequestDetails"),
    path('ApiGetPaiementRequestDetailsDouble', ApiGetPaiementRequestDetailsDouble, name="ApiGetPaiementRequestDetailsDouble"),
    
    path('ApiDeleteEcheancier', ApiDeleteEcheancier, name="ApiDeleteEcheancier"),
    path('ApiLoadEntiteLegal', ApiLoadEntiteLegal, name="ApiLoadEntiteLegal"),
    
    path("echeanciers-specials/",ListeEcheancierSpecial, name="ListeEcheancierSpecial"),
    path('ApiListEcheancierSpecial', ApiListEcheancierSpecial, name="ApiListEcheancierSpecial"),
    path('ApiApproveEcheancierSpecial', ApiApproveEcheancierSpecial, name="ApiApproveEcheancierSpecial"),
    path('ApiRejectEcheancierSpecial', ApiRejectEcheancierSpecial, name="ApiRejectEcheancierSpecial"),
    path('ApiStoreEcheancierSpecial', ApiStoreEcheancierSpecial, name="ApiStoreEcheancierSpecial"),

    path('ApiApplyRemiseToPaiement', ApiApplyRemiseToPaiement, name="ApiApplyRemiseToPaiement"),
    path('ApiStoreClientPaiement', ApiStoreClientPaiement, name="ApiStoreClientPaiement"),
    
    path('ApiDeletePaiement', ApiDeletePaiement, name="ApiDeletePaiement"),
    path("ApiApplyEcheancierSpecial", ApiApplyEcheancierSpecial, name="ApiApplyEcheancierSpecial"),
    path('ApiLoadSpecialites', ApiLoadSpecialites, name="ApiLoadSpecialites"),

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
    path('rembourssement/details/<int:pk>/',DetailsRembourssement, name="DetailsRembourssement"),
    path('ApiLoadRemboursements/', ApiLoadRemboursements, name="ApiLoadRemboursements"),

    path('ApiCheckEcheancierState', ApiCheckEcheancierState, name="ApiCheckEcheancierState"),
    path('ApiCheckStateModel', ApiCheckStateModel, name="ApiCheckStateModel"),

    ## details attente paiement
    path('ApiGetEntrepriseDetails', ApiGetEntrepriseDetails, name="ApiGetEntrepriseDetails"),

    ## details suivie echeancier
    path('ApiGetEntrepriseInfos', ApiGetEntrepriseInfos, name="ApiGetEntrepriseInfos"),

    path('ApiCheckForPayments', ApiCheckForPayments, name="ApiCheckForPayments"),

    path('ApiGetProspectsList', ApiGetProspectsList, name="ApiGetProspectsList"),


    ##### Gestion des depenses
    path('depenses/liste/',PageDepenses, name="PageDepenses"),
    path('ApiListeDepenses', ApiListeDepenses, name="ApiListeDepenses"),
    path('depenses/creation/', PageNouvelleDepense, name="PageNouvelleDepense"),

    #### Gestion des fournisseurs
    path('fournisseurs/liste/',PageFournisseur, name="PageFournisseur"),
    path('ApiListeFournisseurs',ApiListeFournisseurs, name="ApiListeFournisseurs"),
    path('fournisseur/nouveau-fournisseur/',PageNouveauFournisseur, name="PageNouveauFournisseur"),
    path('fournisseur/details/<int:pk>/', PageDetailsFournisseur, name="PageDetailsFournisseur"),
    path('enregistrer_fournisseur', enregistrer_fournisseur, name="enregistrer_fournisseur"),
    path('UpdateFournisseur', UpdateFournisseur, name="UpdateFournisseur"),
    path('ApiLoadFournisseur', ApiLoadFournisseur, name="ApiLoadFournisseur"),

    #### Gestion des dépenses
    path('parametres/type-depense/', liste_types_depenses, name="liste_types_depenses"),
    path('ApiLoadTypeDepense', ApiLoadTypeDepense, name="ApiLoadTypeDepense"),
    path('ApiStoreNewType', ApiStoreNewType, name="ApiStoreNewType"),
    path('ApiAddCategorieComptable', ApiAddCategorieComptable, name="ApiAddCategorieComptable"),
    path('ApiLoadCategories', ApiLoadCategories, name="ApiLoadCategories"),
    path('ApiGetCategorie', ApiGetCategorie, name="ApiGetCategorie"),
    path('ApiFilterSousCategrorie', ApiFilterSousCategrorie, name="ApiFilterSousCategrorie"),
    path('ApiStoreDepense', ApiStoreDepense, name="ApiStoreDepense"),
    path('ApiGetDepenseDetails',ApiGetDepenseDetails,name="ApiGetDepenseDetails"),
    path('ApiUpdateDepense', ApiUpdateDepense, name="ApiUpdateDepense"),
    path('ApiValidateDepense', ApiValidateDepense, name="ApiValidateDepense"),
    path('ApiDeleteDepense', ApiDeleteDepense, name="ApiDeleteDepense"),

    path('ApiLoadPaiements',ApiLoadPaiements , name="ApiLoadPaiements"),

    path('caisse/brouillard/', PageBrouillardCaisse, name="PageBrouillardCaisse"),
    path('brouillard_caisse_json', brouillard_caisse_json, name="brouillard_caisse_json"),

    path('plan-comptable/',PagePlanComptable, name="PagePlanComptable"),
    path('plan-comptable/create-modal/', CreateCompteModal, name="CreateCompteModal"),
    path('plan-comptable/api/', PlanComptableAPI, name="PlanComptableAPI"),


]