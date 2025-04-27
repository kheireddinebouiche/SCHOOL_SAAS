from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .form import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django_tenants.utils import schema_context
from django.contrib.auth.models import User


@login_required(login_url='login')
def Index(request):
    
    tenant = getattr(request, 'tenant', None)
    # Get the schema name or set it to "Unknown" if no tenant is found
    schema_name = tenant.schema_name if tenant else "Unknown"

    return HttpResponse(f"<h4>Bienvenue sur votre site public {schema_name}</h4>")

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