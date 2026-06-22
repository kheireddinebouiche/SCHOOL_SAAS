from institut_app.decorators import module_permission_required
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from t_crm.models import FicheDeVoeux,RemiseAppliquerLine,RemiseAppliquer, UserActionLog
from t_remise.models import *
from t_groupe.models import *
from django.db.models import Sum
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from institut_app.decorators import *

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def AttentesPaiements(request):
    context = {
       
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/comptabilite/tresorerie/attentes_de_paiement.html', context)

@login_required(login_url="insitut_app:login")
@module_permission_required('tre', 'view')
def ApiListeDemandePaiement(request):
    listes = ClientPaiementsRequest.objects.select_related("promo", "specialite", "client",'specialite_double').filter(client__statut = "instance")
    
    promo_id = request.GET.get('promo_id')
    formation_id = request.GET.get('formation_id')
    
    if promo_id:
        listes = listes.filter(promo_id=promo_id)
        
    if formation_id:
        listes = listes.filter(formation_id=formation_id)
    data = []
    for obj in listes:
        has_rembourssement = Rembourssements.objects.filter(client = obj.client, is_done=False).exists()

        # Alertes échéancier spécial
        special_echeancier = EcheancierSpecial.objects.filter(prospect=obj.client).last()
        echeancier_special_alerte = None
        if special_echeancier:
            if not special_echeancier.is_approuved:
                echeancier_special_alerte = "en_attente"
            elif not special_echeancier.is_validate:
                echeancier_special_alerte = "non_accepte"
        
        # Alertes remise
        remise_appliquer = RemiseAppliquerLine.objects.filter(prospect=obj.client).select_related('remise_appliquer').last()
        remise_alerte = None
        if remise_appliquer and remise_appliquer.remise_appliquer:
            if not remise_appliquer.remise_appliquer.is_approuved:
                remise_alerte = "en_attente"
            else:
                remise_alerte = "traitee"

        # Vérifier si le prospect a des paiements dus ou des paiements effectués
        has_due_payments = False
        if obj.client:
            due_query = Q(client=obj.client)
            pay_query = Q(prospect=obj.client)
            if obj.promo:
                due_query &= Q(promo=obj.promo)
                pay_query &= Q(promo=obj.promo)
            
            has_due_payments = DuePaiements.objects.filter(due_query).exists() or \
                               Paiements.objects.filter(pay_query).exists() or \
                               obj.paid

        data.append({
            "id": obj.id,
            "motif": obj.motif,
            "motif_label": obj.get_motif_display(),
            "promo": obj.promo.id if obj.promo else None,
            "formation": obj.formation.id if obj.formation else None,
            "promo_session": obj.promo.session if obj.promo else None,
            "promo_begin" : obj.promo.begin_year,
            "promo_end" : obj.promo.end_year,
            "specialite": obj.specialite.id if obj.specialite else None,
            "amount" : obj.amount if obj.amount else (obj.specialite.prix if obj.specialite else ((obj.specialite_double.prix_spec1 or 0) + (obj.specialite_double.prix_spec2 or 0)) if obj.specialite_double else 0),
            "nom": obj.client.nom if obj.client else None,
            "prenom": obj.client.prenom if obj.client else None,
            "is_double" : obj.client.is_double if obj.client.is_double else None,
            "created_at": obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "etat": obj.etat,
            "etat_label": obj.get_etat_display() if hasattr(obj, "get_etat_display") else None,
            "has_rembourssement" : has_rembourssement,
            "echeancier_special_alerte": echeancier_special_alerte,
            "remise_alerte": remise_alerte,
            "paid": obj.paid,
            "has_due_payments": has_due_payments,
            "formation_label": obj.specialite.formation.nom if obj.specialite else (obj.specialite_double.label if obj.specialite_double else ""),
            "specialite_label": obj.specialite.label if obj.specialite else "",
        })
    
    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def PageDetailsDemandePaiement(request, pk):

    obj = ClientPaiementsRequest.objects.get(id = pk)
    
    # Log de consultation
    UserActionLog.objects.create(
        user=request.user,
        action_type='VIEW',
        target_model='ClientPaiementsRequest',
        target_id=str(pk),
        details=f"Consultation des détails de la demande de paiement pour l'étudiant {obj.client.nom} {obj.client.prenom}.",
        ip_address=request.META.get('REMOTE_ADDR')
    )
    params = ParametreFinancier.get_instance()
    context = {
        'tenant' : request.tenant,
        'pk' : pk,
        'payment_types': PaymentType.objects.all(),
        'activer_ticket_caisse': params.activer_ticket_caisse
    }

    if obj.client.is_double:
        return render(request,"tenant_folder/comptabilite/tresorerie/details_attente_paiement_double.html", context)
    else:
        return render(request, "tenant_folder/comptabilite/tresorerie/details_attente_paiement.html", context)


@login_required(login_url="institut_app:login")
@ajax_required
@module_permission_required('tre', 'view')
def ApiLoadRefundData(request):
    liste = Rembourssements.objects.all().values('is_done','client__nom', 'client__prenom', 'client__id', 'motif_rembourssement', 'etat','created_at', 'id').order_by('-created_at')
    for i in liste:
        i_obj = Rembourssements.objects.get(id = i['id'])
        i['etat_label'] = i_obj.get_etat_display()
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
@ajax_required
@module_permission_required('tre', 'view')
def ApiLoadRefundDetails(request):
    if request.method == "GET":
        id = request.GET.get('id')
        obj = Rembourssements.objects.get(id = id)
        paiements_qs = Paiements.objects.filter(prospect=obj.client, is_refund=False).exclude(Q(context='frais_i') | Q(is_frais_inscription=True) | Q(paiement_label__icontains="inscription"))
        paiement_lines = paiements_qs.filter(Q(is_done=True) | Q(mode_paiement='esp')).aggregate(total=Sum('montant_paye'))['total'] or 0

        # Récupération des informations de groupe
        groupes = []
        for gl in GroupeLine.objects.filter(student=obj.client):
            if gl.groupe and gl.groupe.nom not in groupes:
                groupes.append(gl.groupe.nom)
        for aff in AffectationGroupe.objects.filter(etudiant=obj.client):
            if aff.groupe and aff.groupe.nom not in groupes:
                groupes.append(aff.groupe.nom)
        
        group_display = ", ".join(groupes) if groupes else "Non affecté"

        # Récupération de l'historique des absences
        from t_etudiants.models import HistoriqueAbsence
        abs_query = HistoriqueAbsence.objects.filter(etudiant=obj.client)
        absences_list = []
        for abs_obj in abs_query:
            if abs_obj.historique:
                for entry in abs_obj.historique:
                    entry_date = entry.get('date', 'N/A')
                    for detail in entry.get('data', []):
                        absences_list.append({
                            'date': entry_date,
                            'module': detail.get('module', 'N/A'),
                            'code': detail.get('code', 'N/A'),
                            'etat': detail.get('etat', 'Absent')
                        })
        
        # Récupération de l'échéancier (montants dus et payés)
        due_query = DuePaiements.objects.filter(client=obj.client).order_by('date_echeance', 'id')
        echeancier_list = []
        for due in due_query:
            paiements_due = Paiements.objects.filter(due_paiements=due)
            paid_amount = paiements_due.filter(Q(is_done=True) | Q(mode_paiement='esp')).aggregate(total=Sum('montant_paye'))['total'] or 0
            attente_amount = paiements_due.filter(is_done=False).exclude(mode_paiement='esp').aggregate(total=Sum('montant_paye'))['total'] or 0
            is_factured = paiements_due.filter(facture__isnull=False).exists()
            echeancier_list.append({
                'label': due.label or 'N/A',
                'montant_due': float(due.montant_due) if due.montant_due else 0.0,
                'montant_paye': float(paid_amount),
                'montant_attente': float(attente_amount),
                'montant_restant': float(due.montant_restant) if due.montant_restant is not None else float((due.montant_due or 0) - paid_amount - attente_amount),
                'date_echeance': due.date_echeance.strftime("%d/%m/%Y") if due.date_echeance else "N/A",
                'is_done': due.is_done,
                'is_factured': is_factured
            })

        data= {
            'client_id': obj.client.id,
            'client_nom' : obj.client.nom,
            'client_prenom' : obj.client.prenom,
            'motif_rembourssement' : obj.motif_rembourssement,
            'date_demande' : obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'etat' : obj.get_etat_display(),
            'paiement_total' : paiement_lines,
            'description': obj.observation or 'N/A',
            'groupe': group_display,
            'absences': absences_list,
            'echeancier': echeancier_list,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'status' : 'error', 'message' : "Méthode non autorisée"}, status=405)
        
