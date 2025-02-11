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


def Index(request):
    tenant = getattr(request, 'tenant', None)
    # Get the schema name or set it to "Unknown" if no tenant is found
    schema_name = tenant.schema_name if tenant else "Unknown"

    form = UserForm()
    profile = ProfilForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        profile = ProfilForm(request.POST)

        if form.is_valid() and profile.is_valid():

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            User = get_user_model()
            User = User.objects.create_user(username=username,email = email,password=password)

            profile = Profile(user = User,adresse = 'Adresse de mon user')
            profile.save()

            return redirect('institut_app:index')


    context = {
        'schema_name' : schema_name,
        'schema_context' : schema_context,
        'form' : form,
        'profile' : profile,
    }

    return render(request, 'tenant_folder/index.html', context)

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

