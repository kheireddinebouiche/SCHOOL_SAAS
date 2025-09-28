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
from institut_app.decorators import *
from t_crm.models import *
from datetime import datetime
from django.utils.timezone import now

@login_required(login_url="institut_app:login")
def ApiLoadConvertedProspects(request):

    clients = Prospets.objects.filter(statut="convertit").values('id', 'nom', 'prenom', 'email', 'telephone').annotate(
        total_paye=Sum('paiements__montant_paye',filter=Q(paiements__context="frais_f"))
    )

    promos = (Promos.objects.filter(etat="active").annotate(
            total_inscrit=Count('promo_fiche_voeux',filter=Q(promo_fiche_voeux__is_confirmed=True) & Q(promo_fiche_voeux__prospect__statut="convertit")) ,
            
            montant_total=Sum('promo_fiche_voeux__specialite__formation__prix_formation',filter=Q(promo_fiche_voeux__is_confirmed=True, promo_fiche_voeux__prospect__statut="convertit"))
            
        ).values('id','code','date_debut','date_fin','begin_year','end_year','session','total_inscrit','montant_total')
    )

    for promo in promos:
        total_paye = Paiements.objects.filter(promo_id=promo['id'],context="frais_f").filter(Q(prospect__statut="convertit") | Q(prospect__statut="annuler")).aggregate(total=Sum('montant_paye'))['total'] or 0

        # Total remboursé pour cette promo
        total_rembourse = Paiements.objects.filter(promo_id=promo['id'],is_refund=True).aggregate(total=Sum('montant_paye'))['total'] or 0

        # Montant payé effectif après remboursement
        promo['montant_paye'] = total_paye - total_rembourse

        # Autres calculs
        promo['montant_rembouser'] = total_rembourse
        promo['montant_echus'] = DuePaiements.objects.filter(is_done=False,promo_id=promo['id'],client__statut="convertit",date_echeance__lt=now().date()).aggregate(total=Sum('montant_restant'))['total'] or 0
        promo['montant_restant'] = DuePaiements.objects.filter( is_done=False,promo_id=promo['id'],client__statut="convertit").aggregate(total=Sum('montant_restant'))['total'] or 0
        promo['nombre_paiement'] = Paiements.objects.filter(promo_id=promo['id'], is_refund=False).count()

    data = {
        'clients': list(clients),
        'promos': list(promos),
    }
    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
def ApiStats(request):
    nombre_inscrit = Prospets.objects.filter(statut="convertit").count()
    nombre_paiement = Paiements.objects.filter(is_refund=False).count()

    montant_echu = (
        DuePaiements.objects.filter(date_echeance__lt=now().date(), is_done=False, is_annulated = False).aggregate(total=Sum('montant_restant'))['total'] or 0
    )

    paiement_attente = (
        DuePaiements.objects.filter(is_done=False, is_annulated=False).aggregate(total=Sum('montant_restant'))['total'] or 0
    )

    data = {
        'nombre_inscrit': nombre_inscrit,
        'nombre_paiement': nombre_paiement,
        'montant_echu': montant_echu,
        'paiement_attente': paiement_attente,
    }

    return JsonResponse({"data": data})


@login_required(login_url="institut_app:login")
def DetailsEcheancierClient(request, pk):
    context = {
        'pk': pk
    }
    return render(request, 'tenant_folder/comptabilite/echeancier/details-suivie-echeancier.html', context)

@login_required(login_url="institut_app:login")
@ajax_required
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


