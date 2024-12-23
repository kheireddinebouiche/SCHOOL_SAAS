from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

app_name="institut_app"

urlpatterns = [
    
    path('',Index, name="index"),
    path('login/',LoginView.as_view(), name="login"),
    path('logout/',LogoutView.as_view(), name="logout"),
    
]
