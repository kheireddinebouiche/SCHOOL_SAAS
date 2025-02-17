from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('institut_app.urls',namespace='institut_app')),
    path('rh/',include('t_rh.urls',namespace='t_rh')),
    path('crm/',include('t_crm.urls',namespace='t_crm')),
    
]
