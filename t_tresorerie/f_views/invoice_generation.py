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

        if not paiement_id:
            return JsonResponse({'status': 'error', 'message': 'ID de paiement manquant'})
        
        if not tva_percent:
             return JsonResponse({'status': 'error', 'message': 'TVA manquante'})

        try:
            paiement = Paiements.objects.get(num=paiement_id) # The frontend uses 'num' as ID in data-id attribute
        except Paiements.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Paiement introuvable'})

        # 1. Determine Enterprise (Entite)
        # User rule: "pour l'entite emettrice prend l'entite du paiement"
        entite = None
        if paiement.due_paiements and paiement.due_paiements.entite:
            entite = paiement.due_paiements.entite
        elif paiement.refund_id and paiement.refund_id.entite:
            entite = paiement.refund_id.entite
        
        # If still no entity, try to trace back through logic in Paiements.save()
        if not entite and paiement.due_paiements and paiement.due_paiements.ref_echeancier and paiement.due_paiements.ref_echeancier.entite:
             entite = paiement.due_paiements.ref_echeancier.entite
        
        if not entite:
             return JsonResponse({'status': 'error', 'message': 'Impossible de déterminer l\'entité émettrice du paiement'})

        # 2. Determine Client
        # User rule: "le client est le prospet concerne par le paiement"
        client = paiement.prospect
        if not client:
             return JsonResponse({'status': 'error', 'message': 'Client introuvable lié à ce paiement'})

        # 3. Create Facture
        # Check if invoice already exists for this payment? 
        # The user didn't specify, but it's good practice. However, "Paiements" side doesn't have a direct link to "Facture" unless we add one or check if there is a Facture linked to this payment.
        # Wait, the `Paiement` model in `t_conseil` has a foreign key to `Facture`. But `t_tresorerie.Paiements` is different.
        # We are generating a `t_conseil.Facture` from `t_tresorerie.Paiements`.
        # Accessing `t_conseil` models.
        
        tva_decimal = Decimal(tva_percent)

        facture = Facture(
            client=client,
            entreprise=entite,
            date_emission=datetime.date.today(),
            date_echeance=datetime.date.today(), # Paid immediately essentially, or match payment date? User didn't specify, implies "now".
            tva=tva_decimal,
            show_tva=True, # Assuming yes since we are selecting TVA
            mode_paiement='virement', # Default or map from paiement.mode_paiement
            etat='paye', # Since it comes from a payment, it should be paid?
            module_source='tresorerie',
            # Or 'battente' if they want to manage it? 
            # "la ligne de la facture est la meme que le paiement effectuer" -> It reflects a payment.
            # Let's set it to 'paye' or 'envoye'. 'paye' makes more sense if it's already paid. 
            # Actually, `t_conseil.Facture` doesn't have a direct "related payment" link to `t_tresorerie.Paiements`.
            # We will just create the invoice.
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

        # 4. Create LigneFacture
        # "la ligne de la facture est la meme que le paiement effectuer en enlevant le n° du reçue"
        # The payment label/description
        description = paiement.paiement_label or "Paiement"
        if paiement.observation:
            description += f" - {paiement.observation}"
        
        # Payment amount is typically TTC.
        # If user selects TVA 19%, does the payment amount include 19%?
        # Usually yes.
        # Price = HT * (1 + TVA/100)
        # HT = Price / (1 + TVA/100)
        
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
