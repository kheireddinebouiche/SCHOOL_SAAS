from django.urls import path
from .views import *

app_name="t_tresorerie"

urlpatterns = [

    path('attentes-de-paiements/', AttentesPaiements, name="attentes_de_paiements"),
    path('ApiListeDemandePaiement', ApiListeDemandePaiement, name="ApiListeDemandePaiement"),
    path('ApiDeleteDemandePaiement', ApiDeleteDemandePaiement, name="ApiDeleteDemandePaiement"),
]