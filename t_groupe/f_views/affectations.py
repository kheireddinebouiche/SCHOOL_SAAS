from django.shortcuts import render, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from t_crm.models import *
from t_etudiants.models import Etudiant
from t_conseil.models import Participant
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
            "formation_label": v["specialite__formation__nom"],
            "nombre_etudiants": v["nombre"],
            "nombre_double": 0,
        }

    # =====================================================
    # 2️⃣ Spécialités DOUBLE → réparties en spec1 & spec2
    # =====================================================
    voeux_doubles = (
        FicheVoeuxDouble.objects
        .select_related(
            "specialite", 
            "specialite__specialite1", "specialite__specialite1__formation",
            "specialite__specialite2", "specialite__specialite2__formation"
        )
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
                result[spec.id]["nombre_double"] += 1
            else:
                result[spec.id] = {
                    "specialite_id": spec.id,
                    "specialite_label": spec.label,
                    "formation_label": spec.formation.nom if spec.formation else "N/A",
                    "nombre_etudiants": 1,
                    "nombre_double": 1,
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
    
    liste = Groupe.objects.filter(promotion__code=promoId, specialite_id=specialite, etat__in=['inscription', 'inscription_terminee']).annotate(total=Count('groupe_line_groupe')).values('id', 'nom', 'min_student', 'max_student', 'etat', 'total')

    return JsonResponse(list(liste), safe=False)


@login_required(login_url="institut_app:login")
def ApiGetSpecialiteDatas(request):

    if request.method == 'GET':

        specialite = request.GET.get('specialite')
        promo = request.GET.get('promo')
        
        object = Specialites.objects.filter(id = specialite).values('id','label','code','condition_access')
        nb_groupe = Groupe.objects.filter(promotion__code=promo, specialite_id=specialite, etat='inscription').count()
        nb_groupe_brouillon = Groupe.objects.filter(promotion__code=promo, specialite_id=specialite, etat='brouillon').count()

        data = {
            'specialite' : list(object),
            'nb_groupe' : nb_groupe,
            'nb_groupe_brouillon': nb_groupe_brouillon,
        }

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"status":"error", "message": "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
def ApiGetBrouillonGroupes(request):
    """Retourne la liste des groupes en mode brouillon pour une spécialité et promotion données."""
    if request.method == 'GET':
        specialite = request.GET.get('specialite')
        promo = request.GET.get('promo')

        if not specialite or not promo:
            return JsonResponse([], safe=False)

        groupes = Groupe.objects.filter(
            promotion__code=promo,
            specialite_id=specialite,
            etat='brouillon'
        ).values('id', 'nom', 'etat')

        return JsonResponse(list(groupes), safe=False)
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})




@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiAffectStudentToGroupe(request):
    if request.method == "POST":
        studentId = request.POST.get('studentId')
        groupId = request.POST.get('groupId')
        specialite = request.POST.get('specialite')


        if not studentId and not groupId:
            return JsonResponse({"status":"error",'message':'Informations manquantes'})

        try:
            groupe_obj = Groupe.objects.get(id=groupId)
            if groupe_obj.etat == 'inscription_terminee':
                return JsonResponse({"status": "error", "message": "Les inscriptions pour ce groupe sont terminées."})
        except Groupe.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Groupe non trouvé."})

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

@login_required(login_url="institut_app:login")
def AutreAffectationPage(request):
    return render(request, 'tenant_folder/scolarite/autre_affectation.html')

@login_required(login_url="institut_app:login")
def ApiParticipantsConfirmes(request):
    participants = Participant.objects.filter(is_confirmed_for_scolarite=True).select_related('prospect')
    data = []
    for p in participants:
        status = "Non affecté"
        groupe_nom = None
        
        if p.prospect:
            affectation = AffectationGroupe.objects.filter(etudiant=p.prospect).select_related('groupe').first()
            if affectation:
                status = "Affecté"
                groupe_nom = affectation.groupe.nom
        
        data.append({
            'id': p.id,
            'nom': p.nom,
            'prenom': p.prenom,
            'email': p.email,
            'telephone': p.telephone,
            'poste': p.poste,
            'scolarite_note': p.scolarite_note,
            'status_affectation': status,
            'groupe_nom': groupe_nom,
        })
    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
def ApiAffectParticipantToAcademicGroupe(request):
    if request.method == "POST":
        participant_id_single = request.POST.get('participant_id')
        participant_ids_bulk = request.POST.getlist('participant_ids[]')
        group_id = request.POST.get('groupId')

        if not group_id:
            return JsonResponse({'status': 'error', 'message': 'Groupe manquant'})

        ids_to_process = participant_ids_bulk if participant_ids_bulk else ([participant_id_single] if participant_id_single else [])

        if not ids_to_process:
            return JsonResponse({'status': 'error', 'message': 'Aucun participant sélectionné'})

        try:
            groupe = Groupe.objects.get(id=group_id)
        except Groupe.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Groupe non trouvé'})

        success_count = 0
        errors = []

        with transaction.atomic():
            for pid in ids_to_process:
                try:
                    participant = Participant.objects.get(id=pid)
                except Participant.DoesNotExist:
                    errors.append(f"Participant introuvable.")
                    continue

                # 1. Ensure/Create Prospect
                prospect = participant.prospect
                if not prospect:
                    from django.utils.text import slugify
                    base_email = participant.email or f"{slugify(participant.nom)}.{slugify(participant.prenom)}_{pid}@auto.com"
                    prospect = Prospets.objects.create(
                        nom=participant.nom,
                        prenom=participant.prenom,
                        email=base_email,
                        telephone=participant.telephone,
                        statut="convertit",
                        context="con",
                        type_prospect="particulier"
                    )
                    participant.prospect = prospect
                    participant.save()
                else:
                    if prospect.statut != "convertit":
                        prospect.statut = "convertit"
                        prospect.save()

                # 2. Ensure/Create Etudiant (Scolarité record)
                etudiant = Etudiant.objects.filter(relation=prospect).first()
                if not etudiant:
                    etudiant_by_email = Etudiant.objects.filter(email=prospect.email).first()
                    if etudiant_by_email:
                        etudiant = etudiant_by_email
                        etudiant.relation = prospect
                        etudiant.save()
                    else:
                        etudiant = Etudiant.objects.create(
                            relation=prospect,
                            email=prospect.email,
                            telephone=prospect.telephone or ""
                        )

                # 3. Assign to Groupe
                if not AffectationGroupe.objects.filter(etudiant=prospect, specialite=groupe.specialite).exists():
                    GroupeLine.objects.create(
                        student=prospect,
                        groupe=groupe
                    )
                    AffectationGroupe.objects.create(
                        etudiant=prospect,
                        groupe=groupe,
                        specialite=groupe.specialite
                    )
                    success_count += 1
                else:
                    errors.append(f"{participant.nom} est déjà affecté à cette spécialité.")

        if success_count > 0:
            if errors:
                return JsonResponse({'status': 'success', 'message': f'{success_count} participant(s) affecté(s). Quelques erreurs ignorées.'})
            return JsonResponse({'status': 'success', 'message': f'{success_count} participant(s) affecté(s) avec succès !'})
        else:
            return JsonResponse({'status': 'error', 'message': "Aucun participant n'a pu être affecté.", 'errors': errors})

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)