from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import *
from .models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from t_groupe.models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods


@login_required(login_url="institut_app:login")
def ListeDesSalles(request):
    salles = Salle.objects.all()
    context = {
        'salles' : salles
    }
    return render(request, 'tenant_folder/timetable/liste_des_salles.html', context)


@login_required(login_url="institut_app:login")
def ListeDesEmploie(request):
    liste = Timetable.objects.all()
    context = {
        'timetables' : liste
    }
    return render(request ,'tenant_folder/timetable/liste_des_emploies.html', context)

@login_required(login_url="institut_app:login")
def CreateTimeTable(request):
    pass


@login_required(login_url="institut_app:login")
def timetable_view(request):
    pass


@login_required(login_url="institut_app:login")
def timetable_edit(request, pk):
    timetable = Timetable.objects.get(id = pk)
    context = {
        'timetable' : timetable,
    }
    if timetable.is_configured:
        return render(request, 'tenant_folder/timetable/configure_timetable_cours.html', context)
    else:
        return render(request, 'tenant_folder/timetable/configuration_emploie.html', context)


@login_required(login_url="institut_app:login")
def timetable_configure(request, pk):
    timetable = Timetable.objects.get(id = pk)
    crenau = ModelCrenau.objects.all()
    context = {
        'timetable' : timetable,
        'crenau' : crenau,
    }
    if timetable.is_configured:
        return render(request, 'tenant_folder/timetable/configure_timetable_cours.html', context)
    else:
        return render(request, 'tenant_folder/timetable/configuration_emploie.html', context)
    
@login_required(login_url="institut_app:login")
def ApiMakeTimetableDone(request):
    pass
@login_required(login_url="institut_app:login")
def save_session(request):
    pass