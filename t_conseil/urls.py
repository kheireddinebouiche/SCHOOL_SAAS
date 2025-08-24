from django.urls import path
from .views import *

app_name="t_conseil"

urlpatterns = [

  path('liste-des-thematiques/',ListeThematique, name="ListeThematique"),

  path('nouveau-devis/', AddNewDevis, name="AddNewDevis"),

  path('configuration-devis/<str:pk>/', configure_devis , name="configure-devis"),
   
]