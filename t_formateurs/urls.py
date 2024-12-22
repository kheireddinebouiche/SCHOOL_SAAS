from django.contrib import admin
from django.urls import path
from .views import *

app_name="t_formateurs"

urlpatterns = [
   path('liste-des-formateurs/',ListFormateur, name="ListFormateur"),
]
