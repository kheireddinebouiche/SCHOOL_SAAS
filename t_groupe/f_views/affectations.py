from django.shortcuts import render, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url="institut_app:login")
def AffectationPage(request):
    return render(request, 'tenant_folder/scolarite/attente_affectation.html')

@login_required(login_url="institut_app:login")
def ApiLoadAttenteAffectation(request):
    pass

def ApiListePromosEnAttente(request):
    pass
