from t_timetable.models import Timetable
from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import *
from ..forms import *
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from t_etudiants.models import *
from t_groupe.models import *
from t_formations.models import Promos
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required



@login_required(login_url="institut_app:login")
def PageCommission(request):
    commissions = Commissions.objects.all()
    all_promotions = Promos.objects.all()
    context = {
        'commissions': commissions,
        'all_promotions': all_promotions
    }
    return render(request, 'tenant_folder/exams/commission/liste_des_commissions.html', context)


@login_required(login_url="institut_app:login")
def ApiListeDesCommission(request):
    if request.method == "GET":
        commissions = Commissions.objects.all()
        data = []
        for commission in commissions:
            data.append({
                'id': commission.id,
                'nom': commission.label,
                'description': commission.criters
            })
        return JsonResponse({"status": "success", "data": data})
    else:
        return JsonResponse({"status": "error"})

from django.contrib import messages

@login_required(login_url="institut_app:login")
@transaction.atomic
def NouvelleCommission(request):
    form = CommissionForm()
    if request.method == "POST":
        form = CommissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La commision à été crée avec succès")
            return redirect('t_exam:PageCommission')
        else:
            # Afficher les erreurs de validation spécifiques
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")

    context = {
        'form' : form,
    }
    return render(request, 'tenant_folder/exams/commission/nouvelle_commission.html', context)

@login_required(login_url="institut_app:login")
def DetailsCommission(request, pk):
    obj = Commissions.objects.get(id = pk)
   
    context = {
        'commission' : obj,
        'groupes' : obj.groupes.all()
    }
    return render(request, "tenant_folder/exams/commission/details_commission.html", context)

@login_required(login_url="institut_app:login")
@transaction.atomic
def UpdateCommission(request, pk):
    commission = Commissions.objects.get(id = pk)
    form = CommissionForm(instance = commission)
    if request.method == "POST":
        form = CommissionForm(request.POST, instance = commission)
        if form.is_valid():
            form.save()
            messages.success(request,"Les données de la commission ont été mis à jours avec succès")
            return redirect('t_exam:PageCommission')
        else:
            messages.error(request,"Une erreur c'est produite lors du traitement de la requete")
            return redirect('t_exam:UpdateCommission')

    context = {
        'form' : form,
        'commission' : commission
    }
    return render(request,'tenant_folder/exams/commission/update_commission.html', context)

@login_required(login_url="institut_app:login")
def validate_commission(request):
    if request.method == "POST":
        commissionId = request.POST.get('commissionId')
        comment = request.POST.get('comment', '')

        if not commissionId:
            return JsonResponse({"status" : "error",'message' : "Informations manquante"})

        try:

            commission = Commissions.objects.get(id=commissionId)
            
            commission.is_validated = True
            commission.comment = comment
            commission.save()
            messages.success(request, "La commission a été valider avec succès")
            return JsonResponse({"status": "success","message": "La commission a été validée avec succès"})
        
        except Commissions.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "La commission n'existe pas"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Une erreur est survenue: {str(e)}"
            })
    else:
        return JsonResponse({
            "status": "error",
            "message": "Méthode non autorisée"
        })

@login_required(login_url="institut_app:login")
def delete_commission(request, pk):
    if request.method == "POST":
        try:
            commission = Commissions.objects.get(id=pk)

            # Supprimer la commission
            commission.delete()

            return JsonResponse({
                "status": "success",
                "message": "La commission a été supprimée avec succès"
            })
        except Commissions.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "La commission n'existe pas"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Une erreur est survenue: {str(e)}"
            })
    else:
        return JsonResponse({
            "status": "error",
            "message": "Méthode non autorisée"
        })
    
@login_required(login_url="institut_app:login")
def ApiGetGroupeDetails(request):
    if request.method == "GET":
        groupe_id = request.GET.get("id")

        if not groupe_id:
            return JsonResponse({"status": "error", "message": "groupe_id manquant"})
        semester  = Timetable.objects.filter(groupe_id=groupe_id, status="enc").last()
        if not semester:
            return JsonResponse({"status": "error", "message": "Le semestre n'est pas encours"})
        historiques = (
            HistoriqueAbsence.objects
            .filter(ligne_presence__registre__groupe_id=groupe_id, ligne_presence__registre__semestre=semester.semestre, etat=False)
            .select_related(
                'etudiant',
                'ligne_presence__module',
                'ligne_presence__registre'
            )
        )
        
        result = {}

        for h in historiques:
            etudiant_id = h.etudiant.id
            
            if etudiant_id not in result:
                result[etudiant_id] = {
                    "etudiant": {
                        "id": h.etudiant.id,
                        "nom": h.etudiant.nom,
                        "prenom": h.etudiant.prenom,
                        "matricule" : h.etudiant.matricule_interne,
                        "etat": h.etat,
                        
                    },
                    "historique": [],
                    "historique_ids": [],
                }

            # Fusion de l'historique JSON
            result[etudiant_id]["historique_ids"].append(h.id)
            result[etudiant_id]["historique"].extend(h.historique)

        return JsonResponse(list(result.values()), safe=False)

    return JsonResponse({"status": "error"})

