import datetime
from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum
from django_tenants.utils import schema_context
from app.models import Institut
from associe_app.models import BudgetCampaign, BudgetLine, PostesBudgetaire, BudgetLineDetail, GlobalPaymentType, GlobalPaymentCategory, GlobalDepensesCategory
from t_tresorerie.models import Paiements, Depenses, AutreProduit, SpecialiteCompte
from t_crm.models import FicheDeVoeux, FicheVoeuxDouble

def get_campaign_realization_data(campaign, target_instituts, as_of_date=None):
    """
    Calculates budget realization data for a campaign across one or more institutes.
    Args:
        campaign: BudgetCampaign instance
        target_instituts: QuerySet or list of Institut instances
    Returns:
        A dictionary containing combined_postes, totals, and ratios.
    """
    # 1. Prepare Ratios
    c_year = campaign.date_debut.year
    t1_start = datetime.date(c_year, 7, 1)
    t1_end = datetime.date(c_year, 9, 30)
    t2_start = datetime.date(c_year, 10, 1)
    t2_end = datetime.date(c_year, 12, 31)
    t3_start = datetime.date(c_year + 1, 1, 1)
    t3_end = datetime.date(c_year + 1, 3, 31)
    t4_start = datetime.date(c_year + 1, 4, 1)
    t4_end = datetime.date(c_year + 1, 6, 30)
    
    today_date = as_of_date if as_of_date else timezone.now().date()
    
    def get_ratio(start, end, today):
        if today < start: return Decimal('0')
        if today > end: return Decimal('1')
        total_days = (end - start).days + 1
        elapsed = (today - start).days + 1
        return Decimal(str(elapsed)) / Decimal(str(total_days))
        
    t1_ratio = get_ratio(t1_start, t1_end, today_date)
    t2_ratio = get_ratio(t2_start, t2_end, today_date)
    t3_ratio = get_ratio(t3_start, t3_end, today_date)
    t4_ratio = get_ratio(t4_start, t4_end, today_date)

    # 2. Identify Current Quarter for current_q_months filter
    month = today_date.month
    if month in [7, 8, 9]: current_q_months = [7, 8, 9]
    elif month in [10, 11, 12]: current_q_months = [10, 11, 12]
    elif month in [1, 2, 3]: current_q_months = [1, 2, 3]
    else: current_q_months = [4, 5, 6]

    # 3. Initialize Accumulators
    all_allocations = {} # Key: poste_id -> {montant, t1_montant, ...}
    all_realisations = {} # Key: poste_id -> {montant, t1_montant, ...}

    # 4. Fetch Budget Postes (Public)
    all_postes = PostesBudgetaire.objects.prefetch_related('payment_categories', 'depense_categories').order_by('-type', 'order', 'label')
    
    # 5. Loop Through Instituts and Collect Data
    for inst in target_instituts:
        # A. Collect Allocations (Public Schema)
        details = BudgetLineDetail.objects.filter(campaign=campaign, institut=inst)
        for d in details:
            pid = d.poste_id
            if pid not in all_allocations:
                all_allocations[pid] = {
                    'montant': Decimal('0'),
                    't1_montant': Decimal('0'),
                    't2_montant': Decimal('0'),
                    't3_montant': Decimal('0'),
                    't4_montant': Decimal('0'),
                }
            
            all_allocations[pid]['montant'] += d.montant
            t1 = d.t1_percent or 0
            t2 = d.t2_percent or 0
            t3 = d.t3_percent or 0
            t4 = d.t4_percent or 0
            
            # Default to 25% each if no percentages are defined but an amount exists
            if (t1 + t2 + t3 + t4) == 0 and d.montant > 0:
                t1 = t2 = t3 = t4 = Decimal('25')
            
            all_allocations[pid]['t1_montant'] += (d.montant * t1) / 100
            all_allocations[pid]['t2_montant'] += (d.montant * t2) / 100
            all_allocations[pid]['t3_montant'] += (d.montant * t3) / 100
            all_allocations[pid]['t4_montant'] += (d.montant * t4) / 100

        # B. Collect Realizations (Tenant Schema)
        with schema_context(inst.schema_name):
            def add_real(p_id, val, date_pay):
                if val is None or val == 0: return
                if p_id not in all_realisations:
                    all_realisations[p_id] = {
                        'montant': Decimal('0'),
                        't1_montant': Decimal('0'),
                        't2_montant': Decimal('0'),
                        't3_montant': Decimal('0'),
                        't4_montant': Decimal('0'),
                        'months': {m: Decimal('0') for m in range(1, 13)}
                    }
                
                real = all_realisations[p_id]
                if date_pay:
                    m = date_pay.month
                    if m in [7, 8, 9]: real['t1_montant'] += val
                    elif m in [10, 11, 12]: real['t2_montant'] += val
                    elif m in [1, 2, 3]: real['t3_montant'] += val
                    elif m in [4, 5, 6]: real['t4_montant'] += val
                    
                    real['months'][m] += val
                    real['montant'] += val
                else:
                    real['montant'] += val

            # Revenu
            paiements = Paiements.objects.filter(
                date_paiement__gte=campaign.date_debut,
                date_paiement__lte=campaign.date_fin,
                payment_type__isnull=False
            ).prefetch_related('lettrages', 'payment_type')
            
            for p in paiements:
                # 1. Verification of Cheque/Transfer validation
                if p.mode_paiement in ['che', 'vir'] and not p.lettrages.exists(): continue
                
                target_g_cat = None
                
                # A. Identify Potential Categories from Student Specialties
                student_categories = []
                if p.due_paiements:
                    client = p.due_paiements.client
                    promo = p.due_paiements.promo
                    if client and promo:
                        # Try Standard Fiche
                        fiche = FicheDeVoeux.objects.filter(prospect=client, promo=promo, is_confirmed=True).first()
                        fiches = [fiche] if fiche else []
                        
                        # Try Double Diplomation Fiche
                        fiche_double = FicheVoeuxDouble.objects.filter(prospect=client, promo=promo, is_confirmed=True).first()
                        if fiche_double: fiches.append(fiche_double)
                        
                        for f in fiches:
                            specs = []
                            # Determine if it's a standard or double fiche
                            if isinstance(f, FicheDeVoeux):
                                if f.specialite_id: specs.append(f.specialite_id)
                            elif isinstance(f, FicheVoeuxDouble):
                                # For Double Diplomation, we must follow the relation to the DoubleDiplomation model
                                dd = f.specialite
                                if dd:
                                    if dd.specialite1_id: specs.append(dd.specialite1_id)
                                    if dd.specialite2_id: specs.append(dd.specialite2_id)
                            
                            for spec_id in specs:
                                sc = SpecialiteCompte.objects.filter(specialite_id=spec_id).select_related('compte').first()
                                if sc and sc.compte:
                                    with schema_context('public'):
                                        gc = None
                                        if sc.compte.global_id:
                                            gc = GlobalPaymentCategory.objects.filter(id=sc.compte.global_id).first()
                                        if not gc:
                                            gc = GlobalPaymentCategory.objects.filter(name=sc.compte.name).first()
                                    
                                    if gc:
                                        # Store with entity context for filtering
                                        from t_formations.models import Specialites
                                        # This query must run in the tenant context
                                        s_obj = Specialites.objects.filter(id=spec_id).select_related('formation__entite_legal').first()
                                        ent_id = s_obj.formation.entite_legal_id if s_obj and s_obj.formation else None
                                        student_categories.append({'cat': gc, 'ent_id': ent_id})

                # B. Filtering by Payment Entity (Crucial for Double Diplomation)
                if p.entite_id and student_categories:
                    # Pick the category linked to the specialty of the SAME entity
                    for item in student_categories:
                        if item['ent_id'] == p.entite_id:
                            target_g_cat = item['cat']
                            break
                
                # C. Fallback 1: If no entity match but we have categories (Standard case)
                if not target_g_cat and student_categories:
                    target_g_cat = student_categories[0]['cat']

                # D. Fallback 2: Mapping via PaymentType (Global Configuration)
                if not target_g_cat and p.payment_type:
                    with schema_context('public'):
                        global_pt = GlobalPaymentType.objects.filter(name=p.payment_type.name).prefetch_related('payment_categories').first()
                        if global_pt:
                            # Still try to find one matching the entity if possible
                            cats = list(global_pt.payment_categories.all())
                            if cats:
                                target_g_cat = cats[0] # Default to first, NO FRACTIONATION
                
                # 2. Add Realization to the correct Budget Poste
                if target_g_cat:
                    with schema_context('public'):
                        poste = PostesBudgetaire.objects.filter(payment_categories=target_g_cat).first()
                        if poste:
                            add_real(poste.id, p.montant_paye, p.date_paiement)

            # Autre Produits
            autres = AutreProduit.objects.filter(date_paiement__gte=campaign.date_debut, date_paiement__lte=campaign.date_fin, payment_type__isnull=False).prefetch_related('lettrages', 'payment_type')
            for ap in autres:
                if ap.mode_paiement in ['che', 'vir'] and not ap.lettrages.exists(): continue
                with schema_context('public'):
                    global_pt = GlobalPaymentType.objects.filter(name=ap.payment_type.name).prefetch_related('payment_categories').first()
                    if global_pt:
                        cats = global_pt.payment_categories.all()
                        if cats:
                            # Use the first category found that matches a budget poste
                            for g_cat in cats:
                                poste = PostesBudgetaire.objects.filter(payment_categories=g_cat).first()
                                if poste: 
                                    add_real(poste.id, ap.montant_paiement, ap.date_paiement)
                                    break 

            # Depenses
            depenses = Depenses.objects.filter(date_paiement__gte=campaign.date_debut, date_paiement__lte=campaign.date_fin, category__isnull=False).prefetch_related('category')
            for d in depenses:
                with schema_context('public'):
                    g_cat = GlobalDepensesCategory.objects.filter(name=d.category.name).first()
                    if g_cat:
                        poste = PostesBudgetaire.objects.filter(depense_categories=g_cat).first()
                        if poste: add_real(poste.id, d.montant_ttc, d.date_paiement)

    # 6. Structure Final Data
    structured_postes = []
    combined_postes = []
    
    total_dispatched_recette = Decimal('0')
    total_pro_rata_recette = Decimal('0')
    total_realized_recette = Decimal('0')
    
    total_dispatched_depense = Decimal('0')
    total_pro_rata_depense = Decimal('0')
    total_realized_depense = Decimal('0')
    
    # Re-structure postes for hierarchy display
    for p in all_postes:
        if p.parent is None:
            children = [child for child in all_postes if child.parent_id == p.id]
            display_postes = []
            if p.payment_categories.exists() or p.depense_categories.exists() or not children:
                display_postes.append(p)
            display_postes.extend(children)
            
            group_data = {
                'parent_poste': p,
                'is_standalone': not children,
                'display_postes': []
            }

            for dp in display_postes:
                alloc = all_allocations.get(dp.id, {'montant': 0, 't1_montant': 0, 't2_montant': 0, 't3_montant': 0, 't4_montant': 0})
                real = all_realisations.get(dp.id, {'montant': 0, 't1_montant': 0, 't2_montant': 0, 't3_montant': 0, 't4_montant': 0})

                full_t1 = Decimal(str(alloc['t1_montant']))
                full_t2 = Decimal(str(alloc['t2_montant']))
                full_t3 = Decimal(str(alloc['t3_montant']))
                full_t4 = Decimal(str(alloc['t4_montant']))
                full_prevu = full_t1 + full_t2 + full_t3 + full_t4
                
                t1_prevu = round(full_t1 * t1_ratio, 2)
                t2_prevu = round(full_t2 * t2_ratio, 2)
                t3_prevu = round(full_t3 * t3_ratio, 2)
                t4_prevu = round(full_t4 * t4_ratio, 2)
                prevu = t1_prevu + t2_prevu + t3_prevu + t4_prevu
                
                realise = Decimal(str(real['montant']))
                t1_realise = Decimal(str(real['t1_montant']))
                t2_realise = Decimal(str(real['t2_montant']))
                t3_realise = Decimal(str(real['t3_montant']))
                t4_realise = Decimal(str(real['t4_montant']))

                if dp.type == 'recette':
                    total_dispatched_recette += full_prevu
                    total_pro_rata_recette += prevu
                    total_realized_recette += realise
                else:
                    total_dispatched_depense += full_prevu
                    total_pro_rata_depense += prevu
                    total_realized_depense += realise

                group_data['display_postes'].append({
                    'poste': dp,
                    'global': {
                        'prevu': prevu,
                        'full_prevu': full_prevu,
                        'realise': realise,
                        'ecart': realise - prevu,
                        'taux': (realise / prevu * 100) if prevu > 0 else (Decimal('100') if realise > 0 else Decimal('0')),
                    },
                    't1': {'prevu': t1_prevu, 'full_prevu': full_t1, 'realise': t1_realise, 'ecart': t1_realise - t1_prevu},
                    't2': {'prevu': t2_prevu, 'full_prevu': full_t2, 'realise': t2_realise, 'ecart': t2_realise - t2_prevu},
                    't3': {'prevu': t3_prevu, 'full_prevu': full_t3, 'realise': t3_realise, 'ecart': t3_realise - t3_prevu},
                    't4': {'prevu': t4_prevu, 'full_prevu': full_t4, 'realise': t4_realise, 'ecart': t4_realise - t4_prevu},
                    'months': real.get('months', {m: Decimal('0') for m in range(1, 13)})
                })
            
            combined_postes.append(group_data)

    return {
        'combined_postes': combined_postes,
        'totals': {
            'dispatched_recette': total_dispatched_recette,
            'pro_rata_recette': total_pro_rata_recette,
            'realized_recette': total_realized_recette,
            'recette_ecart': total_realized_recette - total_pro_rata_recette,
            
            'dispatched_depense': total_dispatched_depense,
            'pro_rata_depense': total_pro_rata_depense,
            'realized_depense': total_realized_depense,
            'depense_ecart': total_realized_depense - total_pro_rata_depense,
            
            'global_dispatched': total_dispatched_recette - total_dispatched_depense,
            'global_realized': total_realized_recette - total_realized_depense
        },
        'ratios': {
            't1': t1_ratio,
            't2': t2_ratio,
            't3': t3_ratio,
            't4': t4_ratio
        },
        'trimester_totals': {
            't1': {
                'full_r': sum(dp['t1']['full_prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'pro_r': sum(dp['t1']['prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'real_r': sum(dp['t1']['realise'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'full_d': sum(dp['t1']['full_prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
                'pro_d': sum(dp['t1']['prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
                'real_d': sum(dp['t1']['realise'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
            },
            't2': {
                'full_r': sum(dp['t2']['full_prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'pro_r': sum(dp['t2']['prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'real_r': sum(dp['t2']['realise'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'full_d': sum(dp['t2']['full_prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
                'pro_d': sum(dp['t2']['prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
                'real_d': sum(dp['t2']['realise'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
            },
            't3': {
                'full_r': sum(dp['t3']['full_prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'pro_r': sum(dp['t3']['prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'real_r': sum(dp['t3']['realise'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'full_d': sum(dp['t3']['full_prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
                'pro_d': sum(dp['t3']['prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
                'real_d': sum(dp['t3']['realise'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
            },
            't4': {
                'full_r': sum(dp['t4']['full_prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'pro_r': sum(dp['t4']['prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'real_r': sum(dp['t4']['realise'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'full_d': sum(dp['t4']['full_prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
                'pro_d': sum(dp['t4']['prevu'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
                'real_d': sum(dp['t4']['realise'] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
            }
        },
        'monthly_totals': {
            m: {
                'real_r': sum(dp['months'][m] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'real_d': sum(dp['months'][m] for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
                # Approximation of monthly plan: 1/3 of the trimester it belongs to
                'plan_r': sum(dp[t_key]['full_prevu']/3 for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'plan_d': sum(dp[t_key]['full_prevu']/3 for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
                # Pro-rata for the month (simplified: 100% if month passed, current progress if current month)
                'pro_r': sum(dp[t_key]['full_prevu']/3 * Decimal(str(month_ratio(m, today_date))) for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'recette'),
                'pro_d': sum(dp[t_key]['full_prevu']/3 * Decimal(str(month_ratio(m, today_date))) for g in combined_postes for dp in g['display_postes'] if dp['poste'].type == 'depense'),
            } for m, t_key in {
                **{m: 't1' for m in [7, 8, 9]},
                **{m: 't2' for m in [10, 11, 12]},
                **{m: 't3' for m in [1, 2, 3]},
                **{m: 't4' for m in [4, 5, 6]}
            }.items()
        }
    }

def month_ratio(m, current_date):
    if current_date.month > m:
        # Fiscal year overlap check: Aug-Dec are months 8-12
        # If current is Jan (1) and target is Dec (12), target is passed.
        # This logic is simplified for now.
        pass
    
    # Simple check for fiscal year context (Aug start)
    target_date_val = m if m >= 7 else m + 12
    current_date_val = current_date.month if current_date.month >= 7 else current_date.month + 12
    
    if current_date_val > target_date_val: return 1.0
    if current_date_val < target_date_val: return 0.0
    
    # Current month: progress by day
    import calendar
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    return current_date.day / days_in_month
