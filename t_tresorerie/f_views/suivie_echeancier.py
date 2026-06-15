from institut_app.decorators import module_permission_required
from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from t_crm.models import RemiseAppliquer, Prospets, FicheDeVoeux, UserActionLog
from django.db.models import Q, Sum, F, Case, When, Value, CharField, Count
from institut_app.decorators import *
from t_crm.models import *
from datetime import datetime
from django.utils.timezone import now

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiLoadConvertedProspects(request):

    # Total payé par étudiant (tous contextes confondus, hors remboursements)
    clients = Prospets.objects.filter(statut="convertit").values('id', 'nom', 'prenom', 'email', 'telephone', 'is_double').annotate(
        total_paye=Sum('paiements__montant_paye', filter=Q(paiements__is_refund=False))
    )

    promos = list(Promos.objects.filter(etat="active").values('id', 'code', 'begin_year', 'end_year', 'session'))

    for promo in promos:
        # Total à payer : Somme des montants dûs de tous les étudiants convertis de la promo
        promo['montant_total'] = DuePaiements.objects.filter(
            promo_id=promo['id'],
            client__statut="convertit",
            is_annulated=False
        ).aggregate(total=Sum('montant_due'))['total'] or 0

        # Total payé : Somme de tous les paiements (hors remboursements) 
        # On inclut les paiements directement liés à la promo OU liés via DuePaiements de la promo
        payments_qs = Paiements.objects.filter(is_refund=False).filter(
            Q(promo_id=promo['id']) | Q(due_paiements__promo_id=promo['id'])
        ).filter(
            Q(prospect__statut="convertit") | Q(prospect__statut="annuler")
        ).distinct()
        
        total_paye = payments_qs.aggregate(total=Sum('montant_paye'))['total'] or 0

        # Total remboursé pour cette promo calculé dynamiquement depuis les Rembourssements réels appliqués
        prospect_ids = list(payments_qs.values_list('prospect_id', flat=True).distinct())
        if prospect_ids:
            total_rembourse = Rembourssements.objects.filter(
                client_id__in=prospect_ids,
                is_appliced=True
            ).aggregate(total=Sum('allowed_amount'))['total'] or 0
        else:
            total_rembourse = 0

        # Montant payé effectif après remboursement
        promo['montant_paye'] = float(total_paye) - float(total_rembourse)

        # Autres calculs
        promo['montant_rembouser'] = float(total_rembourse)
        
        # Échus : Montant restant des échéances dépassées non payées (is_done=False)
        promo['montant_echu'] = DuePaiements.objects.filter(
            is_done=False,
            is_annulated=False,
            promo_id=promo['id'],
            client__statut="convertit",
            date_echeance__lt=now().date()
        ).aggregate(total=Sum('montant_restant'))['total'] or 0

        # Reste à payer : Total des montants restants (futurs + échus)
        promo['montant_restant'] = DuePaiements.objects.filter(
            is_done=False,
            is_annulated=False,
            promo_id=promo['id'],
            client__statut="convertit"
        ).aggregate(total=Sum('montant_restant'))['total'] or 0

        promo['nombre_paiement'] = payments_qs.count()
        
        # Nombre d'inscrits convertis
        promo['total_inscrit'] = Prospets.objects.filter(
            statut="convertit",
            duepaiements__promo_id=promo['id']
        ).distinct().count() or FicheDeVoeux.objects.filter(promo_id=promo['id'], is_confirmed=True, prospect__statut="convertit").count()

    data = {
        'clients': list(clients),
        'promos': list(promos),
    }
    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiStats(request):
    nombre_inscrit = Prospets.objects.filter(statut="convertit").count()
    nombre_paiement = Paiements.objects.filter(is_refund=False, prospect__statut="convertit").count()

    montant_echu = (
        DuePaiements.objects.filter(date_echeance__lt=now().date(), is_done=False, is_annulated = False, client__statut="convertit").aggregate(total=Sum('montant_restant'))['total'] or 0
    )

    paiement_attente = (
        DuePaiements.objects.filter(is_done=False, is_annulated=False, client__statut="convertit").aggregate(total=Sum('montant_restant'))['total'] or 0
    )

    data = {
        'nombre_inscrit': nombre_inscrit,
        'nombre_paiement': nombre_paiement,
        'montant_echu': montant_echu,  # Correctly labeled for overdue
        'paiement_attente': paiement_attente,  # Correctly labeled for all pending
    }

    return JsonResponse({"data": data})


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def DetailsEcheancierClient(request, pk):
    context = {
        'pk': pk,
        'payment_types': PaymentType.objects.all()
    }
    return render(request, 'tenant_folder/comptabilite/echeancier/details-suivie-echeancier.html', context)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def DetailsEcheancierClientDouble(request, pk):
    context = {
        'pk' : pk,
        'payment_types': PaymentType.objects.all()
    }
    return render(request,'tenant_folder/comptabilite/echeancier/details-suivie-echeancier-double.html', context)



