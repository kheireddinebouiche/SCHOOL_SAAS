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


@login_required(login_url='institut_app:login')
def ApiLoadProspectPerosnalInfos(request):
    id_prospect = request.GET.get('id_prospect')
    prospect = Prospets.objects.filter(id=id_prospect).values('created_at','id','nin','nom','prenom','email','telephone','type_prospect','canal','etat','entreprise','poste_dans_entreprise','observation').first()

    return JsonResponse(prospect, safe=False)


def ApiLoadProspectRendezVous(request):
   pass

################################### Gestion des notes ##################################################
@login_required(login_url='institut_app:login')
def ApiLoadNote(request):
    prospect_id = request.GET.get('id_prospect')
    notes = NotesProcpects.objects.filter(id = prospect_id).values('id','prospect','created_by','created_at','note')
    return JsonResponse(list(notes), safe=False)
    
@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiStoreNote(request):
    pass

@login_required(login_url='institut_app:login')
def ApiDeleteNote(request):
    pass

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiUpdateNote(request):
    pass


################################### !Gestion des notes##################################################


###################################Fiche de voeux prospect #############################################
@login_required(login_url='institut_app:login')
def ApiLoadFicheVoeuxProspect(request):
    id_prospect = request.GET.get('id_prospect')
    prospect = Prospets.objects.get(id = id_prospect)
    fiche_voeux = FicheDeVoeux.objects.filter(prospect = prospect)

    fiche_voeux_list = []
    for fiche in fiche_voeux:
        fiche_voeux_list.append({
            'id': fiche.id,
            'specialite_code': fiche.specialite.code,
            'specialite_label': fiche.specialite.label,
            'specialite_id' : fiche.specialite.id,
            'specialite_id_formation': fiche.specialite.formation.id
        })
    return JsonResponse({'fiche_voeux': fiche_voeux_list})

@login_required(login_url='institut_app:login')
def ApiUpdateFicheVoeuxProspect(request):
    pass

def ApiDeleteFicheVoeuxProspect(request):
    pass

###################################Fiche de voeux prospect #############################################