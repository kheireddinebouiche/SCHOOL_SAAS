from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from ..models import PaymentCategory, Paiements, AutreProduit, SpecialiteCompte
from django.apps import apps
import datetime

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
    from django.db.models import Q, F, ExpressionWrapper, DecimalField
    
    # Pre-fetch all categories to avoid N+1 and build ancestry map
    all_categories = list(PaymentCategory.objects.all())
    cat_map = {c.id: c for c in all_categories}
    children_map = {c.id: [] for c in all_categories}
    for c in all_categories:
        if c.parent_id:
            if c.parent_id in children_map:
                children_map[c.parent_id].append(c)

    def get_descendant_ids(cat_id):
        """Recursively get list of [cat_id, child_id, grandchild_id, ...]"""
        ids = [cat_id]
        if cat_id in children_map:
            for child in children_map[cat_id]:
                ids.extend(get_descendant_ids(child.id))
        return ids

    entites = Entreprise.objects.all().order_by('designation')
    
    report_data_by_entity = []
    
    # Try to get the DASMapping and Paiement models from t_conseil dynamically
    try:
        DASMapping = apps.get_model('t_conseil', 'DASMapping')
        Paiement = apps.get_model('t_conseil', 'Paiement')
    except (LookupError, ImportError):
        DASMapping = None
        Paiement = None

    today = datetime.date.today()
    
    # Determine default fiscal year (if today < Aug 1st, we are in year Y-1 / Y)
    default_year = today.year if today.month >= 8 else today.year - 1
    
    try:
        selected_year = int(request.GET.get('year', default_year))
    except ValueError:
        selected_year = default_year
        
    start_date = datetime.date(selected_year, 8, 1)
    end_date = datetime.date(selected_year + 1, 7, 31)
    
    grand_total_all = 0

    def _get_category_stats(cat_ids, ent):
        """Helper to calculate stats for a list of category IDs (inclusive of descendants)."""
        # 1. Student Payments
        # Find specialties linked to ANY of these categories
        specialite_ids = SpecialiteCompte.objects.filter(compte_id__in=cat_ids).values_list('specialite_id', flat=True)
        
        base_student_qs = Paiements.objects.filter(
            prospect__prospect_fiche_voeux__specialite_id__in=specialite_ids,
            prospect__prospect_fiche_voeux__is_confirmed=True,
            prospect__prospect_fiche_voeux__specialite__formation__entite_legal=ent,
            date_paiement__gte=start_date,
            date_paiement__lte=end_date
        ).exclude(
            prospect__prospect_fiche_voeux_double__is_confirmed=True
        ).exclude(
            context='rach'
        ).distinct()
        
        student_std_total = base_student_qs.aggregate(total=Sum('montant_paye'))['total'] or 0

        # 1.b Double Diplomation Payments (Full Amount based on Formation Match)
        # We attribute the payment to the speciality that matches the Payment's Echeancier Formation
        
        # Helper to filter payments for this entity
        def filter_payments_by_entity(qs):
            return qs.filter(
                Q(due_paiements__entite=ent) | 
                Q(due_paiements__entite__isnull=True, due_paiements__ref_echeancier__entite=ent) |
                Q(due_paiements__isnull=True, refund_id__entite=ent)
            )

        # 1. Match Specialite 1 (Speciality 1's Formation == Payment's Formation)
        dbl_1_qs = Paiements.objects.filter(
            prospect__prospect_fiche_voeux_double__specialite__specialite1_id__in=specialite_ids,
            prospect__prospect_fiche_voeux_double__is_confirmed=True,
            # strict match: Payment Formation ID == Specialite 1 Formation ID
            due_paiements__ref_echeancier__formation__id=F('prospect__prospect_fiche_voeux_double__specialite__specialite1__formation__id'),
            date_paiement__gte=start_date,
            date_paiement__lte=end_date
        ).exclude(context='rach').distinct()
        
        # 2. Match Specialite 2 (Speciality 2's Formation == Payment's Formation)
        dbl_2_qs = Paiements.objects.filter(
            prospect__prospect_fiche_voeux_double__specialite__specialite2_id__in=specialite_ids,
            prospect__prospect_fiche_voeux_double__is_confirmed=True,
             # strict match: Payment Formation ID == Specialite 2 Formation ID
            due_paiements__ref_echeancier__formation__id=F('prospect__prospect_fiche_voeux_double__specialite__specialite2__formation__id'),
            date_paiement__gte=start_date,
            date_paiement__lte=end_date
        ).exclude(context='rach').distinct()

        student_dbl_total = filter_payments_by_entity(dbl_1_qs).aggregate(t=Sum('montant_paye'))['t'] or 0
        student_dbl_total += filter_payments_by_entity(dbl_2_qs).aggregate(t=Sum('montant_paye'))['t'] or 0

        student_total = student_std_total + student_dbl_total

        # 2. Consulting Payments
        consulting_total = 0
        if Paiement and DASMapping:
            thematique_ids = DASMapping.objects.filter(payment_category_id__in=cat_ids).values_list('thematique_id', flat=True)
            consulting_total = Paiement.objects.filter(
                facture__lignes_facture__thematique_id__in=thematique_ids,
                facture__entreprise=ent,
                date_paiement__gte=start_date,
                date_paiement__lte=end_date
            ).distinct().aggregate(total=Sum('montant'))['total'] or 0

        # 3. Other Products
        other_total = AutreProduit.objects.filter(compte_id__in=cat_ids, entite=ent, date_paiement__gte=start_date, date_paiement__lte=end_date).aggregate(total=Sum('montant_paiement'))['total'] or 0

        # 4. Rachat de Crédit
        rachat_total = 0
        has_rachat_cat = PaymentCategory.objects.filter(id__in=cat_ids, category_type='rachat_credit').exists()
        
        if has_rachat_cat:
             # Sum ALL Rachat payments for this entity
             # Filter logic mirrors _get_category_details logic
             rachat_qs = Paiements.objects.filter(context='rach').filter(
                Q(due_paiements__entite=ent) |
                Q(due_paiements__entite__isnull=True, due_paiements__ref_echeancier__entite=ent) |
                Q(due_paiements__entite__isnull=True, due_paiements__ref_echeancier__entite__isnull=True, due_paiements__ref_echeancier__formation__entite_legal=ent)
             ).filter(date_paiement__gte=start_date, date_paiement__lte=end_date)
             rachat_total = rachat_qs.aggregate(t=Sum('montant_paye'))['t'] or 0

        grand_total = float(student_total) + float(consulting_total) + float(other_total) + float(rachat_total)

        
        # Merge Rachat into Other Products Total for Display (as requested by user correction)
        other_total = float(other_total) + float(rachat_total)

        return {
            'student_total': student_total,
            'consulting_total': consulting_total,
            'other_total': other_total,
            'rachat_total': rachat_total, # Kept for reference
            'grand_total': grand_total
        }

    # Identify Root Categories
    root_categories = [c for c in all_categories if c.parent is None]
    # Sort roots by name
    root_categories.sort(key=lambda x: x.name)

    def _get_category_details(cat_id, ent):
        """Helper to get breakdown details for a single category (Direct only)."""
        details = []
        
        category = cat_map.get(cat_id)
        
        # 0. Rachat de Crédit Details (If Category is Rachat type)
        if category and category.category_type == 'rachat_credit':
             rachat_qs = Paiements.objects.filter(context='rach').filter(
                Q(due_paiements__entite=ent) |
                Q(due_paiements__entite__isnull=True, due_paiements__ref_echeancier__entite=ent) |
                Q(due_paiements__entite__isnull=True, due_paiements__ref_echeancier__entite__isnull=True, due_paiements__ref_echeancier__formation__entite_legal=ent)
             ).filter(date_paiement__gte=start_date, date_paiement__lte=end_date)
             
             # Group Rachat by Specialite (similar to students)
             rachat_groups = rachat_qs.values('prospect__prospect_fiche_voeux__specialite__label').annotate(total=Sum('montant_paye')).order_by('-total')
             
             for g in rachat_groups:
                 if g['total'] > 0:
                     details.append({
                        'label': f"{g['prospect__prospect_fiche_voeux__specialite__label'] or 'Sans Spécialité'} (Rachat)",
                        'total': float(g['total']),
                        'type': 'Etudiant'
                     })
                     
             # Fallback if no groups but has total (rare but possible with data inconsistencies)
             if not details:
                 rachat_total = rachat_qs.aggregate(t=Sum('montant_paye'))['t'] or 0
                 if rachat_total > 0:
                     details.append({
                        'label': "Rachat de Crédit (Autres)",
                        'total': float(rachat_total),
                        'type': 'Etudiant'
                     })
        
        # 1. Student Details (Group by Specialite)
        specialite_ids = SpecialiteCompte.objects.filter(compte_id=cat_id).values_list('specialite_id', flat=True)
        if specialite_ids:
            base_student_qs = Paiements.objects.filter(
                prospect__prospect_fiche_voeux__specialite_id__in=specialite_ids,
                prospect__prospect_fiche_voeux__is_confirmed=True
            ).exclude(
                prospect__prospect_fiche_voeux_double__is_confirmed=True
            ).exclude(
                context='rach'
            ).distinct()
            
            # Apply Entity Filter (Formation based)
            student_qs = base_student_qs.filter(
                prospect__prospect_fiche_voeux__specialite__formation__entite_legal=ent,
                date_paiement__gte=start_date,
                date_paiement__lte=end_date
            )
            
            # Group by Specialite Label
            student_groups = student_qs.values('prospect__prospect_fiche_voeux__specialite__label').annotate(total=Sum('montant_paye')).order_by('-total')
            
            for g in student_groups:
                if g['total'] > 0:
                    details.append({
                        'label': g['prospect__prospect_fiche_voeux__specialite__label'] or "Sans Spécialité",
                        'total': float(g['total']),
                        'type': 'Etudiant'
                    })
            
            
            # 1.b Double Diplomation Details
            
            # Helper to filter payments for this entity
            def filter_payments_by_entity(qs):
                return qs.filter(
                    Q(due_paiements__entite=ent) | 
                    Q(due_paiements__entite__isnull=True, due_paiements__ref_echeancier__entite=ent) |
                    Q(due_paiements__isnull=True, refund_id__entite=ent)
                )

            # Match Specialite 1
            dbl_1_qs = Paiements.objects.filter(
                prospect__prospect_fiche_voeux_double__specialite__specialite1_id__in=specialite_ids,
                prospect__prospect_fiche_voeux_double__is_confirmed=True,
                due_paiements__ref_echeancier__formation__id=F('prospect__prospect_fiche_voeux_double__specialite__specialite1__formation__id'),
                date_paiement__gte=start_date,
                date_paiement__lte=end_date
            ).exclude(context='rach').distinct()
            
            dbl_1_filtered = filter_payments_by_entity(dbl_1_qs)

            dbl_1_groups = dbl_1_filtered.values(
                dd_label=F('prospect__prospect_fiche_voeux_double__specialite__label'), 
                spec_label=F('prospect__prospect_fiche_voeux_double__specialite__specialite1__label')
            ).annotate(full_total=Sum('montant_paye')).order_by('-full_total')

            for g in dbl_1_groups:
                 if g['full_total'] > 0:
                    lbl = f"{g['spec_label'] or 'Inconnue'} (Double: {g['dd_label'] or ''})"
                    details.append({'label': lbl, 'total': float(g['full_total']), 'type': 'Etudiant'})

            # Match Specialite 2
            dbl_2_qs = Paiements.objects.filter(
                prospect__prospect_fiche_voeux_double__specialite__specialite2_id__in=specialite_ids,
                prospect__prospect_fiche_voeux_double__is_confirmed=True,
                due_paiements__ref_echeancier__formation__id=F('prospect__prospect_fiche_voeux_double__specialite__specialite2__formation__id')
            ).exclude(context='rach').distinct()
            
            dbl_2_filtered = filter_payments_by_entity(dbl_2_qs)
            
            dbl_2_groups = dbl_2_filtered.values(
                dd_label=F('prospect__prospect_fiche_voeux_double__specialite__label'), 
                spec_label=F('prospect__prospect_fiche_voeux_double__specialite__specialite2__label')
            ).annotate(full_total=Sum('montant_paye')).order_by('-full_total')

            for g in dbl_2_groups:
                 if g['full_total'] > 0:
                    lbl = f"{g['spec_label'] or 'Inconnue'} (Double: {g['dd_label'] or ''})"
                    details.append({'label': lbl, 'total': float(g['full_total']), 'type': 'Etudiant'})

        # 2. Consulting Details (Group by Thematique)
        if Paiement and DASMapping:
            thematiques = DASMapping.objects.filter(payment_category_id=cat_id).values_list('thematique__label', flat=True).distinct()
            # It's harder to group strict by thematique if mapping is M2M or complex, 
            # but let's try direct grouping on the Invoice Lines linked to these thematiques
            
            # We need to filter Paiements that match the Entite AND the Category's thematiques
            # And then group them by that Thematique
            
            thematique_ids = DASMapping.objects.filter(payment_category_id=cat_id).values_list('thematique_id', flat=True)
            
            if thematique_ids:
                 # Note: A single invoice might have multiple lines. A payment pays the invoice.
                 # Apportioning payment to lines is hard if partial. 
                 # Assuming 1-to-1 or simple case for report: Just show the totals of Payments
                 # linked to invoices containing these thematiques?
                 # Better: Group by Facture Title or Thematique Label if possible.
                 # Given the complexity, let's try grouping by `facture__lignes_facture__thematique__label`
                 # This might duplicate payments if an invoice has 2 lines of same thematique?
                 # Let's stick to distinct payments sum per thematique filter.
                 
                 # Alternative: Iterate thematiques and calc sum for each. Safe but N queries.
                 # Given low number of thematiques per category, this is acceptable.
                 pass # Logic below implemented as iteration for safety

            ds_maps = DASMapping.objects.filter(payment_category_id=cat_id).select_related('thematique')
            for dsm in ds_maps:
                if not dsm.thematique: continue
                # Calc total for this specific thematique
                t_total = Paiement.objects.filter(
                    facture__lignes_facture__thematique=dsm.thematique,
                    facture__entreprise=ent,
                    date_paiement__gte=start_date,
                    date_paiement__lte=end_date
                    # Consulting context usually differs, safe to assume standard
                ).distinct().aggregate(total=Sum('montant'))['total'] or 0
                
                if t_total > 0:
                    details.append({
                        'label': dsm.thematique.label,
                        'total': t_total,
                        'type': 'Conseil'
                    })

        # 3. Other Details (Group by Label)
        other_qs = AutreProduit.objects.filter(compte_id=cat_id, entite=ent, date_paiement__gte=start_date, date_paiement__lte=end_date).values('label').annotate(total=Sum('montant_paiement')).order_by('-total')
        for g in other_qs:
             if g['total'] > 0:
                details.append({
                    'label': g['label'] or "Autre",
                    'total': g['total'],
                    'type': 'Autre'
                })

        return details

    for ent in entites:
        entity_report_data = [] 
        entity_total_sum = 0
        
        def _process_category_recursive(category, level, ent):
            """
            Recursively process a category and its children.
            Returns the accumulated total for this branch (to add to entity total).
            Appends processed data to `entity_report_data`.
            """
            # 1. Stats and Details
            descendant_ids = get_descendant_ids(category.id)
            stats = _get_category_stats(descendant_ids, ent)
            details = _get_category_details(category.id, ent)
            
            # 2. Add this category to the flat list
            # We add it regardless of total, as requested.
            entity_report_data.append({
                'category': category,
                'stats': stats,
                'details': details,
                'level': level,  # 0 for root, 1 for child, 2 for grandchild...
                'is_root': level == 0,
                'is_parent': bool(children_map.get(category.id))  # True if it has children list not empty
            })
            
             # Update total logic to include Rachat if present
            branch_total = stats['grand_total']

            # 3. Process Children
            direct_children = children_map.get(category.id, [])
            direct_children.sort(key=lambda x: x.name)
            
            for child in direct_children:
                _process_category_recursive(child, level + 1, ent)
                
            return branch_total

        for root in root_categories:
            branch_sum = _process_category_recursive(root, 0, ent)
            
            # Root stats already include children sums via _get_category_stats(descendants)
            # So to get the Entity Total, we just need to sum the Roots' Grand Totals.
            # However, _process_category_recursive appends to list.
            # We can just sum up the stats['grand_total'] of all items where level=0
            pass

        # Calculate Entity Total from Roots only to avoid double counting
        entity_total_sum = sum(item['stats']['grand_total'] for item in entity_report_data if item['level'] == 0)

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
        'total_all': grand_total_all,
        'selected_year': selected_year,
        'available_years': range(2023, default_year + 2) # Example range, customize as needed
    }

    return render(request, 'tenant_folder/tresorerie/reporting_das.html', context)

