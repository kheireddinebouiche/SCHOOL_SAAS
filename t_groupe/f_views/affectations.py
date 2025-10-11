from django.shortcuts import render, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from t_crm.models import *
from django.db.models import Count

@login_required(login_url="institut_app:login")
def AffectationPage(request):
    return render(request, 'tenant_folder/scolarite/attente_affectation.html')

@login_required(login_url="institut_app:login")
def ApiLoadAttenteAffectation(request):
    pass

@login_required(login_url="institut_app:login")
def ApiListePromosEnAttente(request):
    promo = Promos.objects.filter(etat = "active")
    data = []
    for i in promo:

        nombre_etudiant = FicheDeVoeux.objects.filter(promo_id = i.id, is_confirmed = True,prospect__statut = "convertit", prospect__is_affected=False).count()

        data.append({
            'id' : i.id,
            'label': i.label,
            'code': i.code,
            'begin_year': i.begin_year,
            'end_year': i.end_year,
            'session': i.get_session_display(),
            'session_key': i.session,
            'date_debut': i.date_debut,
            'date_fin': i.date_fin,
            'created_at': i.created_at.strftime("%Y-%m-%d"),
            'nombre_etudiants' : nombre_etudiant,
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app")
def ApiSpecialiteByPromo(request):
    if request.method == "GET":
        promoCode = request.GET.get('promoCode')

        specialites = (FicheDeVoeux.objects.filter(promo__code = promoCode, is_confirmed=True)
                        .filter(promo__code=promoCode, is_confirmed=True,prospect__statut = "convertit")
                        .values('specialite__id', 'specialite__label')
                        .annotate(nombre_etudiants=Count('id'))
                        .order_by('specialite__label')
                    )

        return JsonResponse(list(specialites),safe=False) 

@login_required(login_url="institut_app:login")
def AffectationAuGroupe(request, pk, code):
    context = {
        'specialite_id': pk,
        'promo_code': code,
    }
    return render(request, 'tenant_folder/scolarite/affectation_au_groupe.html', context)


@login_required(login_url="insitut_app:login")
def ApiListeStudentNotAffected(request):
    promoId = request.GET.get('promoId')
    specialite = request.GET.get('specialite') 


    liste = (Prospets.objects
             .filter(statut = "convertit", prospect_fiche_voeux__specialite_id=specialite, prospect_fiche_voeux__promo__code = promoId)
             .values('id','nom','prenom','email','telephone','statut','matricule','matricule_interne','is_affected'))

    return JsonResponse(list(liste), safe=False)


@login_required(login_url="institut_app:login")
def ApiGroupeListeForAffectation(request):
    promoId = request.GET.get('promoId')
    specialite = request.GET.get('specialite') 
    
    liste = Groupe.objects.filter(promotion__code=promoId,specialite_id=specialite).annotate(total=Count('groupe_line_groupe')).values('id', 'nom', 'min_student', 'max_student', 'etat', 'total')

    return JsonResponse(list(liste), safe=False)


@login_required(login_url="institut_app:login")
def ApiGetSpecialiteDatas(request):

    if request.method == 'GET':

        specialite = request.GET.get('specialite')
        promo = request.GET.get('promo')
        
        object = Specialites.objects.filter(id = specialite).values('id','label','code','condition_access')
        nb_groupe= Groupe.objects.filter(promotion__code = promo, specialite_id = specialite).count()

        data = {
            'specialite' : list(object),
            'nb_groupe' : nb_groupe,
        }

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"status":"error", "message": "Methode non autoriser"})


@login_required(login_url="institut_app:login")
def ApiAffectStudentToGroupe(request):
    studentId = request.POST.get('studentId')
    groupId = request.POST.get('groupId')
    pass