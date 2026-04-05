from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F
from t_formations.models import Specialites, DoubleDiplomation, Promos
from django.db.models.functions import TruncDate
from ..models import Prospets
from datetime import datetime, timedelta
from django.utils import timezone

@login_required(login_url='institut_app:login')
def crm_reporting(request):
    promos = Promos.objects.filter(etat='active')
    context = {
        'tenant': request.tenant,
        'promos': promos,
    }
    return render(request, 'tenant_folder/crm/reporting.html', context)

@login_required(login_url='institut_app:login')
def ApiGetCrmReportingData(request):
    promo_id = request.GET.get('promo_id')

    # Base queryset for all academic reporting
    base_qs = Prospets.objects.filter(context='acc').exclude(is_ets_prospect=True).exclude(type_prospect='entreprise')\
        .filter(conseil_commercial__isnull=True)\
        .filter(opportunites__isnull=True)\
        .filter(client_devis__isnull=True)

    # 1. Prospects per Status (Statut)
    status_data = base_qs.values('statut').annotate(count=Count('id')).order_by('-count')
    statut_dict = dict(Prospets._meta.get_field('statut').choices)
    formatted_status = []
    for item in status_data:
        label = statut_dict.get(item['statut'], item['statut'])
        formatted_status.append({
            'label': label,
            'count': item['count'],
            'code': item['statut']
        })

    # 2. Prospects per Type
    type_data = base_qs.values('type_prospect').annotate(count=Count('id')).order_by('-count')
    formatted_type = []
    type_dict = dict(Prospets._meta.get_field('type_prospect').choices)
    for item in type_data:
        label = type_dict.get(item['type_prospect'], item['type_prospect'])
        formatted_type.append({
            'label': label,
            'count': item['count']
        })

    # 3. Prospects per Channel
    channel_data = base_qs.values('canal').annotate(count=Count('id')).order_by('-count')
    formatted_channel = []
    canal_dict = dict(Prospets._meta.get_field('canal').choices)
    for item in channel_data:
        label = canal_dict.get(item['canal'], item['canal'])
        formatted_channel.append({
            'label': label,
            'count': item['count']
        })

    # 4. Evolution (Last 30 days)
    last_30_days = timezone.now() - timedelta(days=30)
    evolution_data = base_qs.filter(created_at__gte=last_30_days)\
        .annotate(date=TruncDate('created_at'))\
        .values('date')\
        .annotate(count=Count('id'))\
        .order_by('date')
    
    formatted_evolution = []
    for item in evolution_data:
        formatted_evolution.append({
            'date': item['date'].strftime('%Y-%m-%d'),
            'count': item['count']
        })

    # 5. Key Metrics (KPIs)
    kpi_qs = base_qs
    if promo_id:
        kpi_qs = kpi_qs.filter(
            Q(prospect_fiche_voeux__promo__id=promo_id) | 
            Q(prospect_fiche_voeux_double__promo__id=promo_id)
        ).distinct()

    total_prospects = kpi_qs.count()
    total_converted = kpi_qs.filter(statut='convertit').count()
    conversion_rate = round((total_converted / total_prospects * 100), 2) if total_prospects > 0 else 0
    total_new_this_month = kpi_qs.filter(created_at__month=timezone.now().month, created_at__year=timezone.now().year).count()
    total_without_voeux = kpi_qs.filter(prospect_fiche_voeux__isnull=True, prospect_fiche_voeux_double__isnull=True).count()
    total_canceled = kpi_qs.filter(statut='annuler').count()

    # --- Matrix Data ---
    simple_filter = Q(specialite_fiche_voeux__promo_id=promo_id) if promo_id else Q()
    double_filter = Q(fichevoeuxdouble__promo_id=promo_id) if promo_id else Q()

    matrix_simple_qs = Specialites.objects.annotate(
        visiteur=Count('specialite_fiche_voeux', filter=Q(specialite_fiche_voeux__prospect__statut='visiteur') & Q(specialite_fiche_voeux__prospect__context='acc') & Q(specialite_fiche_voeux__prospect__is_ets_prospect=False) & ~Q(specialite_fiche_voeux__prospect__type_prospect='entreprise') & Q(specialite_fiche_voeux__prospect__conseil_commercial__isnull=True) & Q(specialite_fiche_voeux__prospect__opportunites__isnull=True) & Q(specialite_fiche_voeux__prospect__client_devis__isnull=True) & simple_filter),
        prinscrit=Count('specialite_fiche_voeux', filter=Q(specialite_fiche_voeux__prospect__statut='prinscrit') & Q(specialite_fiche_voeux__prospect__context='acc') & Q(specialite_fiche_voeux__prospect__is_ets_prospect=False) & ~Q(specialite_fiche_voeux__prospect__type_prospect='entreprise') & Q(specialite_fiche_voeux__prospect__conseil_commercial__isnull=True) & Q(specialite_fiche_voeux__prospect__opportunites__isnull=True) & Q(specialite_fiche_voeux__prospect__client_devis__isnull=True) & simple_filter),
        instance=Count('specialite_fiche_voeux', filter=Q(specialite_fiche_voeux__prospect__statut='instance') & Q(specialite_fiche_voeux__prospect__context='acc') & Q(specialite_fiche_voeux__prospect__is_ets_prospect=False) & ~Q(specialite_fiche_voeux__prospect__type_prospect='entreprise') & Q(specialite_fiche_voeux__prospect__conseil_commercial__isnull=True) & Q(specialite_fiche_voeux__prospect__opportunites__isnull=True) & Q(specialite_fiche_voeux__prospect__client_devis__isnull=True) & simple_filter),
        convertit=Count('specialite_fiche_voeux', filter=Q(specialite_fiche_voeux__prospect__statut='convertit') & Q(specialite_fiche_voeux__prospect__context='acc') & Q(specialite_fiche_voeux__prospect__is_ets_prospect=False) & ~Q(specialite_fiche_voeux__prospect__type_prospect='entreprise') & Q(specialite_fiche_voeux__prospect__conseil_commercial__isnull=True) & Q(specialite_fiche_voeux__prospect__opportunites__isnull=True) & Q(specialite_fiche_voeux__prospect__client_devis__isnull=True) & simple_filter),
        annuler=Count('specialite_fiche_voeux', filter=Q(specialite_fiche_voeux__prospect__statut='annuler') & Q(specialite_fiche_voeux__prospect__context='acc') & Q(specialite_fiche_voeux__prospect__is_ets_prospect=False) & ~Q(specialite_fiche_voeux__prospect__type_prospect='entreprise') & Q(specialite_fiche_voeux__prospect__conseil_commercial__isnull=True) & Q(specialite_fiche_voeux__prospect__opportunites__isnull=True) & Q(specialite_fiche_voeux__prospect__client_devis__isnull=True) & simple_filter),
        total=Count('specialite_fiche_voeux', filter=Q(specialite_fiche_voeux__prospect__context='acc') & Q(specialite_fiche_voeux__prospect__is_ets_prospect=False) & ~Q(specialite_fiche_voeux__prospect__type_prospect='entreprise') & Q(specialite_fiche_voeux__prospect__conseil_commercial__isnull=True) & Q(specialite_fiche_voeux__prospect__opportunites__isnull=True) & Q(specialite_fiche_voeux__prospect__client_devis__isnull=True) & simple_filter)
    ).values('label', 'formation__nom', 'visiteur', 'prinscrit', 'instance', 'convertit', 'annuler', 'total').order_by('-total')

    matrix_double_qs = DoubleDiplomation.objects.annotate(
        visiteur=Count('fichevoeuxdouble', filter=Q(fichevoeuxdouble__prospect__statut='visiteur') & Q(fichevoeuxdouble__prospect__context='acc') & Q(fichevoeuxdouble__prospect__is_ets_prospect=False) & ~Q(fichevoeuxdouble__prospect__type_prospect='entreprise') & Q(fichevoeuxdouble__prospect__conseil_commercial__isnull=True) & Q(fichevoeuxdouble__prospect__opportunites__isnull=True) & Q(fichevoeuxdouble__prospect__client_devis__isnull=True) & double_filter),
        prinscrit=Count('fichevoeuxdouble', filter=Q(fichevoeuxdouble__prospect__statut='prinscrit') & Q(fichevoeuxdouble__prospect__context='acc') & Q(fichevoeuxdouble__prospect__is_ets_prospect=False) & ~Q(fichevoeuxdouble__prospect__type_prospect='entreprise') & Q(fichevoeuxdouble__prospect__conseil_commercial__isnull=True) & Q(fichevoeuxdouble__prospect__opportunites__isnull=True) & Q(fichevoeuxdouble__prospect__client_devis__isnull=True) & double_filter),
        instance=Count('fichevoeuxdouble', filter=Q(fichevoeuxdouble__prospect__statut='instance') & Q(fichevoeuxdouble__prospect__context='acc') & Q(fichevoeuxdouble__prospect__is_ets_prospect=False) & ~Q(fichevoeuxdouble__prospect__type_prospect='entreprise') & Q(fichevoeuxdouble__prospect__conseil_commercial__isnull=True) & Q(fichevoeuxdouble__prospect__opportunites__isnull=True) & Q(fichevoeuxdouble__prospect__client_devis__isnull=True) & double_filter),
        convertit=Count('fichevoeuxdouble', filter=Q(fichevoeuxdouble__prospect__statut='convertit') & Q(fichevoeuxdouble__prospect__context='acc') & Q(fichevoeuxdouble__prospect__is_ets_prospect=False) & ~Q(fichevoeuxdouble__prospect__type_prospect='entreprise') & Q(fichevoeuxdouble__prospect__conseil_commercial__isnull=True) & Q(fichevoeuxdouble__prospect__opportunites__isnull=True) & Q(fichevoeuxdouble__prospect__client_devis__isnull=True) & double_filter),
        annuler=Count('fichevoeuxdouble', filter=Q(fichevoeuxdouble__prospect__statut='annuler') & Q(fichevoeuxdouble__prospect__context='acc') & Q(fichevoeuxdouble__prospect__is_ets_prospect=False) & ~Q(fichevoeuxdouble__prospect__type_prospect='entreprise') & Q(fichevoeuxdouble__prospect__conseil_commercial__isnull=True) & Q(fichevoeuxdouble__prospect__opportunites__isnull=True) & Q(fichevoeuxdouble__prospect__client_devis__isnull=True) & double_filter),
        total=Count('fichevoeuxdouble', filter=Q(fichevoeuxdouble__prospect__context='acc') & Q(fichevoeuxdouble__prospect__is_ets_prospect=False) & ~Q(fichevoeuxdouble__prospect__type_prospect='entreprise') & Q(fichevoeuxdouble__prospect__conseil_commercial__isnull=True) & Q(fichevoeuxdouble__prospect__opportunites__isnull=True) & Q(fichevoeuxdouble__prospect__client_devis__isnull=True) & double_filter)
    ).values('label', 'visiteur', 'prinscrit', 'instance', 'convertit', 'annuler', 'total').order_by('-total')

    return JsonResponse({
        'status_distribution': formatted_status,
        'type_distribution': formatted_type,
        'channel_distribution': formatted_channel,
        'evolution': formatted_evolution,
        'matrix_simple': list(matrix_simple_qs),
        'matrix_double': list(matrix_double_qs),
        'kpi': {
            'total': total_prospects,
            'converted': total_converted,
            'conversion_rate': conversion_rate,
            'new_this_month': total_new_this_month,
            'without_voeux': total_without_voeux,
            'canceled': total_canceled
        }
    })
