from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import PaymentType

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
