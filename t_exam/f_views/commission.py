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
def validate_commission(request, pk):
    if request.method == "POST":
        try:
            commission = Commissions.objects.get(id=pk)
            comment = request.POST.get('comment', '')

            # Valider la commission
            commission.is_validated = True
            commission.save()

            return JsonResponse({
                "status": "success",
                "message": "La commission a été validée avec succès"
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

        historiques = (
            HistoriqueAbsence.objects
            .filter(ligne_presence__registre__groupe_id=groupe_id, etat=False)
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

    else:
        return JsonResponse({"status":"error"})
    
@login_required(login_url="institut_app:login")
@transaction.atomic
def close_commission(request, pk):
    obj = Commissions.objects.get(id = pk)
    pass