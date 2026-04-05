from django.urls import path
from .views import *

app_name="t_remise"

urlpatterns = [

    path('liste-des-remises/', ListeRemise, name="ListeRemise"),
    path('ApiListeRemise/', ApiListeRemise, name="api_liste_remise"),
    path('ApiCreateRemise/', ApiCreateRemise, name="api_create_remise"),
    path('ApiDetailsRemise/', ApiDetailsRemise, name="api_details_remise"),
    path('ApiActivateRemise/', ApiActivateRemise, name="api_activate_remise"),
    path('ApiDeactivateRemise/', ApiDeactivateRemise, name="api_deactivate_remise"),
    path('ApiUpdateRemise/', ApiUpdateRemise, name="api_update_remise"),
    path('ApiDeleteRemise/', ApiDeleteRemise, name="api_delete_remise"),

]