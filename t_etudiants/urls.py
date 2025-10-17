from django.contrib import admin
from django.urls import path
from .views import *
from .f_views.presences import *

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
   path('ApiAjouterHistoriqueAbsence', ApiAjouterHistoriqueAbsence, name="ApiAjouterHistoriqueAbsence"),
   path('ApiGetHistoriqueEtudiant/<int:pk>/', ApiGetHistoriqueEtudiant, name="ApiGetHistoriqueEtudiant"),
]