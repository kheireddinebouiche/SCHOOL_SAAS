from institut_app.decorators import module_permission_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from t_tresorerie.models import Paiements
from t_conseil.models import Facture, LignesFacture, ConseilConfiguration
from decimal import Decimal, ROUND_HALF_UP
import datetime

def get_client_voeux_info(client, entite=None):
    from t_crm.models import FicheDeVoeux, FicheVoeuxDouble
    if not client:
        return ""
    if client.is_double:
        voeux = FicheVoeuxDouble.objects.filter(prospect=client, is_confirmed=True).select_related('specialite__specialite1__formation', 'specialite__specialite2__formation').first()
        if not voeux:
            voeux = FicheVoeuxDouble.objects.filter(prospect=client).select_related('specialite__specialite1__formation', 'specialite__specialite2__formation').first()
        if voeux and voeux.specialite:
            if entite:
                if voeux.specialite.specialite1 and voeux.specialite.specialite1.formation and voeux.specialite.specialite1.formation.entite_legal == entite:
                    return f" ({voeux.specialite.specialite1.formation.nom} - {voeux.specialite.specialite1.label})"
                if voeux.specialite.specialite2 and voeux.specialite.specialite2.formation and voeux.specialite.specialite2.formation.entite_legal == entite:
                    return f" ({voeux.specialite.specialite2.formation.nom} - {voeux.specialite.specialite2.label})"
            
            f1 = voeux.specialite.specialite1.formation.nom if voeux.specialite.specialite1 and voeux.specialite.specialite1.formation else ""
            f2 = voeux.specialite.specialite2.formation.nom if voeux.specialite.specialite2 and voeux.specialite.specialite2.formation else ""
            formations = " / ".join([f for f in [f1, f2] if f])
            if formations:
                return f" ({formations} - {voeux.specialite.label})"
            return f" ({voeux.specialite.label})"
    else:
        voeux = FicheDeVoeux.objects.filter(prospect=client, is_confirmed=True).select_related('specialite__formation').first()
        if not voeux:
            voeux = FicheDeVoeux.objects.filter(prospect=client).select_related('specialite__formation').first()
        if voeux and voeux.specialite:
            formation_nom = voeux.specialite.formation.nom if voeux.specialite.formation else ""
            return f" ({formation_nom} - {voeux.specialite.label})"
    return ""