@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'view')
def ApiAccepteRembourssement(request):
    montantRembourser = request.GET.get('montantRembourser')
    dateRemboursement = request.GET.get('dateRemboursement')
    modePaiement = request.GET.get('modePaiement')
    client = request.GET.get('client')
    id_remboursement = request.GET.get('id_remboursement') 

    obj_rembourssement = Rembourssements.objects.get(id = id_remboursement)
    obj_rembourssement.mode_rembourssement = modePaiement
    obj_rembourssement.allowed_amount = montantRembourser
    obj_rembourssement.etat = "acp"
    obj_rembourssement.is_done = True
    obj_rembourssement.save()


    return JsonResponse({'status' : 'success'})

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'view')
def ApiRejectRembourssement(request):
    id_remboursement = request.GET.get('id_remboursement') 
    motif = request.GET.get('motifRejet') 

    obj = Rembourssements.objects.get(id = id_remboursement)
    obj.etat = 'ref'
    obj.observation = motif
    obj.is_done = True
    obj.save()

    return JsonResponse({'status' : 'success'}) 

@login_required(login_url="institut_app:login")
@require_http_methods(["POST"])
@module_permission_required('tre', 'add')
def ApiSaveSelectedEcheancier(request):
    try:
        id_demande = request.POST.get('id_demande')
        id_echeancier = request.POST.get('id_echeancier')
        
        if not id_demande or not id_echeancier:
            return JsonResponse({'status': 'error', 'message': 'Paramètres manquants'}, status=400)
            
        obj = ClientPaiementsRequest.objects.get(id=id_demande)
        echeancier = EcheancierPaiement.objects.get(id=id_echeancier)
        
        obj.ref_echeancier = echeancier
        obj.save()
        
        # Log d'application d'échéancier
        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='ClientPaiementsRequest',
            target_id=str(id_demande),
            details=f"Application du modèle d'échéancier '{echeancier.model.label}' (ID: {id_echeancier}) pour l'étudiant {obj.client.nom} {obj.client.prenom}.",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return JsonResponse({'status': 'success', 'message': 'Modèle d\'échéancier enregistré avec succès'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500) 

########################################## Fonction qui permet d'afficher tous les détails du demandeur de paiement ###############################
@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetDetailsDemandePaiement(request):  
    if request.method == "GET":
        id= request.GET.get('id_demande')
        obj = ClientPaiementsRequest.objects.get(id = id)
        voeux = FicheDeVoeux.objects.filter(prospect=obj.client, is_confirmed=True).select_related("specialite").first()

        # Check if we should override the default echeancier
        override_echeancier_id = request.GET.get('override_echeancier_id')
        echeancierId = None
        
        if override_echeancier_id and override_echeancier_id != 'null':
            try:
                echeancierId = EcheancierPaiement.objects.get(id=int(override_echeancier_id))
            except (EcheancierPaiement.DoesNotExist, ValueError):
                pass
        
        # If no override, check if there's a saved echeancier on the request
        if not echeancierId and obj.ref_echeancier:
            echeancierId = obj.ref_echeancier

        if not echeancierId:
            try:
                # First, try to find a specialty-specific default echeancier
                echeancierId = EcheancierPaiement.objects.filter(
                    formation_id=voeux.specialite.formation.id, 
                    specialite=voeux.specialite,
                    is_default=True, 
                    model__promo=voeux.promo
                ).first()

                # If not found, fallback to the formation-level default echeancier
                if not echeancierId:
                    echeancierId = EcheancierPaiement.objects.get(
                        formation_id=voeux.specialite.formation.id, 
                        specialite__isnull=True,
                        is_default=True, 
                        model__promo=voeux.promo
                    )
            except EcheancierPaiement.DoesNotExist:
                # Fallback to the first active echeancier if no default is found
                echeancierId = EcheancierPaiement.objects.filter(
                    formation_id=voeux.specialite.formation.id,
                    model__promo=voeux.promo,
                    is_active=True
                ).first()
                
                if not echeancierId:
                    return JsonResponse({'status': 'error', 'error_type': 'missing_echeancier', 'message': "Échéancier non trouvé pour cette spécialité et promo."}, status=200)
    
        if echeancierId and echeancierId.model and not echeancierId.model.has_frais_inscription:
            frais_inscription = None
        else:
            frais_inscription = echeancierId.frais_inscription if echeancierId else None
    
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
        special_echeancier_validate = False

        try:
            group = GroupeLine.objects.get(student=obj.client)

            groupe_data = {
                'groupe_nom' : group.groupe.nom,
                'groupe_semestre' : group.groupe.semestre,
            }

        except GroupeLine.DoesNotExist:
            groupe_data = {}
            group = None

        due_paiement = DuePaiements.objects.filter(client=obj.client).filter(Q(is_done=False) | Q(montant_restant__gt=0))

        if due_paiement.count() > 0:
            has_due_paiement = True
            total_initial = DuePaiements.objects.filter(client = obj.client).aggregate(total=Sum('montant_due'))['total'] or 0
            for i in due_paiement:
                due_paiement_data.append({
                    'id_due_paiement' : i.id,
                    'montant_due'  : i.montant_due,
                    'montant_restant' : i.montant_restant,
                    'label' : i.label,
                    'date_echeance' : i.date_echeance,
                    'entite_nom' : i.entite.designation if i.entite else (i.ref_echeancier.entite.designation if i.ref_echeancier and i.ref_echeancier.entite else "Non définie"),
                })
        else:
            has_due_paiement = False
            due_paiement_data = []

        done_paiements = Paiements.objects.filter(prospect = obj.client).order_by('due_paiements__date_echeance', 'id')
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
                    'is_refund' : i.is_refund,
                    'logo_header': i.due_paiements.entite.entete_logo.url if i.due_paiements and i.due_paiements.entite and i.due_paiements.entite.entete_logo else (echeancierId.entite.entete_logo.url if echeancierId and echeancierId.entite and echeancierId.entite.entete_logo else None),
                    'logo_footer': i.due_paiements.entite.pied_page_logo.url if i.due_paiements and i.due_paiements.entite and i.due_paiements.entite.pied_page_logo else (echeancierId.entite.pied_page_logo.url if echeancierId and echeancierId.entite and echeancierId.entite.pied_page_logo else None),
                    'facture_id': i.facture.id if i.facture else None,
                    'facture_num': i.facture.num_facture if i.facture else None,
                    'montant_restant': montant_restant_val,
                    'has_printed_quittance': i.has_printed_quittance,
                    'quittance_printed_at': i.quittance_printed_at.strftime("%Y-%m-%d %H:%M:%S") if i.quittance_printed_at else None,
                    'quittance_printed_by': i.quittance_printed_by,
                })

        else:
            paiements_done_data = []

        obj_echeacncier_speial = EcheancierSpecial.objects.filter(prospect = obj.client).last()
        special_echeancier_frais_inscription_entite_id = echeancierId.entite.id if echeancierId.entite else None
        special_echeancier_frais_inscription_entite_nom = echeancierId.entite.designation if echeancierId.entite else None
        
        if obj_echeacncier_speial:
            line_echeancier_special = EcheancierPaiementSpecialLine.objects.filter(echeancier = obj_echeacncier_speial)
            echeancier_state_approuvel = obj_echeacncier_speial.is_approuved
            has_special_echeancier = True
            special_echeancier_validate = obj_echeacncier_speial.is_validate
            
            if special_echeancier_validate and obj_echeacncier_speial.entite:
                special_echeancier_frais_inscription_entite_id = obj_echeacncier_speial.entite.id
                special_echeancier_frais_inscription_entite_nom = obj_echeacncier_speial.entite.designation

            special_echeancier_data = []
            for i in line_echeancier_special:
                special_echeancier_data.append({
                    'id_echeancier_special' : i.id,
                    'taux' : i.taux,
                    'value' : i.value,
                    'date_echeancier' : i.date_echeancier,
                    'montant_tranche' : i.montant_tranche,
                    'entite_id' : i.entite.id if i.entite else None,
                    'entite_nom' : i.entite.designation if i.entite else None,
                })


        echeancier = echeancierId
        liste_echeancier = EcheancierPaiementLine.objects.filter(echeancier = echeancier)
        
        remiseObj = RemiseAppliquerLine.objects.filter(prospect = obj.client).last()

        if remiseObj and remiseObj.remise_appliquer:
            
            remise = remiseObj.remise_appliquer.remise
            is_approuved_remise = remiseObj.remise_appliquer.is_approuved
            reduction_type = remise.label
            id_reduction = remiseObj.remise_appliquer.id
            is_applicated_remise = remiseObj.remise_appliquer.is_applicated
            
            prix_formation = voeux.specialite.prix
            
            if remise.is_value:
                # Fixed amount discount
                montant_remise = prix_formation - (remise.montant or 0)
                remise_valeur = remise.montant
            else:
                # Percentage discount
                taux = remise.taux or 0
                montant_remise = prix_formation - ((taux * prix_formation) / 100)
                remise_valeur = taux

            remiseDatas = {
                'valeur' : remise_valeur,
                'is_value' : remise.is_value,
                'remise_approuver' : is_approuved_remise,
                'remise_appliquer' : is_applicated_remise,
                'type_remise' : reduction_type,
                'montant_remise' : montant_remise,
                'montant_sans_remise' : prix_formation,
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
                'entite_id' : i.entite.id if i.entite else None,
                'entite_nom' : i.entite.designation if i.entite else None,
            })

        ## Changement de d'echeancier -- a remplacer une fois valider par l'utilisateur
        if obj_echeacncier_speial and obj_echeacncier_speial.is_validate:
            echeancier_data = special_echeancier_data
            frais_inscription = obj_echeacncier_speial.frais_inscription
        
        refund = Rembourssements.objects.filter(client = obj.client).last()
        refund_data = []
        if refund:
            paiements = Paiements.objects.filter(prospect = obj.client, context = "frais_f" ).aggregate(total=Sum('montant_paye'))['total'] or 0
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
                'mode_rembourssement' : refund.mode_rembourssement,
                "mode_rembourssement_label" : refund.get_mode_rembourssement_display(),
                'observation' : refund.observation, 
                'montant_paye' : paiements,
                'facture_numero': refund.facture.num_facture if refund.facture else None,
            }
        else:
            has_pending_refund = False
            refund_data = []
        
        user_data = {
            "demandeur_id" : obj.client.id,
            "demandeur_nom": obj.client.nom,
            "demandeur_prenom": obj.client.prenom,
            "demandeur_email" : obj.client.email,
            "demandeur_telephone" : obj.client.telephone,
            "demandeur_date_naissance" : obj.client.date_naissance if obj.client.date_naissance else "Non complété",
            "demandeur_adresse" : obj.client.adresse if obj.client.adresse else "Non complété",
            "demandeur_lieu_naissance" : obj.client.lieu_naissance if obj.client.date_naissance else "Non complété",
            "demandeur_date_inscription" : obj.client.created_at.strftime("%Y-%m-%d"),
            "statut_demandeur": obj.client.statut,
            "client_id" : obj.client.id,
            "motif": obj.get_motif_display(),
            "created_at": obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "has_printed_engagement": obj.client.has_printed_engagement,
            "engagement_printed_at": obj.client.engagement_printed_at.strftime("%Y-%m-%d %H:%M:%S") if obj.client.engagement_printed_at else None,
            "engagement_printed_by": obj.client.engagement_printed_by,
        }

        voeux_data = {
            'specialite_id' : voeux.specialite.id,
            'specialite_label' : voeux.specialite.label,
            'formation' : voeux.specialite.formation.nom,
            'entite' : voeux.specialite.formation.entite_legal.designation,
            'entite_ville' : voeux.specialite.formation.entite_legal.ville,
            'promo' : voeux.promo.code,
            'prix_formation' : voeux.specialite.prix,
            'frais_inscription' : frais_inscription,
            'date_frais_inscription': echeancierId.date_frais_inscription.strftime("%Y-%m-%d") if echeancierId and echeancierId.date_frais_inscription else None,
            'logo_header' : voeux.specialite.formation.entite_legal.entete_logo.url,
            'logo_footer' : voeux.specialite.formation.entite_legal.pied_page_logo.url,
        }

        total_solde = total_initial - total_paiement if has_due_paiement and has_paiement else 0

        # Available echeanciers for this specialty and promo
        available_echeanciers = EcheancierPaiement.objects.filter(
            Q(specialite=voeux.specialite) | Q(specialite__isnull=True),
            formation_id=voeux.specialite.formation.id,
            model__promo=voeux.promo,
            is_active=True
        ).values('id', 'model__label', 'is_default')

        data = {
            'user_data' : user_data,
            'voeux' : voeux_data,
            'frais_inscription' : frais_inscription,
            'echeancier' : list(echeancier_data),
            'groupe_data': groupe_data,
            'remise' : remiseDatas,
            'has_special_echeancier' : has_special_echeancier,
            'id_echeancier_special' : obj_echeacncier_speial.id if obj_echeacncier_speial else None,
            'id_echeancier' : echeancierId.id,
            'available_echeanciers': list(available_echeanciers),
            'has_saved_echeancier': obj.ref_echeancier is not None,
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
            'special_echeancier_validate' : special_echeancier_validate,
            'special_echeancier_frais_inscription_entite_id' : special_echeancier_frais_inscription_entite_id,
            'special_echeancier_frais_inscription_entite_nom' : special_echeancier_frais_inscription_entite_nom,
            'annee_academique' : voeux.promo.annee_academique,
            "has_invoice": done_paiements.filter(is_refund=False, facture__isnull=False).exists() if has_paiement else False,

        }

        return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetDetailsDemandePaiementDouble(request):
    if request.method == "GET":
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
        special_echeancier_validate = False
        id_special_echeancier = 0

        id= request.GET.get('id_demande')
        obj = ClientPaiementsRequest.objects.get(id = id)
        voeux = FicheVoeuxDouble.objects.filter(prospect=obj.client, is_confirmed=True).first()

        # Determine target specialty and promo
        target_spec_double_id = None
        target_promo_id = None
        
        if obj.specialite_double:
            target_spec_double_id = obj.specialite_double.id
        elif voeux and voeux.specialite:
            target_spec_double_id = voeux.specialite.id
            
        if obj.promo:
            target_promo_id = obj.promo.id
        elif voeux and voeux.promo:
            target_promo_id = voeux.promo.id

        # Check if we should override the default echeancier
        override_echeancier_id = request.GET.get('override_echeancier_id')
        echeancierId = None
        
        if override_echeancier_id and override_echeancier_id != 'null':
            try:
                echeancierId = EcheancierPaiement.objects.get(id=int(override_echeancier_id))
            except (EcheancierPaiement.DoesNotExist, ValueError):
                pass
        
        # If no override, check if there's a saved echeancier on the request
        if not echeancierId and obj.ref_echeancier:
            echeancierId = obj.ref_echeancier

        if not echeancierId and target_spec_double_id and target_promo_id:
            echeancierId = EcheancierPaiement.objects.filter(
                formation_double_id=target_spec_double_id, 
                is_default=True, 
                model__promo_id=target_promo_id
            ).last()
            
            if not echeancierId:
                # Fallback to the first active echeancier
                echeancierId = EcheancierPaiement.objects.filter(
                    formation_double_id=target_spec_double_id, 
                    model__promo_id=target_promo_id, 
                    is_active=True
                ).first()
            
        if not echeancierId:
            return JsonResponse({
                'status': 'error', 
                'error_type': 'missing_echeancier', 
                'message': "Échéancier non trouvé.",
                'debug_info': {
                    'target_spec_double_id': target_spec_double_id,
                    'target_promo_id': target_promo_id,
                    'has_voeux': voeux is not None
                }
            }, status=200)

        echeancier = echeancierId
        if echeancier and echeancier.model and not echeancier.model.has_frais_inscription:
            frais_inscription = None
        else:
            frais_inscription = echeancier.frais_inscription if echeancier else 0

        due_paiement = DuePaiements.objects.filter(client=obj.client).filter(Q(is_done=False) | Q(montant_restant__gt=0))

        if due_paiement.count() > 0:
            has_due_paiement = True
            total_initial = DuePaiements.objects.filter(client = obj.client).aggregate(total=Sum('montant_due'))['total'] or 0
            for i in due_paiement:
                due_paiement_data.append({
                    'id_due_paiement' : i.id,
                    'montant_due'  : i.montant_due,
                    'montant_restant' : i.montant_restant,
                    'label' : i.label,
                    'date_echeance' : i.date_echeance,
                    'entite_nom' : i.entite.designation if i.entite else (i.ref_echeancier.entite.designation if i.ref_echeancier and i.ref_echeancier.entite else "Non définie"),
                })
        else:
            has_due_paiement = False
            due_paiement_data = []

        done_paiements = Paiements.objects.filter(prospect = obj.client).order_by('due_paiements__date_echeance', 'id')
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
                    'reference_paiement' : i.reference_paiement,
                    'is_refund' : i.is_refund,
                    'logo_header': i.due_paiements.entite.entete_logo.url if i.due_paiements and i.due_paiements.entite and i.due_paiements.entite.entete_logo else (echeancierId.entite.entete_logo.url if echeancierId and echeancierId.entite and echeancierId.entite.entete_logo else None),
                    'logo_footer': i.due_paiements.entite.pied_page_logo.url if i.due_paiements and i.due_paiements.entite and i.due_paiements.entite.pied_page_logo else (echeancierId.entite.pied_page_logo.url if echeancierId and echeancierId.entite and echeancierId.entite.pied_page_logo else None),
                    'facture_id': i.facture.id if i.facture else None,
                    'facture_num': i.facture.num_facture if i.facture else None,
                    'montant_restant': montant_restant_val,
                    'has_printed_quittance': i.has_printed_quittance,
                    'quittance_printed_at': i.quittance_printed_at.strftime("%Y-%m-%d %H:%M:%S") if i.quittance_printed_at else None,
                    'quittance_printed_by': i.quittance_printed_by,
                })

        else:
            paiements_done_data = []

        remiseObj = RemiseAppliquerLine.objects.filter(prospect = obj.client).last()

        if remiseObj and remiseObj.remise_appliquer:
            
            remise = remiseObj.remise_appliquer.remise
            is_approuved_remise = remiseObj.remise_appliquer.is_approuved
            reduction_type = remise.label
            id_reduction = remiseObj.remise_appliquer.id
            is_applicated_remise = remiseObj.remise_appliquer.is_applicated
            
            prix_formation = (voeux.specialite.prix_spec1 or 0) + (voeux.specialite.prix_spec2 or 0)
            
            if remise.is_value:
                # Fixed amount discount
                montant_remise = prix_formation - (remise.montant or 0)
                remise_valeur = remise.montant
            else:
                # Percentage discount
                taux = remise.taux or 0
                montant_remise = prix_formation - ((taux * prix_formation) / 100)
                remise_valeur = taux

            remiseDatas = {
                'valeur' : remise_valeur,
                'is_value' : remise.is_value,
                'remise_approuver' : is_approuved_remise,
                'remise_appliquer' : is_applicated_remise,
                'type_remise' : reduction_type,
                'montant_remise' : montant_remise,
                'montant_sans_remise' : prix_formation,
                'id_applied_reduction' : id_reduction,
            }

        else:
            remiseDatas = None

        obj_echeacncier_speial = EcheancierSpecial.objects.filter(prospect = obj.client).last()
        special_echeancier_frais_inscription_entite_id = echeancierId.entite.id if echeancierId and echeancierId.entite else None
        special_echeancier_frais_inscription_entite_nom = echeancierId.entite.designation if echeancierId and echeancierId.entite else None

        if obj_echeacncier_speial:
            line_echeancier_special = EcheancierPaiementSpecialLine.objects.filter(echeancier = obj_echeacncier_speial)
            echeancier_state_approuvel = obj_echeacncier_speial.is_approuved
            has_special_echeancier = True
            special_echeancier_validate = obj_echeacncier_speial.is_validate
            
            if special_echeancier_validate and obj_echeacncier_speial.entite:
                special_echeancier_frais_inscription_entite_id = obj_echeacncier_speial.entite.id
                special_echeancier_frais_inscription_entite_nom = obj_echeacncier_speial.entite.designation
            
            if special_echeancier_validate:
                frais_inscription = obj_echeacncier_speial.frais_inscription

            ##Id echeancier
            id_special_echeancier = obj_echeacncier_speial.id

            special_echeancier_data = []
            for i in line_echeancier_special:
                special_echeancier_data.append({
                    'id_echeancier_special' : i.id,
                    'taux' : i.taux,
                    'value' : i.value,
                    'date_echeancier' : i.date_echeancier,
                    'montant_tranche' : i.montant_tranche,
                    'entite_id' : i.entite.id if i.entite else None,
                    'entite_nom' : i.entite.designation if i.entite else None,
                })

        liste_echeancier = EcheancierPaiementLine.objects.filter(echeancier = echeancier)
        echeancier_data=[]
        for i in liste_echeancier:
            echeancier_data.append({
                'id': i.id,
                'taux' : i.taux,
                'value' : i.value,
                'montant_tranche' : i.montant_tranche,
                'date_echeancier' : i.date_echeancier,
                'entite_id' : i.entite.id if i.entite else None,
                'entite_nom' : i.entite.designation if i.entite else None,
            })

        ## Changement de d'echeancier -- a remplacer une fois valider par l'utilisateur
        if obj_echeacncier_speial and obj_echeacncier_speial.is_validate:
            echeancier_data = special_echeancier_data

        refund = Rembourssements.objects.filter(client = obj.client).last()
        refund_data = []
        if refund:
            paiements = Paiements.objects.filter(prospect = obj.client, context = "frais_f" ).aggregate(total=Sum('montant_paye'))['total'] or 0
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
                'mode_rembourssement' : refund.mode_rembourssement,
                "mode_rembourssement_label" : refund.get_mode_rembourssement_display(),
                'observation' : refund.observation, 
                'montant_paye' : paiements,
                'facture_numero': refund.facture.num_facture if refund.facture else None,
            }
        else:
            has_pending_refund = False
            refund_data = []

        user_data = {
            "demandeur_id" : obj.client.id,
            "demandeur_nom": obj.client.nom,
            "demandeur_prenom": obj.client.prenom,
            "demandeur_email" : obj.client.email,
            "demandeur_telephone" : obj.client.telephone,
            "demandeur_date_naissance" : obj.client.date_naissance if obj.client.date_naissance else "Non complété",
            "demandeur_adresse" : obj.client.adresse if obj.client.adresse else "Non complété",
            "demandeur_lieu_naissance" : obj.client.lieu_naissance if obj.client.date_naissance else "Non complété",
            "demandeur_date_inscription" : obj.client.created_at.strftime("%Y-%m-%d"),
            "statut_demandeur": obj.client.statut,
            "client_id" : obj.client.id,
            "motif": obj.get_motif_display(),
            "created_at": obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "has_printed_engagement": obj.client.has_printed_engagement,
            "engagement_printed_at": obj.client.engagement_printed_at.strftime("%Y-%m-%d %H:%M:%S") if obj.client.engagement_printed_at else None,
            "engagement_printed_by": obj.client.engagement_printed_by,
        }

        # Use resolved objects for the response
        resolved_spec_double = obj.specialite_double or (voeux.specialite if voeux else None)
        resolved_promo = obj.promo or (voeux.promo if voeux else None)

        other_data = {
            'id' : echeancierId.id,
            'modele' : echeancierId.model.label if echeancierId.model else "Sans modèle",
            'formation' : f"{echeancierId.formation_double.specialite1.label} / {echeancierId.formation_double.specialite2.label}" if echeancierId.formation_double and echeancierId.formation_double.specialite1 and echeancierId.formation_double.specialite2 else (echeancierId.formation_double.label if echeancierId.formation_double else "Double Diplomation"),
            'specialite_1' : echeancierId.formation_double.specialite1.label if echeancierId.formation_double and echeancierId.formation_double.specialite1 else "",
            'specialite_2' : echeancierId.formation_double.specialite2.label if echeancierId.formation_double and echeancierId.formation_double.specialite2 else "",
        }

        voeux_data = {
            'specialite_id' : resolved_spec_double.id if resolved_spec_double else None,
            'specialite_label' : resolved_spec_double.label if resolved_spec_double else "Non spécifié",
            'formation' : f"{resolved_spec_double.specialite1.label} / {resolved_spec_double.specialite2.label}" if resolved_spec_double and resolved_spec_double.specialite1 and resolved_spec_double.specialite2 else "Non spécifié",
            'formation_label' : "Double Diplomation",
            'promo' : resolved_promo.code if resolved_promo else "N/A",
            'prix_formation' : (resolved_spec_double.prix_spec1 or 0) + (resolved_spec_double.prix_spec2 or 0) if resolved_spec_double else 0,
            'frais_inscription' : frais_inscription,
            'date_frais_inscription': echeancierId.date_frais_inscription.strftime("%Y-%m-%d") if echeancierId and echeancierId.date_frais_inscription else None,
            'logo_header' : echeancierId.entite.entete_logo.url if echeancierId and echeancierId.entite and echeancierId.entite.entete_logo else None,
            'logo_footer' : echeancierId.entite.pied_page_logo.url if echeancierId and echeancierId.entite and echeancierId.entite.pied_page_logo else None,
        }

        specialite_data_price = {
            'prix_1' : resolved_spec_double.prix_spec1 if resolved_spec_double else 0,
            'formation_1_label' : resolved_spec_double.specialite1.formation.nom if resolved_spec_double and resolved_spec_double.specialite1 and resolved_spec_double.specialite1.formation else "",
            'specialite_1_label' : resolved_spec_double.specialite1.label if resolved_spec_double and resolved_spec_double.specialite1 else "Spécialité 1",
            'entite_1' : resolved_spec_double.specialite1.formation.entite_legal.id if resolved_spec_double and resolved_spec_double.specialite1 and resolved_spec_double.specialite1.formation and resolved_spec_double.specialite1.formation.entite_legal else None,
            'prix_2' : resolved_spec_double.prix_spec2 if resolved_spec_double else 0,
            'formation_2_label' : resolved_spec_double.specialite2.formation.nom if resolved_spec_double and resolved_spec_double.specialite2 and resolved_spec_double.specialite2.formation else "",
            'specialite_2_label' : resolved_spec_double.specialite2.label if resolved_spec_double and resolved_spec_double.specialite2 else "Spécialité 2",
            'entite_2' : resolved_spec_double.specialite2.formation.entite_legal.id if resolved_spec_double and resolved_spec_double.specialite2 and resolved_spec_double.specialite2.formation and resolved_spec_double.specialite2.formation.entite_legal else None,
        }

        # Available echeanciers for this double specialty and promo
        available_echeanciers = []
        if resolved_spec_double and resolved_promo:
            available_echeanciers = EcheancierPaiement.objects.filter(
                formation_double=resolved_spec_double,
                model__promo=resolved_promo,
                is_active=True
            ).values('id', 'model__label', 'is_default')

        data = {
            'user_data' : user_data,
            'voeux' : voeux_data,
            'frais_inscription' : frais_inscription,
            'echeancier' : list(echeancier_data),
            "has_due_paiement" : has_due_paiement,
            "due_paiement_data" : due_paiement_data,
            "total_initial" : total_initial if has_due_paiement else 0,
            "paiements_done_data" : paiements_done_data,
            "has_paiement" : has_paiement,
            "total_paiement" : total_paiement if has_paiement else 0,
            'id_echeancier' : echeancierId.id,
            'available_echeanciers': list(available_echeanciers),
            'has_saved_echeancier': obj.ref_echeancier is not None,
            "has_invoice": done_paiements.filter(is_refund=False, facture__isnull=False).exists() if has_paiement else False,
            "refund_data" : refund_data,
            "has_pending_refund" : has_pending_refund,
            'has_processed_refund'  : has_processed_refund,
            'is_appliced' : is_appliced,
            'remise' : remiseDatas,
            'echeancier_special_state_approuvel' : echeancier_state_approuvel,
            'has_special_echeancier' : has_special_echeancier,
            'special_echeancier_validate' : special_echeancier_validate,
            'special_echeancier_frais_inscription_entite_id' : special_echeancier_frais_inscription_entite_id,
            'special_echeancier_frais_inscription_entite_nom' : special_echeancier_frais_inscription_entite_nom,
            'specialite_data_price' : specialite_data_price,
            'special_echeancier_line' : special_echeancier_data,
            'echancierSpecialeId': id_special_echeancier,
            'annee_academique' : voeux.promo.annee_academique,

        }

        return JsonResponse(data ,safe=False)

    else:
        return JsonResponse({"status" : "error"})


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'add')
def ApiLoadDoubleFormation(request):
    if request.method == "GET":
        liste = DoubleDiplomation.objects.all().values(
            'id','label','prix',
            'specialite1__label','specialite1__formation__nom','specialite1__formation__entite_legal__id','prix_spec1',
            'specialite2__label','specialite2__formation__nom','specialite2__formation__entite_legal__id','prix_spec2'
        )
        return JsonResponse(list(liste), safe=False)

    else:
        return JsonResponse({"status" : "error"})

