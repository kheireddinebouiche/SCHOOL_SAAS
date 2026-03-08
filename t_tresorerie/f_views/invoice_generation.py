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
            paiement = Paiements.objects.get(num=paiement_id) # The frontend uses 'num' as ID in data-id attribute
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
        # ... (rest of the code)
        description = paiement.paiement_label or "Paiement"
        if paiement.observation:
            description += f" - {paiement.observation}"
        
        montant_ttc = paiement.montant_paye
        montant_ht = montant_ttc / (1 + (tva_decimal / 100))
        
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
