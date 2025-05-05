from django.contrib import admin
from django.urls import path
from .views import *

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

]