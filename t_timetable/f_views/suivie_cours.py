from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..forms import *
from ..models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from t_groupe.models import *



@login_required(login_url="institut_app:login")
def PageSuivieCours(request):
    seances = TimetableEntry.objects.all()
    groupes = Groupe.objects.all()
    context = {
        'seances' : seances,
        'groupes' : groupes,
    }

    return render(request, 'tenant_folder/timetable/avancement/suivie_cours.html', context)


