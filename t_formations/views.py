from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


def listModules(request):
    modules = Modules.objects.all()
    return render(request, 't_formations/modules.html', {'modules': modules})

def listSpecialites(request):
    specialites = Specialites.objects.all()
    return render(request, 't_formations/specialites.html', {'specialites': specialites})

def listFormations(request):
    formations = Formation.objects.all()
    return render(request, 't_formations/formations.html', {'formations': formations})

def listFraisInscription(request):
    frais = FraisInscription.objects.all()
    return render(request, 't_formations/frais.html', {'frais': frais})

def addFormation(request):
    form = NewFormationForm()
    if request.method == 'POST':
        form = NewFormationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formation ajoutée avec succès')
            return redirect('listFormations')
    return render(request, 'tenant_folder/formations/nouvelle_formations.html', {'form': form})


def addSpecialite(request):
    pass

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

def detailFormation(request):
    pass

def detailSpecialite(request):
    pass

def detailModule(request):
    pass

def detailFraisInscription(request):
    pass



