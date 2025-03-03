from django.contrib import admin
from django.urls import path
from .views import *

app_name="t_etudiants"

urlpatterns = [

   path('liste-des-etudiants/', ListeStudents, name="ListeStudents"),
]