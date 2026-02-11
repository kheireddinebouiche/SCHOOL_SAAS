from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import GlobalPaymentCategory, GlobalDepensesCategory
from .forms import GlobalPaymentCategoryForm, GlobalDepensesCategoryForm
from django.contrib import messages
from .utils import sync_global_categories
from app.models import Institut
from django_tenants.utils import schema_context
from t_tresorerie.models import PaymentCategory, DepensesCategory
from t_crm.models import Prospets, Opportunite
from django.db.models import Sum, Count

@login_required(login_url='login')
def index(request):
    return render(request, 'public_folder/configuration_index.html')

@login_required(login_url='login')
def configuration_budget(request):
    return render(request, 'public_folder/configuration.html')

@login_required(login_url='login')
def configuration_structure(request):
    return render(request, 'public_folder/configuration.html')

# --- Global Payment Category Views ---

@login_required(login_url='login')
def global_payment_category_list(request):
    categories = GlobalPaymentCategory.objects.all()
    form = GlobalPaymentCategoryForm()
    return render(request, 'associe_app/global_payment_category_list.html', {'categories': categories, 'form': form})

@login_required(login_url='login')
def global_payment_category_create(request):
    if request.method == 'POST':
        form = GlobalPaymentCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Catégorie de paiement créée avec succès.'})
            return redirect('global_payment_category_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.as_json()})
    return redirect('global_payment_category_list')

@login_required(login_url='login')
def global_payment_category_edit(request, pk):
    category = get_object_or_404(GlobalPaymentCategory, pk=pk)
    if request.method == 'POST':
        form = GlobalPaymentCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Catégorie de paiement modifiée avec succès.'})
            return redirect('global_payment_category_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.as_json()})
    
    # For loading form data via AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'name': category.name,
            'parent': category.parent.id if category.parent else '',
            'category_type': category.category_type
        })
    return redirect('global_payment_category_list')

