from institut_app.decorators import module_permission_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import PaymentType
from django.http import JsonResponse

@login_required
@module_permission_required('tre', 'view')
def payment_type_list(request):
    """
    Vue en lecture seule pour afficher les types de paiement synchronisés.
    """
    payment_types = PaymentType.objects.all().prefetch_related('payment_categories')
    
    context = {
        'titre_page': 'Types de Paiement',
        'titre_section': 'Configuration Financière',
        'sous_titre': 'Liste des types de paiement synchronisés',
        'payment_types': payment_types,
    }
    return render(request, 'tenant_folder/tresorerie/payment_type_list.html', context)

@login_required
@module_permission_required('tre', 'view')
def ApiListePaymentTypes(request):
    """
    API endpoint to list all payment types in JSON format,
    including any globally configured penalty/fee amounts.
    """
    from ..models import PenaltyGlobalConfiguration
    config = PenaltyGlobalConfiguration.get_solo()
    
    payment_types = PaymentType.objects.all()
    results = []
    for pt in payment_types:
        matching_amounts = []
        
        if config.penalite_retard_payment_type_id == pt.id:
            matching_amounts.append(float(config.penalite_retard))
        if config.prix_rachat_credit_payment_type_id == pt.id:
            matching_amounts.append(float(config.prix_rachat_credit))
        if config.frais_duplicata_payment_type_id == pt.id:
            matching_amounts.append(float(config.frais_duplicata))
            
        configured_amount = None
        if matching_amounts:
            non_zero_amounts = [amt for amt in matching_amounts if amt > 0]
            if non_zero_amounts:
                configured_amount = non_zero_amounts[0]
            else:
                configured_amount = matching_amounts[0]
            
        results.append({
            'id': pt.id,
            'name': pt.name,
            'default_amount': configured_amount
        })
        
    return JsonResponse(results, safe=False)
