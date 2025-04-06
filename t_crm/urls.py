from django.contrib import admin
from django.urls import path
from .views import *

app_name="t_crm"

urlpatterns = [
    
    path('nouveau-visiteur/',nouveauVisiteur, name="nouveau_visiteur"),
    path('liste-des-visiteurs/',listeVisiteurs, name="liste_visiteurs"),
    path('ApiListeVisiteurs',ApiListeVisiteurs, name="ApiListeVisiteurs"),
    path('details-visiteur/<int:pk>/',detailsVisiteur, name="details_visiteur"),
    path('mise-a-jours/<int:pk>/', updateVisiteur, name="updateVisiteur"),
    path('delete-visiteur/', supprimerVisiteur, name="supprimer_visiteur"),

    path('ApiGetSpecialite',ApiGetSpecialite,name="ApiGetSpecialite"),
    path('ApiGETDemandeInscription', ApiGETDemandeInscription,name="ApiGETDemandeInscription"),
    path('ApiAddNewDemandeInscription',ApiAddNewDemandeInscription,name='ApiAddNewDemandeInscription'),
    path('liste-demande-inscription/', ListeDemandeInscription, name="ListeDemandeInscription"),
    path('ApiGetListeDemandeInscription', ApiGetListeDemandeInscription, name="ApiGetListeDemandeInscription"),
    path('ApiGetGrideDemandeInscription', ApiGetGrideDemandeInscription, name="ApiGetGrideDemandeInscription"),
   
    
    path('ApiConfirmDemandeInscription', ApiConfirmDemandeInscription, name="ApiConfirmDemandeInscription"),
    path('ApiAnnulerDemandeInscription', ApiAnnulerDemandeInscription, name="ApiAnnulerDemandeInscription"),
]
