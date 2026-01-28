from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from ..models import PaymentCategory, Paiements, AutreProduit, SpecialiteCompte
from django.apps import apps

@login_required(login_url="institut_app:login")
def ReportingDAS(request):
    """
    Dashboard showing total amounts grouped by PaymentCategory.
    Aggregates data from multiple sources:
    1. Student Payments (linked via SpecialiteCompte)
    2. Consulting Payments (linked via DASMapping in t_conseil)
    3. Other Products (linked via AutreProduit.compte)
    """
    categories = PaymentCategory.objects.all().order_by('name')
    report_data = []
    
    # Try to get the DASMapping and Paiement models from t_conseil dynamically
    # to avoid circular imports if any, and for cleaner modularity.
    try:
        DASMapping = apps.get_model('t_conseil', 'DASMapping')
        Paiement = apps.get_model('t_conseil', 'Paiement')
    except (LookupError, ImportError):
        DASMapping = None
        Paiement = None

    for cat in categories:
        # 1. Student Payments
        # We find specialties linked to this category
        specialite_ids = SpecialiteCompte.objects.filter(compte=cat).values_list('specialite_id', flat=True)
        # Sum of payments made by students in these specialties
        # We follow: Paiements -> Prospets -> FicheDeVoeux (confirmed) -> Specialite
        student_total = Paiements.objects.filter(
            prospect__prospect_fiche_voeux__specialite_id__in=specialite_ids,
            prospect__prospect_fiche_voeux__is_confirmed=True
        ).aggregate(total=Sum('montant_paye'))['total'] or 0

        # 2. Consulting Payments (t_conseil)
        consulting_total = 0
        if Paiement and DASMapping:
            # Find thematiques linked to this category via DASMapping
            thematique_ids = DASMapping.objects.filter(payment_category=cat).values_list('thematique_id', flat=True)
            # Sum of payments for invoices that include these thematiques
            consulting_total = Paiement.objects.filter(
                facture__lignes_facture__thematique_id__in=thematique_ids
            ).distinct().aggregate(total=Sum('montant'))['total'] or 0

        # 3. Other Products
        other_total = AutreProduit.objects.filter(compte=cat).aggregate(total=Sum('montant_paiement'))['total'] or 0

        grand_total = float(student_total) + float(consulting_total) + float(other_total)

        if grand_total > 0 or cat.children.exists(): # Include if there's money or it's a parent
            report_data.append({
                'category': cat,
                'student_total': student_total,
                'consulting_total': consulting_total,
                'other_total': other_total,
                'grand_total': grand_total
            })

    context = {
        'tenant': request.tenant,
        'report_data': report_data,
        'total_all': sum(item['grand_total'] for item in report_data)
    }

    return render(request, 'tenant_folder/tresorerie/reporting_das.html', context)
