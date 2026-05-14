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
            # Total paid = Base_TTC + Timbre
            # Timbre = round(Base_TTC * 0.01, 0)
            
            # First guess
            base_ttc = montant_paye / (Decimal('1') + (config_fin.taux_timbre / Decimal('100')))
            timbre = Decimal('0')
            
            # Refinement loop to handle rounding/thresholds of timbre
            for _ in range(3):
                # Calculate timbre based on current base_ttc guess
                t_val = base_ttc * (config_fin.taux_timbre / Decimal('100'))
                if t_val < config_fin.timbre_min: t_val = config_fin.timbre_min
                elif t_val > config_fin.timbre_max: t_val = config_fin.timbre_max
                timbre = t_val.quantize(Decimal('1'))
                
                base_ttc = montant_paye - timbre
            
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
