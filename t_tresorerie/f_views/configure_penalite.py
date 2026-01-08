from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import chain
from datetime import datetime
from django.db.models import F, Value,CharField, Q
from django.db.models.functions import Coalesce
from itertools import chain
from django.db.models.functions import Concat



@login_required(login_url="institut_app:login")
def PageConfPenalite(request):
    return render(request,'tenant_folder/comptabilite/conf/liste_promo.html')


@login_required(login_url="institut_app:login")
def ApiLoadPromo(request):
    if request.method == "GET":
        promo = Promos.objects.all()
        data = []
        for i in promo:
            data.append({
                'id': i.id,
                'begin_year' : i.begin_year,
                'end_year' : i.end_year,
                'session' : i.get_session_display(),
                'prix_rachat_credit' : i.prix_rachat_credit,
                'penalite_retard' : i.penalite_retard,
            })
        return JsonResponse(data, safe=False)

    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
def ApiUpdatePromoConfig(request):
    if request.method == 'POST':
        try:
            promo_id = request.POST.get('promo_id')
            prix_rachat_credit = request.POST.get('prix_rachat_credit')
            penalite_retard = request.POST.get('penalite_retard')

            promo = Promos.objects.get(id=promo_id)
            promo.prix_rachat_credit = Decimal(prix_rachat_credit)
            promo.penalite_retard = Decimal(penalite_retard)
            promo.save()

            return JsonResponse({'status': 'success', 'message': 'Promotion mise à jour avec succès.'})
        except Promos.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Promotion non trouvée.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)