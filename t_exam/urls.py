from django.contrib import admin
from django.urls import path
from .views import *

app_name="t_exam"

urlpatterns = [

   path('liste-des-sessions/', ListeSession, name="ListeSession"),
   path('NewSession', NewSession, name="NewSession"),
   path('ApiListSession', ApiListSession, name="ApiListSession"),
   path('ApiDeleteSession', ApiDeleteSession, name="ApiDeleteSession"),
]