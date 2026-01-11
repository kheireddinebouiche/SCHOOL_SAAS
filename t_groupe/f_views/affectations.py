from django.shortcuts import render, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from t_crm.models import *
from django.db.models import Count,Q,Exists, OuterRef

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

# @login_required(login_url="institut_app")
# def ApiSpecialiteByPromo(request):
#     if request.method == "GET":
#         promoCode = request.GET.get('promoCode')

#         specialites = (FicheDeVoeux.objects.filter(promo__code = promoCode, is_confirmed=True)
#                         .filter(promo__code=promoCode, is_confirmed=True,prospect__statut = "convertit", prospect__is_affected = False)
#                         .values('specialite__id', 'specialite__label')
#                         .annotate(nombre_etudiants=Count('id'))
#                         .order_by('specialite__label')
#                     )

#         return JsonResponse(list(specialites),safe=False)

@login_required(login_url="institut_app")
def ApiSpecialiteByPromo(request):
    if request.method != "GET":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    promoCode = request.GET.get("promoCode")

    if not promoCode:
        return JsonResponse({"error": "promoCode manquant"}, status=400)

    result = {}

    # =====================================================
    # 1️⃣ Spécialités simples
    # =====================================================
    voeux_simples = (
        FicheDeVoeux.objects.filter(
            promo__code=promoCode,
            is_confirmed=True,
            prospect__statut="convertit",
            prospect__is_affected=False
        )
        .values("specialite__id", "specialite__label","specialite__formation__nom")
        .annotate(nombre=Count("id"))
    )

    for v in voeux_simples:
        sid = v["specialite__id"]
        result[sid] = {
            "specialite_id": sid,
            "specialite_label": v["specialite__label"],
            "nombre_etudiants": v["nombre"],
        }

    # =====================================================
    # 2️⃣ Spécialités DOUBLE → réparties en spec1 & spec2
    # =====================================================
    voeux_doubles = (
        FicheVoeuxDouble.objects
        .select_related("specialite", "specialite__specialite1", "specialite__specialite2")
        .filter(
            promo__code=promoCode,
            is_confirmed=True,
            prospect__statut="convertit",
            prospect__is_affected=False
        )
    )

    for voeu in voeux_doubles:
        double_spec = voeu.specialite

        for spec in [double_spec.specialite1, double_spec.specialite2]:
            if not spec:
                continue

            if spec.id in result:
                result[spec.id]["nombre_etudiants"] += 1
            else:
                result[spec.id] = {
                    "specialite_id": spec.id,
                    "specialite_label": spec.label,
                    "nombre_etudiants": 1,
                }

    # =====================================================
    # 3️⃣ Tri final
    # =====================================================
    response = sorted(result.values(), key=lambda x: x["specialite_label"])

    return JsonResponse(response, safe=False)

@login_required(login_url="institut_app:login")
def AffectationAuGroupe(request, pk, code):
    context = {
        'specialite_id': pk,
        'promo_code': code,
    }
    return render(request, 'tenant_folder/scolarite/affectation_au_groupe.html', context)


# @login_required(login_url="insitut_app:login")
# def ApiListeStudentNotAffected(request):
#     promoCode = request.GET.get('promoId')
#     specialite_id = request.GET.get('specialite')

#     if not promoCode or not specialite_id:
#         return JsonResponse([], safe=False)

#     liste = (
#         Prospets.objects
#         .filter(statut="convertit")
#         .filter(
#             Q(
#                 prospect_fiche_voeux__promo__code=promoCode,
#                 prospect_fiche_voeux__specialite_id=specialite_id,
#                 prospect_fiche_voeux__is_confirmed=True
#             )
#             |
#             Q(
#                 prospect_fiche_voeux_double__promo__code=promoCode,
#                 prospect_fiche_voeux_double__is_confirmed=True,
#                 prospect_fiche_voeux_double__specialite__specialite1_id=specialite_id
#             )
#             |
#             Q(
#                 prospect_fiche_voeux_double__promo__code=promoCode,
#                 prospect_fiche_voeux_double__is_confirmed=True,
#                 prospect_fiche_voeux_double__specialite__specialite2_id=specialite_id
#             )
#         )
        
#         .distinct()
#         .values(
#             'id',
#             'nom',
#             'prenom',
#             'email',
#             'telephone',
#             'statut',
#             'matricule',
#             'matricule_interne',
#             'is_affected',
#             'groupe_line_student__groupe__id',
#             'groupe_line_student__groupe__nom'
#         )
#     )

#     return JsonResponse(list(liste), safe=False)