def create_invoice_from_payment_object(paiement, tva_percent, show_tva, skip_timbre):
    # 1. Determine Enterprise (Entite)
    entite = paiement.entite
    
    if not entite:
         raise Exception("L'entité émettrice n'est pas renseignée pour ce paiement.")

    # 2. Determine Client
    # User rule: "le client est le prospet concerne par le paiement"
    client = paiement.prospect
    if not client:
         raise Exception("Client introuvable lié à ce paiement")

    # Check if invoice already exists for this payment
    if paiement.facture:
         raise Exception(f"Une facture a déjà été générée pour ce paiement (N° {paiement.facture.num_facture})")

    # 3. Create Facture
    tva_decimal = Decimal(str(tva_percent)) if show_tva and tva_percent else Decimal('0')

    facture = Facture(
        client=client,
        entreprise=entite,
        date_emission=datetime.date.today(),
        date_echeance=datetime.date.today(),
        tva=tva_decimal,
        show_tva=show_tva,
        mode_paiement='virement',
        etat='brouillon',
        module_source='tresorerie',
    )
    # Map payment mode
    mode_map = {
        'vir': 'virement',
        'che': 'cheque',
        'esp': 'espece',
        'autre': 'autre'
    }
    facture.mode_paiement = mode_map.get(paiement.mode_paiement, 'autre')
    
    facture.save() # This triggers num_facture generation

    # Link payment to facture
    paiement.facture = facture
    paiement.save()

    # 4. Create LigneFacture
    description = paiement.paiement_label or "Paiement"
    if paiement.observation:
        description += f" - {paiement.observation}"
    
    voeux_info = get_client_voeux_info(client, entite=entite)
    long_desc = ""
    if voeux_info:
        long_desc = voeux_info.strip(' ()')
    
    montant_paye = Decimal(str(paiement.montant_paye))
    
    # Reverse calculate HT and TVA, accounting for potential Stamp Duty
    from t_tresorerie.models import ParametreFinancier
    config_fin = ParametreFinancier.get_instance()
    
    apply_timbre = False
    if not skip_timbre:
        if config_fin.activer_timbre or paiement.mode_paiement == 'esp':
            # We use the same condition as Facture.get_timbre()
            if not config_fin.timbre_cash_only or paiement.mode_paiement == 'esp':
                apply_timbre = True
    
    if apply_timbre:
        # Under LF 2025/Dynamic configuration: Total paid (montant_paye) = base_ttc + timbre
        # We use an iterative numerical refinement loop to find the exact base_ttc
        import math
        import json
        
        # Load and parse the bareme JSON from config
        try:
            bareme = json.loads(config_fin.timbre_bareme)
        except Exception:
            bareme = [
                {"min_ttc": 0, "max_ttc": 300, "rate": 0.0, "is_exempt": True},
                {"min_ttc": 301, "max_ttc": 30000, "rate": 1.0, "is_exempt": False},
                {"min_ttc": 30001, "max_ttc": 100000, "rate": 1.5, "is_exempt": False},
                {"min_ttc": 100001, "max_ttc": None, "rate": 2.0, "is_exempt": False}
            ]
        
        # Ensure sort order by min_ttc
        bareme = sorted(bareme, key=lambda b: b.get('min_ttc', 0))
        
        # Helper to calculate timbre for a given ttc_brut and rate
        def calculate_timbre_for_bracket(ttc_val, bracket_rate, is_ex):
            if is_ex or bracket_rate == Decimal('0'):
                return Decimal('0')
            nb_t = Decimal(str(math.ceil(ttc_val / 100)))
            raw_timbre = nb_t * bracket_rate
            min_stamp = max(config_fin.timbre_min, Decimal('5'))
            if raw_timbre < min_stamp:
                raw_timbre = min_stamp
            return Decimal(str(math.ceil(raw_timbre)))
            
        # 1. Tranche Detection to avoid boundary oscillations
        selected_bracket = None
        for b in bareme:
            min_ttc = Decimal(str(b.get('min_ttc', 0)))
            max_ttc = b.get('max_ttc')
            rate_val = Decimal(str(b.get('rate', 0.0)))
            is_ex = b.get('is_exempt', rate_val == Decimal('0'))
            
            # Check range in terms of total paid amount (min_ttc + timbre_at_min, max_ttc + timbre_at_max)
            t_min = calculate_timbre_for_bracket(min_ttc, rate_val, is_ex)
            paye_min = min_ttc + t_min
            
            if max_ttc is not None:
                max_ttc = Decimal(str(max_ttc))
                t_max = calculate_timbre_for_bracket(max_ttc, rate_val, is_ex)
                paye_max = max_ttc + t_max
                if paye_min <= montant_paye <= paye_max:
                    selected_bracket = b
                    break
            else:
                if montant_paye >= paye_min:
                    selected_bracket = b
                    break
                    
        if not selected_bracket:
            selected_bracket = bareme[-1]
            
        bracket_rate = Decimal(str(selected_bracket.get('rate', 0.0)))
        is_ex = selected_bracket.get('is_exempt', bracket_rate == Decimal('0'))
        
        # Start loop with a robust estimation
        base_ttc = montant_paye - calculate_timbre_for_bracket(montant_paye, bracket_rate, is_ex)
        
        # 5 iterations are guaranteed to perfectly converge within the correct bracket range
        for _ in range(5):
            timbre = calculate_timbre_for_bracket(base_ttc, bracket_rate, is_ex)
            base_ttc = montant_paye - timbre
            
        # Final verification of dynamic timbre
        timbre = calculate_timbre_for_bracket(base_ttc, bracket_rate, is_ex)
        
        # Now we have base_ttc = HT + TVA
        # HT = base_ttc / (1 + TVA_percent / 100)
        montant_ht = base_ttc / (Decimal('1') + (tva_decimal / Decimal('100')))
    else:
        # No timbre, just standard reverse TVA
        montant_ht = montant_paye / (Decimal('1') + (tva_decimal / Decimal('100')))
    
    # Round HT to 2 decimal places as it's stored in DecimalField(10, 2)
    montant_ht = montant_ht.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    if apply_timbre:
        facture.montant_timbre = timbre
        facture.save()
    
    ligne = LignesFacture(
        facture=facture,
        description=description,
        long_description=long_desc,
        quantite=1,
        prix_unitaire=montant_ht,
        montant_ht=montant_ht,
        tva_percent=tva_decimal,
        remise_percent=0
    )
    ligne.save()
    return facture


