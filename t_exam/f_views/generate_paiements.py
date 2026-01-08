from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import ModelBuilltins, BuiltinTypeNote, BuiltinSousNote
from t_formations.models import Formation, Modules
from t_timetable.models import Salle
from t_exam.models import *
from t_groupe.models import Groupe,GroupeLine
from django.db import transaction, IntegrityError
import json
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from t_tresorerie.models import DuePaiements


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiGenerateDuePaiements(request):
    if request.method == "POST":
        commisison_result_id = request.POST.get('commission_result_id')
        
        if not commisison_result_id:
            return JsonResponse({"status":"error","message":"ID de la commission résultat manquant."})

        obj = CommisionResult.objects.get(id = commisison_result_id)
        montant_paiement = obj.commission.promo.prix_rachat_credit
        promo = obj.commission.promo
        modules  = obj.modules.count()
        montant_total = modules * montant_paiement
        obj.is_generated = True
        obj.save()
        
        try:
            nouveau_paiement = DuePaiements(
                client_id = obj.etudiants.id,
                label = "Rachat de crédit",
                montant_due = montant_total,
                date_echeance = obj.commission.updated_at,
                promo = promo,
                type = 'rach',
                
            )
            nouveau_paiement.save()

            return JsonResponse({"status":'success','message' : "Paiment enregistrer avec success"})

        except Exception as e:
            return JsonResponse({"status":"error",'message':str(e)})
    else:
        return JsonResponse({"status":"error",'message':'Méthode non autorisée.'})




   