@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetLunchedSpec(request):
    if request.method == "GET":
        id_promo = request.GET.get("id_promo")

        if not id_promo:
            return JsonResponse({"status": "error", "message": "id_promo manquant"})

        # 🔹 Spécialités normales
        simple_specs = (
            FicheDeVoeux.objects
            .filter(promo_id=id_promo, is_confirmed=True)
            .values(
                "specialite__id",
                "specialite__label"
            )
            .annotate(
                total_student=Count(
                    "prospect",
                    filter=Q(prospect__statut="convertit"),
                    distinct=True
                )
            )
            .order_by("specialite__label")
        )

        simple_data = [
            {
                "id": s["specialite__id"],
                "label": s["specialite__label"],
                "type": "simple",
                "total_student": s["total_student"]
            }
            for s in simple_specs
        ]

        # 🔹 Spécialités double diplomation
        double_specs = (
            FicheVoeuxDouble.objects
            .filter(promo_id=id_promo, is_confirmed=True)
            .values(
                "specialite__id",
                "specialite__label"
            )
            .annotate(
                total_student=Count(
                    "prospect",
                    filter=Q(prospect__statut="convertit"),
                    distinct=True
                )
            )
            .order_by("specialite__label")
        )

        double_data = [
            {
                "id": d["specialite__id"],
                "label": d["specialite__label"],
                "type": "double",
                "total_student": d["total_student"]
            }
            for d in double_specs
        ]

        # 🔹 Fusion finale
        result = simple_data + double_data

        return JsonResponse(result, safe=False)

