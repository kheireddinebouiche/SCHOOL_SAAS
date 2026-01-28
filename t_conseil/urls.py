from django.urls import path
from .views import *
from .f_views.prospects import *

app_name="t_conseil"

urlpatterns = [

  path('liste-des-thematiques/',ListeThematique, name="ListeThematique"),

  path('nouveau-devis/', AddNewDevis, name="AddNewDevis"),
  path('configuration-devis/<str:pk>/', configure_devis , name="configure-devis"),
  path('details-devis/<str:pk>/', DetailsDevis, name="DetailsDevis"),
  path('liste-des-devis/', ListeDesDevis, name="ListeDesDevis"),

  path('ApiSaveThematique' , ApiSaveThematique, name="ApiSaveThematique"),

  path('ApiLoadThematique' , ApiLoadThematique, name="ApiLoadThematique"),

  path('ApiLoadThematiqueDetails', ApiLoadThematiqueDetails, name="ApiLoadThematiqueDetails"),

  path('archive-thematique/', ArchiveThematique, name="ArchiveThematique"),

  path('ApiLoadArchivedThematique', ApiLoadArchivedThematique, name="ApiLoadArchivedThematique"),
  path('ApiArchiveThematique', ApiArchiveThematique, name="ApiArchiveThematique"),
  path('ApiActivateThematique', ApiActivateThematique, name="ApiActivateThematique"),
  path('ApiUpdateThematique', ApiUpdateThematique, name="ApiUpdateThematique"),
  path('ApiDeleteFinalThematique', ApiDeleteFinalThematique, name="ApiDeleteFinalThematique"),



  path('prospects-en-instance/',ListeProspectConseil, name="prospectInstance"),
  path('ApiLoadProspect',ApiLoadProspect, name="ApiLoadProspect"),
  path('ApiTransformeToClient',ApiTransformeToClient, name="ApiTransformeToClient"),

  path('ApiListeProspect',ApiListeProspect, name="ApiListeProspect"),
  
  path('ApiCreateProspect', ApiCreateProspect, name="ApiCreateProspect"),
  path('ApiQuickCreateProspect', ApiQuickCreateProspect, name="ApiQuickCreateProspect"),
  path('ApiSaveLigneDevis', ApiSaveLigneDevis, name="ApiSaveLigneDevis"),
  path('ApiSaveDevisItems', ApiSaveDevisItems, name="ApiSaveDevisItems"),
   path('ApiStartTransformationDevisToFacture', ApiStartTransformationDevisToFacture, name="ApiStartTransformationDevisToFacture"),
  path('ApiFetchEnterpriseTvas', ApiFetchEnterpriseTvas, name="ApiFetchEnterpriseTvas"),

  
  path('liste-des-factures/', ListeDesFactures, name="ListeDesFactures"),
  path('nouvelle-facture/', AddNewFacture, name="AddNewFacture"),
  path('configuration-facture/<str:pk>/', configure_facture, name="configure-facture"),
  path('details-facture/<str:pk>/', DetailsFacture, name="DetailsFacture"),
  path('configuration/', ConfigurationConseil, name="ConfigurationConseil"),
  
  path('dashboard/', ConseilDashboard, name="ConseilDashboard"),
  path('pipeline/', PipelineConseil, name="PipelineConseil"),
  path('api/pipeline/update-stage/', ApiUpdatePipelineStage, name="ApiUpdatePipelineStage"),
  path('api/pipeline/toggle-favorite/', ApiToggleFavorite, name="ApiToggleFavorite"),
  path('api/pipeline/convert-to-devis/', ApiConvertProspectToDevis, name="ApiConvertProspectToDevis"),
  path('api/pipeline/create-opportunite/', ApiCreateOpportunite, name="ApiCreateOpportunite"),
  path('api/pipeline/get-opportunite/', ApiGetOpportunite, name="ApiGetOpportunite"),
  path('api/pipeline/update-opportunite/', ApiUpdateOpportunite, name="ApiUpdateOpportunite"),
  path('api/pipeline/delete/', ApiDeleteOpportunite, name="ApiDeleteOpportunite"),
  path('api/facture/add-paiement/', ApiAddPaiement, name="ApiAddPaiement"),
  path('api/devis/delete/', ApiDeleteDevis, name="ApiDeleteDevis"),
  path('api/devis/validate/', ApiValidateDevis, name="ApiValidateDevis"),
  path('api/devis/revert-to-draft/', ApiRevertDevisToDraft, name="ApiRevertDevisToDraft"),
  
  path('api/facture/save-items/', ApiSaveFactureItems, name="ApiSaveFactureItems"),
  path('api/facture/validate/', ApiValidateFacture, name="ApiValidateFacture"),
  path('api/facture/revert-to-draft/', ApiRevertFactureToDraft, name="ApiRevertFactureToDraft"),
  path('api/facture/delete/', ApiDeleteFacture, name="ApiDeleteFacture"),
  
  path('das/', ListeDAS, name="ListeDAS"),
  path('api/das/save/', ApiSaveDAS, name="ApiSaveDAS"),
  path('api/das/delete/', ApiDeleteDAS, name="ApiDeleteDAS"),

  path('export/pipeline/', ExportPipelineCsv, name="ExportPipelineCsv"),
]