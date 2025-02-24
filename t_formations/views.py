from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django_tenants.utils import get_tenant_model, schema_context

TenantModel = get_tenant_model()
tenants = TenantModel.objects.filter(tenant_type='second')

def listModules(request):
    modules = Modules.objects.all()
    return render(request, 't_formations/modules.html', {'modules': modules})

def listSpecialites(request):
    specialites = Specialites.objects.all()
    context = {
        'liste' : specialites,
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/formations/liste_des_specialites.html', context)

def listFormations(request):
    formations = Formation.objects.all()
    context = {
        'liste': formations,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/formations/liste_des_formations.html', context)

def listFraisInscription(request):
    frais = FraisInscription.objects.all()
    return render(request, 't_formations/frais.html', {'frais': frais})

@transaction.atomic
def addFormation(request):
    
    if request.tenant.tenant_type == 'master':
        form = NewFormationFormMaster()
    else:
        form = NewFormationForm()

    if request.method == 'POST':
        form = NewFormationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formation ajoutée avec succès')
            return redirect('t_formations:listFormations')
    context = {
        'form' : form,
    }
    return render(request, 'tenant_folder/formations/nouvelle_formations.html', context)

@transaction.atomic
def AddPartenaire(request):
    form = NewPartenaireForm()
    if request.method == 'POST':
        form = NewPartenaireForm(request.POST)
        if form.is_valid():
            partenaires = form.save()
            for tenant in tenants:
                with schema_context(tenant.schema_name):
                    Partenaires.objects.create(
                        nom  = partenaires.nom,
                        adresse = partenaires.adresse,
                        telephone = partenaires.telephone,
                        email = partenaires.email,
                        site_web = partenaires.site_web,
                    )
            messages.success(request, 'Partenaire ajouté avec succès')
            return redirect('t_formations:listPartenaires')
        
    context = {
        'form' : form,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/formations/new_partenaire.html', context)

def detailsPartenaire(request, pk):
    partenaire = Partenaires.objects.get(id=pk)
    context = {
        'partenaire' : partenaire,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/formations/details_partenaire.html', context)

def deletePartenaire(request, pk):
    partenaire = Partenaires.objects.get(id=pk)
    partenaire.delete()
    messages.success(request, 'Partenaire supprimé avec succès')
    return redirect('t_formations:listPartenaires')

def ListeDesPartenaires(request):
    liste = Partenaires.objects.all()
    context = {
        'liste' : liste,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/formations/liste_des_partenaires.html', context)

@transaction.atomic
def addSpecialite(request):
    form = NewSpecialiteForm()
    if request.method == 'POST':
        form = NewSpecialiteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Spécialité ajoutée avec succès")
            return redirect('t_formations:listSpecialites')
           
        else:
            errors = " | ".join(["{}: {}".format(field, ", ".join(errors)) for field, errors in form.errors.items()])
            messages.error(request, f"{errors}")
            return redirect('t_formations:addSpecialite')
        
    else:
        context = {
            'form' : form,
            'tenant' : request.tenant,
        }

        return render(request, 'tenant_folder/formations/nouvelle_specialite.html', context)

def addModule(request):
    pass

def addFraisInscription(request):
    pass

def updateFormation(request):
    pass

def updateSpecialite(request):
    pass

def updateModule(request):
    pass

def updateFraisInscription(request):
    pass

def deleteFormation(request):
    pass

def deleteSpecialite(request):
    pass

def deleteModule(request):
    pass

def deleteFraisInscription(request):
    pass

def detailFormation(request, pk):
    formation = Formation.objects.get(id = pk)
    specialite = Specialites.objects.filter(formation = formation)

    context = {
        'formation' : formation,
        'tenant' : request.tenant,
        'specialite' : specialite,
    }
    return render(request, 'tenant_folder/formations/details_formation.html', context)

def detailSpecialite(request):
    pass

def detailModule(request):
    pass

def detailFraisInscription(request):
    pass



