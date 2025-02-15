from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django_tenants.utils import schema_context
from .form import *
from .models import Profile
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect

@login_required(login_url='institut_app:login')
def Index(request):
    tenant = getattr(request, 'tenant', None)
    # Get the schema name or set it to "Unknown" if no tenant is found
    schema_name = tenant.schema_name if tenant else "Unknown"

    return render(request, 'tenant_folder/index.html')

def logout_view(request):
    logout(request)
    messages.success(request,'Vous étes maintenant déconnecter')
    return redirect('institut_app:login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue, {user.username} ! Vous êtes connecté.")
            return redirect('institut_app:index')  # Redirigez vers une page de votre choix
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    
    return render(request, 'registration/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        new_user = User(
            username=username,
            email=email,
            
        )
        new_user.set_password(password1)
        new_user.save()
        messages.success(request, 'Compte créé avec succès')
        return redirect('institut_app:login')
 
    return render(request, 'registration/register.html')