from t_groupe.models import GroupeLine

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetClientEcheancier(request):
    if request.method == "GET":

        id_client= request.GET.get('id')

        obj = Prospets.objects.get(id = id_client)
        
        voeux = FicheDeVoeux.objects.filter(prospect=obj, is_confirmed=True).select_related("specialite").first()
        

        echeancierId = EcheancierPaiement.objects.filter(formation_id = voeux.specialite.formation.id, model__promo = voeux.promo).first()

        try:
            groupe = GroupeLine.objects.filter(student_id = id_client).first()
            
            groupe_data = {
                'id' : groupe.groupe.id,
                'nom' : groupe.groupe.nom,
                'semestre' : groupe.groupe.semestre,
            }
        except:
            groupe_data = {
                'id' : None,
                'nom' : None,
                'semestre' : None,
            }

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

        # Toutes les tranches (payées + non payées) pour l'engagement PDF
        all_due_paiements_qs = DuePaiements.objects.filter(client=obj, is_annulated=False).order_by('date_echeance')
        all_due_paiement_data = []
        for i in all_due_paiements_qs:
            all_due_paiement_data.append({
                'id_due_paiement': i.id,
                'montant_due': float(i.montant_due),
                'montant_restant': float(i.montant_restant),
                'label': i.label,
                'date_echeance': str(i.date_echeance),
                'is_done': i.is_done,
            })

        if due_paiement.count() > 0:
            has_due_paiement = True
            total_initial = DuePaiements.objects.filter(client = obj, is_annulated=False).aggregate(total=Sum('montant_due'))['total'] or 0
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

        done_paiements = Paiements.objects.filter(prospect = obj).order_by('due_paiements__date_echeance', 'id')
        if done_paiements.count()>0:
            has_paiement = True
            total_paiement = done_paiements.filter(is_refund = False).aggregate(total=Sum('montant_paye'))['total'] or 0
            for i in done_paiements:
                # Calculate the remaining balance of the tranche immediately after this payment
                if i.due_paiements:
                    prev_total = Paiements.objects.filter(
                        due_paiements=i.due_paiements,
                        id__lte=i.id,
                        is_refund=False
                    ).aggregate(total=Sum('montant_paye'))['total'] or 0
                    montant_restant_val = float(i.due_paiements.montant_due - prev_total)
                else:
                    montant_restant_val = None

                paiements_done_data.append({
                    'id': i.id,
                    'montant_paye' : i.montant_paye,
                    'date_paiement' : i.date_paiement,
                    'label_paiements' : i.due_paiements.label if i.due_paiements and i.due_paiements.label else i.paiement_label,
                    'num' : i.num,
                    'mode_paiement' : i.get_mode_paiement_display(),
                    'mode_paiement_code' : i.mode_paiement,
                    'reference_paiement' : i.reference_paiement,
                    'is_refund' : i.is_refund, 'facture_num' : i.facture.num_facture if i.facture else None, 'facture_id' : i.facture.id if i.facture else None, 'entite_id': i.entite.id if i.entite else None,
                    'montant_restant': montant_restant_val,
                    'has_printed_quittance': i.has_printed_quittance,
                    'quittance_printed_at': i.quittance_printed_at.strftime("%Y-%m-%d %H:%M:%S") if i.quittance_printed_at else None,
                    'quittance_printed_by': i.quittance_printed_by,
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

        echeancier = EcheancierPaiement.objects.filter(formation = voeux.specialite.formation, is_default=True, model__promo = voeux.promo).first()
        liste_echeancier = EcheancierPaiementLine.objects.filter(echeancier = echeancier)
        
        remiseObj = RemiseAppliquerLine.objects.filter(prospect = obj).last()

        if remiseObj and remiseObj.remise_appliquer:
            
            remise = remiseObj.remise_appliquer.remise
            remise_appliquer = remise.montant if remise.is_value else remise.taux
            is_approuved_remise = remiseObj.remise_appliquer.is_approuved
            reduction_type = remise.label
            id_reduction = remiseObj.remise_appliquer.id

            remiseDatas = {
                'valeur' : remise_appliquer,
                'is_value' : remiseObj.remise_appliquer.remise.is_value,
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
            "has_financial_alert": obj.has_financial_alert,
            "financial_alert_message": obj.financial_alert_message,
            "can_disable_alert": obj.financial_alert_user == request.user if obj.has_financial_alert else True,
            "alert_user_name": f"{obj.financial_alert_user.first_name} {obj.financial_alert_user.last_name}" if obj.financial_alert_user else None,
            "has_printed_engagement": obj.has_printed_engagement,
            "engagement_printed_at": obj.engagement_printed_at.strftime("%Y-%m-%d %H:%M:%S") if obj.engagement_printed_at else None,
            "engagement_printed_by": obj.engagement_printed_by,
        }

        # Extraction des frais d'inscription depuis DuePaiements
        frais_inscription_due = DuePaiements.objects.filter(client=obj, label__icontains="inscription").first()
        frais_inscription_val = float(frais_inscription_due.montant_due) if frais_inscription_due else voeux.specialite.formation.frais_inscription

        voeux_data = {
            'specialite_id' : voeux.specialite.id,
            'specialite_label' : voeux.specialite.label,
            'formation' : voeux.specialite.formation.nom,
            'formation_label' : voeux.specialite.formation.nom,
            'entite' : voeux.specialite.formation.entite_legal.designation,
            'entite_ville' : voeux.specialite.formation.entite_legal.ville,
            'promo' : voeux.promo.code,
            'prix_formation' : voeux.specialite.prix,
            'frais_inscription' : frais_inscription_val,
            'logo_header' : voeux.specialite.formation.entite_legal.entete_logo.url if voeux.specialite.formation.entite_legal.entete_logo else None,
            'logo_footer' : voeux.specialite.formation.entite_legal.pied_page_logo.url if voeux.specialite.formation.entite_legal.pied_page_logo else None,
        }

        total_solde = total_initial - total_paiement if has_due_paiement and has_paiement else 0

        data = {
            'user_data' : user_data,
            'voeux' : voeux_data,
            'echeancier' : list(echeancier_data),
            'groupe' : groupe_data,
            'remise' : remiseDatas,
            'has_special_echeancier' : has_special_echeancier,
            'id_echeancier_special' : obj_echeacncier_speial.id if obj_echeacncier_speial else None,
            'special_echeancier_line' : list(special_echeancier_data),
            'echeancier_special_state_approuvel' : echeancier_state_approuvel,
            "has_due_paiement" : has_due_paiement,
            "due_paiement_data" : due_paiement_data,
            "all_due_paiement_data" : all_due_paiement_data,
            "has_paiement" : has_paiement,
            "paiements_done_data" : paiements_done_data,
            "total_paiement" : total_paiement if has_paiement else 0,
            "total_initial" : total_initial if has_due_paiement else 0,
            "total_solde" : total_solde ,
            "has_pending_refund" : has_pending_refund,
            'has_processed_refund'  : has_processed_refund,
            'is_appliced' : is_appliced,
            "refund_data" : refund_data,
            "has_invoice": done_paiements.filter(is_refund=False, facture__isnull=False).exists() if has_paiement else False,
        }

        return JsonResponse(data, safe=False)
    
@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetClientEcheancierDouble(request):
    if request.method == "GET":

        id_client= request.GET.get('id')

        obj = Prospets.objects.get(id = id_client)
        
        voeux = FicheVoeuxDouble.objects.filter(prospect=obj, is_confirmed=True).select_related("specialite").first()
        

        echeancierId = EcheancierPaiement.objects.filter(formation_double_id = voeux.specialite.id, model__promo = voeux.promo).first()

        groupe = GroupeLine.objects.filter(student_id = id_client).first()

        groupe_data = {}
        
        if groupe:
            groupe_data = {
                'id' : groupe.groupe.id,
                'nom' : groupe.groupe.nom,
                'semestre' : groupe.groupe.semestre,
            }


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

        # Toutes les tranches (payées + non payées) pour l'engagement PDF
        all_due_paiements_qs = DuePaiements.objects.filter(client=obj, is_annulated=False).order_by('date_echeance')
        all_due_paiement_data = []
        for i in all_due_paiements_qs:
            all_due_paiement_data.append({
                'id_due_paiement': i.id,
                'montant_due': float(i.montant_due),
                'montant_restant': float(i.montant_restant),
                'label': i.label,
                'date_echeance': str(i.date_echeance),
                'is_done': i.is_done,
            })

        if due_paiement.count() > 0:
            has_due_paiement = True
            total_initial = DuePaiements.objects.filter(client = obj, is_annulated=False).aggregate(total=Sum('montant_due'))['total'] or 0
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

        done_paiements = Paiements.objects.filter(prospect = obj).order_by('due_paiements__date_echeance', 'id')
        if done_paiements.count()>0:
            has_paiement = True
            total_paiement = done_paiements.filter(is_refund = False).aggregate(total=Sum('montant_paye'))['total'] or 0
            for i in done_paiements:
                # Calculate the remaining balance of the tranche immediately after this payment
                if i.due_paiements:
                    prev_total = Paiements.objects.filter(
                        due_paiements=i.due_paiements,
                        id__lte=i.id,
                        is_refund=False
                    ).aggregate(total=Sum('montant_paye'))['total'] or 0
                    montant_restant_val = float(i.due_paiements.montant_due - prev_total)
                else:
                    montant_restant_val = None

                paiements_done_data.append({
                    'id': i.id,
                    'montant_paye' : i.montant_paye,
                    'date_paiement' : i.date_paiement,
                    'label_paiements' : i.due_paiements.label if i.due_paiements and i.due_paiements.label else i.paiement_label,
                    'num' : i.num,
                    'mode_paiement' : i.get_mode_paiement_display(),
                    'mode_paiement_code' : i.mode_paiement,
                    'reference_paiement' : i.reference_paiement,
                    'is_refund' : i.is_refund, 'facture_num' : i.facture.num_facture if i.facture else None, 'facture_id' : i.facture.id if i.facture else None, 'entite_id': i.entite.id if i.entite else None,
                    'montant_restant': montant_restant_val,
                    'has_printed_quittance': i.has_printed_quittance,
                    'quittance_printed_at': i.quittance_printed_at.strftime("%Y-%m-%d %H:%M:%S") if i.quittance_printed_at else None,
                    'quittance_printed_by': i.quittance_printed_by,
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

        echeancier = EcheancierPaiement.objects.filter(formation_double = voeux.specialite, is_default=True, model__promo = voeux.promo).first()
        liste_echeancier = EcheancierPaiementLine.objects.filter(echeancier = echeancier)
        
        remiseObj = RemiseAppliquerLine.objects.filter(prospect = obj).last()

        if remiseObj and remiseObj.remise_appliquer:
            
            remise = remiseObj.remise_appliquer.remise
            remise_appliquer = remise.montant if remise.is_value else remise.taux
            is_approuved_remise = remiseObj.remise_appliquer.is_approuved
            reduction_type = remise.label
            id_reduction = remiseObj.remise_appliquer.id

            remiseDatas = {
                'valeur' : remise_appliquer,
                'is_value' : remiseObj.remise_appliquer.remise.is_value,
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
            "has_financial_alert": obj.has_financial_alert,
            "financial_alert_message": obj.financial_alert_message,
            "can_disable_alert": obj.financial_alert_user == request.user if obj.has_financial_alert else True,
            "alert_user_name": f"{obj.financial_alert_user.first_name} {obj.financial_alert_user.last_name}" if obj.financial_alert_user else None,
            "has_printed_engagement": obj.has_printed_engagement,
            "engagement_printed_at": obj.engagement_printed_at.strftime("%Y-%m-%d %H:%M:%S") if obj.engagement_printed_at else None,
            "engagement_printed_by": obj.engagement_printed_by,
        }

        # Extraction des frais d'inscription depuis DuePaiements
        frais_inscription_due = DuePaiements.objects.filter(client=obj, label__icontains="inscription").first()
        frais_inscription_val = float(frais_inscription_due.montant_due) if frais_inscription_due else voeux.specialite.frais_inscription

        voeux_data = {
            'specialite_id' : voeux.specialite.id,
            'specialite_label' : voeux.specialite.label,
            'formation' : f"{voeux.specialite.specialite1.label} / {voeux.specialite.specialite2.label}" if voeux.specialite and voeux.specialite.specialite1 and voeux.specialite.specialite2 else "Double Diplomation",
            'promo' : voeux.promo.code,
            'prix_formation' : (voeux.specialite.prix_spec1 or 0) + (voeux.specialite.prix_spec2 or 0) if voeux.specialite else 0,
            'frais_inscription' : frais_inscription_val,
            'logo_header' : echeancierId.entite.entete_logo.url if echeancierId and echeancierId.entite and echeancierId.entite.entete_logo else None,
            'logo_footer' : echeancierId.entite.pied_page_logo.url if echeancierId and echeancierId.entite and echeancierId.entite.pied_page_logo else None,
            'entite' : echeancierId.entite.designation if echeancierId and echeancierId.entite else "Double Diplomation",
            'entite_ville' : echeancierId.entite.ville if echeancierId and echeancierId.entite else "",
        }

        total_solde = total_initial - total_paiement if has_due_paiement and has_paiement else 0

        data = {
            'user_data' : user_data,
            'voeux' : voeux_data,
            'echeancier' : list(echeancier_data),
            'groupe' : groupe_data,
            'remise' : remiseDatas,
            'has_special_echeancier' : has_special_echeancier,
            'id_echeancier_special' : obj_echeacncier_speial.id if obj_echeacncier_speial else None,
            'special_echeancier_line' : list(special_echeancier_data),
            'echeancier_special_state_approuvel' : echeancier_state_approuvel,
            "has_due_paiement" : has_due_paiement,
            "due_paiement_data" : due_paiement_data,
            "all_due_paiement_data" : all_due_paiement_data,
            "has_paiement" : has_paiement,
            "paiements_done_data" : paiements_done_data,
            "total_paiement" : total_paiement if has_paiement else 0,
            "total_initial" : total_initial if has_due_paiement else 0,
            "total_solde" : total_solde ,
            "has_pending_refund" : has_pending_refund,
            'has_processed_refund'  : has_processed_refund,
            'is_appliced' : is_appliced,
            "refund_data" : refund_data,
            "has_invoice": done_paiements.filter(is_refund=False, facture__isnull=False).exists() if has_paiement else False,
        }

        return JsonResponse(data, safe=False)
    

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'add')
def ApiSaveRefundOperation(request):
    if request.method == "POST":
        id_client = request.POST.get('id_client')
        amount = request.POST.get('refund_amount')
        amount = str(amount).replace(',', '.') if amount else 0
        mode_rembourssement = request.POST.get('mode_rembourssement')
        id_refund = request.POST.get('id_refund')
        entite_select = request.POST.get('entite_select')
        category_id = request.POST.get('category_select')

        allocations_str = request.POST.get('allocations')
        allocations = json.loads(allocations_str) if allocations_str else {}

        if float(amount) > 0 and not entite_select and not allocations:
            return JsonResponse({"status":"error",'message':"Entité prenant en charge le rembourssement manquante"})
        prospect = Prospets.objects.get(id=id_client)
        if prospect.is_double:
            promo = FicheVoeuxDouble.objects.filter(prospect=prospect, is_confirmed=True).last()
        else:
            promo = FicheDeVoeux.objects.filter(prospect=prospect, is_confirmed=True).last()

        if not promo:
            return JsonResponse({"status":"error",'message':"Promotion non trouvée pour ce client"})

        print(f"DEBUG REFUND: id_client={id_client}, fiche_id={promo.id}, promo_id={promo.promo_id}")

        obj_refund = Rembourssements.objects.get(id = id_refund)
        
        # Determine the primary entity for the refund object
        # If there are allocations, we'll try to find the entity with the max amount later or just use entite_select if available
        if entite_select:
            obj_refund.entite = Entreprise.objects.get(id = entite_select)
        
        if category_id:
            obj_refund.category_id = category_id
            
        obj_refund.save()
        # refund_paiement = Paiements(
        #     prospect = Prospets.objects.get(id = id_client),
        #     paiement_label = "Rembourssement",
        #     montant_paye = amount,
        #     date_paiement = datetime.now(),
        #     mode_paiement = mode_rembourssement,
        #     is_refund = True,
        #     promo_id = promo.promo.id,
        #     refund_id = obj_refund,
           
        # )

        # refund_paiement.save()

        from collections import defaultdict
        
        # Build a mapping of entite_id -> amount
        entite_amounts = defaultdict(float)
        entite_amounts_for_depense = defaultdict(float)
        
        if allocations:
            for p_id_str, p_amount in allocations.items():
                try:
                    p = Paiements.objects.get(id=int(p_id_str))
                    # Use payment's entity, fallback to entite_select
                    e_id = p.entite_id if p.entite else entite_select
                    if e_id:
                        entite_amounts[e_id] += float(p_amount)

                    is_cashed = True
                    if p.mode_paiement in ['che', 'vir']:
                        op_bancaire = OperationsBancaire.objects.filter(paiement=p, operation_type='entree').first()
                        if op_bancaire and not op_bancaire.is_paid:
                            # Pour la contre-passation, on laisse is_cashed=True afin que le script 
                            # génère automatiquement une "sortie" (OperationsBancaire) de même montant,
                            # ce qui viendra équilibrer l' "entrée" en attente de recouvrement (511).
                            if float(p_amount) >= float(op_bancaire.montant):
                                op_bancaire.justification = (op_bancaire.justification or '') + f" (Annulé par remboursement {obj_refund.id})"
                                op_bancaire.save()
                                p.is_done = True
                                p.is_refund = True
                                p.save()
                                is_cashed = False
                            else:
                                op_bancaire.montant = float(op_bancaire.montant) - float(p_amount)
                                op_bancaire.save()
                                is_cashed = False

                    # Génération de la quittance d'annulation (montant négatif)
                    Paiements.objects.create(
                        prospect=p.prospect,
                        paiement_label=f"Annulation (Remboursement #{obj_refund.id})",
                        montant_paye=-float(p_amount),
                        date_paiement=now().date(),
                        mode_paiement=p.mode_paiement,
                        is_refund=True,
                        refund_id=obj_refund,
                        promo=p.promo,
                        entite=p.entite,
                        context=p.context,
                        is_done=True
                    )

                    if is_cashed or p.mode_paiement not in ['che', 'vir']:
                        if e_id:
                            entite_amounts_for_depense[e_id] += float(p_amount)

                except Paiements.DoesNotExist:
                    continue
        else:
            # Fallback if no allocations are provided (legacy behavior)
            if entite_select:
                entite_amounts[entite_select] = float(amount)
                entite_amounts_for_depense[entite_select] = float(amount)
            
        # Update obj_refund entite to the one with the highest refund amount if not set
        if not obj_refund.entite and entite_amounts:
            max_entite_id = max(entite_amounts, key=entite_amounts.get)
            obj_refund.entite = Entreprise.objects.get(id=max_entite_id)
            obj_refund.save()

        # Create distinct OperationsBancaire ONLY for cashed amounts
        for e_id, e_amount in entite_amounts_for_depense.items():
            if e_amount > 0:
                if mode_rembourssement in ["che", "vir"]:
                    OperationsBancaire.objects.create(
                        operation_type="sortie",
                        remboursement=obj_refund,
                        montant=e_amount,
                    )

        from t_conseil.models import Facture
        
        for p_id_str, p_amount in allocations.items():
            try:
                paiement = Paiements.objects.get(id=int(p_id_str))
                
                PaiementRemboursement.objects.create(
                    client=prospect,
                    remboursement=obj_refund,
                    paiement=paiement,
                    montant=p_amount,
                    mode_paiement=mode_rembourssement,
                    date_remboursement=now()
                )

                if paiement.facture:
                    # Créer une Facture d'Avoir Partielle
                    facture_avoir = Facture.objects.create(
                        client=prospect,
                        facture_source=paiement.facture,
                        type_facture='avoir',
                        tva=paiement.facture.tva,
                        show_tva=paiement.facture.show_tva,
                        entreprise=paiement.facture.entreprise,
                        mode_paiement=mode_rembourssement,
                        module_source='tresorerie',
                        conditions_commerciales=f"Avoir sur la facture N°{paiement.facture.num_facture} généré suite au remboursement partiel/total de {p_amount} DA."
                    )
                    
                    from t_conseil.models import LignesFacture
                    LignesFacture.objects.create(
                        facture=facture_avoir,
                        description=f"Remboursement partiel/total sur paiement {paiement.id}",
                        quantite=1,
                        prix_unitaire=p_amount,
                        montant_ht=p_amount,
                        tva_percent=0
                    )
                    
                    # On attache la facture d'avoir au remboursement
                    obj_refund.facture = facture_avoir
            except Paiements.DoesNotExist:
                continue

        obj_refund.is_appliced = True
        obj_refund.save()

        # Update or create cumulative refund for the promo dynamically to avoid out-of-sync issues
        clients_in_promo_standard = FicheDeVoeux.objects.filter(promo_id=promo.promo_id).values_list('prospect_id', flat=True)
        clients_in_promo_double = FicheVoeuxDouble.objects.filter(promo_id=promo.promo_id).values_list('prospect_id', flat=True)
        all_client_ids = set(list(clients_in_promo_standard) + list(clients_in_promo_double))
        
        total_refunds_in_promo = Rembourssements.objects.filter(
            client_id__in=all_client_ids,
            is_appliced=True
        ).aggregate(total=Sum('allowed_amount'))['total'] or 0
        
        promo_refund, created = PromoRembourssement.objects.get_or_create(promo_id=promo.promo_id)
        promo_refund.montant = Decimal(total_refunds_in_promo)
        promo_refund.save()

        cancel_enrollment = request.POST.get('cancel_enrollment') == 'true'
        if cancel_enrollment:
            prospect.statut = "annuler"
            prospect.etat = "annuler"
            prospect.motif_annulation = "rembourssement"
            prospect.save()
            DuePaiements.objects.filter(client_id=prospect.id, type="frais_f").update(is_annulated=True)
            ClientPaiementsRequest.objects.filter(client_id=prospect.id).update(etat='annulation_approuver')
            
            # Supprimer les opérations bancaires non encaissées (paiement en attente de recouvrement)
            uncashed_payments = Paiements.objects.filter(prospect=prospect, is_done=False, is_refund=False)
            for up in uncashed_payments:
                OperationsBancaire.objects.filter(paiement=up, is_paid=False).delete()
                up.is_done = True
                up.is_refund = True
                up.observation = (up.observation or "") + " (Annulé suite à l'annulation d'inscription)"
                up.save()
            
            # Archiver les demandes de dérogation en attente
            derogations = Derogations.objects.filter(demandeur=prospect, etat=False)
            for derog in derogations:
                derog.etat = True
                derog.statut = 'rejetee'
                derog.observation = "Archivée automatiquement suite à l'annulation de l'inscription."
                derog.save()

        # Mettre à jour l'observation du prospect et supprimer la fiche de voeux
        if prospect.is_double:
            specialty_text = f"{promo.specialite.specialite1.label} / {promo.specialite.specialite2.label}" if promo.specialite else "Inconnue"
        else:
            specialty_text = promo.specialite.label if promo.specialite else "Inconnue"
        
        promo_text = promo.promo.code if promo.promo else "Inconnue"
        obs_text = f" Ancienne spécialité demandée : {specialty_text} (Promo : {promo_text})."
        
        if prospect.observation:
            prospect.observation += f"\n{obs_text}"
        else:
            prospect.observation = obs_text
        prospect.save()
        
        # Annuler toutes les fiches de voeux (standard et double) sans les supprimer
        FicheDeVoeux.objects.filter(prospect=prospect).update(is_confirmed=False)
        FicheVoeuxDouble.objects.filter(prospect=prospect).update(is_confirmed=False)

        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='Rembourssement',
            target_id=str(id_refund),
            details=f"Exécution d'un remboursement de {amount} DA pour l'étudiant {prospect.nom} {prospect.prenom}.",
            ip_address=request.META.get('REMOTE_ADDR')
        )

       
        return JsonResponse({"status" : "success","rembourssementId" : obj_refund.id})
    else:
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiShowRefundTraiteResult(request):
    id_demande = request.GET.get('id_demande')
    if not id_demande:
        return JsonResponse({"status": "error", "message": "Identifiant de demande manquant"}, status=400)
    
    try:
        rembourssement_obj = Rembourssements.objects.get(id=id_demande)
    except Rembourssements.DoesNotExist:
        return JsonResponse({"status": "error", "message": "La demande de remboursement n'existe pas"}, status=404)

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


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetEntrepriseInfos(request):
    id_client = request.GET.get('id_client')
    print(id_client)
    
    entreprise = None
    
    # Try FicheDeVoeux first
    voeux = FicheDeVoeux.objects.filter(prospect_id=id_client, is_confirmed=True).first()
    if voeux and voeux.specialite and voeux.specialite.formation and voeux.specialite.formation.entite_legal:
        entreprise = voeux.specialite.formation.entite_legal
    
    # If not found, try FicheVoeuxDouble
    if not entreprise:
        voeux_double = FicheVoeuxDouble.objects.filter(prospect_id=id_client, is_confirmed=True).first()
        if voeux_double and voeux_double.specialite and voeux_double.specialite.specialite1 and voeux_double.specialite.specialite1.formation and voeux_double.specialite.specialite1.formation.entite_legal:
            entreprise = voeux_double.specialite.specialite1.formation.entite_legal
   
    if not entreprise:
        return JsonResponse({"status": "error", "message": "Informations entreprise non trouvées"}, status=404)

    data = {
        'designation' : entreprise.designation,
        'rc' : entreprise.rc,
        'nif' : entreprise.nif,
        'art' : entreprise.art,
        'telephone' : entreprise.telephone,
    }

    return JsonResponse(data)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetProspectsList(request):

    if request.method == "GET":

        promo_id = request.GET.get('promo_id')
        specialite_id = request.GET.get('specialite_id')
        spec_type = request.GET.get('type')  # simple | double

        if not all([promo_id, specialite_id, spec_type]):
            return JsonResponse({
                'status': 'error',
                'message': 'Paramètres manquants'
            }, status=400)

        # 🔹 Cas spécialité simple
        if spec_type == "simple":
            prospects = Prospets.objects.filter(
                statut="convertit",
                prospect_fiche_voeux__promo_id=promo_id,
                prospect_fiche_voeux__specialite_id=specialite_id,
                prospect_fiche_voeux__is_confirmed=True
            )

        # 🔹 Cas double diplomation
        elif spec_type == "double":
            prospects = Prospets.objects.filter(
                statut="convertit",
                prospect_fiche_voeux_double__promo_id=promo_id,
                prospect_fiche_voeux_double__specialite_id=specialite_id,
                prospect_fiche_voeux_double__is_confirmed=True
            )

        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Type invalide'
            }, status=400)

        prospects = prospects.distinct().values(
            'id', 'nom', 'prenom', 'email', 'telephone', 'created_at','is_double'
        )

        prospects_list = []
        for prospect in prospects:
            prospects_list.append({
                'id': prospect['id'],
                'nom': prospect['nom'],
                'prenom': prospect['prenom'],
                'full_name': f"{prospect['nom']} {prospect['prenom']}",
                'email': prospect['email'],
                'telephone': prospect['telephone'],
                'created_at': prospect['created_at'].strftime("%Y-%m-%d")
                    if prospect['created_at'] else "",
                'is_double' : prospect['is_double'],
            })

        return JsonResponse({'prospects': prospects_list}, safe=False)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'change')