########################################## Fonction qui permet d'afficher tous les détails du demandeur de paiement ###############################

@module_permission_required('tre', 'delete')
def ApiDeleteDemandePaiement(request):
    id_demande = request.GET.get('id_demande')
    try:
        obj = ClientPaiementsRequest.objects.get(id=id_demande)
        client = obj.client
        if client:
            client.statut = 'prinscrit'
            client.save()
            
            # Log the deletion
            UserActionLog.objects.create(
                user=request.user,
                action_type='DELETE',
                target_model='ClientPaiementsRequest',
                target_id=str(obj.id),
                details=f"Suppression de la demande de paiement (Motif: {obj.get_motif_display()}) pour l'étudiant {client.nom} {client.prenom}. Statut client réinitialisé à 'Pré-inscrit'.",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
        obj.delete()
        return JsonResponse({'status' : 'success', "message" : "La suppression a été effectuée avec succès et le statut du client a été réinitialisé."})
    except ClientPaiementsRequest.DoesNotExist:
        return JsonResponse({'status' : 'error', "message" : "Demande de paiement introuvable."})
    except Exception as e:
        return JsonResponse({'status' : 'error', "message" : str(e)})

@module_permission_required('tre', 'change')
def PageConfigPaiementSeuil(request):
    return render(request, 'tenant_folder/comptabilite/tresorerie/config.html', {'tenant' : request.tenant})

@module_permission_required('tre', 'change')
def PageConfigPaiementFacturation(request):
    try:
        from t_conseil.models import ConseilConfiguration, TvaConseil
        from t_tresorerie.models import PlanComptable
        from django.contrib import messages
        from django.shortcuts import redirect
        
        config, created = ConseilConfiguration.objects.get_or_create(entreprise=None)
        
        from t_tresorerie.models import PaymentCategory, DepensesCategory
        recettes_categories = PaymentCategory.objects.all().order_by('name')
        depenses_categories = DepensesCategory.objects.all().order_by('name')
        
        if request.method == "POST":
            action = request.POST.get('action')
            if action == 'add_tva':
                label = request.POST.get('tva_label')
                valeur = request.POST.get('tva_valeur')
                if label and valeur:
                    try:
                        TvaConseil.objects.create(label=label, valeur=valeur)
                        messages.success(request, f"TVA '{label}' ajoutée avec succès.")
                    except Exception as e:
                        messages.error(request, f"Erreur : {e}")
                else:
                    messages.warning(request, "Veuillez remplir le libellé et la valeur.")
                    
            elif action == 'delete_tva':
                tva_id = request.POST.get('tva_id')
                if tva_id:
                    TvaConseil.objects.filter(id=tva_id).delete()
                    messages.success(request, "TVA supprimée.")
                    
            else:
                # Optional: handle saving default TVA
                try:
                    default_tva = request.POST.get('default_tva_percent')
                    if default_tva:
                        config.default_tva_percent = default_tva
                        
                    config.show_tva_on_devis = request.POST.get('show_tva_on_devis') == 'on'
                    config.show_tva_on_facture = request.POST.get('show_tva_on_facture') == 'on'
                    config.save()
                    messages.success(request, "Configuration mise à jour.")
                except Exception as e:
                    messages.error(request, f"Erreur : {e}")
                    
            return redirect('t_tresorerie:PageConfigPaiementFacturation')
            
        tvas = TvaConseil.objects.all().order_by('valeur')
    except ImportError:
        config = None
        tvas = []
        comptes_comptables = []
        
    from institut_app.models import Entreprise
    entreprises = Entreprise.objects.all().order_by('designation')

    return render(request, 'tenant_folder/comptabilite/tresorerie/config_paiement_facturation.html', {
        'tenant': request.tenant,
        'config': config,
        'tvas': tvas,
        'recettes_categories': recettes_categories,
        'depenses_categories': depenses_categories,
        'entreprises': entreprises,
    })

@module_permission_required('tre', 'view')
def ApiListSeuilPaiement(request):
    liste = SeuilPaiements.objects.all().values('id','specialite','specialite__label','specialite__code','label','valeur','created_at','updated_at')
    
    return JsonResponse(list(liste), safe=False)

@module_permission_required('tre', 'view')
def ApiListeSpecialite(request):
    liste = Specialites.objects.all().values('id','label','code')
    return JsonResponse(list(liste), safe=False)

@module_permission_required('tre', 'add')
def ApiAddNewSeuil(request):
    label = request.POST.get('label')
    specialite = request.POST.get('specialite')
    valeur = request.POST.get('valeur')
    if label and specialite and valeur:
        new_seuil = SeuilPaiements(
            label = label,
            specialite = Specialites.objects.get(id = specialite),
            valeur = valeur
        )
        new_seuil.save()
        return JsonResponse({'status' : 'success', 'message' : "Les données ont été enregistrées avec succès"})
    else:
        return JsonResponse({'status' : 'error', 'message' : "Veuillez remplir tous les champs"})
    
@module_permission_required('tre', 'delete')
def ApiDeleteSeuil(request):

    id = request.GET.get('id')
    if id:
        obj = SeuilPaiements.objects.get(id = id)
        obj.delete()
        return JsonResponse({'status' : 'success' , 'message' : "La suppression à été effectuer avec succès"})
    else:
        return JsonResponse({'status' : 'error' , 'message' : "Erreur, l'objet n'a pas été trouvé !"})
    
@module_permission_required('tre', 'view')
def ApiGetPaiementLine(request):
    pass


from django.db.models import Q

@module_permission_required('tre', 'view')
def ApiGetRequestPaiementsLine(request):
    id= request.GET.get('id')

    request = ClientPaiementsRequest.objects.get(id=id)
    lignes = clientPaiementsRequestLine.objects.filter(paiement_request=request).filter(Q(etat="auc") | Q(etat="part"))  
    

    data = []
    for ligne in lignes:
        data.append({
            'id': ligne.id,
            'label': ligne.get_motif_paiement_display(),  
            'montant_paye': ligne.montant_paye,
            'montant_restant': ligne.montant_restant,
            'etat' : ligne.etat,
        })

    return JsonResponse(data, safe=False)

@module_permission_required('tre', 'view')
def ApiListPaiementDone(request):
    id = request.GET.get('id')

    demande_obj = ClientPaiementsRequest.objects.get(id = id)
    listes = Paiements.objects.filter(paiement_line__paiement_request__id = demande_obj.id)

    data = []
    for liste in listes:
        data.append({
            'id' : liste.id,
            'label' : liste.paiement_line.get_motif_paiement_display(),
            'etat_label' : liste.get_etat_display(),
            'etat' : liste.etat,
            'montant_paye' : liste.montant_paye,
            'date_paiement' : liste.date_paiement,
            'observation' : liste.observation,
        })

    return JsonResponse(data, safe=False)

@transaction.atomic
@module_permission_required('tre', 'add')
def ApiStorePaiement(request):

    due_paiements = request.POST.get('due_paiements')
    date_paiement = request.POST.get('date_paiement')
    received_amount = request.POST.get('received_amount')
    observation = request.POST.get('observation')
    mode_paiement = request.POST.get('mode_paiement')
    paiement_ref = request.POST.get('paiement_ref')
    paymentType = request.POST.get('paymentType')
    
    if not due_paiements or not date_paiement or not received_amount or not mode_paiement:
        return JsonResponse({'status' : 'error', 'message' : "Veuillez remplir tous les champs"})
    else:


        paiement_line_obj = clientPaiementsRequestLine.objects.get(id = due_paiements)

        if paiement_line_obj.montant_restant >= Decimal(received_amount):

            if paiement_line_obj.montant_paye == Decimal(received_amount):
                paiement_line_obj.etat= "ter"
                paiement_line_obj.montant_restant = 0
            else:
                paiement_line_obj.etat= "part"
                paiement_line_obj.montant_restant = paiement_line_obj.montant_restant - Decimal(received_amount)
            
            if paiement_line_obj.montant_restant == 0:
                paiement_line_obj.etat = "ter"

            paiement_line_obj.save()

            new_paiement = Paiements(
                paiement_line = paiement_line_obj,
                montant_paye = received_amount,
                date_paiement = date_paiement,
                observation = observation,
                mode_paiement = mode_paiement,
                reference_paiement = paiement_ref,
                payment_type_id = paymentType if paymentType else None,
                is_done = (mode_paiement == 'esp' or mode_paiement == 'espece'),
            )

            new_paiement.save()

            if paiement_line_obj.montant_restant == 0:
                paiement_line_obj.etat = "ter"

            prospect = paiement_line_obj.paiement_request.client
            UserActionLog.objects.create(
                user=request.user,
                action_type='CREATE',
                target_model='Paiement',
                target_id=str(new_paiement.id),
                details=f"Paiement de {received_amount} DA enregistré pour {prospect.nom} {prospect.prenom} ({paiement_line_obj.get_motif_paiement_display()}).",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({'status' : 'success', 'message' : 'Le paiement a été enregistré avec succès'})
        
        elif paiement_line_obj.montant_restant < Decimal(received_amount):

            return JsonResponse({'status' : 'error', 'message' : 'Le montant payé ne peut pas être supérieur au montant restant à payer'})
        else:
            return JsonResponse({'status' : 'error', 'message' : 'Le montant payé ne peut pas être supérieur au montant restant à payer'})

@module_permission_required('tre', 'view')
def ApiDetailsReceivedPaiement(request):
    id = request.GET.get('id')

    paiement_obj = Paiements.objects.get(id = id)

    data = {
        'num': paiement_obj.num,
        'label_paiements': paiement_obj.due_paiements.label if paiement_obj.due_paiements and paiement_obj.due_paiements.label else paiement_obj.paiement_label,
        'montant_paye' : paiement_obj.montant_paye,
        'date_paiement' : paiement_obj.date_paiement,
        'observation' :  paiement_obj.observation,
        'mode_paiement' : paiement_obj.get_mode_paiement_display(),
        'reference_paiement' : paiement_obj.reference_paiement,
        'type_paiement': paiement_obj.payment_type.name if paiement_obj.payment_type else '-',
    }

    return JsonResponse(data, safe=False)

@module_permission_required('tre', 'delete')
def ApiDeletePaiement(request):
    if request.user.has_perm('t_tresorerie.delete_paiements'):
        id= request.GET.get('id')
        if id:
            obj = Paiements.objects.get(id = id)

            obj.paiement_line.montant_restant = obj.paiement_line.montant_restant + Decimal(obj.montant_paye)

            if obj.paiement_line.montant_paye == obj.paiement_line.montant_paye:
                obj.paiement_line.etat = "auc"
            else:
                obj.paiement_line.etat = "part"

            obj.paiement_line.save()
            obj.delete()
            return JsonResponse({'status' : 'success', 'message' : "La suppression a été effectuée avec succès"})
        else:
            return JsonResponse({'status' : 'error', 'message' : "Erreur, l'objet n'a pas été trouvé !"})
    else:
        return JsonResponse({'status' : 'error', 'message' : "Vous n'avez pas le droit d'effectuer cette action"})
    
@login_required(login_url='institut_app:login')
@module_permission_required('tre', 'view')
def PageRemboursement(request):
    return render(request, 'tenant_folder/comptabilite/tresorerie/remboursement.html',{'tenant' : request.tenant})

@login_required(login_url='institut_app:login')
@transaction.atomic
@module_permission_required('tre', 'view')
def ApiSetRembourssement(request):
    id = request.GET.get('id')
    paiement = Paiements.objects.get(id = id)

    paiement.etat = "dmr"
    paiement.save()

    return JsonResponse({'status' : 'success', 'message' : "La demande de remboursement a été enregistrée avec succès"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetEntrepriseDetails(request):
    id_demande = request.GET.get('id_demande')
    try:
        obj = ClientPaiementsRequest.objects.get(id=id_demande)
    except ClientPaiementsRequest.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Demande non trouvée"}, status=404)

    entreprise = None
    
    # Try FicheDeVoeux first
    voeux = FicheDeVoeux.objects.filter(prospect=obj.client, is_confirmed=True).first()
    if voeux and voeux.specialite and voeux.specialite.formation and voeux.specialite.formation.entite_legal:
        entreprise = voeux.specialite.formation.entite_legal
    
    # If not found, try FicheVoeuxDouble
    if not entreprise:
        voeux_double = FicheVoeuxDouble.objects.filter(prospect=obj.client, is_confirmed=True).first()
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

    return JsonResponse(data, safe=False)


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiCheckForPayments(request):
    if request.method == "GET":
        id_demande = request.GET.get('id_demande')
        demande = ClientPaiementsRequest.objects.get(id = id_demande)
        client = demande.client
        if client:
            paiements = Paiements.objects.filter(prospect = client)

            if paiements.exists():
                return JsonResponse({"status" : "success"})
            else:
                return JsonResponse({"status" : "error"})
        else:

            return JsonResponse({"status" : "system-error",'message' : "ID client manquant"})
    else:

        return JsonResponse({'status' : "system-error",'message' : "Methode non autoriser"})
    
@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def liste_types_depenses(request):
    return render(request, 'tenant_folder/comptabilite/depenses/type_depense.html')


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetEntite(request):
    if request.method == "GET":
        entite = Entreprise.objects.all().values("id","designation")
        return JsonResponse(list(entite), safe=False)

    else:
        return JsonResponse({"status":"error","message":"methode non autoriser"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiListeFormationsPrices(request):
    from t_formations.models import Formation
    formations = Formation.objects.all().values('id', 'nom', 'code', 'frais_inscription', 'prix_formation')
    return JsonResponse(list(formations), safe=False)

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'change')
def ApiUpdateFormationPrice(request):
    from t_formations.models import Formation
    if request.method == "POST":
        id = request.POST.get('id')
        frais = request.POST.get('frais_inscription')
        prix = request.POST.get('prix_formation')
        
        try:
            obj = Formation.objects.get(id=id)
            if frais:
                obj.frais_inscription = frais
            if prix:
                obj.prix_formation = prix
            obj.save()
            return JsonResponse({'status': 'success', 'message': 'Prix mis à jour avec succès'})
        except Formation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Formation non trouvée'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiListeSpecialitesPrices(request):
    from t_formations.models import Specialites
    formation_code = request.GET.get('formation_id')
    query = Specialites.objects.all()
    if formation_code:
        query = query.filter(formation=formation_code)
        
    specialites = query.values('id', 'label', 'code', 'prix', 'prix_double_diplomation', 'formation__nom')
    return JsonResponse(list(specialites), safe=False)

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'change')
def ApiUpdateSpecialitePrice(request):
    from t_formations.models import Specialites
    if request.method == "POST":
        id = request.POST.get('id')
        prix = request.POST.get('prix')
        prix_double = request.POST.get('prix_double_diplomation')
        
        try:
            obj = Specialites.objects.get(id=id)
            if prix:
                obj.prix = prix
            if prix_double:
                obj.prix_double_diplomation = prix_double
            obj.save()
            return JsonResponse({'status': 'success', 'message': 'Prix mis à jour avec succès'})
        except Specialites.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Spécialité non trouvée'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'change')
def ApiBulkUpdateSpecialitePrice(request):
    from t_formations.models import Specialites
    if request.method == "POST":
        ids = request.POST.getlist('ids[]')
        prix = request.POST.get('prix')
        
        if not ids:
            return JsonResponse({'status': 'error', 'message': 'Aucune spécialité sélectionnée'})
        if not prix:
            return JsonResponse({'status': 'error', 'message': 'Prix non valide'})
            
        try:
            Specialites.objects.filter(id__in=ids).update(prix=prix)
            return JsonResponse({'status': 'success', 'message': f'{len(ids)} spécialités mises à jour avec succès'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiListeDoubleDiplomationPrices(request):
    from t_formations.models import DoubleDiplomation
    combinaisons = DoubleDiplomation.objects.all().values(
        'id', 'label', 'prix', 'frais_inscription', 'prix_spec1', 'prix_spec2',
        'specialite1__label', 'specialite2__label'
    )
    return JsonResponse(list(combinaisons), safe=False)

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'change')
def ApiUpdateDoubleDiplomationPrice(request):
    from t_formations.models import DoubleDiplomation
    if request.method == "POST":
        id = request.POST.get('id')
        prix = request.POST.get('prix')
        frais = request.POST.get('frais_inscription')
        prix1 = request.POST.get('prix_spec1')
        prix2 = request.POST.get('prix_spec2')
        
        try:
            obj = DoubleDiplomation.objects.get(id=id)
            if prix:
                obj.prix = prix
            if frais:
                obj.frais_inscription = frais
            if prix1:
                obj.prix_spec1 = prix1
            if prix2:
                obj.prix_spec2 = prix2
            obj.save()
            return JsonResponse({'status': 'success', 'message': 'Prix mis à jour avec succès'})
        except DoubleDiplomation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Combinaison non trouvée'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetParametreFinancier(request):
    """Returns the current financial parameter settings."""
    import json
    params = ParametreFinancier.get_instance()
    try:
        bareme_json = json.loads(params.timbre_bareme)
    except Exception:
        bareme_json = []
    return JsonResponse({
        'bloquer_date_paiement': params.bloquer_date_paiement,
        'activer_timbre': params.activer_timbre,
        'activer_ticket_caisse': params.activer_ticket_caisse,
        'taux_timbre': str(params.taux_timbre),
        'timbre_min': str(params.timbre_min),
        'timbre_max': str(params.timbre_max),
        'timbre_cash_only': params.timbre_cash_only,
        'timbre_bareme': bareme_json,
        'relance_echeancier_sujet': params.relance_echeancier_sujet,
        'relance_echeancier_corps': params.relance_echeancier_corps,
        'compte_tva_collectee_id': params.compte_tva_collectee_id,
        'compte_tva_deductible_id': params.compte_tva_deductible_id,
        'compte_timbre_collecte_id': params.compte_timbre_collecte_id,
        'compte_timbre_charge_id': params.compte_timbre_charge_id,
    })

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'change')
def ApiUpdateParametreFinancier(request):
    """Updates the financial parameter settings."""
    if request.method == 'POST':
        import json
        params = ParametreFinancier.get_instance()
        
        bloquer = request.POST.get('bloquer_date_paiement')
        if bloquer is not None:
            params.bloquer_date_paiement = bloquer.lower() in ('true', '1', 'on')
            
        activer_timbre = request.POST.get('activer_timbre')
        if activer_timbre is not None:
            params.activer_timbre = activer_timbre.lower() in ('true', '1', 'on')
            
        activer_ticket_caisse = request.POST.get('activer_ticket_caisse')
        if activer_ticket_caisse is not None:
            params.activer_ticket_caisse = activer_ticket_caisse.lower() in ('true', '1', 'on')
            
        taux = request.POST.get('taux_timbre')
        if taux is not None:
            params.taux_timbre = taux
            
        t_min = request.POST.get('timbre_min')
        if t_min is not None:
            params.timbre_min = t_min
            
        t_max = request.POST.get('timbre_max')
        if t_max is not None:
            params.timbre_max = t_max
            
        cash_only = request.POST.get('timbre_cash_only')
        if cash_only is not None:
            params.timbre_cash_only = cash_only.lower() in ('true', '1', 'on')

        bareme = request.POST.get('timbre_bareme')
        if bareme is not None:
            try:
                # Validate JSON structure
                json.loads(bareme)
                params.timbre_bareme = bareme
            except json.JSONDecodeError:
                pass
                
        compte_tva_collectee_id = request.POST.get('compte_tva_collectee_id')
        if compte_tva_collectee_id is not None:
            params.compte_tva_collectee_id = compte_tva_collectee_id if compte_tva_collectee_id else None
            
        compte_tva_deductible_id = request.POST.get('compte_tva_deductible_id')
        if compte_tva_deductible_id is not None:
            params.compte_tva_deductible_id = compte_tva_deductible_id if compte_tva_deductible_id else None
            
        compte_timbre_collecte_id = request.POST.get('compte_timbre_collecte_id')
        if compte_timbre_collecte_id is not None:
            params.compte_timbre_collecte_id = compte_timbre_collecte_id if compte_timbre_collecte_id else None
            
        compte_timbre_charge_id = request.POST.get('compte_timbre_charge_id')
        if compte_timbre_charge_id is not None:
            params.compte_timbre_charge_id = compte_timbre_charge_id if compte_timbre_charge_id else None

        # Relance Echeancier
        sujet = request.POST.get('relance_echeancier_sujet')
        if sujet is not None:
            params.relance_echeancier_sujet = sujet

        relance_corps = request.POST.get('relance_echeancier_corps')
        if relance_corps is not None:
            params.relance_echeancier_corps = relance_corps
            
        params.save()
        return JsonResponse({
            'status': 'success', 
            'bloquer_date_paiement': params.bloquer_date_paiement,
            'activer_timbre': params.activer_timbre
        })
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@module_permission_required('tre', 'change')
def ApiUpdateQuittanceFormat(request):
    if request.method == 'POST':
        try:
            entreprise_id = request.POST.get('entreprise_id')
            format_str = request.POST.get('quittance_format', 'N°{seq}/ST/{entite}/{wilaya}/{annexe}/{mois}/{annee}')
            seq_length = int(request.POST.get('quittance_sequence_length', 6))
            from institut_app.models import Entreprise
            entreprise = Entreprise.objects.get(id=entreprise_id)
            entreprise.quittance_format = format_str
            entreprise.quittance_sequence_length = seq_length
            entreprise.save()
            return JsonResponse({'status': 'success', 'message': 'Format mis à jour avec succès'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})