@login_required(login_url="institut_app:login")
def ApiGetCommissionResults(request):
    if request.method == "GET":
        id_commission = request.GET.get('idCommission')
        results = (CommisionResult.objects
                   .filter(commission_id = id_commission)
                   .select_related('etudiants')
                   .prefetch_related('modules'))
        
        try:
             commission = Commissions.objects.get(id=id_commission)
        except Commissions.DoesNotExist:
             return JsonResponse({"status": "error", "message": "Commission introuvable"})
        
        data = []
        for r in results:
            data.append({
                "id": r.id,
                "nom": r.etudiants.nom,
                "prenom": r.etudiants.prenom,
                "modules": list(
                    r.modules.values('id', 'code', 'label')
                ),
                "result": r.get_result_display(),
                "commentaire": r.commentaire,
                "is_generated": r.is_generated,
                "group_name": GroupeLine.objects.filter(student=r.etudiants, groupe__in=commission.groupes.all()).first().groupe.nom if GroupeLine.objects.filter(student=r.etudiants, groupe__in=commission.groupes.all()).exists() else "N/A"
            })
        
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"status":"error"})
    
@login_required(login_url="institut_app:login")
@transaction.atomic
def close_commission(request, pk):
    from ..models import SessionExam, SessionExamLine
    from t_timetable.models import Timetable

    obj = Commissions.objects.get(id=pk)

    if not pk:
        return JsonResponse({"status": "error", 'message': "Information manquante"})

    # Récupérer les données de planification d'examen si elles existent
    planifier_session = request.POST.get('planifier_session')
    session_nom = request.POST.get('session_nom')
    type_session = request.POST.get('type_session')
    date_debut = request.POST.get('date_debut')
    date_fin = request.POST.get('date_fin')

    obj.is_closed = True

    try:
        obj.save()

        # Si la planification de session est demandée, créer les enregistrements
        if planifier_session == 'true':
            # Convertir le type de session pour correspondre aux choix du modèle
            type_session_mapping = {
                'ordinaire': 'normal',
                'rattrapage': 'rattrapage'
            }
            mapped_type_session = type_session_mapping.get(type_session, 'normal')

            # Créer la session d'examen
            session_exam = SessionExam.objects.create(
                label=session_nom,
                code=session_nom,
                type_session=mapped_type_session,
                date_debut=date_debut,
                date_fin=date_fin,
                commission=obj
            )

            # Pour chaque groupe de la commission, créer une ligne de session d'examen
            for groupe in obj.groupes.all():
                # Récupérer le semestre du groupe à partir du modèle Timetable
                timetable = Timetable.objects.filter(groupe=groupe, status="enc").first()
                semestre = timetable.semestre if timetable else None

                # Créer la ligne de session d'examen
                session_exam_line = SessionExamLine.objects.create(
                    session=session_exam,
                    groupe=groupe,
                    semestre=semestre
                )

                # Extraire les données de CommissionResult et créer les ExamPlanification
                # Récupérer les étudiants appartenant au groupe
                from t_groupe.models import GroupeLine
                etudiants_du_groupe = GroupeLine.objects.filter(groupe=groupe).values_list('student', flat=True)

                commission_results = CommisionResult.objects.filter(
                    commission=obj,
                    etudiants__in=etudiants_du_groupe  # Filtrer par étudiants du groupe
                ).select_related('etudiants').prefetch_related('modules')

                # Créer une ExamPlanification pour chaque combinaison étudiant-module-type d'examen
                for result in commission_results:
                    # Déterminer le type d'examen basé sur le résultat
                    type_mapping = {
                        'exam': 'normal',
                        'rach': 'rachat',
                        'ajou': 'rattrage'
                    }

                    type_examen = type_mapping.get(result.result, 'normal')

                    # Pour chaque module dans le résultat, créer une planification
                    # Utiliser distinct() pour éviter les doublons
                    for module in result.modules.all().distinct():
                        # Vérifier si une ExamPlanification existe déjà pour cette combinaison
                        from ..models import ExamPlanification
                        exam_planification, created = ExamPlanification.objects.get_or_create(
                            exam_line=session_exam_line,
                            module=module,
                            type_examen=type_examen,
                            defaults={
                                # Les champs date, salle, heures et mode_examination sont laissés vides
                                # comme demandé
                            }
                        )
                        # Pour déboguer, on peut voir ce qui est créé
                        if created:
                            print(f"Création d'ExamPlanification: Etudiant={result.etudiants}, Module={module}, Type={type_examen}")
                        else:
                            print(f"ExamPlanification existe déjà: Etudiant={result.etudiants}, Module={module}, Type={type_examen}")

        return JsonResponse({'status' : 'success', 'message' : "Suppression effectuée avec succès"})
    except Exception as e:
        return JsonResponse({"status": "error", 'message': str(e)})