from django.urls import path
from institut_app.decorators import submenu_access_required
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
from .f_views.suivi_cheques import *

from .f_views.plan_comptable import *
from .f_views import facturation
from .f_views.produits import *
from .f_views.imputation_comptable_specialite import *
from .f_views.autre_paiement import *
from .f_views.invoice_generation import *
from .f_views.configure_penalite import *
from .f_views.reporting_das import *
from .f_views.type_depense import *
from .f_views.payment_types import *
from .f_views.suivi_paiements import *
from .views_paie import *

from t_conseil.views import ListeDesFactures, ListeDesDevis, ListeDesClients

from t_crm.f_views.remise import (
    ListeRemiseApplique, AipLoadRemise, ApiStoreApplicedReduction,
    ApiStoreSingleReduction,
    ApiloadRemiseAppliquer, ApiLoadRemiseAppliquerDetails,
    ApiGetReductionDetails, ApiActivateRemiseAppliquer,
    ApiLoadProspectParticulier, ApiDeleteRemiseAppliquer
)

app_name="t_tresorerie"

urlpatterns = [

    # Suivi Cheques
    path('caisse/suivi-cheques-emis/', submenu_access_required("tre", "banque")(PageSuiviChequesEmis), name="PageSuiviChequesEmis"),
    path('caisse/api/suivi-cheques-emis/list/', ApiListChequesEmis, name="ApiListChequesEmis"),
    path('caisse/api/suivi-cheques-emis/update/', ApiUpdateChequeStatut, name="ApiUpdateChequeStatut"),


    path('attentes-de-paiements/', submenu_access_required("tre", "tresorerie")(AttentesPaiements), name="attentes_de_paiements"),
    path('ApiListeDemandePaiement', ApiListeDemandePaiement, name="ApiListeDemandePaiement"),
    path('ApiDeleteDemandePaiement', ApiDeleteDemandePaiement, name="ApiDeleteDemandePaiement"),

    path('ApiGetDetailsDemandePaiement', ApiGetDetailsDemandePaiement, name="ApiGetDetailsDemandePaiement"),
    path('ApiGetDetailsDemandePaiementDouble', ApiGetDetailsDemandePaiementDouble, name="ApiGetDetailsDemandePaiementDouble"),
    path('ApiSaveSelectedEcheancier', ApiSaveSelectedEcheancier, name="ApiSaveSelectedEcheancier"),

    path('details-paiement-request/<int:pk>/',PageDetailsDemandePaiement, name="PageDetailsDemandePaiement"),

    path('configuration/' , submenu_access_required("tre", "parametres")(PageConfigPaiementSeuil), name="PageConfigPaiementSeuil"),
    path('configuration/paiement-facturation/', submenu_access_required("tre", "parametres")(PageConfigPaiementFacturation), name="PageConfigPaiementFacturation"),
    path('ApiListSeuilPaiement', ApiListSeuilPaiement, name="ApiListSeuilPaiement"),

    path('ApiListeSpecialite', ApiListeSpecialite, name="ApiListeSpecialite"),
    path('ApiAddNewSeuil', ApiAddNewSeuil, name="ApiAddNewSeuil"),
    path('ApiDeleteSeuil', ApiDeleteSeuil, name="ApiDeleteSeuil"),
    path('ApiGetRequestPaiementsLine', ApiGetRequestPaiementsLine, name="ApiGetRequestPaiementsLine"),

    path('ApiListPaiementDone', ApiListPaiementDone, name="ApiListPaiementDone"),
    path('ApiStorePaiement', ApiStorePaiement, name="ApiStorePaiement"),
    path('ApiDeletePaiement', ApiDeletePaiement, name="ApiDeletePaiement"),

    path('ApiDetailsReceivedPaiement', ApiDetailsReceivedPaiement, name="ApiDetailsReceivedPaiement"),

    path('remboursements/', submenu_access_required("tre", "remboursement")(PageRemboursement) , name="PageRemboursement"),
    path('ApiSetRembourssement', ApiSetRembourssement, name="ApiSetRembourssement"),


    path('modeles-echeancier/', submenu_access_required("tre", "echeanciers")(ListeModelEcheancier), name="ListeModelEcheancier"),
    path('ApiLoadModelEcheancier', ApiLoadModelEcheancier, name="ApiLoadModelEcheancier"),
    path('ApiLoadFormations', ApiLoadFormations, name="ApiLoadFormations"),

    path('ApiLoadEcheancierDetails', ApiLoadEcheancierDetails, name="ApiLoadEcheancierDetails"),
    path('ApiSaveEcheancier', ApiSaveEcheancier, name="ApiSaveEcheancier"),
    path('ApiUpdateEcheancier', ApiUpdateEcheancier, name="ApiUpdateEcheancier"),
    path('ApiSetEcheancierDefault', ApiSetEcheancierDefault, name="ApiSetEcheancierDefault"),
    path('ApiToggleEcheancierAvailability', ApiToggleEcheancierAvailability, name="ApiToggleEcheancierAvailability"),
    path('ApiSaveModeleEcheancier', ApiSaveModeleEcheancier, name="ApiSaveModeleEcheancier"),
    path('ApiLoadModeleEcheancierDetails', ApiLoadModeleEcheancierDetails, name="ApiLoadModeleEcheancierDetails"),
    path('ApiUpdateModeleEcheancier', ApiUpdateModeleEcheancier, name="ApiUpdateModeleEcheancier"),

    path('configuration-des-echeancier/', submenu_access_required("tre", "echeanciers")(CreeEcheancier), name="CreeEcheancier"),
    path('echeanciers-configures/', submenu_access_required("tre", "echeanciers")(ListeEcheanciersConfigures), name="ListeEcheanciersConfigures"),
    path('ApiLoadEcheanciersConfigures', ApiLoadEcheanciersConfigures, name="ApiLoadEcheanciersConfigures"),
    path('echeancier-appliquer/',echeancierAppliquer, name="echeancierAppliquer"),
    path("ApiLoadDoubleFormation", ApiLoadDoubleFormation, name="ApiLoadDoubleFormation"),

    path('ApiLoadPromo', ApiLoadPromo, name="ApiLoadPromo"),

    path('ApiGetPaiementRequestDetails', ApiGetPaiementRequestDetails, name="ApiGetPaiementRequestDetails"),
    path('ApiGetPaiementRequestDetailsDouble', ApiGetPaiementRequestDetailsDouble, name="ApiGetPaiementRequestDetailsDouble"),
    path('ApiCancelPaiementRequest', ApiCancelPaiementRequest, name="ApiCancelPaiementRequest"),
    path('ApiCancelDuePaiements', ApiCancelDuePaiements, name="ApiCancelDuePaiements"),
    
    path('ApiDeleteEcheancier', ApiDeleteEcheancier, name="ApiDeleteEcheancier"),
    path('ApiBulkDeleteEcheanciers', ApiBulkDeleteEcheanciers, name="ApiBulkDeleteEcheanciers"),
    path('ApiLoadEntiteLegal', ApiLoadEntiteLegal, name="ApiLoadEntiteLegal"),
    
    path("echeanciers-specials/",submenu_access_required("tre", "echeanciers")(ListeEcheancierSpecial), name="ListeEcheancierSpecial"),
    path('ApiListEcheancierSpecial', ApiListEcheancierSpecial, name="ApiListEcheancierSpecial"),
    path('ApiApproveEcheancierSpecial', ApiApproveEcheancierSpecial, name="ApiApproveEcheancierSpecial"),
    path('ApiRejectEcheancierSpecial', ApiRejectEcheancierSpecial, name="ApiRejectEcheancierSpecial"),
    path('ApiStoreEcheancierSpecial', ApiStoreEcheancierSpecial, name="ApiStoreEcheancierSpecial"),

    path('ApiApplyRemiseToPaiement', ApiApplyRemiseToPaiement, name="ApiApplyRemiseToPaiement"),
    path('ApiCancelRemiseToPaiement', ApiCancelRemiseToPaiement, name="ApiCancelRemiseToPaiement"),
    path('ApiStoreClientPaiement', ApiStoreClientPaiement, name="ApiStoreClientPaiement"),
    
    path('ApiDeletePaiement', ApiDeletePaiement, name="ApiDeletePaiement"),
    path("ApiApplyEcheancierSpecial", ApiApplyEcheancierSpecial, name="ApiApplyEcheancierSpecial"),
    path("ApiCancelEcheancierSpecial", ApiCancelEcheancierSpecial, name="ApiCancelEcheancierSpecial"),
    path('ApiLoadSpecialites', ApiLoadSpecialites, name="ApiLoadSpecialites"),

    path('ApiConfirmInscription', ApiConfirmInscription, name="ApiConfirmInscription"),
    path('ApiConfirmInscriptionDouble', ApiConfirmInscriptionDouble, name="ApiConfirmInscriptionDouble"),

    path('ApiRequestRefundPaiement', ApiRequestRefundPaiement, name="ApiRequestRefundPaiement"),
    path('ApiLoadRefundData', ApiLoadRefundData, name="ApiLoadRefundData"),
    path('ApiLoadRefundDetails', ApiLoadRefundDetails, name="ApiLoadRefundDetails"),

    path('ApiAccepteRembourssement', ApiAccepteRembourssement, name="ApiAccepteRembourssement"),
    path('ApiRejectRembourssement', ApiRejectRembourssement, name="ApiRejectRembourssement"),

    path('suivie-des-echeanciers/', submenu_access_required("tre", "tresorerie")(SuivieEcheancier), name="SuivieEcheancier"),
    path('ApiLoadConvertedProspects', ApiLoadConvertedProspects, name="ApiLoadConvertedProspects"),
    path('api/mark_engagement_printed/<int:prospect_id>/', ApiMarkEngagementPrinted, name="mark_engagement_printed"),
    path('api/mark_quittance_printed/', ApiMarkQuittancePrinted, name="mark_quittance_printed"),

    path('details-suivie-echeancier/<int:pk>/', DetailsEcheancierClient, name="DetailsEcheancierClient"),
    path('details-suivie-echeancier/double-diplomation/<int:pk>/', DetailsEcheancierClientDouble, name="DetailsEcheancierClientDouble"),

    path('liste-des-paiements/', submenu_access_required("tre", "tresorerie")(ListeDesPaiements), name="ListeDesPaiements"),
    path('ApiListePaiements', ApiListePaiements, name="ApiListePaiements"),
    path('api/print-ticket-caisse/<int:paiement_id>/', PrintTicketCaisse, name='PrintTicketCaisse'),

    path('ApiGetLunchedSpec', ApiGetLunchedSpec, name="ApiGetLunchedSpec"),

    path('ApiGetClientEcheancier', ApiGetClientEcheancier, name="ApiGetClientEcheancier"),
    path('ApiGetClientEcheancierDouble',ApiGetClientEcheancierDouble, name="ApiGetClientEcheancierDouble"),

    path('ApiSaveRefundOperation', ApiSaveRefundOperation, name="ApiSaveRefundOperation"),
    path('ApiStats', ApiStats, name="ApiStats"),
    path('ApiShowRefundTraiteResult', ApiShowRefundTraiteResult, name="ApiShowRefundTraiteResult"),

    path('liste-des-rembourssements/', submenu_access_required("tre", "remboursement")(listeDesRembourssement), name="listeDesRembourssement"),
    path('rembourssement/details/<int:pk>/',submenu_access_required("tre", "remboursement")(DetailsRembourssement), name="DetailsRembourssement"),
    path('rembourssement/cancel/<int:pk>/', ApiCancelRefund, name="ApiCancelRefund"),
    path('ApiLoadRemboursements/', ApiLoadRemboursements, name="ApiLoadRemboursements"),
    path('api/search-prospect-refund/', ApiSearchProspectForRefund, name="ApiSearchProspectForRefund"),

    path('ApiCheckEcheancierState', ApiCheckEcheancierState, name="ApiCheckEcheancierState"),
    path('ApiCheckStateModel', ApiCheckStateModel, name="ApiCheckStateModel"),

    ## details attente paiement
    path('ApiGetEntrepriseDetails', ApiGetEntrepriseDetails, name="ApiGetEntrepriseDetails"),

    ## details suivie echeancier
    path('ApiGetEntrepriseInfos', ApiGetEntrepriseInfos, name="ApiGetEntrepriseInfos"),

    path('ApiCheckForPayments', ApiCheckForPayments, name="ApiCheckForPayments"),

    path('ApiGetProspectsList', ApiGetProspectsList, name="ApiGetProspectsList"),
    path('ApiToggleFinancialAlert', ApiToggleFinancialAlert, name="ApiToggleFinancialAlert"),
    path('ApiSendEmailRelance', ApiSendEmailRelance, name="ApiSendEmailRelance"),


    ##### Gestion des depenses
    path('depenses/liste/',submenu_access_required("tre", "depenses")(PageDepenses), name="PageDepenses"),
    path('ApiListeDepenses', ApiListeDepenses, name="ApiListeDepenses"),
    path('depenses/creation/', submenu_access_required("tre", "depenses")(PageNouvelleDepense), name="PageNouvelleDepense"),
    path('depenses/details/<int:id>/', submenu_access_required("tre", "depenses")(PageDetailDepense), name="PageDetailDepense"),

    #### Gestion des fournisseurs
    path('fournisseurs/liste/',submenu_access_required("tre", "fournisseurs")(PageFournisseur), name="PageFournisseur"),
    path('ApiListeFournisseurs',ApiListeFournisseurs, name="ApiListeFournisseurs"),
    path('fournisseur/nouveau-fournisseur/',submenu_access_required("tre", "fournisseurs")(PageNouveauFournisseur), name="PageNouveauFournisseur"),
    path('fournisseur/details/<int:pk>/', submenu_access_required("tre", "fournisseurs")(PageDetailsFournisseur), name="PageDetailsFournisseur"),
    path('enregistrer_fournisseur', enregistrer_fournisseur, name="enregistrer_fournisseur"),
    path('UpdateFournisseur', UpdateFournisseur, name="UpdateFournisseur"),
    path('ApiLoadFournisseur', ApiLoadFournisseur, name="ApiLoadFournisseur"),
    path('ApiCreerReglementFournisseur', ApiCreerReglementFournisseur, name="ApiCreerReglementFournisseur"),
    path('ApiGetReglementsFournisseur', ApiGetReglementsFournisseur, name="ApiGetReglementsFournisseur"),
    path('ApiUpdateChequeStatus', ApiUpdateChequeStatus, name="ApiUpdateChequeStatus"),

    #### Gestion des dÃ©penses
    path('parametres/type-depense/', submenu_access_required("tre", "parametres")(liste_types_depenses), name="liste_types_depenses"),
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
    path('ApiRecordExpensePayment', ApiRecordExpensePayment, name="ApiRecordExpensePayment"),
    
    # Depenses Categories
    path('ApiLoadDepensesCategories', ApiLoadDepensesCategories, name="ApiLoadDepensesCategories"),
    path('ApiStoreDepenseCategory', ApiStoreDepenseCategory, name="ApiStoreDepenseCategory"),
    path('ApiUpdateDepenseCategory', ApiUpdateDepenseCategory, name="ApiUpdateDepenseCategory"),
    path('ApiDeleteDepenseCategory', ApiDeleteDepenseCategory, name="ApiDeleteDepenseCategory"),
    path('ApiLoadEntites/', ApiLoadEntites, name='ApiLoadEntites'),

    path('ApiLoadPaiements',ApiLoadPaiements , name="ApiLoadPaiements"),

    path('caisse/brouillard/espece/', submenu_access_required("tre", "caisse")(PageBrouillardCaisse), name="PageBrouillardCaisse"),
    path('caisse/brouilland/banque/',submenu_access_required("tre", "banque")(PageBrouillardBanque), name="PageBrouillardBanque"),

    path('brouillard_caisse_json', brouillard_caisse_json, name="brouillard_caisse_json"),
    path('brouillard_banck_json', brouillard_banck_json, name="brouillard_banck_json"),
    path('api_set_solde_initial', api_set_solde_initial, name="api_set_solde_initial"),
    path('api_list_soldes_initiaux', api_list_soldes_initiaux, name="api_list_soldes_initiaux"),
    path('brouillard_banque', brouillard_banque, name="brouillard_banque"),

    path('caisse/depot-banque/', submenu_access_required("tre", "caisse")(PageDepotBanque), name="PageDepotBanque"),
    path('api/list-depots-banque/', api_list_depots_banque, name="api_list_depots_banque"),
    path('api/get-depot-banque/<int:pk>/', api_get_depot_banque, name="api_get_depot_banque"),
    path('api/create-depot-banque/', api_create_depot_banque, name="api_create_depot_banque"),
    path('api/update-depot-banque/<int:pk>/', api_update_depot_banque, name="api_update_depot_banque"),
    path('api/delete-depot-banque/<int:pk>/', api_delete_depot_banque, name="api_delete_depot_banque"),
    path('imprimer-remise-fonds/<int:pk>/', imprimer_remise_fonds, name="imprimer_remise_fonds"),
    path('banque/situation-des-comptes/', submenu_access_required("tre", "banque")(PageSituationComptes), name="PageSituationComptes"),

    path('imputation-bancaire/', submenu_access_required("tre", "banque")(ImputationBancaire), name="ImputationBancaire"),
    path('api/delete-imputation/', ApiDeleteImputationBancaire, name="ApiDeleteImputationBancaire"),
    path('ApiReturnUndonePaiament', ApiReturnUndonePaiament, name="ApiReturnUndonePaiament"),
    path('ApiImputeBankPaiment', ApiImputeBankPaiment, name="ApiImputeBankPaiment"),

    path('plan-comptable/',submenu_access_required("tre", "parametres")(PagePlanComptable), name="PagePlanComptable"),
    path('plan-comptable/create-modal/', CreateCompteModal, name="CreateCompteModal"),
    path('plan-comptable/api/', PlanComptableAPI, name="PlanComptableAPI"),
    path('plan-comptable-recettes-depenses/', submenu_access_required("tre", "parametres")(PagePlanComptableRecetteDepense), name="PagePlanComptableRecetteDepense"),


    path('ApiLoadEntrepises', ApiLoadEntrepises, name="ApiLoadEntrepises"),
    path('details/client/<int:pk>/',ClientDetails, name="ClientDetails"),
    path('ApiDetailsPaiement', ApiDetailsPaiement, name="ApiDetailsPaiement"),
    path('ApiListBankAccount', ApiListBankAccount, name="ApiListBankAccount"),


    ##### Facturation 
    path('facturation/liste/', submenu_access_required("tre", "factures")(facturation.PageFacturation), name="PageFacturation"),
    path('facturation/avoir/liste/', submenu_access_required("tre", "factures")(facturation.PageFacturesAvoir), name="PageFacturesAvoir"),
    path('ApiListeDesFactures', facturation.ApiListeDesFactures, name="ApiListeDesFactures"),
    path('ApiDemanderRemboursement', facturation.ApiDemanderRemboursement, name="ApiDemanderRemboursement"),
    path('details-facture/<str:pk>/', submenu_access_required("tre", "factures")(facturation.TresorerieViewFacture), name="TresorerieViewFacture"),
    path('ApiDeleteFacture', facturation.ApiDeleteFacture, name="ApiDeleteFacture"),
    path('ApiValidateFacture', facturation.ApiValidateFacture, name="ApiValidateFacture"),
    path('ApiGetDraftInvoiceDetails', facturation.ApiGetDraftInvoiceDetails, name="ApiGetDraftInvoiceDetails"),
    path('ApiUpdateDraftInvoice', ApiUpdateDraftInvoice, name="ApiUpdateDraftInvoice"),
    path('facturation/modifier/<int:pk>/', submenu_access_required("tre", "factures")(facturation.PageModifierFacture), name="PageModifierFacture"),
    path('ApiUpdateFactureLignes', facturation.ApiUpdateFactureLignes, name="ApiUpdateFactureLignes"),
    path('ApiUpdateFactureClientOverride', facturation.ApiUpdateFactureClientOverride, name="ApiUpdateFactureClientOverride"),
    path('print-facture/<str:pk>/', facturation.PrintFactureTresorerie, name="PrintFactureTresorerie"),
    path('ApiUpdateReferencePaiement', ApiUpdateReferencePaiement, name="ApiUpdateReferencePaiement"),


    path('categorie-produits/liste/', submenu_access_required("tre", "parametres")(PageProduits), name="PageProduits"),

    ##### Gestion des categories de produits (PaymentCategory)
    path('categories-produits/liste/', submenu_access_required("tre", "parametres")(PageCategoriesProduits), name="PageCategoriesProduits"),
    path('ApiListeCategoriesProduits', ApiListeCategoriesProduits, name="ApiListeCategoriesProduits"),
    path('ApiCreerCategorieProduit', ApiCreerCategorieProduit, name="ApiCreerCategorieProduit"),
    path('ApiModifierCategorieProduit', ApiModifierCategorieProduit, name="ApiModifierCategorieProduit"),
    path('ApiSupprimerCategorieProduit', ApiSupprimerCategorieProduit, name="ApiSupprimerCategorieProduit"),
    path('ApiGenerateInvoiceFromPayment', generate_invoice_from_payment, name="ApiGenerateInvoiceFromPayment"),
    path('ApiGenerateConsolidatedInvoice', generate_consolidated_invoice, name="ApiGenerateConsolidatedInvoice"),
    path('ApiGetCategorieProduit/<int:pk>/', ApiGetCategorieProduit, name="ApiGetCategorieProduit"),


    path('imputation-comptable/specialite/liste/', submenu_access_required("tre", "parametres")(PageImputationComptable), name="PageImputationComptable"),

    path('LoadSpecialiteComptes',LoadSpecialiteComptes, name="LoadSpecialiteComptes"),
    path('LoadSpecialites',LoadSpecialites, name="LoadSpecialites"),
    path('LoadComptes',LoadComptes, name="LoadComptes"),
    path('UpdateSpecialiteCompte',UpdateSpecialiteCompte , name="UpdateSpecialiteCompte"),
    path('CreateSpecialiteCompte',CreateSpecialiteCompte, name="CreateSpecialiteCompte"),
    path('DeleteSpecialiteCompte',DeleteSpecialiteCompte,name="DeleteSpecialiteCompte"),


    path('paiements/autres/liste/', submenu_access_required("tre", "autres_paiements")(PageAutrePaiements), name="pageautrespaiement"),
    path('paiements/autres/nouveau/', submenu_access_required("tre", "autres_paiements")(PageNouveauAutrePaiement), name="PageNouveauAutrePaiement"),
    path('ApiListeAutresPaiements', ApiListeAutresPaiements, name="ApiListeAutresPaiements"),
    path('ApiStoreAutrePaiement', ApiStoreAutrePaiement, name="ApiStoreAutrePaiement"),
    path('ApiGetAutrePaiement/<int:pk>/', ApiGetAutrePaiement, name="ApiGetAutrePaiement"),
    path('ApiUpdateAutrePaiement', ApiUpdateAutrePaiement, name="ApiUpdateAutrePaiement"),
    path('ApiDeleteAutrePaiement', ApiDeleteAutrePaiement, name="ApiDeleteAutrePaiement"),
    path('api_liste_clients', api_liste_clients, name="api_liste_clients"),
    path('CreateClientFromTresorerie', CreateClientFromTresorerie, name="CreateClientFromTresorerie"),



    path('penalite/liste/',submenu_access_required("tre", "parametres")(PageConfPenalite),name="PageConfPenalite"),
    path('api/update-promo-config/', ApiUpdatePromoConfig, name='ApiUpdatePromoConfig'),
    path('api/load-penalty-config/', ApiLoadPenaltyConfig, name='ApiLoadPenaltyConfig'),
    path('api/update-penalty-config/', ApiUpdatePenaltyConfig, name='ApiUpdatePenaltyConfig'),

    path('penalite/demandes-paiements/',submenu_access_required("tre", "tresorerie")(ListePenalite),name="ListePenalite"),
    path('api/liste-due-paiements/', ApiListeDuePenalite, name='ApiListeDuePenalite'),
    path('api/delete-due-paiement/', ApiDeleteDuePenalite, name='ApiDeleteDuePenalite'),
    path('api/pay-due-paiement/', ApiPayDuePenalite, name='ApiPayDuePenalite'),
    path('penalite/print-receipt/<int:paiement_id>/', PrintReceipt, name='PrintReceipt'),

    path('ApiGetEntite',ApiGetEntite, name="ApiGetEntite"),


    path('reporting-das/', ReportingDAS, name='ReportingDAS'),
    
    path('recouvrement/', submenu_access_required("tre", "banque")(PageRecouvrement), name='PageRecouvrement'),
    path('api/update-effective-date/', ApiUpdateEffectiveDate, name='ApiUpdateEffectiveDate'),
    path('api/delete-recouvrement/', ApiDeleteRecouvrementPaiement, name='ApiDeleteRecouvrementPaiement'),
    path('api/list-recouvrement-paiements/', ApiListRecouvrementPaiements, name='ApiListRecouvrementPaiements'),
    path('api/list-historique-recouvrement/', ApiListHistoriqueRecouvrement, name='ApiListHistoriqueRecouvrement'),
    path('api/recouvrement-stats/', ApiRecouvrementStats, name='ApiRecouvrementStats'),
    path('payment-types/', submenu_access_required("tre", "parametres")(payment_type_list), name='payment_type_list'),

    path('api/liste-formations-prices/', ApiListeFormationsPrices, name="ApiListeFormationsPrices"),
    path('api/update-formation-price/', ApiUpdateFormationPrice, name="ApiUpdateFormationPrice"),
    path('api/liste-specialites-prices/', ApiListeSpecialitesPrices, name="ApiListeSpecialitesPrices"),
    path('api/update-specialite-price/', ApiUpdateSpecialitePrice, name="ApiUpdateSpecialitePrice"),
    path('api/bulk-update-specialite-price/', ApiBulkUpdateSpecialitePrice, name="ApiBulkUpdateSpecialitePrice"),
    path('api/liste-double-diplomation-prices/', ApiListeDoubleDiplomationPrices, name="ApiListeDoubleDiplomationPrices"),
    path('api/update-double-diplomation-price/', ApiUpdateDoubleDiplomationPrice, name="ApiUpdateDoubleDiplomationPrice"),
    path('api/list-payment-types/', ApiListePaymentTypes, name='ApiListePaymentTypes'),
    path('api/update-payment-type/', ApiUpdatePaymentType, name='ApiUpdatePaymentType'),

    # Paramètres Financiers Généraux
    path('api/get-parametre-financier/', ApiGetParametreFinancier, name='ApiGetParametreFinancier'),
    path('api/update-parametre-financier/', ApiUpdateParametreFinancier, name='ApiUpdateParametreFinancier'),
    path('api/update-quittance-format/', ApiUpdateQuittanceFormat, name='ApiUpdateQuittanceFormat'),

    path('api/get-prospect-payments-by-nin/', facturation.ApiGetProspectPaymentsByNin, name='ApiGetProspectPaymentsByNin'),

    path('suivi-des-paiements/', submenu_access_required("tre", "tresorerie")(PageSuiviPaiements), name="PageSuiviPaiements"),
    path('ApiSuiviPaiements', ApiSuiviPaiements, name="ApiSuiviPaiements"),

    # Vues de consultation pour Executive Education
    path('factures-executive/', submenu_access_required("tre", "exec_edu")(ListeDesFactures), name="tresorerie_factures_conseil"),
    path('devis-executive/', submenu_access_required("tre", "exec_edu")(ListeDesDevis), name="tresorerie_devis_conseil"),
    path('clients-executive/', submenu_access_required("tre", "exec_edu")(ListeDesClients), name="tresorerie_clients_conseil"),

    # Gestion de la paie
    path('paies/liste/', submenu_access_required("tre", "tresorerie")(liste_paie_finance), name="liste_paie_finance"),
    path('paies/lancer-depense/', submenu_access_required("tre", "tresorerie")(lancer_depense_paie), name="lancer_depense_paie"),

    # Gestion des reductions
    path('gestion-des-reductions/', submenu_access_required("tre", "tresorerie")(ListeRemiseApplique), name="ListeRemiseApplique"),
    path('AipLoadRemise', AipLoadRemise, name="AipLoadRemise"),
    path('ApiLoadProspectParticulier', ApiLoadProspectParticulier, name="ApiLoadProspectParticulier"),
    path('ApiStoreApplicedReduction', ApiStoreApplicedReduction, name="ApiStoreApplicedReduction"), 
    path('ApiStoreSingleReduction', ApiStoreSingleReduction, name="ApiStoreSingleReduction"), 
    path('ApiloadRemiseAppliquer', ApiloadRemiseAppliquer, name="ApiloadRemiseAppliquer"),
    path('ApiLoadRemiseAppliquerDetails', ApiLoadRemiseAppliquerDetails, name="ApiLoadRemiseAppliquerDetails"),
    path('ApiGetReductionDetails', ApiGetReductionDetails, name="ApiGetReductionDetails"),
    path('ApiActivateRemiseAppliquer', ApiActivateRemiseAppliquer, name="ApiActivateRemiseAppliquer"),
    path('ApiDeleteRemiseAppliquer', ApiDeleteRemiseAppliquer, name="ApiDeleteRemiseAppliquer"),
]
