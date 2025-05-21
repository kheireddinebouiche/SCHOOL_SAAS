from django.urls import path
from .views import *

app_name="t_tresorerie"

urlpatterns = [

    path('attentes-de-paiements/', AttentesPaiements, name="attentes_de_paiements"),
    path('ApiListeDemandePaiement', ApiListeDemandePaiement, name="ApiListeDemandePaiement"),
    path('ApiDeleteDemandePaiement', ApiDeleteDemandePaiement, name="ApiDeleteDemandePaiement"),

    path('ApiGetDetailsDemandePaiement', ApiGetDetailsDemandePaiement, name="ApiGetDetailsDemandePaiement"),

    path('details-paiement-request/<int:pk>/',PageDetailsDemandePaiement, name="PageDetailsDemandePaiement"),

    path('configuration/' , PageConfigPaiementSeuil, name="PageConfigPaiementSeuil"),
    path('ApiListSeuilPaiement', ApiListSeuilPaiement, name="ApiListSeuilPaiement"),

    path('ApiListeSpecialite', ApiListeSpecialite, name="ApiListeSpecialite"),
    path('ApiAddNewSeuil', ApiAddNewSeuil, name="ApiAddNewSeuil"),
    path('ApiDeleteSeuil', ApiDeleteSeuil, name="ApiDeleteSeuil"),
    path('ApiGetRequestPaiementsLine', ApiGetRequestPaiementsLine, name="ApiGetRequestPaiementsLine"),

    path('ApiListPaiementDone', ApiListPaiementDone, name="ApiListPaiementDone"),
    path('ApiStorePaiement', ApiStorePaiement, name="ApiStorePaiement"),
]