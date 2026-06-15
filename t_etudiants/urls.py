from django.contrib import admin
from django.urls import path
from .views import *
from .f_views.presences import *
from .f_views.contrat import *

from institut_app.decorators import submenu_access_required
app_name="t_etudiants"

urlpatterns = [

   path('liste-des-etudiants/', submenu_access_required("scol", "etudiants")(ListeStudents), name="ListeStudents"),
   path('ApiListeDesEtudiants', submenu_access_required("scol", "etudiants")(ApiListeDesEtudiants), name="ApiListeDesEtudiants"),
   path('ApiSaveStudentDatas', submenu_access_required("scol", "etudiants")(ApiSaveStudentDatas), name="ApiSaveStudentDatas"),
   path('ApiSaveStudentNote', submenu_access_required("scol", "etudiants")(ApiSaveStudentNote), name="ApiSaveStudentNote"),
   path('ApiUpdateStudentNote', submenu_access_required("scol", "etudiants")(ApiUpdateStudentNote), name="ApiUpdateStudentNote"),
   path('ApiAccomplirNote', submenu_access_required("scol", "etudiants")(ApiAccomplirNote), name="ApiAccomplirNote"),
   path('ApiSaveStudentRappel', submenu_access_required("scol", "etudiants")(ApiSaveStudentRappel), name="ApiSaveStudentRappel"),
   path('ApiUpdateReminder', submenu_access_required("scol", "etudiants")(ApiUpdateReminder), name="ApiUpdateReminder"),


   path('registres-cours/', submenu_access_required("scol", "presences")(RegistrePage), name="RegistrePage"),
   path('ApiSaveRegistreGroupe', submenu_access_required("scol", "presences")(ApiSaveRegistreGroupe), name="ApiSaveRegistreGroupe"),
   path('details-registre/<int:pk>/', submenu_access_required("scol", "presences")(DetailsRegistrePresence), name="DetailsRegistrePresence"),
   path('liste_registres', submenu_access_required("scol", "presences")(liste_registres), name="liste_registres"),

   path('details-liste-presence/<int:pk>/', submenu_access_required("scol", "presences")(DetailsListePresence), name="DetailsListePresence"),
   path('ApiLoadDatas', submenu_access_required("scol", "presences")(ApiLoadDatas), name="ApiLoadDatas"),
   path('ApiAjouterHistoriqueAbsence', submenu_access_required("scol", "presences")(ApiAjouterHistoriqueAbsence), name="ApiAjouterHistoriqueAbsence"),
   path('ApiGetHistoriqueEtudiant/<int:pk>/<int:id_ligne>/', submenu_access_required("scol", "presences")(ApiGetHistoriqueEtudiant), name="ApiGetHistoriqueEtudiant"),
   path('ApiUpdateAbsenceReason', submenu_access_required("scol", "presences")(ApiUpdateAbsenceReason), name="ApiUpdateAbsenceReason"),
   
   path('presences-des-etudiants/',submenu_access_required("scol", "presences")(ListeDesEtudiants), name="ListeDesEtudiants"),
   path('etat-presences/', submenu_access_required("scol", "presences")(EtatPresences), name='EtatPresences'),
   path('etat-presences/excel/', submenu_access_required("scol", "presences")(ExportPresencesExcel), name='ExportPresencesExcel'),
   path('etat-presences/pdf/', submenu_access_required("scol", "presences")(ExportPresencesPDF), name='ExportPresencesPDF'),

   path('contrat/modele/',submenu_access_required("scol", "contrats")(PageModeleContrat), name="PageModeleContrat"),
   path('contrat/modele/load/', submenu_access_required("scol", "contrats")(ApiLoadModelesContrat), name="ApiLoadModelesContrat"),
   path('contrat/modele/delete/', submenu_access_required("scol", "contrats")(ApiDeleteModeleContrat), name="ApiDeleteModeleContrat"),
   path('contrat/modele/update/', submenu_access_required("scol", "contrats")(ApiUpdateModeleContrat), name="ApiUpdateModeleContrat"),
   path('ApiCreateModeleContrat',submenu_access_required("scol", "contrats")(ApiCreateModeleContrat), name="ApiCreateModeleContrat"),
   path('contrat/modele/articles/load/', submenu_access_required("scol", "contrats")(ApiLoadArticlesContrat), name="ApiLoadArticlesContrat"),
   path('contrat/modele/articles/create/', submenu_access_required("scol", "contrats")(ApiCreateArticleContrat), name="ApiCreateArticleContrat"),
   path('contrat/modele/articles/update/', submenu_access_required("scol", "contrats")(ApiUpdateArticleContrat), name="ApiUpdateArticleContrat"),
   path('contrat/modele/articles/delete/', submenu_access_required("scol", "contrats")(ApiDeleteArticleContrat), name="ApiDeleteArticleContrat"),

   path('ApiGetModeleContratByFormation', submenu_access_required("scol", "contrats")(ApiGetModeleContratByFormation), name="ApiGetModeleContratByFormation"),

   path('ApiGetStudentFinancialsData', submenu_access_required("scol", "etudiants")(ApiGetStudentFinancialsData), name="ApiGetStudentFinancialsData"),

   path('transfert/', submenu_access_required("scol", "transferts")(StudentTransfert), name="StudentTransfert"),
   path('demandes-transfert/', submenu_access_required("scol", "transferts")(StudentTransfertList), name="StudentTransfertList"),

   path('api/request-transfer/', submenu_access_required("scol", "transferts")(ApiRequestTransfer), name="ApiRequestTransfer"),
   path('api/get-specialites-promos/', submenu_access_required("scol", "transferts")(ApiGetSpecialitesPromos), name="ApiGetSpecialitesPromos"),
   path('api/update-transfer-status/', submenu_access_required("scol", "transferts")(ApiUpdateTransferStatus), name="ApiUpdateTransferStatus"),
   path('api/execute-transfer/', submenu_access_required("scol", "transferts")(ApiExecuteTransfer), name="ApiExecuteTransfer"),
   path('api/get-groups-for-transfer/', submenu_access_required("scol", "transferts")(ApiGetGroupsForTransfer), name="ApiGetGroupsForTransfer"),
   path('api/delete_transfer_request/', submenu_access_required("scol", "transferts")(ApiDeleteTransferRequest), name="ApiDeleteTransferRequest"),
]