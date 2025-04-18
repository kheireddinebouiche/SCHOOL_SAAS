from django.contrib import admin
from django.urls import path,include
from .views import *
from .admin import tenant_admin_site
from django.contrib.auth.views import LoginView, LogoutView


app_name="app"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Index, name="index"),  
    path('admin_tenant/', tenant_admin_site.urls),
    path('nouveau-compte/', new_tenant, name="nouveau-tenant"),
    path('liste-comptes/', tenant_list, name="tenant_list"),
    
    path('nouveau-utilisateur/', CreateSuperUser, name="CreateSuperUser"),
    
    path('login/',LoginView.as_view(), name="login"),
    path('logout/',LogoutView.as_view(), name="logout"),


]
