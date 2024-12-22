from django.contrib import admin
from django.urls import path,include
from .views import *

app_name="app"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('institut_app.urls',namespace='institut_app')),
    path('formateurs/',include('t_formateurs.urls',namespace='t_formateurs')),
]
