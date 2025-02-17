from django.shortcuts import render
from .models import *
from .forms import *


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
    pass

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



