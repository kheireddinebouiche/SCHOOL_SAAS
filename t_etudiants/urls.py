from django.contrib import admin
from django.urls import path
from .views import *
from .f_views.presences import *
from .f_views.contrat import *

app_name="t_etudiants"

urlpatterns = [

   path('liste-des-etudiants/', ListeStudents, name="ListeStudents"),
   path('ApiListeDesEtudiants', ApiListeDesEtudiants, name="ApiListeDesEtudiants"),
   path('ApiSaveStudentDatas', ApiSaveStudentDatas, name="ApiSaveStudentDatas"),
   path('ApiSaveStudentNote', ApiSaveStudentNote, name="ApiSaveStudentNote"),
   path('ApiUpdateStudentNote', ApiUpdateStudentNote, name="ApiUpdateStudentNote"),
   path('ApiAccomplirNote', ApiAccomplirNote, name="ApiAccomplirNote"),
   path('ApiSaveStudentRappel', ApiSaveStudentRappel, name="ApiSaveStudentRappel"),
   path('ApiUpdateReminder', ApiUpdateReminder, name="ApiUpdateReminder"),


   path('registres-cours/', RegistrePage, name="RegistrePage"),
   path('ApiSaveRegistreGroupe', ApiSaveRegistreGroupe, name="ApiSaveRegistreGroupe"),
   path('details-registre/<int:pk>/', DetailsRegistrePresence, name="DetailsRegistrePresence"),
   path('liste_registres', liste_registres, name="liste_registres"),

   path('details-liste-presence/<int:pk>/', DetailsListePresence, name="DetailsListePresence"),
   path('ApiLoadDatas', ApiLoadDatas, name="ApiLoadDatas"),
   path('ApiAjouterHistoriqueAbsence', ApiAjouterHistoriqueAbsence, name="ApiAjouterHistoriqueAbsence"),
   path('ApiGetHistoriqueEtudiant/<int:pk>/<int:id_ligne>/', ApiGetHistoriqueEtudiant, name="ApiGetHistoriqueEtudiant"),
   
   path('presences-des-etudiants/',ListeDesEtudiants, name="ListeDesEtudiants"),

   path('contrat/modele/',PageModeleContrat, name="PageModeleContrat"),
   path('contrat/modele/load/', ApiLoadModelesContrat, name="ApiLoadModelesContrat"),
   path('contrat/modele/delete/', ApiDeleteModeleContrat, name="ApiDeleteModeleContrat"),
   path('contrat/modele/update/', ApiUpdateModeleContrat, name="ApiUpdateModeleContrat"),
   path('ApiCreateModeleContrat',ApiCreateModeleContrat, name="ApiCreateModeleContrat"),
   path('contrat/modele/articles/load/', ApiLoadArticlesContrat, name="ApiLoadArticlesContrat"),
   path('contrat/modele/articles/create/', ApiCreateArticleContrat, name="ApiCreateArticleContrat"),
   path('contrat/modele/articles/update/', ApiUpdateArticleContrat, name="ApiUpdateArticleContrat"),
   path('contrat/modele/articles/delete/', ApiDeleteArticleContrat, name="ApiDeleteArticleContrat"),

   path('ApiGetModeleContratByFormation', ApiGetModeleContratByFormation, name="ApiGetModeleContratByFormation"),

   path('ApiGetStudentFinancialsData', ApiGetStudentFinancialsData, name="ApiGetStudentFinancialsData"),
]