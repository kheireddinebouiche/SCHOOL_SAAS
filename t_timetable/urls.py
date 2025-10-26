from django.contrib import admin
from django.urls import path,include
from .views import *
from.f_views.salles import *
from .f_views.crenaux import *
from .f_views.affectation_modules import *

app_name="t_timetable"

urlpatterns = [
    
    path('liste', ListeDesEmploie, name="ListeDesEmploie"),
    path('creation/', CreateTimeTable, name="CreateTimeTable"),
    path('details/emploie/<int:pk>/',timetable_view, name="timetable_view"),
    path('modifications/emploie/<int:pk>/', timetable_edit, name="timetable_edit"),
    path('configuration/emploie/<int:pk>/', timetable_configure, name="timetable_configure"),
    path('ApiMakeTimetableDone', ApiMakeTimetableDone, name="ApiMakeTimetableDone"),
    path('save_session', save_session, name="save_session"),
    path('ApiCreateTimeTable', ApiCreateTimeTable, name="ApiCreateTimeTable"),
    path('ApiLoadTableEntry', ApiLoadTableEntry, name="ApiLoadTableEntry"),
    path('ApiMakeTimetableDraft', ApiMakeTimetableDraft, name="ApiMakeTimetableDraft"),
    path('ApiValidateTimetable', ApiValidateTimetable, name="ApiValidateTimetable"),
    path('ApiPausetimeTable', ApiPausetimeTable, name="ApiPausetimeTable"),
   

    ### SALLES DE COURS ###
    path('classroom/liste/',ListeDesSalles, name="ListeDesSalles"),
    path('classroom/creer/', CreerSalle, name="CreerSalle"),
    path('classroom/modifier/<int:salle_id>/', EditerSalle, name="EditerSalle"),
    path('classroom/supprimer/<int:salle_id>/', SupprimerSalle, name="SupprimerSalle"),
    path('classroom/data/<int:salle_id>/', get_salle_data, name="get_salle_data"),


    ### GESTION DES CRENAUX ###
    path('crenaux/liste/',ListeModel, name="ListeModelCrenau"),
    path('create_model/',create_model, name="create_model"),
    path('details/creneau/<int:pk>/', model_creneau_detail, name="model_creneau_detail"),
    path('edit/creneau/<int:pk>/', model_creneau_edit, name="model_creneau_edit"),
    path('save_model_crenau/', save_model_crenau, name="save_model_crenau"),
    path('activate_model_crenau/', activate_model_crenau, name="activate_model_crenau"),

    ### FILTRAGE ###
    path('FilterFormateur', FilterFormateur, name="FilterFormateur"),
    path('modules/affectations/', PageAffectation, name="PageAffectation"),
    path('LoadAssignedProf', LoadAssignedProf, name="LoadAssignedProf"),
    path('ApiLoadModules', ApiLoadModules, name="ApiLoadModules"),
    path('ApiAffectTrainer', ApiAffectTrainer, name="ApiAffectTrainer"),
    path('ApiGetAffectations', ApiGetAffectations, name="ApiGetAffectations"),
    path('ApiDeaffectTrainer',ApiDeaffectTrainer, name="ApiDeaffectTrainer"),

]