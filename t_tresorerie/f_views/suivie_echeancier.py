from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from t_crm.models import RemiseAppliquer, Prospets, FicheDeVoeux
from django.db.models import Q, Sum, F, Case, When, Value, CharField, Count


@login_required(login_url="institut_app:login")
def ApiLoadConvertedProspects(request):

    clients = Prospets.objects.filter(statut="convertit").values('id', 'nom', 'prenom', 'email', 'telephone').annotate(
        total_paye=Sum('paiements__montant_paye',filter=Q(paiements__context="frais_f"))
    )

    promos = (Promos.objects.filter(etat="active").annotate(
            total_inscrit=Count('promo_fiche_voeux',filter=Q(promo_fiche_voeux__is_confirmed=True) & Q(promo_fiche_voeux__prospect__statut="convertit")) ,
            montant_total=Sum('promo_fiche_voeux__specialite__formation__prix_formation',filter=Q(promo_fiche_voeux__is_confirmed=True))
        ).values('id','code','date_debut','date_fin','begin_year','end_year','session','total_inscrit','montant_total')
    )

    for promo in promos:
        promo['montant_paye'] = Paiements.objects.filter(promo_id=promo['id'],context="frais_f", prospect__statut="convertit").aggregate(total=Sum('montant_paye'))['total'] or 0
        

    data = {
        'clients': list(clients),
        'promos': list(promos),
    }
    return JsonResponse(data, safe=False)


@login_required(login_url="institut_app:login")
def DetailsEcheancierClient(request, pk):
    context = {
        'client_id': pk
    }
    return render(request, 'tenant_folder/comptabilite/echeancier/details-suivie-echeancier.html', context)

def ApiGetLunchedSpec(request):
    if request.method == "GET":
        id_promo = request.GET.get("id_promo")

       
        liste = (
            FicheDeVoeux.objects.filter(promo_id=id_promo, is_confirmed=True).values("specialite__id", "specialite__label")
            .annotate(
                total_student=Count( "prospect",filter=Q(prospect__statut="convertit"),distinct=True)
            ).order_by("specialite__label")
        )


        return JsonResponse(list(liste), safe=False)

