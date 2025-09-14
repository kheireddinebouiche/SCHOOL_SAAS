from django.urls import path
from .views import *

app_name="t_remise"

urlpatterns = [

    path('liste-des-remises/', ListeRemise, name="ListeRemise"),
    path('ApiListeRemise/', ApiListeRemise, name="ApiListeRemise"),
    path('ApiCreateRemise', ApiCreateRemise, name="ApiCreateRemise"),
    path('ApiDetailsRemise', ApiDetailsRemise, name="ApiDetailsRemise"),
    path('ApiActivateRemise', ApiActivateRemise, name="ApiActivateRemise"),

]