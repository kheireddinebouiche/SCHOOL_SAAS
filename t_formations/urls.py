from django.contrib import admin
from django.urls import path
from .views import *

app_name="t_formations"

urlpatterns = [

    path('nouvelle-formation/', addFormation, name="addFormation"),
    path('nouvelle-specialite/', addSpecialite, name="addSpecialite"),
]
