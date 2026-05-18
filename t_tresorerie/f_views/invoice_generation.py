from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from t_tresorerie.models import Paiements
from t_conseil.models import Facture, LignesFacture, ConseilConfiguration
from decimal import Decimal
import datetime

@login_required
@require_POST
def generate_invoice_from_payment(request):
    try:
        paiement_id = request.POST.get('paiement_id')
        tva_percent = request.POST.get('tva_percent')
        show_tva = request.POST.get('show_tva', 'true').lower() == 'true'

        if not paiement_id:
            return JsonResponse({'status': 'error', 'message': 'ID de paiement manquant'})
        
        if show_tva and not tva_percent:
             return JsonResponse({'status': 'error', 'message': 'TVA manquante'})

        try:
            paiement = Paiements.objects.get(id=paiement_id)
        except Paiements.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Paiement introuvable'})

        # 1. Determine Enterprise (Entite)
        entite = paiement.entite
        
        if not entite:
             return JsonResponse({'status': 'error', 'message': 'L\'entité émettrice n\'est pas renseignée pour ce paiement.'})

        # 2. Determine Client
        # User rule: "le client est le prospet concerne par le paiement"
        client = paiement.prospect
        if not client:
             return JsonResponse({'status': 'error', 'message': 'Client introuvable lié à ce paiement'})

        # Check if invoice already exists for this payment
        if paiement.facture:
             return JsonResponse({'status': 'error', 'message': 'Une facture a déjà été générée pour ce paiement', 'num_facture': paiement.facture.num_facture})

        # 3. Create Facture
        tva_decimal = Decimal(tva_percent) if show_tva else Decimal('0')

        facture = Facture(
            client=client,
            entreprise=entite,
            date_emission=datetime.date.today(),
            date_echeance=datetime.date.today(),
            tva=tva_decimal,
            show_tva=show_tva,
            mode_paiement='virement',
            etat='paye',
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
        
        montant_paye = Decimal(str(paiement.montant_paye))
        
        # Reverse calculate HT and TVA, accounting for potential Stamp Duty
        from t_tresorerie.models import ParametreFinancier
        config_fin = ParametreFinancier.get_instance()
        
        apply_timbre = False
        if config_fin.activer_timbre:
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
        montant_ht = montant_ht.quantize(Decimal('0.01'))
        
        if apply_timbre:
            facture.montant_timbre = timbre
            facture.save()
        
        ligne = LignesFacture(
            facture=facture,
            description=description,
            quantite=1,
            prix_unitaire=montant_ht,
            montant_ht=montant_ht,
            tva_percent=tva_decimal,
            remise_percent=0
        )
        ligne.save()

        return JsonResponse({'status': 'success', 'message': 'Facture générée avec succès', 'num_facture': facture.num_facture})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