@login_required
@require_POST
@module_permission_required('tre', 'add')
def generate_invoice_from_payment(request):
    try:
        paiement_id = request.POST.get('paiement_id')
        tva_percent = request.POST.get('tva_percent')
        show_tva = request.POST.get('show_tva', 'true').lower() == 'true'
        skip_timbre = request.POST.get('skip_timbre', 'false').lower() == 'true'

        if not paiement_id:
            return JsonResponse({'status': 'error', 'message': 'ID de paiement manquant'})
        
        if show_tva and not tva_percent:
             return JsonResponse({'status': 'error', 'message': 'TVA manquante'})

        try:
            paiement = Paiements.objects.get(id=paiement_id)
        except Paiements.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Paiement introuvable'})

        facture = create_invoice_from_payment_object(paiement, tva_percent, show_tva, skip_timbre)
        return JsonResponse({'status': 'success', 'message': 'Facture générée avec succès', 'num_facture': facture.num_facture})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
@require_POST
@module_permission_required('tre', 'add')
def generate_consolidated_invoice(request):
    try:
        prospect_id = request.POST.get('prospect_id')
        payment_ids_str = request.POST.get('payment_ids')
        tva_percent = request.POST.get('tva_percent')
        show_tva = request.POST.get('show_tva', 'true').lower() == 'true'
        skip_timbre = request.POST.get('skip_timbre', 'false').lower() == 'true'
        consolidation_mode = request.POST.get('consolidation_mode', 'multi_line')

        if not prospect_id:
            return JsonResponse({'status': 'error', 'message': 'ID de prospect manquant'})
        if not payment_ids_str:
            return JsonResponse({'status': 'error', 'message': 'Aucun paiement sélectionné'})
        if show_tva and not tva_percent:
             return JsonResponse({'status': 'error', 'message': 'TVA manquante'})

        payment_ids = [int(x.strip()) for x in payment_ids_str.split(',') if x.strip()]
        payments = Paiements.objects.filter(id__in=payment_ids, facture__isnull=True)
        if not payments.exists():
            return JsonResponse({'status': 'error', 'message': 'Aucun paiement non facturé sélectionné'})

        first_payment = payments.first()
        entite = first_payment.entite
        client = first_payment.prospect
        
        if not entite:
             return JsonResponse({'status': 'error', 'message': 'L\'entité émettrice n\'est pas renseignée.'})
        if not client:
             return JsonResponse({'status': 'error', 'message': 'Client introuvable lié aux paiements'})

        has_cash_payment = payments.filter(mode_paiement='esp').exists()

        mode_map = {
            'vir': 'virement',
            'che': 'cheque',
            'esp': 'espece',
            'autre': 'autre'
        }
        if has_cash_payment:
            main_payment_mode = 'espece'
        else:
            main_payment_mode = mode_map.get(first_payment.mode_paiement, 'autre')

        tva_decimal = Decimal(tva_percent) if show_tva else Decimal('0')
        facture = Facture(
            client=client,
            entreprise=entite,
            date_emission=datetime.date.today(),
            date_echeance=datetime.date.today(),
            tva=tva_decimal,
            show_tva=show_tva,
            mode_paiement=main_payment_mode,
            etat='brouillon',
            module_source='tresorerie',
        )
        facture.save()

        # Link all payments to this consolidated facture
        for p in payments:
            p.facture = facture
            p.save()

        from t_tresorerie.models import ParametreFinancier
        config_fin = ParametreFinancier.get_instance()

        def get_ht_amount(montant_paye, mode_paye):
            apply_timbre = False
            if not skip_timbre:
                if config_fin.activer_timbre or mode_paye == 'esp':
                    if not config_fin.timbre_cash_only or mode_paye == 'esp':
                        apply_timbre = True
            
            if apply_timbre:
                import math
                import json
                try:
                    bareme = json.loads(config_fin.timbre_bareme)
                except Exception:
                    bareme = [
                        {"min_ttc": 0, "max_ttc": 300, "rate": 0.0, "is_exempt": True},
                        {"min_ttc": 301, "max_ttc": 30000, "rate": 1.0, "is_exempt": False},
                        {"min_ttc": 30001, "max_ttc": 100000, "rate": 1.5, "is_exempt": False},
                        {"min_ttc": 100001, "max_ttc": None, "rate": 2.0, "is_exempt": False}
                    ]
                bareme = sorted(bareme, key=lambda b: b.get('min_ttc', 0))
                
                def calculate_timbre_for_bracket(ttc_val, bracket_rate, is_ex):
                    if is_ex or bracket_rate == Decimal('0'):
                        return Decimal('0')
                    nb_t = Decimal(str(math.ceil(ttc_val / 100)))
                    raw_timbre = nb_t * bracket_rate
                    min_stamp = max(config_fin.timbre_min, Decimal('5'))
                    if raw_timbre < min_stamp:
                        raw_timbre = min_stamp
                    return Decimal(str(math.ceil(raw_timbre)))
                
                selected_bracket = None
                for b in bareme:
                    min_ttc = Decimal(str(b.get('min_ttc', 0)))
                    max_ttc = b.get('max_ttc')
                    rate_val = Decimal(str(b.get('rate', 0.0)))
                    is_ex_val = b.get('is_exempt', rate_val == Decimal('0'))
                    
                    t_min = calculate_timbre_for_bracket(min_ttc, rate_val, is_ex_val)
                    paye_min = min_ttc + t_min
                    
                    if max_ttc is not None:
                        max_ttc = Decimal(str(max_ttc))
                        t_max = calculate_timbre_for_bracket(max_ttc, rate_val, is_ex_val)
                        paye_max = max_ttc + t_max
                        if paye_min <= montant_paye <= paye_max:
                            selected_bracket = b
                            break
                    else:
                        if montant_paye >= paye_min:
                            selected_bracket = b
                            break
                            
                if not selected_bracket:
                    selected_bracket = bareme[-1]
                    
                bracket_rate = Decimal(str(selected_bracket.get('rate', 0.0)))
                is_ex_bracket = selected_bracket.get('is_exempt', bracket_rate == Decimal('0'))
                
                base_ttc = montant_paye - calculate_timbre_for_bracket(montant_paye, bracket_rate, is_ex_bracket)
                for _ in range(5):
                    timbre_val = calculate_timbre_for_bracket(base_ttc, bracket_rate, is_ex_bracket)
                    base_ttc = montant_paye - timbre_val
                
                timbre_final = calculate_timbre_for_bracket(base_ttc, bracket_rate, is_ex_bracket)
                montant_ht = base_ttc / (Decimal('1') + (tva_decimal / Decimal('100')))
                return montant_ht.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), timbre_final
            else:
                montant_ht = montant_paye / (Decimal('1') + (tva_decimal / Decimal('100')))
                return montant_ht.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), Decimal('0')

        total_timbre = Decimal('0')

        if consolidation_mode == 'single_line':
            sum_montant_paye = sum(Decimal(str(p.montant_paye)) for p in payments)
            consolidated_mode = 'esp' if has_cash_payment else first_payment.mode_paiement
            montant_ht, timbre_val = get_ht_amount(sum_montant_paye, consolidated_mode)
            total_timbre = timbre_val

            description = f"Consolidation globale de {payments.count()} paiements"
            promos = list(set(p.promo.code for p in payments if p.promo))
            if promos:
                description += f" - Promotions: {', '.join(promos)}"
            voeux_info = get_client_voeux_info(client, entite=entite)
            long_desc = ""
            if voeux_info:
                long_desc = voeux_info.strip(' ()')

            ligne = LignesFacture(
                facture=facture,
                description=description,
                long_description=long_desc,
                quantite=1,
                prix_unitaire=montant_ht,
                montant_ht=montant_ht,
                tva_percent=tva_decimal,
                remise_percent=0
            )
            ligne.save()
        else:
            for p in payments:
                p_montant_paye = Decimal(str(p.montant_paye))
                montant_ht, timbre_val = get_ht_amount(p_montant_paye, p.mode_paiement)
                total_timbre += timbre_val

                desc = p.paiement_label or "Paiement"
                if p.promo:
                    desc += f" (Promo: {p.promo.code})"
                if p.observation:
                    desc += f" - {p.observation}"
                voeux_info = get_client_voeux_info(client, entite=p.entite)
                long_desc = ""
                if voeux_info:
                    long_desc = voeux_info.strip(' ()')

                ligne = LignesFacture(
                    facture=facture,
                    description=desc,
                    long_description=long_desc,
                    quantite=1,
                    prix_unitaire=montant_ht,
                    montant_ht=montant_ht,
                    tva_percent=tva_decimal,
                    remise_percent=0
                )
                ligne.save()

        if total_timbre > 0:
            facture.montant_timbre = total_timbre
            facture.save()

        return JsonResponse({
            'status': 'success', 
            'message': 'Facture consolidée générée avec succès', 
            'num_facture': facture.num_facture
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
@require_POST
@module_permission_required('tre', 'change')
def ApiUpdateDraftInvoice(request):
    try:
        facture_id = request.POST.get('facture_id')
        payment_ids_str = request.POST.get('payment_ids')
        tva_percent = request.POST.get('tva_percent')
        show_tva = request.POST.get('show_tva', 'true').lower() == 'true'
        skip_timbre = request.POST.get('skip_timbre', 'false').lower() == 'true'
        consolidation_mode = request.POST.get('consolidation_mode', 'multi_line')
        
        client_nom_override = request.POST.get('client_nom_override', '')
        client_prenom_override = request.POST.get('client_prenom_override', '')
        client_nin_override = request.POST.get('client_nin_override', '')

        if not facture_id:
            return JsonResponse({'status': 'error', 'message': 'ID de facture manquant'})
        if not payment_ids_str:
            return JsonResponse({'status': 'error', 'message': 'Aucun paiement sélectionné'})
        if show_tva and not tva_percent:
             return JsonResponse({'status': 'error', 'message': 'TVA manquante'})

        try:
            facture = Facture.objects.get(id=facture_id, module_source='tresorerie')
        except Facture.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Facture introuvable'})

        payment_ids = [int(x.strip()) for x in payment_ids_str.split(',') if x.strip()]
        
        # Check if the payments are valid: either null or already linked to THIS invoice
        payments = Paiements.objects.filter(id__in=payment_ids).select_related('prospect', 'promo', 'entite')
        if not payments.exists():
            return JsonResponse({'status': 'error', 'message': 'Aucun paiement trouvé'})

        for p in payments:
            if p.facture and p.facture.id != facture.id:
                return JsonResponse({'status': 'error', 'message': f'Le règlement {p.num or p.id} est déjà associé à la facture {p.facture.num_facture}'})

        first_payment = payments.first()
        entite = first_payment.entite
        client = first_payment.prospect
        
        if not entite:
             return JsonResponse({'status': 'error', 'message': 'L\'entité émettrice n\'est pas renseignée.'})
        if not client:
             return JsonResponse({'status': 'error', 'message': 'Client introuvable lié aux paiements'})

        has_cash_payment = payments.filter(mode_paiement='esp').exists()

        mode_map = {
            'vir': 'virement',
            'che': 'cheque',
            'esp': 'espece',
            'autre': 'autre'
        }
        if has_cash_payment:
            main_payment_mode = 'espece'
        else:
            main_payment_mode = mode_map.get(first_payment.mode_paiement, 'autre')

        tva_decimal = Decimal(tva_percent) if show_tva else Decimal('0')

        from django.db import transaction
        with transaction.atomic():
            # Update Facture attributes
            facture.tva = tva_decimal
            facture.show_tva = show_tva
            facture.mode_paiement = main_payment_mode
            facture.client_nom_override = client_nom_override if client_nom_override else None
            facture.client_prenom_override = client_prenom_override if client_prenom_override else None
            facture.client_nin_override = client_nin_override if client_nin_override else None
            
            # Reset relations for existing payments
            facture.tresorerie_paiements.update(facture=None)
            
            # Delete old LignesFacture
            facture.lignes_facture.all().delete()
            
            # Link newly selected payments
            for p in payments:
                p.facture = facture
                p.save()

            from t_tresorerie.models import ParametreFinancier
            config_fin = ParametreFinancier.get_instance()

            def get_ht_amount(montant_paye, mode_paye):
                apply_timbre = False
                if not skip_timbre:
                    if config_fin.activer_timbre or mode_paye == 'esp':
                        if not config_fin.timbre_cash_only or mode_paye == 'esp':
                            apply_timbre = True
                
                if apply_timbre:
                    import math
                    import json
                    try:
                        bareme = json.loads(config_fin.timbre_bareme)
                    except Exception:
                        bareme = [
                            {"min_ttc": 0, "max_ttc": 300, "rate": 0.0, "is_exempt": True},
                            {"min_ttc": 301, "max_ttc": 30000, "rate": 1.0, "is_exempt": False},
                            {"min_ttc": 30001, "max_ttc": 100000, "rate": 1.5, "is_exempt": False},
                            {"min_ttc": 100001, "max_ttc": None, "rate": 2.0, "is_exempt": False}
                        ]
                    bareme = sorted(bareme, key=lambda b: b.get('min_ttc', 0))
                    
                    def calculate_timbre_for_bracket(ttc_val, bracket_rate, is_ex):
                        if is_ex or bracket_rate == Decimal('0'):
                            return Decimal('0')
                        nb_t = Decimal(str(math.ceil(ttc_val / 100)))
                        raw_timbre = nb_t * bracket_rate
                        min_stamp = max(config_fin.timbre_min, Decimal('5'))
                        if raw_timbre < min_stamp:
                            raw_timbre = min_stamp
                        return Decimal(str(math.ceil(raw_timbre)))
                    
                    selected_bracket = None
                    for b in bareme:
                        min_ttc = Decimal(str(b.get('min_ttc', 0)))
                        max_ttc = b.get('max_ttc')
                        rate_val = Decimal(str(b.get('rate', 0.0)))
                        is_ex_val = b.get('is_exempt', rate_val == Decimal('0'))
                        
                        t_min = calculate_timbre_for_bracket(min_ttc, rate_val, is_ex_val)
                        paye_min = min_ttc + t_min
                        
                        if max_ttc is not None:
                            max_ttc = Decimal(str(max_ttc))
                            t_max = calculate_timbre_for_bracket(max_ttc, rate_val, is_ex_val)
                            paye_max = max_ttc + t_max
                            if paye_min <= montant_paye <= paye_max:
                                selected_bracket = b
                                break
                        else:
                            if montant_paye >= paye_min:
                                selected_bracket = b
                                break
                                
                    if not selected_bracket:
                        selected_bracket = bareme[-1]
                        
                    bracket_rate = Decimal(str(selected_bracket.get('rate', 0.0)))
                    is_ex_bracket = selected_bracket.get('is_exempt', bracket_rate == Decimal('0'))
                    
                    base_ttc = montant_paye - calculate_timbre_for_bracket(montant_paye, bracket_rate, is_ex_bracket)
                    for _ in range(5):
                        timbre_val = calculate_timbre_for_bracket(base_ttc, bracket_rate, is_ex_bracket)
                        base_ttc = montant_paye - timbre_val
                    
                    timbre_final = calculate_timbre_for_bracket(base_ttc, bracket_rate, is_ex_bracket)
                    montant_ht = base_ttc / (Decimal('1') + (tva_decimal / Decimal('100')))
                    return montant_ht.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), timbre_final
                else:
                    montant_ht = montant_paye / (Decimal('1') + (tva_decimal / Decimal('100')))
                    return montant_ht.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), Decimal('0')

            total_timbre = Decimal('0')

            if consolidation_mode == 'single_line':
                sum_montant_paye = sum(Decimal(str(p.montant_paye)) for p in payments)
                consolidated_mode = 'esp' if has_cash_payment else first_payment.mode_paiement
                montant_ht, timbre_val = get_ht_amount(sum_montant_paye, consolidated_mode)
                total_timbre = timbre_val

                description = f"Consolidation globale de {payments.count()} paiements"
                promos = list(set(p.promo.code for p in payments if p.promo))
                if promos:
                    description += f" - Promotions: {', '.join(promos)}"
                voeux_info = get_client_voeux_info(client)
                if voeux_info:
                    description += voeux_info

                au_profit_text = ""
                if facture.client_nom_override:
                    au_profit_text = f" (Au profit de : {client.nom} {client.prenom or ''})".strip()
                    description += f" {au_profit_text}"

                ligne = LignesFacture(
                    facture=facture,
                    description=description,
                    long_description="",
                    quantite=1,
                    prix_unitaire=montant_ht,
                    montant_ht=montant_ht,
                    tva_percent=tva_decimal,
                    remise_percent=0
                )
                ligne.save()
            else:
                for p in payments:
                    p_montant_paye = Decimal(str(p.montant_paye))
                    montant_ht, timbre_val = get_ht_amount(p_montant_paye, p.mode_paiement)
                    total_timbre += timbre_val

                    desc = p.paiement_label or "Paiement"
                    if p.promo:
                        desc += f" (Promo: {p.promo.code})"
                    if p.observation:
                        desc += f" - {p.observation}"
                    voeux_info = get_client_voeux_info(client)
                    if voeux_info:
                        desc += voeux_info

                    au_profit_text = ""
                    if facture.client_nom_override:
                        au_profit_text = f" (Au profit de : {client.nom} {client.prenom or ''})".strip()
                        desc += f" {au_profit_text}"

                    ligne = LignesFacture(
                        facture=facture,
                        description=desc,
                        long_description="",
                        quantite=1,
                        prix_unitaire=montant_ht,
                        montant_ht=montant_ht,
                        tva_percent=tva_decimal,
                        remise_percent=0
                    )
                    ligne.save()

            facture.montant_timbre = total_timbre
            facture.save()

        return JsonResponse({
            'status': 'success', 
            'message': 'Facture brouillon mise à jour avec succès', 
            'num_facture': facture.num_facture
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': repr(e)})
