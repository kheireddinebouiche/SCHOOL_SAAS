from django.urls import path
from .views import *
# Utilise un chemin relatif
from .f_views.commission import *
from .f_views.action_views import examen_action, rachat_action, ajourne_action

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

   path('models-pv/', ModelBuilltinPage, name="ModelBuilltinPage"),
   path('ApiListModeleBuilltins', ApiListModeleBuilltins, name="ApiListModeleBuilltins"),

   path('NewModelBuilltin', NewModelBuilltin, name="NewModelBuilltin"),
   path('ApiDeleteModelBuitltin' , ApiDeleteModelBuitltin, name="ApiDeleteModelBuitltin"),
   path('ApiLoadTypeNote', ApiLoadTypeNote, name="ApiLoadTypeNote"),
   path('ApiAddNewType', ApiAddNewType, name="ApiAddNewType"),
   path('ApiDeleteTypeNote', ApiDeleteTypeNote, name="ApiDeleteTypeNote"),

   path('ApiGetTypeNoteDetails',ApiGetTypeNoteDetails, name="ApiGetTypeNoteDetails"),
   path('ApiUpdateTypeNote', ApiUpdateTypeNote, name="ApiUpdateTypeNote"),

   path('pv-note/<int:pk>/', ApiExamResult, name="ApiExamResult"),
   path('SaveNoteAjax', SaveNoteAjax , name="SaveNoteAjax"),

   path('ApiDeleteGroupeSessionLine', ApiDeleteGroupeSessionLine, name="ApiDeleteGroupeSessionLine"),


   path('commission/liste/', PageCommission, name="PageCommission"),
   path('commission/nouvelle/', NouvelleCommission, name="NouvelleCommission"),
   path('commission/modification/<int:pk>/', UpdateCommission, name="UpdateCommission"),
   path('commission/details/<int:pk>/', DetailsCommission, name="DetailsCommission"),
   path('validate_commission/<int:pk>/', validate_commission, name="validate_commission"),

   path('delete_commission/<int:pk>/', delete_commission, name="delete_commission"),
   path('ApiGetGroupeDetails', ApiGetGroupeDetails, name="ApiGetGroupeDetails"),

   path('examen_action', examen_action, name="examen_action"),
   path('rachat_action', rachat_action, name="rachat_action"),
   path('ajourne_action', ajourne_action, name="ajourne_action"),

]