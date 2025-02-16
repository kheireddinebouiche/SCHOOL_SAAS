from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView



app_name="institut_app"

urlpatterns = [
    
    path('',Index, name="index"),
   
    path('login/',login_view, name="login"),
    path('register/', register, name="register"),
    path('logout/',logout_view, name="logout"),

    path('nouvelle-entreprise/', NewEntreprise, name="new_entreprise"),
    path('liste-des-entreprise/', ListeEntreprises, name="liste_entreprise"),
    path('modification-entreprise/<int:id>/', ModifierEntreprise, name="modifier_entreprise"),
    
]