def ApiToggleFinancialAlert(request):
    if request.method == "POST":
        id_client = request.POST.get('id_client')
        action = request.POST.get('action') # 'enable' or 'disable'
        message = request.POST.get('message', 'Étudiant en situation irrégulière pour défaut de paiement')

        try:
            student = Prospets.objects.get(id=id_client)
            
            if action == 'enable':
                student.has_financial_alert = True
                student.financial_alert_message = message
                student.financial_alert_user = request.user
                student.financial_alert_date = now()
                student.save()
                return JsonResponse({"status": "success", "message": "Alerte activée avec succès"})
            
            elif action == 'disable':
                # Restriction: only the user who set the alert can disable it
                if student.financial_alert_user and student.financial_alert_user != request.user:
                    return JsonResponse({"status": "error", "message": "Seul l'utilisateur ayant activé l'alerte peut la désactiver"})
                
                student.has_financial_alert = False
                student.financial_alert_message = None
                student.financial_alert_user = None
                student.financial_alert_date = None
                student.save()

                UserActionLog.objects.create(
                    user=request.user,
                    action_type='UPDATE',
                    target_model='Prospets',
                    target_id=str(id_client),
                    details=f"Alerte financière {action == 'enable' and 'activée' or 'désactivée'} pour l'étudiant {student.nom} {student.prenom}. {action == 'enable' and 'Motif: ' + message or ''}",
                    ip_address=request.META.get('REMOTE_ADDR')
                )

                return JsonResponse({"status": "success", "message": "Alerte désactivée avec succès"})
            
            return JsonResponse({"status": "error", "message": "Action non reconnue"})
        
        except Prospets.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Étudiant introuvable"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'view')
