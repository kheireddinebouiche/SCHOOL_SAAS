from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from ..models import PaymentCategory, Paiements, AutreProduit, SpecialiteCompte
from django.apps import apps

@login_required(login_url="institut_app:login")
def ReportingDAS(request):
    """
    Dashboard showing total amounts grouped by PaymentCategory AND Entreprise.
    Aggregates data from multiple sources:
    1. Student Payments (linked via SpecialiteCompte)
    2. Consulting Payments (linked via DASMapping in t_conseil)
    3. Other Products (linked via AutreProduit.compte)
    """
    from institut_app.models import Entreprise
    
    categories = PaymentCategory.objects.all().order_by('name')
    entites = Entreprise.objects.all().order_by('designation')
    
    report_data_by_entity = []
    
    # Try to get the DASMapping and Paiement models from t_conseil dynamically
    try:
        DASMapping = apps.get_model('t_conseil', 'DASMapping')
        Paiement = apps.get_model('t_conseil', 'Paiement')
    except (LookupError, ImportError):
        DASMapping = None
        Paiement = None

    grand_total_all = 0

    for ent in entites:
        entity_report_data = []
        entity_total_sum = 0
        
        for cat in categories:
            # 1. Student Payments
            # We find specialties linked to this category
            specialite_ids = SpecialiteCompte.objects.filter(compte=cat).values_list('specialite_id', flat=True)
            
            # Base Query for Student Payments
            base_student_qs = Paiements.objects.filter(
                prospect__prospect_fiche_voeux__specialite_id__in=specialite_ids,
                prospect__prospect_fiche_voeux__is_confirmed=True
            )
            
            # Sum linked via DuePaiements to this Entity
            student_total_due = base_student_qs.filter(due_paiements__entite=ent).aggregate(total=Sum('montant_paye'))['total'] or 0
            
            # Sum linked via Refund (if DuePaiement is null)
            student_total_refund = base_student_qs.filter(due_paiements__isnull=True, refund_id__entite=ent).aggregate(total=Sum('montant_paye'))['total'] or 0
            
            student_total = student_total_due + student_total_refund

            # 2. Consulting Payments (t_conseil)
            consulting_total = 0
            if Paiement and DASMapping:
                # Find thematiques linked to this category via DASMapping
                thematique_ids = DASMapping.objects.filter(payment_category=cat).values_list('thematique_id', flat=True)
                # Sum of payments for invoices that include these thematiques AND belong to this entity
                consulting_total = Paiement.objects.filter(
                    facture__lignes_facture__thematique_id__in=thematique_ids,
                    facture__entreprise=ent
                ).distinct().aggregate(total=Sum('montant'))['total'] or 0

            # 3. Other Products
            other_total = AutreProduit.objects.filter(compte=cat, entite=ent).aggregate(total=Sum('montant_paiement'))['total'] or 0

            cat_total = float(student_total) + float(consulting_total) + float(other_total)

            if cat_total > 0: # Only include categories with data for this entity
                entity_report_data.append({
                    'category': cat,
                    'student_total': student_total,
                    'consulting_total': consulting_total,
                    'other_total': other_total,
                    'grand_total': cat_total
                })
                entity_total_sum += cat_total

        if entity_report_data:
            report_data_by_entity.append({
                'entity': ent,
                'data': entity_report_data,
                'total': entity_total_sum
            })
            grand_total_all += entity_total_sum

    context = {
        'tenant': request.tenant,
        'report_data_by_entity': report_data_by_entity,
        'total_all': grand_total_all
    }

    return render(request, 'tenant_folder/tresorerie/reporting_das.html', context)