@login_required(login_url="institut_app:login")
def ApiGetClientEcheancier(request):
    if request.method == "GET":

        id_client= request.GET.get('id')

        obj = Prospets.objects.get(id = id_client)
        
        voeux = FicheDeVoeux.objects.filter(prospect=obj, is_confirmed=True).select_related("specialite").first()

        special_echeancier_data = []
        has_special_echeancier = False
        echeancier_state_approuvel = False
        due_paiement_data = []
        paiements_done_data = []
        has_due_paiement = False
        has_paiement = False
        has_pending_refund = False
        has_processed_refund = False
        is_appliced = False

        due_paiement = DuePaiements.objects.filter(client=obj).filter(Q(is_done=False) | Q(montant_restant__gt=0))

        if due_paiement.count() > 0:
            has_due_paiement = True
            total_initial = DuePaiements.objects.filter(client = obj).aggregate(total=Sum('montant_due'))['total'] or 0
            for i in due_paiement:
                due_paiement_data.append({
                    'id_due_paiement' : i.id,
                    'montant_due'  : i.montant_due,
                    'montant_restant' : i.montant_restant,
                    'label' : i.label,
                    'date_echeance' : i.date_echeance,
                })
        else:
            has_due_paiement = False
            due_paiement_data = []

        done_paiements = Paiements.objects.filter(prospect = obj)
        if done_paiements.count()>0:
            has_paiement = True
            total_paiement = done_paiements.filter(is_refund = False).aggregate(total=Sum('montant_paye'))['total'] or 0
            for i in done_paiements:
                paiements_done_data.append({
                    'montant_paye' : i.montant_paye,
                    'date_paiement' : i.date_paiement,
                    'label_paiements' : i.due_paiements.label if i.due_paiements and i.due_paiements.label else i.paiement_label,
                    'num' : i.num,
                    'mode_paiement' : i.get_mode_paiement_display(),
                    'reference_paiement' : i.reference_paiement,
                    'is_refund' : i.is_refund,
                })

        else:
            paiements_done_data = []

        obj_echeacncier_speial = EcheancierSpecial.objects.filter(prospect = obj).last()
        if obj_echeacncier_speial:
            line_echeancier_special = EcheancierPaiementSpecialLine.objects.filter(echeancier = obj_echeacncier_speial)
            echeancier_state_approuvel = obj_echeacncier_speial.is_approuved
            has_special_echeancier = True

            special_echeancier_data = []
            for i in line_echeancier_special:
                special_echeancier_data.append({
                    'id_echeancier_special' : i.id,
                    'taux' : i.taux,
                    'value' : i.value,
                    'date_echeancier' : i.date_echeancier,
                    'montant_tranche' : i.montant_tranche,
                })

        echeancier = EcheancierPaiement.objects.get(formation = voeux.specialite.formation, is_default=True)
        liste_echeancier = EcheancierPaiementLine.objects.filter(echeancier = echeancier)
        
        remiseObj = RemiseAppliquerLine.objects.filter(prospect = obj).last()

        if remiseObj and remiseObj.remise_appliquer:
            
            remise_appliquer = remiseObj.remise_appliquer.remise.taux
            is_approuved_remise = remiseObj.remise_appliquer.is_approuved
            reduction_type = remiseObj.remise_appliquer.remise.label
            id_reduction = remiseObj.remise_appliquer.id

            remiseDatas = {
                'valeur' : remise_appliquer,
                'remise_approuver' : is_approuved_remise,
                'type_remise' : reduction_type,
                'id_applied_reduction' : id_reduction,
            }

        else:
            remiseDatas = None

        echeancier_data=[]
        for i in liste_echeancier:
            echeancier_data.append({
                'id': i.id,
                'taux' : i.taux,
                'value' : i.value,
                'montant_tranche' : i.montant_tranche,
                'date_echeancier' : i.date_echeancier,
            })

        ## Changement de d'echeancier -- a remplacer une fois valider par l'utilisateur
        if obj_echeacncier_speial and obj_echeacncier_speial.is_validate:
            echeancier_data = special_echeancier_data
        
        refund = Rembourssements.objects.filter(client = obj).last()
        refund_data = []
        if refund:
            paiements = Paiements.objects.filter(prospect = obj, context = "frais_f" ).aggregate(total=Sum('montant_paye'))['total'] or 0
            if not refund.is_done:
                has_pending_refund = True
            else:
                has_processed_refund = True
            
            if refund.is_appliced:
                is_appliced = True

            refund_data = {
                'id' : refund.id,
                'motif_rembourssement' : refund.motif_rembourssement,
                'allowed_amount' : refund.allowed_amount,
                'etat' : refund.get_etat_display(),
                'etat_key' : refund.etat,
                'date_de_demande' : refund.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'date_de_traitement' : refund.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                'observation' : refund.observation, 
                'mode_rembourssement' : refund.mode_rembourssement,
                "mode_rembourssement_label" : refund.get_mode_rembourssement_display(),
                'montant_paye' : paiements,
                'is_appliced' : refund.is_appliced,
            }
        else:
            has_pending_refund = False
            refund_data = []
        

        user_data = {
            "demandeur_nom": obj.nom,
            "demandeur_prenom": obj.prenom,
            "statut_demandeur": obj.get_statut_display(),
            "demandeur_email" : obj.email,
            "demandeur_telephone" : obj.telephone,
            "demandeur_date_naissance" : obj.date_naissance if obj.date_naissance else "Non complété",
            "demandeur_adresse" : obj.adresse if obj.adresse else "Non complété",
            "demandeur_lieu_naissance" : obj.lieu_naissance if obj.date_naissance else "Non complété",
            "demandeur_date_inscription" : obj.created_at.strftime("%Y-%m-%d"),
            "client_id" : obj.id,
            "created_at": obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "client_id": obj.id,  # Add client ID to the response
        }

        voeux_data = {
            'specialite_id' : voeux.specialite.id,
            'specialite_label' : voeux.specialite.label,
            'promo' : voeux.promo.code,
            'prix_formation' : voeux.specialite.formation.prix_formation,
            'frais_inscription' : voeux.specialite.formation.frais_inscription,
        }

        total_solde = total_initial - total_paiement if has_due_paiement and has_paiement else 0

        data = {
            'user_data' : user_data,
            'voeux' : voeux_data,
            'echeancier' : list(echeancier_data),
            'remise' : remiseDatas,
            'has_special_echeancier' : has_special_echeancier,
            'id_echeancier_special' : obj_echeacncier_speial.id if obj_echeacncier_speial else None,
            'special_echeancier_line' : list(special_echeancier_data),
            'echeancier_special_state_approuvel' : echeancier_state_approuvel,
            "has_due_paiement" : has_due_paiement,
            "due_paiement_data" : due_paiement_data,
            "has_paiement" : has_paiement,
            "paiements_done_data" : paiements_done_data,
            "total_paiement" : total_paiement if has_paiement else 0,
            "total_initial" : total_initial if has_due_paiement else 0,
            "total_solde" : total_solde ,
            "has_pending_refund" : has_pending_refund,
            'has_processed_refund'  : has_processed_refund,
            'is_appliced' : is_appliced,
            "refund_data" : refund_data,
        }

        return JsonResponse(data, safe=False)
    

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiSaveRefundOperation(request):
    if request.method == "POST":
        id_client = request.POST.get('id_client')
        amount = request.POST.get('refund_amount')
        mode_rembourssement = request.POST.get('mode_rembourssement')
        id_refund = request.POST.get('id_refund')

        promo = FicheDeVoeux.objects.filter(prospect__id = id_client, is_confirmed=True).last()

        obj_refund = Rembourssements.objects.get(id = id_refund)
        refund_paiement = Paiements(
            prospect = Prospets.objects.get(id = id_client),
            paiement_label = "Rembourssement",
            montant_paye = amount,
            date_paiement = datetime.now(),
            mode_paiement = mode_rembourssement,
            is_refund = True,
            promo_id = promo.promo.id,
            refund_id = obj_refund,
        )

        refund_paiement.save()
        obj_refund.is_appliced = True
        obj_refund.save()

        change_client = Prospets.objects.get(id = id_client)
        change_client.statut = "annuler"
        change_client.save()

        DuePaiements.objects.filter(client_id = change_client, type="frais_f").update(is_annulated=True)

       
        return JsonResponse({"status" : "success"})
    else:
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="institut_app:login")
def ApiShowRefundTraiteResult(request):
    id_demande = request.GET.get('id_demande')
    rembourssement_obj = Rembourssements.objects.get(id=id_demande)
    client_paiement = (
        Paiements.objects.filter(prospect=rembourssement_obj.client, is_refund=False)
        .aggregate(total=Sum('montant_paye'))['total'] or 0
    )

    data = {
        'client__prenom': rembourssement_obj.client.prenom,
        'client__nom': rembourssement_obj.client.nom,
        'motif_rembourssement': rembourssement_obj.motif_rembourssement,
        'allowed_amount': rembourssement_obj.allowed_amount,
        'etat': rembourssement_obj.get_etat_display(),
        'is_done': rembourssement_obj.is_done,
        'observation': rembourssement_obj.observation,
        'mode_rembourssement': rembourssement_obj.mode_rembourssement,
        'is_appliced': rembourssement_obj.is_appliced,
        'created_at': rembourssement_obj.created_at.strftime("%d/%m/%Y") if rembourssement_obj.created_at else None,
        'updated_at': rembourssement_obj.updated_at.strftime("%d/%m/%Y") if rembourssement_obj.updated_at else None,
        'client_paiement' : client_paiement,
    }

    return JsonResponse({"data": data})
    