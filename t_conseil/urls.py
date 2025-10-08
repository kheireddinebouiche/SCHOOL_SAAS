from django.urls import path
from .views import *
from .f_views.prospects import *

app_name="t_conseil"

urlpatterns = [

  path('liste-des-thematiques/',ListeThematique, name="ListeThematique"),

  path('nouveau-devis/', AddNewDevis, name="AddNewDevis"),

  path('configuration-devis/<str:pk>/', configure_devis , name="configure-devis"),

  path('ApiSaveThematique' , ApiSaveThematique, name="ApiSaveThematique"),

  path('ApiLoadThematique' , ApiLoadThematique, name="ApiLoadThematique"),

  path('ApiLoadThematiqueDetails', ApiLoadThematiqueDetails, name="ApiLoadThematiqueDetails"),

  path('archive-thematique/', ArchiveThematique, name="ArchiveThematique"),

  path('ApiLoadArchivedThematique', ApiLoadArchivedThematique, name="ApiLoadArchivedThematique"),
  path('ApiArchiveThematique', ApiArchiveThematique, name="ApiArchiveThematique"),
  path('ApiActivateThematique', ApiActivateThematique, name="ApiActivateThematique"),
  path('ApiUpdateThematique', ApiUpdateThematique, name="ApiUpdateThematique"),



  path('prospects-en-instance/',ListeProspectConseil, name="prospectInstance"),
  path('ApiLoadProspect',ApiLoadProspect, name="ApiLoadProspect"),
  path('ApiTransformeToClient',ApiTransformeToClient, name="ApiTransformeToClient"),

  path('ApiListeProspect',ApiListeProspect, name="ApiListeProspect"),
  
   
]