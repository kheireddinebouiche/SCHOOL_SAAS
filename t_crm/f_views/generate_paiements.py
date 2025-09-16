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

def load_preinscrit_promo(id_preinscrit):
    pass

def load_preinscrit_voeux(id_preinscrit):
    pass

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiGeneratePaiementRequest(id_preinscrit):
    preinscrit = Prospets.objects.get(id = id_preinscrit)

    try:
        ClientPaiementsRequest.objects.create(
            client = preinscrit,
        )

        return JsonResponse({'status' : "success"})
    except:
        return JsonResponse({"status" : "error"})