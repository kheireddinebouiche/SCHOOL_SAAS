from django.shortcuts import render,redirect
from django.http import JsonResponse
from ..models import *
from ..forms import *
from django.contrib import messages
from t_tresorerie.models import *
from t_formations.models import *
from django.db import transaction
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied
from functools import wraps
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.utils.dateformat import format


@login_required(login_url="institut_app:login")
def ApiValidateRemider(request):

    id_reminder  = request.POST.get('id_reminder')
    description = request.POST.get('description')
    statut = request.POST.get('statut_reminder')
    if id_reminder and description and statut:
        reminder_obj = RendezVous.objects.get(id = id_reminder)
        reminder_obj.description = description
        reminder_obj.statut = statut
        reminder_obj.save()

        return JsonResponse({"status" : "success"})
    else:
        return JsonResponse({"status" : "error", "message": "Tous les champs sont requis"})

@login_required(login_url="institut_app:login")
def ApiArchiveReminder(request):
    id_reminder = request.GET.get('id_reminder')

    reminder_obj = RendezVous.objects.get(id = id_reminder)
    reminder_obj.archived = True

    reminder_obj.save()

    return JsonResponse({"status" : "success"})
