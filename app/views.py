from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .form import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django_tenants.utils import schema_context
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login



def Index(request):
    tenants = Institut.objects.exclude(schema_name='public')
    
    if request.method == 'POST':
        tenant_slug = request.POST.get('tenant_slug')
        return redirect_to_tenant(request, tenant_slug)
    
    context = {
        'tenants': tenants
    }
    return render(request, 'public_folder/organisation_select.html', context)

def redirect_to_tenant(request, tenant_slug):
    try:
        tenant = Institut.objects.get(nom=tenant_slug)
        domain = Domaine.objects.filter(tenant=tenant, is_primary=True).first()
        
        if domain:
            # Construire l'URL du tenant
            scheme = 'https' if request.is_secure() else 'http'
            tenant_url = f"{scheme}://{domain.domain}"
            
            # Pour le développement local avec port
            if 'localhost' in request.get_host():
                port = request.get_host().split(':')[1] if ':' in request.get_host() else '8000'
                tenant_url = f"{scheme}://{tenant.nom}.localhost:{port}"
            return redirect(tenant_url)
    except Institut.DoesNotExist:
        pass
    
    return redirect('tenant_selection')

def new_tenant(request):
    form = NewTenantForm()
    userForm = NewUser()

    if request.method == 'POST':
        form = NewTenantForm(request.POST)
        userForm = NewUser(request.POST)
        if form.is_valid() and userForm.is_valid():

            nom = form.cleaned_data.get('nom')
            adresse = form.cleaned_data.get('adresse')
            telephone = form.cleaned_data.get('telephone')

            username = userForm.cleaned_data.get('username')
            email = userForm.cleaned_data.get('email')
            password = userForm.cleaned_data.get('password')

            current_site = get_current_site(request)
            domain_name = current_site.domain.split(':')[0]

            tenant = Institut(
                schema_name = nom,
                nom = nom,
                telephone = telephone,
                adresse = adresse,
                tenant_type = 'second',

            )
            tenant.save()

            domain = Domaine(domain=f"{tenant.schema_name}.{domain_name}", tenant=tenant, is_primary=True)
            domain.save()
           
            with schema_context(tenant.schema_name):
                # Create default user
                default_user = User.objects.create_superuser(

                    username=username,
                    email=email,
                    password=password

                )
                default_user.save()

            messages.success(request,'Le compte à été crée avec succès')

            return redirect('index')
        

    context = {
        'form' : form,
        'userForm' : userForm,
    }
    return render(request, 'public_folder/new_tenant.html', context)

def tenant_list(request):
    list = Institut.objects.all()
    return render(request,'public_folder/list_tenant.html',{'list' : list})

def CreateSuperUser(request):
    form = NewUser()
    if request.method == 'POST':
        form = NewUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            
            tenant = getattr(request, 'tenant', None)
            with schema_context(tenant.schema_name):
                user = User.objects.create_superuser(
                    username = username,
                    email = email,
                    password = password
                )

                user.save()

                
            messages.success(request, "L'utilisateur à été crée avec succès")
            return redirect('index')
    else:

        context = {
            'form' : form,
        }
        return render(request,'public_folder/new_user.html', context)
    
def logout_view(request):
    logout(request)
    messages.success(request,'Vous étes maintenant déconnecter')
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue, {user.username} ! Vous êtes connecté.")
            return redirect('index') 
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    
    return render(request, 'registration/login.html')

def profile(request):
    pass

def NombreLead(request):
    return render(request, 'public_folder/marketing/nombres_leads.html')

def socialEngagement(request):
    return render(request, 'public_folder/marketing/social_engagment.html')