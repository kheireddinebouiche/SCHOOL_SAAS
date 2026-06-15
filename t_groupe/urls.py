from django.contrib import admin
from django.urls import path
from .views import *
from .f_views.affectations import *
from .f_views.student import *
from .f_views.groupe_print import GenerateBulkStudentPdf

from institut_app.decorators import submenu_access_required
app_name="t_groupe"

urlpatterns = [

    path('nouveau-groupe/', submenu_access_required("scol", "groupes")(NewGroupe), name="nouveaugroupe"),
    path('liste-des-groupes/', submenu_access_required("scol", "groupes")(ListeGroupe), name="listegroupes"),
    path('details-groupe/<int:pk>/', submenu_access_required("scol", "groupes")(detailsGroupe), name="detailsgroupe"),
    path('mise-à-jour/<int:pk>/', submenu_access_required("scol", "groupes")(UpdateGroupe), name="UpdateGroupe"),
    path('supprimer-groupe/<int:pk>/', submenu_access_required("scol", "groupes")(deleteGroupe), name="deletegroupe"),
    path('brouilon/<int:pk>/', submenu_access_required("scol", "groupes")(makeGroupeBrouillon), name="makeGroupeBrouillon"),
    path('valider-groupe/<int:pk>/',submenu_access_required("scol", "groupes")(validateGroupe), name="validateGroupe"),
    path('closeGroupe/<int:pk>/',submenu_access_required("scol", "groupes")(closeGroupe), name="closeGroupe"),

    path('api-close-inscription/<int:pk>/', submenu_access_required("scol", "groupes")(ApiCloseGroupInscription), name="ApiCloseGroupInscription"),
    path('api-open-inscription/<int:pk>/', submenu_access_required("scol", "groupes")(ApiOpenGroupInscription), name="ApiOpenGroupInscription"),
    path('toggle-admissible-stage/<int:pk>/', submenu_access_required("scol", "groupes")(toggleAdmissibleStage), name="toggleAdmissibleStage"),

    path('ApiGetGroupeList', submenu_access_required("scol", ("groupes", "affectations", "transferts", "etudiants"))(ApiGetGroupeList), name="ApiGetGroupeList"),

    path('affectation-en-attente/',submenu_access_required("scol", "affectations")(AffectationPage), name="AffectationPage"),
    path('ApiLoadAttenteAffectation',submenu_access_required("scol", "affectations")(ApiLoadAttenteAffectation), name="ApiLoadAttenteAffectation"),
    path('ApiListePromosEnAttente', submenu_access_required("scol", ("groupes", "affectations"))(ApiListePromosEnAttente), name="ApiListePromosEnAttente"),
    path('autre-affectation/', submenu_access_required("scol", "affectations")(AutreAffectationPage), name="AutreAffectationPage"),
    path('api/participants-confirmes/', submenu_access_required("scol", "affectations")(ApiParticipantsConfirmes), name="ApiParticipantsConfirmes"),
    path('api/affecter-participant-groupe/', submenu_access_required("scol", "affectations")(ApiAffectParticipantToAcademicGroupe), name="ApiAffectParticipantToAcademicGroupe"),
    path('ApiSpecialiteByPromo', submenu_access_required("scol", "affectations")(ApiSpecialiteByPromo), name="ApiSpecialiteByPromo"),
    path('affectation-au-groupe/<int:pk>/<str:code>/', submenu_access_required("scol", "affectations")(AffectationAuGroupe), name="AffectationAuGroupe"),
    path('ApiListeStudentNotAffected', submenu_access_required("scol", "affectations")(ApiListeStudentNotAffected), name="ApiListeStudentNotAffected"),
    path('ApiGroupeListeForAffectation', submenu_access_required("scol", "affectations")(ApiGroupeListeForAffectation), name="ApiGroupeListeForAffectation"),
    path('ApiGetSpecialiteDatas', submenu_access_required("scol", "affectations")(ApiGetSpecialiteDatas), name="ApiGetSpecialiteDatas"),
    path('ApiGetBrouillonGroupes', submenu_access_required("scol", "affectations")(ApiGetBrouillonGroupes), name="ApiGetBrouillonGroupes"),
    path('ApiAffectStudentToGroupe', submenu_access_required("scol", "affectations")(ApiAffectStudentToGroupe), name="ApiAffectStudentToGroupe"),

    path('profile-etudiant/<int:pk>/', submenu_access_required("scol", "etudiants")(StudentDetails), name="StudentDetails"),
    path('ApiUpdateGroupeCode', submenu_access_required("scol", "groupes")(ApiUpdateGroupeCode) ,name="ApiUpdateGroupeCode"),

    path('ApiCancelStudentAffectation', submenu_access_required("scol", "affectations")(ApiCancelStudentAffectation), name="ApiCancelStudentAffectation"),
    path('ApiUpdate_etudiant',submenu_access_required("scol", "etudiants")(ApiUpdate_etudiant),name="ApiUpdate_etudiant"),
    path('ApiUpdateStudentPassword', submenu_access_required("scol", "etudiants")(ApiUpdateStudentPassword), name="ApiUpdateStudentPassword"),
    path('ApiUpdateStudentPhoto', submenu_access_required("scol", "etudiants")(ApiUpdateStudentPhoto), name="ApiUpdateStudentPhoto"),
    path('ApiSelectSpecialite' , submenu_access_required("scol", ("groupes", "affectations", "transferts"))(ApiSelectSpecialite), name="ApiSelectSpecialite"),
    path('ApiGetFormation', submenu_access_required("scol", ("groupes", "affectations", "contrats", "transferts"))(ApiGetFormation), name="ApiGetFormation"),
    path('ApiListePromo', submenu_access_required("scol", ("groupes", "affectations", "transferts"))(ApiListePromo), name="ApiListePromo"),
    path('ApiCreateGroupe', submenu_access_required("scol", "groupes")(ApiCreateGroupe), name="ApiCreateGroupe"),
    path('ApiDeleteGroupe', submenu_access_required("scol", "groupes")(ApiDeleteGroupe), name="ApiDeleteGroupe"),
    path('api-generate-payment/', submenu_access_required("scol", "groupes")(ApiGenerateGroupPayment), name="ApiGenerateGroupPayment"),

    
    path('students/<int:pk>/print/<slug:template_slug>/', submenu_access_required("scol", "etudiants")(generate_student_pdf.as_view()), name='generate_student_pdf'),
    path('bulk-print/', submenu_access_required("scol", "groupes")(GenerateBulkStudentPdf.as_view()), name='generate_group_students_pdf'),

]
