from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .form import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

def Index(request):
    tenant = getattr(request, 'tenant', None)

    # Get the schema name or set it to "Unknown" if no tenant is found
    schema_name = tenant.schema_name if tenant else "Unknown"

    return HttpResponse(f"<h4>Bienvenue sur votre site public {schema_name}</h4>")

def new_tenant(request):
    form = NewTenantForm()

    if request.method == 'POST':
        form = NewTenantForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data.get('nom')
            adresse = form.cleaned_data.get('adresse')
            telephone = form.cleaned_data.get('telephone')

            current_site = get_current_site(request)
            domain_name = current_site.domain.split(':')[0]

            tenant = Institut(
                schema_name = nom,
                nom = nom,
                telephone = telephone,
                adresse = adresse
            )
            tenant.save()

            domain = Domaine(domain=f"{tenant.schema_name}.{domain_name}", tenant=tenant, is_primary=True)
            domain.save()

            messages.success(request,'Le compte à été crée avec succès')

            return redirect('app:index')
        

    context = {
        'form' : form,
    }
    return render(request, 'public_folder/new_tenant.html', context)

def tenant_list(request):
    list = Institut.objects.all()
    return render(request,'public_folder/list_tenant.html',{'list' : list})