def ApiSendEmailRelance(request):
    if request.method == "POST":
        id_client = request.POST.get('client_id')
        echeance_ids = request.POST.getlist('echeance_ids[]')
        
        if not id_client or not echeance_ids:
            try:
                data = json.loads(request.body)
                if not id_client:
                    id_client = data.get('client_id')
                if not echeance_ids:
                    echeance_ids = data.get('echeance_ids', [])
            except:
                pass

        if not id_client:
            return JsonResponse({"status": "error", "message": "Identifiant du client manquant"}, status=400)

        try:
            student = Prospets.objects.get(id=id_client)
        except Prospets.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Client introuvable"}, status=404)

        email_dest = student.email
        if not email_dest or not email_dest.strip():
            return JsonResponse({
                "status": "error", 
                "message": "Le prospect n'a pas d'adresse e-mail configurée."
            }, status=400)

        # Get unpaid due payments
        due_paiements = DuePaiements.objects.filter(
            client=student,
            is_annulated=False
        ).filter(Q(is_done=False) | Q(montant_restant__gt=0)).order_by('date_echeance')

        # Filter by selected échéance IDs if provided
        if echeance_ids:
            due_paiements = due_paiements.filter(id__in=echeance_ids)

        if not due_paiements.exists():
            return JsonResponse({
                "status": "info", 
                "message": "Aucune échéance en suspens n'a été sélectionnée."
            })

        # Calculate total remaining balance for selected due payments
        total_remaining = sum(item.montant_restant for item in due_paiements)

        # Build outstanding payments list HTML
        table_rows_html = ""
        for item in due_paiements:
            date_str = item.date_echeance.strftime('%d/%m/%Y') if item.date_echeance else "Non spécifiée"
            table_rows_html += f"""
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; color: #1e293b; font-size: 14px;">{item.label}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; color: #64748b; font-size: 14px;">{date_str}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; color: #0f172a; font-weight: 600; font-size: 14px; text-align: right;">{float(item.montant_due):,.2f} DA</td>
                <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; color: #e11d48; font-weight: 600; font-size: 14px; text-align: right;">{float(item.montant_restant):,.2f} DA</td>
            </tr>
            """

        # Load templates from settings
        from t_tresorerie.models import ParametreFinancier
        config_fin = ParametreFinancier.get_instance()
        subject_template = config_fin.relance_echeancier_sujet
        body_template = config_fin.relance_echeancier_corps

        # Replace dynamic variables
        nom = student.nom
        prenom = student.prenom
        annee_courante = str(datetime.now().year)
        total_remaining_formatted = f"{float(total_remaining):,.2f}"
        tenant_name = request.tenant.nom if request.tenant and hasattr(request.tenant, 'nom') else "Notre Établissement"

        # Fetch specialty information (standard and double)
        specialite_labels = []
        try:
            from t_crm.models import FicheDeVoeux, FicheVoeuxDouble
            # Standard wishes
            standard_voeux = FicheDeVoeux.objects.filter(prospect=student, is_confirmed=True)
            for voeu in standard_voeux:
                if voeu.specialite:
                    specialite_labels.append(voeu.specialite.label)
            
            # Double wishes
            double_voeux = FicheVoeuxDouble.objects.filter(prospect=student, is_confirmed=True)
            for voeu in double_voeux:
                if voeu.specialite:
                    specialite_labels.append(voeu.specialite.label)
            
            # Fallback if no confirmed wishes found, check all wishes
            if not specialite_labels:
                for voeu in FicheDeVoeux.objects.filter(prospect=student):
                    if voeu.specialite:
                        specialite_labels.append(voeu.specialite.label)
                for voeu in FicheVoeuxDouble.objects.filter(prospect=student):
                    if voeu.specialite:
                        specialite_labels.append(voeu.specialite.label)
        except Exception:
            pass

        specialite_str = ", ".join(specialite_labels) if specialite_labels else "Non spécifiée"

        subject = subject_template.replace('{nom}', nom).replace('{prenom}', prenom).replace('{annee_courante}', annee_courante).replace('{total_remaining}', total_remaining_formatted).replace('{tenant_name}', tenant_name).replace('SCHOOL SAAS', tenant_name).replace('{specialite}', specialite_str)
        
        if '{specialite}' in body_template:
            html_message = body_template.replace('{specialite}', specialite_str)
        else:
            # Fallback substitution for default template without the placeholder
            html_message = body_template.replace(
                "échéancier de paiement de formation présente",
                f"échéancier de paiement pour la spécialité <strong>{specialite_str}</strong> présente"
            ).replace(
                "échéancier de paiement présente",
                f"échéancier de paiement pour la spécialité <strong>{specialite_str}</strong> présente"
            )

        html_message = html_message.replace('{nom}', nom).replace('{prenom}', prenom).replace('{table_rows}', table_rows_html).replace('{total_remaining}', total_remaining_formatted).replace('{annee_courante}', annee_courante).replace('{tenant_name}', tenant_name).replace('SCHOOL SAAS', tenant_name)

        plain_message = f"Bonjour {nom} {prenom},\n\nNous vous contactons pour vous rappeler que votre échéancier de paiement pour la spécialité {specialite_str} présente des échéances en attente de régularisation pour un montant restant total de {total_remaining_formatted} DA.\n\nMerci de bien vouloir régulariser votre situation au plus vite.\n\nCordialement,\nLe service Trésorerie de {tenant_name}."

        reply_to_list = [request.user.email] if request.user and request.user.email else None

        from saas_admin_app.email_utils import send_platform_email
        success = send_platform_email(
            subject=subject,
            message=plain_message,
            recipient_list=[email_dest],
            html_message=html_message,
            reply_to=reply_to_list,
            from_email_display=tenant_name
        )

        if success:
            UserActionLog.objects.create(
                user=request.user,
                action_type='EMAIL',
                target_model='Prospets',
                target_id=str(id_client),
                details=f"Email de relance envoyé pour l'échéancier de {student.nom} {student.prenom} à l'adresse {email_dest}. Montant relancé: {total_remaining_formatted} DA. Échéances relancées: {', '.join(item.label for item in due_paiements)}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return JsonResponse({"status": "success", "message": "L'email de relance a été envoyé avec succès !"})
        else:
            return JsonResponse({
                "status": "error", 
                "message": "Échec de l'envoi de l'email. Veuillez vérifier la configuration SMTP globale du SaaS Admin."
            }, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required(login_url="institut_app:login")
@require_http_methods(["POST"])
@module_permission_required('tre', 'view')
def ApiMarkEngagementPrinted(request, prospect_id):
    try:
        data = json.loads(request.body)
        signataire = data.get('signataire', 'Inconnu')
        
        prospect = Prospets.objects.get(id=prospect_id)
        prospect.has_printed_engagement = True
        prospect.engagement_printed_at = now()
        prospect.engagement_printed_by = signataire
        prospect.save(update_fields=['has_printed_engagement', 'engagement_printed_at', 'engagement_printed_by'])
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Engagement marqué comme imprimé',
            'printed_at': prospect.engagement_printed_at.strftime('%d/%m/%Y %H:%M'),
            'printed_by': prospect.engagement_printed_by
        })
    except Prospets.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Prospect non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required(login_url="institut_app:login")
@require_http_methods(["POST"])
@module_permission_required('tre', 'view')
def ApiMarkQuittancePrinted(request):
    try:
        data = json.loads(request.body)
        payment_num = data.get('payment_num')
        if not payment_num:
            return JsonResponse({'status': 'error', 'message': 'Numéro de paiement manquant'}, status=400)
        
        user = request.user
        printed_by = f"{user.first_name} {user.last_name}".strip() or user.username
        
        payment = Paiements.objects.get(num=payment_num)
        payment.has_printed_quittance = True
        payment.quittance_printed_at = now()
        payment.quittance_printed_by = printed_by
        payment.save(update_fields=['has_printed_quittance', 'quittance_printed_at', 'quittance_printed_by'])
        
        return JsonResponse({
            'status': 'success',
            'message': 'Impression de la quittance enregistrée avec succès',
            'quittance_printed_at': payment.quittance_printed_at.strftime('%d/%m/%Y à %H:%M'),
            'quittance_printed_by': payment.quittance_printed_by
        })
    except Paiements.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Paiement non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
