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
    try:
        preinscrit = Prospets.objects.get(id = id_preinscrit)

        fiche_voeux = FicheDeVoeux.objects.filter(prospect = preinscrit, is_confirmed = True).first()

        specialite = fiche_voeux.specialite
        promo = fiche_voeux.promo

        try:
            ClientPaiementsRequest.objects.create(
                client = preinscrit,
                promo = promo,
                specialite = specialite,
                motif = "frais_f"
            )

            return JsonResponse({'status' : "success"})
        except:
            return JsonResponse({"status" : "error"})
    except:
        return JsonResponse({'status' : "error"})