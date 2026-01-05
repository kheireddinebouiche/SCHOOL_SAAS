from django.urls import path
from .views import *
# Utilise un chemin relatif
from .f_views.commission import *
from .f_views.modele_builtins import *
from .f_views.action_views import examen_action, rachat_action, ajourne_action
from .f_views.exam_plan import *
from .f_views.deliberation import *

app_name="t_exam"

urlpatterns = [
    path('liste-des-sessions/', ListeSession, name="ListeSession"),
   path('NewSession', NewSession, name="NewSession"),
   path('ApiListSession', ApiListSession, name="ApiListSession"),
   path('ApiDeleteSession', ApiDeleteSession, name="ApiDeleteSession"),

   path('details-session/<int:pk>/', DetailsSession, name="DetailsSession"),
   path('ApiGetSessionDetails', ApiGetSessionDetails, name="ApiGetSessionDetails"),
   path('ApiUpdateSession', ApiUpdateSession, name="ApiUpdateSession"),
   path('ApiCheckLabelDisponibility', ApiCheckLabelDisponibility, name="ApiCheckLabelDisponibility"),

   path('ApiPlaneExam', ApiPlaneExam, name="ApiPlaneExam"),
   path('plannification-examens/<int:pk>/', ExamConfiguration, name="ExamConfiguration"),
   path('ApiLoadDatasForPlanExam', ApiLoadDatasForPlanExam, name="ApiLoadDatasForPlanExam"),

   path("get-exam-plans/", get_exam_planifications, name="get_exam_plans"),
   path("save_exam_plan", save_exam_plan, name="save_exam_plan"),
   path("update_exam/",update_exam_plan, name="update_exam_plan"),
   path('ApiLoadSalle',ApiLoadSalle, name="ApiLoadSalle"),
   path('delete_exam_plan',delete_exam_plan, name="delete_exam_plan"),

   path('close_session_line',close_session_line, name="close_session_line"), 
   path('models-pv/', ModelBuilltinPage, name="ModelBuilltinPage"),
   path('ApiListModeleBuilltins', ApiListModeleBuilltins, name="ApiListModeleBuilltins"),

   path('NewModelBuilltin', NewModelBuilltin, name="NewModelBuilltin"),
   path('ApiDeleteModelBuitltin' , ApiDeleteModelBuitltin, name="ApiDeleteModelBuitltin"),

   # Nouvelles URLs pour la gestion des modèles de bulletins
   path('ApiGetModelBuilltinDetails', ApiGetModelBuilltinDetails, name="ApiGetModelBuilltinDetails"),
   path('ApiUpdateModelBuilltin', ApiUpdateModelBuilltin, name="ApiUpdateModelBuilltin"),
   path('ApiGetTypeNotes', ApiGetTypeNotes, name="ApiGetTypeNotes"),
   path('ApiAddTypeNote', ApiAddTypeNote, name="ApiAddTypeNote"),
   path('ApiUpdateTypeNote', ApiUpdateTypeNote, name="ApiUpdateTypeNote"),
   path('ApiDeleteTypeNote', ApiDeleteTypeNote, name="ApiDeleteTypeNote"),
   path('ApiAddSousNote', ApiAddSousNote, name="ApiAddSousNote"),
   path('ApiUpdateSousNote', ApiUpdateSousNote, name="ApiUpdateSousNote"),
   path('ApiDeleteSousNote', ApiDeleteSousNote, name="ApiDeleteSousNote"),
   path('ApiBulkUpdateSousNotes', ApiBulkUpdateSousNotes, name="ApiBulkUpdateSousNotes"),
   path('ApiGetSousNotesForType', ApiGetSousNotesForType, name="ApiGetSousNotesForType"),


   path('ApiDeleteGroupeSessionLine', ApiDeleteGroupeSessionLine, name="ApiDeleteGroupeSessionLine"),
   path('ApiGetSessionLineDetails',ApiGetSessionLineDetails, name="ApiGetSessionLineDetails"), 
   path('ApiUpdateGroupeSessionLine', ApiUpdateGroupeSessionLine, name="ApiUpdateGroupeSessionLine"),

   path('commission/liste/', PageCommission, name="PageCommission"),
   path('commission/nouvelle/', NouvelleCommission, name="NouvelleCommission"),
   path('commission/modification/<int:pk>/', UpdateCommission, name="UpdateCommission"),
   path('commission/details/<int:pk>/', DetailsCommission, name="DetailsCommission"),
   path('validate_commission/', validate_commission, name="validate_commission"),

   path('delete_commission/<int:pk>/', delete_commission, name="delete_commission"),
   path('ApiGetGroupeDetails', ApiGetGroupeDetails, name="ApiGetGroupeDetails"),

   path('ApiGetSessionDetailsById',ApiGetSessionDetailsById, name="ApiGetSessionDetailsById"),

   path('ApiGetExamPlanificationDetails', ApiGetExamPlanificationDetails, name="ApiGetExamPlanificationDetails"),
   path('ApiUpdateExamPlanification',ApiUpdateExamPlanification, name="ApiUpdateExamPlanification"),

   path('examen_action', examen_action, name="examen_action"),
   path('rachat_action', rachat_action, name="rachat_action"),
   path('ajourne_action', ajourne_action, name="ajourne_action"),

   path('ApiGetCommissionResults', ApiGetCommissionResults, name="ApiGetCommissionResults"),
   path('close_commission/<int:pk>', close_commission, name="close_commission"),

   path('ApiLoadDataToPlan', ApiLoadDataToPlan, name="ApiLoadDataToPlan"),
   path('ApiPlanExam',ApiPlanExam, name="ApiPlanExam"),

   path('preview-pv/<int:pk>/', PreviewPV, name="PreviewPV"),

   path('validate-exam/', validate_exam, name="validate_exam"),
   path('validate_pv_exam/', validate_pv_exam, name="validate_pv_exam"),

   path('generate-pv/<int:pk>/', GeneratePv, name="GeneratePv"),
   path('save_exam_results/<int:pk>/', SaveExamResults, name="save_exam_results"),
   path('get_exam_history/<int:pk>/', GetExamHistory, name="get_exam_history"),
   path('get_calculated_results/<int:pk>/',get_calculated_results, name="get_calculated_results"),

   path('ShowPvModal/<int:pk>', ShowPvModal, name="ShowPvModal"),
   path('GeneratePvModal/<int:pk>/', GeneratePvModal, name="GeneratePvModal"),

   # URLs pour les résultats d'examens
   path('exams-results/', exams_results, name="exams_results"),
   path('api-list-pv-examen/', ApiListPvExamen, name="ApiListPvExamen"),
   path('api-delete-pv-examen/', ApiDeletePvExamen, name="ApiDeletePvExamen"),

   path('preview-pv-examen/<int:pk>/', ShowPv, name="ShowPv"),
   path('ApiDeleteExamPlanification', ApiDeleteExamPlanification, name="ApiDeleteExamPlanification"),

   
    path('deliberation/liste/', PagePvDeliberation, name="PagePvDeliberation"),
    path('ApiLoadDeliberationPv', ApiLoadDeliberationPv, name="ApiLoadDeliberationPv"),

    path('deliberation/results/liste/<int:pk>/',PageDeliberationResult, name="PageDeliberationResult"),
    path('ApiLoadSessionExamLines', ApiLoadSessionExamLines, name="ApiLoadSessionExamLines"),

    # URLs for group deliberation results
    path('groupe-deliberation-results/<int:groupe_id>/', groupe_deliberation_results_view, name="groupe_deliberation_results_view"),
    path('api/groupe-deliberation-results/', get_groupe_deliberation_results_ajax, name="get_groupe_deliberation_results_ajax"),


    path('details-session/exams/plannification/<int:pk>/',PageDetailsSessionExamPlan, name="PageDetailsSessionExamPlan"),

]