@login_required(login_url='login')
def global_payment_category_delete(request, pk):
    category = get_object_or_404(GlobalPaymentCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Catégorie de paiement supprimée avec succès.'})
    return redirect('global_payment_category_list')

# --- Global Depenses Category Views ---

@login_required(login_url='login')
def global_depenses_category_list(request):
    categories = GlobalDepensesCategory.objects.all()
    form = GlobalDepensesCategoryForm()
    return render(request, 'associe_app/global_depenses_category_list.html', {'categories': categories, 'form': form})

@login_required(login_url='login')
def global_depenses_category_create(request):
    if request.method == 'POST':
        form = GlobalDepensesCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Catégorie de dépense créée avec succès.'})
            return redirect('global_depenses_category_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.as_json()})
    return redirect('global_depenses_category_list')

@login_required(login_url='login')
def global_depenses_category_edit(request, pk):
    category = get_object_or_404(GlobalDepensesCategory, pk=pk)
    if request.method == 'POST':
        form = GlobalDepensesCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Catégorie de dépense modifiée avec succès.'})
            return redirect('global_depenses_category_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.as_json()})
    
    # For loading form data via AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'name': category.name,
            'parent': category.parent.id if category.parent else '',
            'payment_category': category.payment_category.id if category.payment_category else ''
        })
    return redirect('global_depenses_category_list')

@login_required(login_url='login')
def global_depenses_category_delete(request, pk):
    category = get_object_or_404(GlobalDepensesCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Catégorie de dépense supprimée avec succès.'})
    return redirect('global_depenses_category_list')

@login_required(login_url='login')
def sync_categories_view(request):
    try:
        sync_global_categories()
        msg = "Synchronisation effectuée avec succès sur tous les tenants."
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': msg})
        messages.success(request, msg)
    except Exception as e:
        msg = f"Erreur lors de la synchronisation : {str(e)}"
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': msg})
        messages.error(request, msg)
    
    return redirect(request.META.get('HTTP_REFERER', 'configuration_index'))

@login_required(login_url='login')
def tenant_data_list(request):
    tenants = Institut.objects.exclude(schema_name='public')
    return render(request, 'associe_app/tenant_visualization.html', {'tenants': tenants})

@login_required(login_url='login')
def get_tenant_categories(request, tenant_id):
    tenant = get_object_or_404(Institut, id=tenant_id)
    payment_categories = []
    depenses_categories = []
    crm_stats = {}
    
    with schema_context(tenant.schema_name):
        # Fetch payment categories
        p_cats = PaymentCategory.objects.all()
        for pc in p_cats:
            payment_categories.append({
                'id': pc.id,
                'name': pc.name,
                'parent': pc.parent.name if pc.parent else '-',
                'type': pc.get_category_type_display()
            })
            
        # Fetch depenses categories
        d_cats = DepensesCategory.objects.all()
        for dc in d_cats:
            depenses_categories.append({
                'id': dc.id,
                'name': dc.name,
                'parent': dc.parent.name if dc.parent else '-',
                'payment_category': dc.payment_category.name if dc.payment_category else '-'
            })

        # CRM Statistics
        all_prospects = Prospets.objects.all()
        crm_stats = {
            'total_prospects': all_prospects.count(),
            'by_status': list(all_prospects.values('statut').annotate(count=Count('statut'))),
            'by_etat': list(all_prospects.values('etat').annotate(count=Count('etat'))),
            'active_opportunities': Opportunite.objects.filter(is_active=True).count(),
            'total_budget': float(Opportunite.objects.filter(is_active=True).aggregate(total=Sum('budget'))['total'] or 0)
        }

    return JsonResponse({
        'status': 'success',
        'tenant_name': tenant.nom,
        'payment_categories': payment_categories,
        'depenses_categories': depenses_categories,
        'crm_stats': crm_stats
    })

@login_required(login_url='login')
def crm_statistics(request):
    tenants = Institut.objects.exclude(schema_name='public').order_by('nom')
    institutes_stats = []
    
    # Prospect Status List
    statuses = ['visiteur', 'prinscrit', 'instance', 'convertit', 'annuler']
    global_stats = {
        'total_prospects': 0,
        'active_opportunities': 0,
        'total_budget': 0,
        'status_counts': {s: 0 for s in statuses}
    }

    for tenant in tenants:
        try:
            with schema_context(tenant.schema_name):
                # Basic counts
                all_prospects = Prospets.objects.all()
                prospects_count = all_prospects.count()
                
                opportunities = Opportunite.objects.filter(is_active=True)
                opportunities_count = opportunities.count()
                budget_sum = float(opportunities.aggregate(total=Sum('budget'))['total'] or 0)

                # Status breakdown for global summation
                for s in statuses:
                    count = all_prospects.filter(statut=s).count()
                    global_stats['status_counts'][s] += count

                institutes_stats.append({
                    'id': tenant.id,
                    'name': tenant.nom,
                    'prospects_count': prospects_count,
                    'opportunities_count': opportunities_count,
                    'budget_sum': budget_sum
                })

                global_stats['total_prospects'] += prospects_count
                global_stats['active_opportunities'] += opportunities_count
                global_stats['total_budget'] += budget_sum
        except Exception as e:
            continue

    context = {
        'tenants': tenants, # For the selector
        'institutes_stats': institutes_stats,
        'global_stats': global_stats,
    }
    return render(request, 'associe_app/crm_statistics.html', context)

@login_required(login_url='login')
def get_crm_stats_api(request, tenant_id):
    """Dynamic API for CRM stats of a specific institute"""
    tenant = get_object_or_404(Institut, id=tenant_id)
    statuses = ['visiteur', 'prinscrit', 'instance', 'convertit', 'annuler']
    
    try:
        with schema_context(tenant.schema_name):
            all_prospects = Prospets.objects.all()
            total_prospects = all_prospects.count()
            
            opportunities = Opportunite.objects.filter(is_active=True)
            active_opportunities = opportunities.count()
            total_budget = float(opportunities.aggregate(total=Sum('budget'))['total'] or 0)
            
            status_breakdown = []
            for s in statuses:
                count = all_prospects.filter(statut=s).count()
                status_breakdown.append({
                    'statut': s,
                    'label': s.capitalize(), # Map these better in frontend or backend
                    'count': count,
                    'percentage': (count / total_prospects * 100) if total_prospects > 0 else 0
                })

            return JsonResponse({
                'status': 'success',
                'tenant_name': tenant.nom,
                'total_prospects': total_prospects,
                'active_opportunities': active_opportunities,
                'total_budget': total_budget,
                'status_breakdown': status_breakdown
            })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url='login')
def purge_tenant_categories(request, tenant_id):
    tenant = get_object_or_404(Institut, id=tenant_id)
    
    if request.method == 'POST':
        try:
            with schema_context(tenant.schema_name):
                # Delete all synchronized categories
                # Note: We are deleting from t_tresorerie.models, not associe_app.models
                DepensesCategory.objects.all().delete()
                PaymentCategory.objects.all().delete()
                
            return JsonResponse({
                'status': 'success', 
                'message': f'Données du tenant "{tenant.nom}" purgées avec succès.'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': f'Erreur lors de la purge: {str(e)}'
            })
            
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

# --- Postes Budgetaires Views ---

from .models import PostesBudgetaire
from .forms import PostesBudgetaireForm

@login_required(login_url='login')
def postes_budgetaires_list(request):
    postes = PostesBudgetaire.objects.all()
    form = PostesBudgetaireForm()
    return render(request, 'associe_app/postes_budgetaires_list.html', {'postes': postes, 'form': form})

@login_required(login_url='login')
def postes_budgetaire_create(request):
    if request.method == 'POST':
        form = PostesBudgetaireForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Poste budgétaire créé avec succès.'})
            return redirect('postes_budgetaires_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.as_json()})
    return redirect('postes_budgetaires_list')

@login_required(login_url='login')
def postes_budgetaire_edit(request, pk):
    poste = get_object_or_404(PostesBudgetaire, pk=pk)
    if request.method == 'POST':
        form = PostesBudgetaireForm(request.POST, instance=poste)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Poste budgétaire modifié avec succès.'})
            return redirect('postes_budgetaires_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.as_json()})
    
    # For loading form data via AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'label': poste.label,
            'type': poste.type,
            'description': poste.description,
            'parent': poste.parent.id if poste.parent else '',
            'depense_categories': list(poste.depense_categories.values_list('id', flat=True)),
            'payment_categories': list(poste.payment_categories.values_list('id', flat=True))
        })
    return redirect('postes_budgetaires_list')

@login_required(login_url='login')
def postes_budgetaire_delete(request, pk):
    poste = get_object_or_404(PostesBudgetaire, pk=pk)
    if request.method == 'POST':
        poste.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Poste budgétaire supprimé avec succès.'})
    return redirect('postes_budgetaires_list')
