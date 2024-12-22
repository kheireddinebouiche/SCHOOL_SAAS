from django.contrib import admin
from django.urls import path,include
from .views import *
from .admin import tenant_admin_site

app_name="app"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Index, name="index"),  
    path('admin_tenant/', tenant_admin_site.urls),
    
]
