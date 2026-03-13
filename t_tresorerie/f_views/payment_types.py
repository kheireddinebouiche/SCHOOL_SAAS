from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import PaymentType
from django.http import JsonResponse

@login_required
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
def ApiListePaymentTypes(request):
    """
    API endpoint to list all payment types in JSON format.
    """
    payment_types = PaymentType.objects.all().values('id', 'name')
    return JsonResponse(list(payment_types), safe=False)