@login_required(login_url="insitut_app:login")
def ApiListeStudentNotAffected(request):
    promoCode = request.GET.get('promoId')
    specialite_id = request.GET.get('specialite')

    if not promoCode or not specialite_id:
        return JsonResponse([], safe=False)

    # ==========================================
    # Sous-requête : étudiant déjà affecté ?
    # ==========================================
    affectation_exists = AffectationGroupe.objects.filter(
        etudiant=OuterRef('pk'),
        specialite_id=specialite_id
    )

    liste = (
        Prospets.objects
        .filter(statut="convertit")
        .filter(
            Q(
                prospect_fiche_voeux__promo__code=promoCode,
                prospect_fiche_voeux__specialite_id=specialite_id,
                prospect_fiche_voeux__is_confirmed=True
            )
            |
            Q(
                prospect_fiche_voeux_double__promo__code=promoCode,
                prospect_fiche_voeux_double__is_confirmed=True,
                prospect_fiche_voeux_double__specialite__specialite1_id=specialite_id
            )
            |
            Q(
                prospect_fiche_voeux_double__promo__code=promoCode,
                prospect_fiche_voeux_double__is_confirmed=True,
                prospect_fiche_voeux_double__specialite__specialite2_id=specialite_id
            )
        )
        .annotate(
            deja_affecte=Exists(affectation_exists)
        )
        .values(
            'id',
            'nom',
            'prenom',
            'email',
            'telephone',
            'statut',
            'matricule',
            'matricule_interne',
            'deja_affecte'
        )
    )

    # ==========================================
    # Ajouter le groupe si déjà affecté
    # ==========================================
    result = []
    for e in liste:
        if e['deja_affecte']:
            affect = AffectationGroupe.objects.filter(
                etudiant_id=e['id'],
                specialite_id=specialite_id
            ).select_related('groupe').first()

            e['etat_affectation'] = "deja_affecte"
            e['groupe_id'] = affect.groupe.id if affect else None
            e['groupe_nom'] = affect.groupe.nom if affect else None
        else:
            e['etat_affectation'] = "non_affecte"
            e['groupe_id'] = None
            e['groupe_nom'] = None

        result.append(e)

    return JsonResponse(result, safe=False)


@login_required(login_url="institut_app:login")
def ApiGroupeListeForAffectation(request):
    promoId = request.GET.get('promoId')
    specialite = request.GET.get('specialite') 
    
    liste = Groupe.objects.filter(promotion__code=promoId,specialite_id=specialite,etat='inscription').annotate(total=Count('groupe_line_groupe')).values('id', 'nom', 'min_student', 'max_student', 'etat', 'total')

    return JsonResponse(list(liste), safe=False)


@login_required(login_url="institut_app:login")
def ApiGetSpecialiteDatas(request):

    if request.method == 'GET':

        specialite = request.GET.get('specialite')
        promo = request.GET.get('promo')
        
        object = Specialites.objects.filter(id = specialite).values('id','label','code','condition_access')
        nb_groupe= Groupe.objects.filter(promotion__code = promo, specialite_id = specialite,etat='inscription').count()

        data = {
            'specialite' : list(object),
            'nb_groupe' : nb_groupe,
        }

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"status":"error", "message": "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiAffectStudentToGroupe(request):
    if request.method == "POST":
        studentId = request.POST.get('studentId')
        groupId = request.POST.get('groupId')
        specialite = request.POST.get('specialite')


        if not studentId and not groupId:
            return JsonResponse({"status":"error",'message':'Informations manquantes'})

        GroupeLine.objects.create(
            student_id = studentId,
            groupe_id = groupId
        )

        AffectationGroupe.objects.create(
            etudiant_id = studentId,
            groupe_id = groupId,
            specialite_id = specialite,
        )

       
        return JsonResponse({"status":  "success"})
    else:
        return JsonResponse({"status" : "error", 'message':"Méthode non autorisée"})
    

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiCancelStudentAffectation(request):
    if request.method == "GET":
        studentId = request.GET.get('studentId')
        specialite = request.GET.get('specialite')

        if not studentId:
            return JsonResponse({"status":"error","message":"Informations manquantes"})
        
        obj = GroupeLine.objects.get(student_id = studentId, groupe__specialite__id = specialite)
        obj.delete()

        AffectationGroupe.objects.get(etudiant_id = studentId, specialite_id = specialite).delete()

        return JsonResponse({"status":"success","message":"L'affectation a été annulée avec succès"})
    else:
        return JsonResponse({"status":"error","message":"Méthode non autorisée"})