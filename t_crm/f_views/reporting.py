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
    # 1. Prospects per Status (Statut)
    # statut choices: ('visiteur','Visiteur'),('prinscrit','Pré-inscrit'),('instance','Instance de paiement'),('convertit','Convertit'),('annuler','Inscription Annulée')
    status_data = Prospets.objects.values('statut').annotate(count=Count('id')).order_by('-count')
    
    # Mapping for better display in charts if needed, usually frontend handles it but we can send labels
    statut_dict = dict(Prospets._meta.get_field('statut').choices)
    formatted_status = []
    for item in status_data:
        label = statut_dict.get(item['statut'], item['statut'])
        formatted_status.append({
            'label': label,
            'count': item['count'],
            'code': item['statut']
        })

    # 2. Prospects per Type (Particulier vs Entreprise)
    type_data = Prospets.objects.values('type_prospect').annotate(count=Count('id')).order_by('-count')
    formatted_type = []
    type_dict = dict(Prospets._meta.get_field('type_prospect').choices)
    for item in type_data:
        label = type_dict.get(item['type_prospect'], item['type_prospect'])
        formatted_type.append({
            'label': label,
            'count': item['count']
        })

    # 3. Prospects per Channel
    channel_data = Prospets.objects.values('canal').annotate(count=Count('id')).order_by('-count')
    formatted_channel = []
    canal_dict = dict(Prospets._meta.get_field('canal').choices)
    for item in channel_data:
        label = canal_dict.get(item['canal'], item['canal'])
        formatted_channel.append({
            'label': label,
            'count': item['count']
        })

    # 4. Evolution (Last 30 days)
    # Use timezone aware datetime
    last_30_days = timezone.now() - timedelta(days=30)
    evolution_data = Prospets.objects.filter(created_at__gte=last_30_days)\
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

    # 5. Key Metrics
    total_prospects = Prospets.objects.count()
    total_converted = Prospets.objects.filter(statut='convertit').count()
    conversion_rate = round((total_converted / total_prospects * 100), 2) if total_prospects > 0 else 0
    total_new_this_month = Prospets.objects.filter(created_at__month=timezone.now().month).count()

    # --- Matrix Data: Speciality x Status ---
    
    # Get promo_id from request
    promo_id = request.GET.get('promo_id')
    
    # Define filters
    simple_filter = Q()
    double_filter = Q()
    
    if promo_id:
        simple_filter = Q(specialite_fiche_voeux__promo_id=promo_id)
        double_filter = Q(fichevoeuxdouble__promo_id=promo_id)

    # 1. Simple Diplomation (FicheDeVoeux -> Specialites)
    # Using the related_name 'specialite_fiche_voeux' from FicheDeVoeux model
    matrix_simple_qs = Specialites.objects.annotate(
        visiteur=Count('specialite_fiche_voeux', filter=Q(specialite_fiche_voeux__prospect__statut='visiteur') & simple_filter),
        prinscrit=Count('specialite_fiche_voeux', filter=Q(specialite_fiche_voeux__prospect__statut='prinscrit') & simple_filter),
        instance=Count('specialite_fiche_voeux', filter=Q(specialite_fiche_voeux__prospect__statut='instance') & simple_filter),
        convertit=Count('specialite_fiche_voeux', filter=Q(specialite_fiche_voeux__prospect__statut='convertit') & simple_filter),
        annuler=Count('specialite_fiche_voeux', filter=Q(specialite_fiche_voeux__prospect__statut='annuler') & simple_filter),
        total=Count('specialite_fiche_voeux', filter=simple_filter)
    ).values('label', 'visiteur', 'prinscrit', 'instance', 'convertit', 'annuler', 'total').order_by('-total')

    # 2. Double Diplomation (FicheVoeuxDouble -> DoubleDiplomation)
    # Default related_name is 'fichevoeuxdouble_set'
    matrix_double_qs = DoubleDiplomation.objects.annotate(
        visiteur=Count('fichevoeuxdouble', filter=Q(fichevoeuxdouble__prospect__statut='visiteur') & double_filter),
        prinscrit=Count('fichevoeuxdouble', filter=Q(fichevoeuxdouble__prospect__statut='prinscrit') & double_filter),
        instance=Count('fichevoeuxdouble', filter=Q(fichevoeuxdouble__prospect__statut='instance') & double_filter),
        convertit=Count('fichevoeuxdouble', filter=Q(fichevoeuxdouble__prospect__statut='convertit') & double_filter),
        annuler=Count('fichevoeuxdouble', filter=Q(fichevoeuxdouble__prospect__statut='annuler') & double_filter),
        total=Count('fichevoeuxdouble', filter=double_filter)
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
            'new_this_month': total_new_this_month
        }
    })
