import datetime
from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum
from django_tenants.utils import schema_context
from app.models import Institut
from associe_app.models import BudgetCampaign, BudgetLine, PostesBudgetaire, BudgetLineDetail, GlobalPaymentType, GlobalPaymentCategory, GlobalDepensesCategory
from t_tresorerie.models import Paiements, Depenses, AutreProduit, SpecialiteCompte
from t_crm.models import FicheDeVoeux, FicheVoeuxDouble

def get_campaign_realization_data(campaign, target_instituts):
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
    t1_start = datetime.date(c_year, 8, 1)
    t1_end = datetime.date(c_year, 10, 31)
    t2_start = datetime.date(c_year, 11, 1)
    t2_end = datetime.date(c_year + 1, 1, 31)
    t3_start = datetime.date(c_year + 1, 2, 1)
    t3_end = datetime.date(c_year + 1, 4, 30)
    t4_start = datetime.date(c_year + 1, 5, 1)
    t4_end = datetime.date(c_year + 1, 7, 31)
    
    today_date = timezone.now().date()
    
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
    if month in [8, 9, 10]: current_q_months = [8, 9, 10]
    elif month in [11, 12, 1]: current_q_months = [11, 12, 1]
    elif month in [2, 3, 4]: current_q_months = [2, 3, 4]
    else: current_q_months = [5, 6, 7]

    # 3. Initialize Accumulators
    all_allocations = {} # Key: poste_id -> {montant, t1_montant, ...}
    all_realisations = {} # Key: poste_id -> {montant, t1_montant, ...}

    # 4. Fetch Budget Postes (Public)
    all_postes = PostesBudgetaire.objects.prefetch_related('payment_categories', 'depense_categories').order_by('order', 'type', 'label')
    
    # 5. Loop Through Instituts and Collect Data
    for inst in target_instituts:
        # A. Collect Allocations (Public Schema)
        details = BudgetLineDetail.objects.filter(campaign=campaign, institut=inst)
        for d in details:
            # ONLY CONSOLIDATED RECORDS (ent_id = 0 and cat_type = 'none')
            if d.entreprise_id != 0 or d.payment_category_id is not None or d.depense_category_id is not None:
                continue

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
            all_allocations[pid]['t1_montant'] += (d.montant * d.t1_percent) / 100 if d.t1_percent else 0
            all_allocations[pid]['t2_montant'] += (d.montant * d.t2_percent) / 100 if d.t2_percent else 0
            all_allocations[pid]['t3_montant'] += (d.montant * d.t3_percent) / 100 if d.t3_percent else 0
            all_allocations[pid]['t4_montant'] += (d.montant * d.t4_percent) / 100 if d.t4_percent else 0

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
                    }
                
                real = all_realisations[p_id]
                if date_pay:
                    m = date_pay.month
                    if m in [8, 9, 10]: real['t1_montant'] += val
                    elif m in [11, 12, 1]: real['t2_montant'] += val
                    elif m in [2, 3, 4]: real['t3_montant'] += val
                    elif m in [5, 6, 7]: real['t4_montant'] += val
                    
                    if m in current_q_months: real['montant'] += val
                else:
                    real['montant'] += val

            # Revenu
            paiements = Paiements.objects.filter(
                date_paiement__gte=campaign.date_debut,
                date_paiement__lte=campaign.date_fin,
                payment_type__isnull=False
            ).prefetch_related('lettrages', 'payment_type')
            
            for p in paiements:
                if p.mode_paiement in ['che', 'vir'] and not p.lettrages.exists(): continue
                
                g_categories = []
                # Specialty Mapping
                if p.due_paiements:
                    client = p.due_paiements.client
                    promo = p.due_paiements.promo
                    if client and promo:
                        fiche = FicheDeVoeux.objects.filter(prospect=client, promo=promo, is_confirmed=True).first()
                        if not fiche: fiche = FicheVoeuxDouble.objects.filter(prospect=client, promo=promo, is_confirmed=True).first()
                        if fiche and fiche.specialite_id:
                            spec_compte = SpecialiteCompte.objects.filter(specialite_id=fiche.specialite_id).first()
                            if spec_compte and spec_compte.compte:
                                with schema_context('public'):
                                    gc = GlobalPaymentCategory.objects.filter(name=spec_compte.compte.name).first()
                                    if gc: g_categories.append(gc)

                # Fallback to PaymentType
                if not g_categories and p.payment_type:
                    with schema_context('public'):
                        global_pt = GlobalPaymentType.objects.filter(name=p.payment_type.name).prefetch_related('payment_categories').first()
                        if global_pt: g_categories = list(global_pt.payment_categories.all())

                if g_categories:
                    val_per_cat = p.montant_paye / len(g_categories)
                    with schema_context('public'):
                        for g_cat in g_categories:
                            poste = PostesBudgetaire.objects.filter(payment_categories=g_cat).first()
                            if poste: add_real(poste.id, val_per_cat, p.date_paiement)

            # Autre Produits
            autres = AutreProduit.objects.filter(date_paiement__gte=campaign.date_debut, date_paiement__lte=campaign.date_fin, payment_type__isnull=False).prefetch_related('lettrages', 'payment_type')
            for ap in autres:
                if ap.mode_paiement in ['che', 'vir'] and not ap.lettrages.exists(): continue
                with schema_context('public'):
                    global_pt = GlobalPaymentType.objects.filter(name=ap.payment_type.name).prefetch_related('payment_categories').first()
                    if global_pt:
                        cats = global_pt.payment_categories.all()
                        if cats:
                            val = ap.montant_paiement / cats.count()
                            for g_cat in cats:
                                poste = PostesBudgetaire.objects.filter(payment_categories=g_cat).first()
                                if poste: add_real(poste.id, val, ap.date_paiement)

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
    total_dispatched_depense = Decimal('0')
    total_realized_recette = Decimal('0')
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
                    total_realized_recette += realise
                else:
                    total_dispatched_depense += full_prevu
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
                })
            
            combined_postes.append(group_data)

    return {
        'combined_postes': combined_postes,
        'totals': {
            'dispatched_recette': total_dispatched_recette,
            'realized_recette': total_realized_recette,
            'recette_ecart': total_realized_recette - total_dispatched_recette,
            'dispatched_depense': total_dispatched_depense,
            'realized_depense': total_realized_depense,
            'depense_ecart': total_realized_depense - total_dispatched_depense,
            'global_dispatched': total_dispatched_recette - total_dispatched_depense,
            'global_realized': total_realized_recette - total_realized_depense
        }
    }
