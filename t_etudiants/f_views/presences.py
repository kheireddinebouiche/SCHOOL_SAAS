from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.contrib.auth.decorators import login_required
from ..forms import *
from t_crm.models import NotesProcpects, RendezVous
from django.db import transaction



@login_required(login_url="institut_app:login")
def RegistrePage(request):
    return render(request, 'tenant_folder/presences/registres.html')