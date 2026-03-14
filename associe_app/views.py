import json
import io
import openpyxl
from openpyxl import Workbook
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse
from .models import GlobalPaymentCategory, GlobalDepensesCategory, GlobalPaymentType, PostesBudgetaire
from .forms import GlobalPaymentCategoryForm, GlobalDepensesCategoryForm, GlobalPaymentTypeForm
from .utils import sync_global_categories
from django.contrib import messages
from app.models import Institut
from django_tenants.utils import schema_context
from t_tresorerie.models import PaymentCategory, DepensesCategory
from t_crm.models import Prospets, Opportunite
from django.db.models import Sum, Count
from institut_app.models import Entreprise
from .models import BudgetCampaign, BudgetLine, PostesBudgetaire, BudgetLineDetail
from .budget_utils import get_campaign_realization_data

@login_required
def sync_payment_types(request):
    if request.method == 'POST':
        try:
            sync_global_categories()
            return JsonResponse({'success': True, 'message': 'Synchronisation terminée avec succès.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur lors de la synchronisation : {str(e)}'})
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'}, status=405)
from t_crm.models import Prospets, Opportunite
from django.db.models import Sum, Count
from institut_app.models import Entreprise
from .models import BudgetCampaign, BudgetLine, PostesBudgetaire, BudgetLineDetail

@login_required(login_url='login')
def index(request):
    return render(request, 'public_folder/configuration_index.html')

@login_required(login_url='login')
def configuration_budget(request):
    return render(request, 'public_folder/configuration.html')

@login_required(login_url='login')
def configuration_structure(request):
    return render(request, 'public_folder/configuration.html')

# --- Global Payment Type Views ---

@login_required(login_url='login')
def global_payment_type_list(request):
    types = GlobalPaymentType.objects.all().order_by('name')
    types_list = []
    for t in types:
        cats = t.payment_categories.all()
        types_list.append({
            'id': t.id,
            'name': t.name,
            'payment_categories': [{'id': c.id, 'name': c.name} for c in cats],
            'category_ids': [c.id for c in cats]
        })
    
    import json
    types_json = json.dumps(types_list)
    
    form = GlobalPaymentTypeForm()
    return render(request, 'associe_app/global_payment_type_list.html', {
        'types': types, 
        'types_json': types_json,
        'form': form
    })

@login_required(login_url='login')
def global_payment_type_create(request):
    if request.method == 'POST':
        form = GlobalPaymentTypeForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Type de paiement créé avec succès.'})
            return redirect('associe_app:global_payment_type_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.get_json_data()})
    return redirect('associe_app:global_payment_type_list')

@login_required(login_url='login')
def global_payment_type_edit(request, pk):
    payment_type = get_object_or_404(GlobalPaymentType, pk=pk)
    if request.method == 'POST':
        form = GlobalPaymentTypeForm(request.POST, instance=payment_type)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Type de paiement modifié avec succès.'})
            return redirect('associe_app:global_payment_type_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.get_json_data()})
    
    # For loading form data via AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'name': payment_type.name,
            'payment_categories': list(payment_type.payment_categories.values_list('id', flat=True))
        })
    return redirect('associe_app:global_payment_type_list')

@login_required(login_url='login')
def global_payment_type_delete(request, pk):
    payment_type = get_object_or_404(GlobalPaymentType, pk=pk)
    if request.method == 'POST':
        payment_type.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Type de paiement supprimé avec succès.'})
    return redirect('associe_app:global_payment_type_list')

# --- Helper Functions for Real-Time Serialization ---

def _get_payment_categories_list():
    categories = GlobalPaymentCategory.objects.all().order_by('name')
    categories_list = []
    for cat in categories:
        categories_list.append({
            'id': cat.id,
            'name': cat.name,
            'parent_id': cat.parent.id if cat.parent else None,
            'type': cat.category_type,
            'type_display': cat.get_category_type_display()
        })
    return categories_list

def _get_depenses_categories_list():
    categories = GlobalDepensesCategory.objects.all().order_by('name')
    categories_list = []
    for cat in categories:
        categories_list.append({
            'id': cat.id,
            'name': cat.name,
            'parent_id': cat.parent.id if cat.parent else None,
            'payment_category': cat.payment_category.name if cat.payment_category else '-',
            'payment_category_id': cat.payment_category.id if cat.payment_category else None
        })
    return categories_list

# --- Global Payment Category Views ---

@login_required(login_url='login')
def global_payment_category_list(request):
    categories_list = _get_payment_categories_list()
    import json
    categories_json = json.dumps(categories_list)
    form = GlobalPaymentCategoryForm()
    return render(request, 'associe_app/global_payment_category_list.html', {
        'categories_json': categories_json,
        'form': form
    })

@login_required(login_url='login')
def global_payment_category_create(request):
    if request.method == 'POST':
        form = GlobalPaymentCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Catégorie de paiement créée avec succès.',
                    'categories': _get_payment_categories_list(),
                    'new_id': category.id,
                    'parent_id': category.parent.id if category.parent else None
                })
            return redirect('associe_app:global_payment_category_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.get_json_data()})
    return redirect('associe_app:global_payment_category_list')

@login_required(login_url='login')
def global_payment_category_edit(request, pk):
    category = get_object_or_404(GlobalPaymentCategory, pk=pk)
    if request.method == 'POST':
        form = GlobalPaymentCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Catégorie de paiement modifiée avec succès.',
                    'categories': _get_payment_categories_list()
                })
            return redirect('associe_app:global_payment_category_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.get_json_data()})
    
    # For loading form data via AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'name': category.name,
            'parent': category.parent.id if category.parent else '',
            'category_type': category.category_type
        })
    return redirect('associe_app:global_payment_category_list')

@login_required(login_url='login')
def global_payment_category_delete(request, pk):
    category = get_object_or_404(GlobalPaymentCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success', 
                'message': 'Catégorie de paiement supprimée avec succès.',
                'categories': _get_payment_categories_list()
            })
    return redirect('associe_app:global_payment_category_list')

@login_required(login_url='login')
def export_payment_categories(request):
    categories = GlobalPaymentCategory.objects.all().order_by('id')
    wb = Workbook()
    ws = wb.active
    ws.title = "Payment Categories"
    
    headers = ['ID', 'Nom', 'Parent_ID', 'Parent_Nom', 'Type']
    ws.append(headers)
    
    for cat in categories:
        ws.append([
            cat.id,
            cat.name,
            cat.parent.id if cat.parent else '',
            cat.parent.name if cat.parent else '',
            cat.category_type
        ])
    
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    response = FileResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="categories_paiement.xlsx"'
    return response

@login_required(login_url='login')
def import_payment_categories(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        filename = file.name.lower()
        data = []
        
        try:
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                wb = openpyxl.load_workbook(file)
                ws = wb.active
                headers = [cell.value for cell in ws[1]]
                for row in ws.iter_rows(min_row=2, values_only=True):
                    if not any(row): continue
                    data.append(dict(zip(headers, row)))
            elif filename.endswith('.json'):
                data = json.load(file)
            else:
                return JsonResponse({'status': 'error', 'message': 'Format non supporté.'})
            
            # Hierarchical Import Logic (Simple multi-pass)
            success_count = 0
            # Pass 1: Roots and updates
            for row in data:
                parent_id = row.get('Parent_ID') or row.get('parent_id')
                # If no parent or parent exists, we can create/update
                parent = None
                if parent_id:
                    parent = GlobalPaymentCategory.objects.filter(id=parent_id).first()
                
                GlobalPaymentCategory.objects.update_or_create(
                    id=row.get('ID') or row.get('id'),
                    defaults={
                        'name': row.get('Nom') or row.get('name'),
                        'parent': parent,
                        'category_type': row.get('Type') or row.get('category_type') or 'standard'
                    }
                )
                success_count += 1
                
            return JsonResponse({
                'status': 'success', 
                'message': f'{success_count} catégories importées.',
                'categories': _get_payment_categories_list()
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erreur: {str(e)}'})
            
    return JsonResponse({'status': 'error', 'message': 'Requête invalide.'})

# --- Global Depenses Category Views ---

@login_required(login_url='login')
def global_depenses_category_list(request):
    categories_list = _get_depenses_categories_list()
    import json
    categories_json = json.dumps(categories_list)
    form = GlobalDepensesCategoryForm()
    return render(request, 'associe_app/global_depenses_category_list.html', {
        'categories_json': categories_json,
        'form': form
    })

@login_required(login_url='login')
def global_depenses_category_create(request):
    if request.method == 'POST':
        form = GlobalDepensesCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Catégorie de dépense créée avec succès.',
                    'categories': _get_depenses_categories_list(),
                    'new_id': category.id,
                    'parent_id': category.parent.id if category.parent else None
                })
            return redirect('associe_app:global_depenses_category_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.get_json_data()})
    return redirect('associe_app:global_depenses_category_list')

@login_required(login_url='login')
def export_depenses_categories(request):
    categories = GlobalDepensesCategory.objects.all().order_by('id')
    wb = Workbook()
    ws = wb.active
    ws.title = "Depenses Categories"
    
    headers = ['ID', 'Nom', 'Parent_ID', 'Parent_Nom', 'Payment_Category_ID', 'Payment_Category_Nom']
    ws.append(headers)
    
    for cat in categories:
        ws.append([
            cat.id,
            cat.name,
            cat.parent.id if cat.parent else '',
            cat.parent.name if cat.parent else '',
            cat.payment_category.id if cat.payment_category else '',
            cat.payment_category.name if cat.payment_category else ''
        ])
    
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    response = FileResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="categories_depenses.xlsx"'
    return response

@login_required(login_url='login')
def import_depenses_categories(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        filename = file.name.lower()
        data = []
        
        try:
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                wb = openpyxl.load_workbook(file)
                ws = wb.active
                headers = [cell.value for cell in ws[1]]
                for row in ws.iter_rows(min_row=2, values_only=True):
                    if not any(row): continue
                    data.append(dict(zip(headers, row)))
            elif filename.endswith('.json'):
                data = json.load(file)
            else:
                return JsonResponse({'status': 'error', 'message': 'Format non supporté.'})
            
            success_count = 0
            for row in data:
                parent_id = row.get('Parent_ID') or row.get('parent_id')
                pay_cat_id = row.get('Payment_Category_ID') or row.get('payment_category_id')
                
                parent = None
                if parent_id:
                    parent = GlobalDepensesCategory.objects.filter(id=parent_id).first()
                
                pay_cat = None
                if pay_cat_id:
                    pay_cat = GlobalPaymentCategory.objects.filter(id=pay_cat_id).first()

                GlobalDepensesCategory.objects.update_or_create(
                    id=row.get('ID') or row.get('id'),
                    defaults={
                        'name': row.get('Nom') or row.get('name'),
                        'parent': parent,
                        'payment_category': pay_cat
                    }
                )
                success_count += 1
                
            return JsonResponse({
                'status': 'success', 
                'message': f'{success_count} catégories importées.',
                'categories': _get_depenses_categories_list()
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erreur: {str(e)}'})
            
    return JsonResponse({'status': 'error', 'message': 'Requête invalide.'})

@login_required(login_url='login')
def global_depenses_category_edit(request, pk):
    category = get_object_or_404(GlobalDepensesCategory, pk=pk)
    if request.method == 'POST':
        form = GlobalDepensesCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Catégorie de dépense modifiée avec succès.',
                    'categories': _get_depenses_categories_list()
                })
            return redirect('associe_app:global_depenses_category_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.get_json_data()})
    
    # For loading form data via AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'name': category.name,
            'parent': category.parent.id if category.parent else '',
            'payment_category': category.payment_category.id if category.payment_category else ''
        })
    return redirect('associe_app:global_depenses_category_list')

@login_required(login_url='login')
def global_depenses_category_delete(request, pk):
    category = get_object_or_404(GlobalDepensesCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success', 
                'message': 'Catégorie de dépense supprimée avec succès.',
                'categories': _get_depenses_categories_list()
            })
    return redirect('associe_app:global_depenses_category_list')

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
    
    return redirect(request.META.get('HTTP_REFERER', 'associe_app:configuration_index'))

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
    postes = PostesBudgetaire.objects.all().order_by('order', 'type', 'label')
    postes_list = []
    for poste in postes:
        postes_list.append({
            'id': poste.id,
            'name': poste.label, # Using 'name' for consistency with other trees
            'label': poste.label,
            'type': poste.type,
            'type_display': poste.get_type_display(),
            'parent_id': poste.parent.id if poste.parent else None,
            'description': poste.description,
            'order': poste.order,
            'depense_categories': [c.id for c in poste.depense_categories.all()],
            'depense_categories_labels': [c.name for c in poste.depense_categories.all()],
            'payment_categories': [c.id for c in poste.payment_categories.all()],
            'payment_categories_labels': [c.name for c in poste.payment_categories.all()]
        })
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(postes_list, safe=False)

    form = PostesBudgetaireForm()
    return render(request, 'associe_app/postes_budgetaires_list.html', {
        'postes': postes, 
        'form': form
    })

@login_required(login_url='login')
def postes_budgetaire_create(request):
    if request.method == 'POST':
        form = PostesBudgetaireForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Poste budgétaire créé avec succès.'})
            return redirect('associe_app:postes_budgetaires_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.get_json_data()})
    return redirect('associe_app:postes_budgetaires_list')

@login_required(login_url='login')
def postes_budgetaire_edit(request, pk):
    poste = get_object_or_404(PostesBudgetaire, pk=pk)
    if request.method == 'POST':
        form = PostesBudgetaireForm(request.POST, instance=poste)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Poste budgétaire modifié avec succès.'})
            return redirect('associe_app:postes_budgetaires_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors.get_json_data()})
    
    # For loading form data via AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'label': poste.label,
            'type': poste.type,
            'description': poste.description,
            'order': poste.order,
            'parent': poste.parent.id if poste.parent else '',
            'depense_categories': list(poste.depense_categories.values_list('id', flat=True)),
            'payment_categories': list(poste.payment_categories.values_list('id', flat=True))
        })
    return redirect('associe_app:postes_budgetaires_list')

@login_required(login_url='login')
def postes_budgetaire_delete(request, pk):
    poste = get_object_or_404(PostesBudgetaire, pk=pk)
    if request.method == 'POST':
        poste.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Poste budgétaire supprimé avec succès.'})
    return redirect('associe_app:postes_budgetaires_list')

# --- Budget Campaign Views ---

@login_required(login_url='login')
def budget_campaign_list(request):
    campaigns = BudgetCampaign.objects.all().order_by('-date_debut')
    active_count = BudgetCampaign.objects.filter(is_active=True).count()
    return render(request, 'associe_app/budget_campaign_list.html', {
        'campaigns': campaigns,
        'active_count': active_count
    })


@login_required(login_url='login')
def budget_campaign_activate(request, campaign_slug):
    campaign = get_object_or_404(BudgetCampaign, slug=campaign_slug)
    if request.method == 'POST':
        try:
            # Toggle the active status
            campaign.is_active = not campaign.is_active
            campaign.save()
            
            action_message = "activée" if campaign.is_active else "désactivée"
            messages.success(request, f"Campagne '{campaign.name}' {action_message} avec succès.")
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': f"Campagne '{campaign.name}' {action_message} avec succès."})
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la modification du statut de la campagne: {e}")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': f"Erreur lors de la modification du statut de la campagne: {e}"})
                
    return redirect('associe_app:budget_campaign_list')

@login_required(login_url='login')
def budget_campaign_delete(request, campaign_slug):
    campaign = get_object_or_404(BudgetCampaign, slug=campaign_slug)
    if request.method == 'POST':
        campaign.delete()
        messages.success(request, f"Campagne '{campaign.name}' supprimée avec succès.")
    return redirect('associe_app:budget_campaign_list')

@login_required(login_url='login')
def budget_campaign_instituts(request, campaign_slug):
    campaign = get_object_or_404(BudgetCampaign, slug=campaign_slug)
    instituts = Institut.objects.exclude(schema_name='public')
    
    # 1. Process Form Submission (Bulk Save)
    if request.method == 'POST':
        try:
            for key, value in request.POST.items():
                if key.startswith('budget_'):
                    # Format: budget_INSTITUTID
                    parts = key.split('_')
                    if len(parts) == 2:
                        inst_id = parts[1]
                        # Robust cleaning for accounting format
                        clean_value = value.replace(' ', '').replace('\xa0', '').replace('\u202f', '')
                        if ',' in clean_value and '.' in clean_value:
                            if clean_value.rfind(',') > clean_value.rfind('.'):
                                clean_value = clean_value.replace('.', '').replace(',', '.')
                            else:
                                clean_value = clean_value.replace(',', '')
                        else:
                            clean_value = clean_value.replace(',', '.')
                        
                        try:
                            amount = float(clean_value) if clean_value else 0
                            if amount >= 0:
                                BudgetLine.objects.update_or_create(
                                    campaign=campaign,
                                    institut_id=inst_id,
                                    defaults={'montant': amount}
                                )
                        except (ValueError, TypeError):
                            continue
            messages.success(request, "Objectifs globaux enregistrés avec succès.")
        except Exception as e:
             messages.error(request, f"Erreur lors de l'enregistrement: {e}")
        return redirect('associe_app:budget_campaign_instituts', campaign_slug=campaign.slug)

    # 2. Build Data for Display
    instituts_data = []
    configured_instituts = 0
    
    # Prefetch extensions to avoid N+1
    from .models import BudgetExtensionRequest
    pending_extensions = BudgetExtensionRequest.objects.filter(
        campaign=campaign, 
        status='pending'
    ).values_list('institut_id', 'id')
    
    # Create a map: institut_id -> request_id
    pending_extensions_map = {inst_id: req_id for inst_id, req_id in pending_extensions}

    for inst in instituts:
        line = BudgetLine.objects.filter(campaign=campaign, institut=inst).first()
        is_configured = line is not None
        if is_configured:
            configured_instituts += 1
            
        instituts_data.append({
            'institut': inst,
            'is_configured': is_configured,
            'montant': line.montant if line else 0,
            'statut': line.statut if line else 'none',
            'pending_extension_id': pending_extensions_map.get(inst.id)
        })
        
    total_inst = len(instituts)
    progress = (configured_instituts / total_inst * 100) if total_inst > 0 else 0
    
    return render(request, 'associe_app/budget_campaign_instituts.html', {
        'campaign': campaign,
        'instituts_data': instituts_data,
        'configured_count': configured_instituts,
        'pending_count': total_inst - configured_instituts,
        'progress': progress,
    })

@login_required(login_url='login')
def budget_campaign_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        # Automatic Date Logic: Fiscal Year starts Aug 1st
        today = date.today()
        if today.month < 8: # Jan - July
            start_year = today.year - 1
        else: # Aug - Dec
            start_year = today.year
            
        date_debut = date(start_year, 8, 1)
        date_fin = date(start_year + 1, 7, 31)
        
        default_name = f"Budget {start_year}-{start_year + 1}"
        
        if not name:
            name = default_name
            
        # Create or Get (to avoid duplicates for same period/name)
        campaign, created = BudgetCampaign.objects.get_or_create(
            name=name,
            defaults={
                'date_debut': date_debut, 
                'date_fin': date_fin, 
                'is_active': False
            }
        )
        
        if created:
            messages.success(request, f"Campagne '{name}' créée avec succès.")
        else:
            messages.info(request, f"La campagne '{name}' existe déjà.")
            
    return redirect('associe_app:budget_campaign_list')

@login_required(login_url='login')
def budget_campaign_review(request, campaign_slug, institut_id):
    """
    Review and Validate/Reject a tenant's budget dispatch proposal.
    """
    campaign = get_object_or_404(BudgetCampaign, slug=campaign_slug)
    institut = get_object_or_404(Institut, id=institut_id)
    budget_line = get_object_or_404(BudgetLine, campaign=campaign, institut=institut)
    
    # Restriction: Admin cannot see details until submitted
    is_visible_to_admin = budget_line.statut in ['submitted', 'validated', 'rejected']
    
    details = BudgetLineDetail.objects.none()
    structured_postes = []
    total_dispatched = 0
    entreprises = []
    row_quarters = {}
    allocations = {}

    if is_visible_to_admin:
        # 1. Global Items (Public)
        all_postes = PostesBudgetaire.objects.prefetch_related('payment_categories', 'depense_categories').order_by('order', 'type', 'label')
        
        structured_postes = []
        for p in all_postes:
            if p.parent is None:
                children = [child for child in all_postes if child.parent_id == p.id]
                display_postes = []
                # If parent has direct categories or no children, add it to display
                if p.payment_categories.exists() or p.depense_categories.exists() or not children:
                    display_postes.append(p)
                display_postes.extend(children)
                
                structured_postes.append({
                    'parent_poste': p,
                    'is_standalone': not children,
                    'display_postes': display_postes
                })

        details = BudgetLineDetail.objects.filter(campaign=campaign, institut=institut)
        # Map: {poste_id}_none_0_0 -> BudgetLineDetail (Aggregated)
        allocations = {}
        for d in details:
            # Aggregate everything at the poste level to match dispatch view
            key = f"{d.poste_id}_none_0_0"
            
            if key not in allocations:
                # We need a copy because we might modify montant
                import copy
                allocations[key] = copy.copy(d)
                # Ensure the copy reflects 'none' category for display logic match
                allocations[key].payment_category_id = None
                allocations[key].depense_category_id = None
            else:
                allocations[key].montant += d.montant
        
        total_dispatched = details.aggregate(Sum('montant'))['montant__sum'] or 0

        # 2. Tenant Specific Entities
        with schema_context(institut.schema_name):
            entreprises = list(Entreprise.objects.all().order_by('designation'))

    if request.method == "POST":
        action = request.POST.get('action')
        commentaire = request.POST.get('commentaire', '')
        
        if action == 'save_quartely':
            # Save quarterly percentages (Row Level)
            # Input format: tX_POSTE_CAT
            updated_details = []
            
            # Create a map of existing details for quick lookup: (poste_id, pay_cat_id, dep_cat_id) -> list of details
            details_map = {}
            for d in details:
                key = (d.poste_id, d.payment_category_id, d.depense_category_id)
                if key not in details_map:
                    details_map[key] = []
                details_map[key].append(d)

            for key, value in request.POST.items():
                if key.startswith('t1_') or key.startswith('t2_') or key.startswith('t3_') or key.startswith('t4_'):
                    # Format: tX_POSTE_CAT
                    parts = key.split('_') 
                    # Expect ['t1', '12', '5'] (cat exists) or ['t1', '12', 'None']
                    if len(parts) >= 3:
                        quarter = parts[0] # t1, t2, t3, t4
                        poste_id = parts[1]
                        cat_id_str = parts[2]
                        
                        try:
                            val = float(value.replace(',', '.')) if value else 0.0
                            val = min(max(val, 0), 100) # Clamp 0-100
                            
                            real_cat_id = int(cat_id_str) if cat_id_str.lower() != 'none' and cat_id_str != '' else None
                            
                            # Update ALL details for this row (Poste + Category)
                            # In this simplified view, we check both payment and depense categories
                            row_details = []
                            if real_cat_id:
                                # Try both payment and depense since we don't know the type from the key alone here
                                row_details.extend(details_map.get((int(poste_id), real_cat_id, None), []))
                                row_details.extend(details_map.get((int(poste_id), None, real_cat_id), []))
                            else:
                                # Get ALL details for this poste, regardless of category
                                # because 'none' means all categories for this poste in the single-row UI
                                for d_key, d_list in details_map.items():
                                    if d_key[0] == int(poste_id):
                                        row_details.extend(d_list)
                            
                            for detail in row_details:
                                if quarter == 't1': detail.t1_percent = val
                                elif quarter == 't2': detail.t2_percent = val
                                elif quarter == 't3': detail.t3_percent = val
                                elif quarter == 't4': detail.t4_percent = val
                                updated_details.append(detail)
                                
                        except ValueError:
                            continue
            
            # Bulk update if possible, or save individually
            # Django bulk_update is efficient
            if updated_details:
                BudgetLineDetail.objects.bulk_update(updated_details, ['t1_percent', 't2_percent', 't3_percent', 't4_percent'])
                
            messages.success(request, "Les pourcentages trimestriels ont été enregistrés.")
            return redirect('associe_app:budget_campaign_review', campaign_slug=campaign.slug, institut_id=institut.id)

        elif action == 'validate':
            budget_line.statut = 'validated'
            budget_line.commentaire = '' # Clear old comments
            messages.success(request, f"Le budget pour {institut.nom} a été validé.")
        elif action == 'reject':
            budget_line.statut = 'rejected'
            budget_line.commentaire = commentaire
        elif action == 'reset':
             # Reset Logic
            BudgetLineDetail.objects.filter(campaign=campaign, institut=institut).delete()
            budget_line.statut = 'draft' # Or whatever starting status is appropriate
            budget_line.commentaire = ''
            messages.info(request, f"La proposition de budget pour {institut.nom} a été réinitialisée.")
        
        budget_line.save()
        return redirect('associe_app:budget_campaign_instituts', campaign_slug=campaign.slug)

    # Prepare row_quarters for template (Collective for all categories of a poste)
    if is_visible_to_admin:
        for d in details:
            # Key: "poste_id_None" (to match template with row_key=pid|add:"_None")
            row_key = f"{d.poste_id}_None"
            
            # We assume all details for the same poste have the same percentages
            if row_key not in row_quarters:
                row_quarters[row_key] = {
                    't1': d.t1_percent,
                    't2': d.t2_percent,
                    't3': d.t3_percent,
                    't4': d.t4_percent
                }

    # 3. Realization Data for this specific institute
    realization_data = get_campaign_realization_data(campaign, [institut])

    context = {
        'campaign': campaign,
        'institut': institut,
        'budget_line': budget_line,
        'structured_postes': structured_postes,
        'entreprises': entreprises,
        'allocations': allocations,
        'total_dispatched': total_dispatched,
        'row_quarters': row_quarters,
        'is_visible_to_admin': is_visible_to_admin,
        
        # Stats
        'remaining': budget_line.montant - total_dispatched,
        'percent_dispatched': (total_dispatched / budget_line.montant * 100) if budget_line.montant > 0 else 0,

        # Realization Data
        'combined_postes': realization_data['combined_postes'],
        'realization_totals': realization_data['totals']
    }
    return render(request, 'associe_app/budget_campaign_review.html', context)

@login_required(login_url="login")
def extension_requests_list(request):
    from .models import BudgetExtensionRequest
    
    requests = BudgetExtensionRequest.objects.select_related('campaign', 'institut').order_by('-created_at')
    
    context = {
        'requests': requests
    }
    return render(request, 'associe_app/extension_requests_list.html', context)

@login_required(login_url="login")
def review_extension(request, request_id):
    from .models import BudgetExtensionRequest, BudgetExtensionItem, BudgetLine, BudgetLineDetail
    from django.db import transaction
    from institut_app.models import Entreprise # Import purely for type hinting if needed, but actual query is dynamic
    # We need to import Entreprise dynamically from the tenant model or similar if possible, 
    # or just use the model known in the context.
    # Actually Entreprise is defined in `institut_app.models` usually, or `tenant_app`. 
    # Let's check where Entreprise is defined. 
    # In `institut_app/views.py` it was used. Let's assume it's available or we use raw SQL/ORM within context.
    # We imported `Entreprise` in `institut_app/views.py` from where? 
    # Likely `from app.models import Entreprise` if valid, or `from institut_app.models import Entreprise`.
    # Based on checking `institut_app/views.py` imports earlier, it wasn't shown explicitly but used.
    # Let's check `app/models.py` or similar later if it fails. 
    # For now, I will use `from app.models import Entreprise` inside the context manager block if needed, 
    # or rely on `details.entreprise_id`.
    
    # Correction: `Entreprise` is likely in `institut_app` or `app` but specific to tenant.
    # I'll use `from app.models import Entreprise` assuming it's the tenant model.
    from institut_app.models import Entreprise 

    ext_request = get_object_or_404(BudgetExtensionRequest, id=request_id)
    items = ext_request.items.select_related('poste', 'payment_category').order_by('poste__label')
    
    if request.method == "POST":
        action = request.POST.get('action')
        comment = request.POST.get('admin_comment', '')
        
        if action == 'approve':
            try:
                with transaction.atomic():
                    # Update BudgetLineDetails
                    for item in items:
                        BudgetLineDetail.objects.update_or_create(
                            campaign=ext_request.campaign,
                            institut=ext_request.institut,
                            poste=item.poste,
                            payment_category=item.payment_category,
                            entreprise_id=item.entreprise_id,
                            defaults={'montant': item.old_amount + item.requested_amount}
                        )
                    
                    
                    ext_request.status = 'approved'
                    ext_request.admin_comment = comment
                    ext_request.save()
                    
                    messages.success(request, f"La demande de rallonge pour {ext_request.institut} a été approuvée.")
                    return redirect('associe_app:extension_requests_list')
                    
            except Exception as e:
                messages.error(request, f"Erreur lors de l'approbation : {str(e)}")
        
        elif action == 'reject':
            ext_request.status = 'rejected'
            ext_request.admin_comment = comment
            ext_request.save()
            messages.warning(request, f"La demande de rallonge pour {ext_request.institut} a été rejetée.")
            return redirect('associe_app:extension_requests_list')

    # Fetch enterprise names mapping
    entreprise_map = {0: 'Global'}
    try:
        with schema_context(ext_request.institut.schema_name):
            ents = Entreprise.objects.all()
            for e in ents:
                entreprise_map[e.id] = e.designation
    except Exception as e:
        print(f"Error fetching entreprises: {e}")

    context = {
        'ext_request': ext_request,
        'items': items,
        'entreprise_map': entreprise_map,
    }
    return render(request, 'associe_app/review_extension.html', context)



@login_required(login_url='login')
def export_postes_budgetaires(request):
    postes = PostesBudgetaire.objects.all().order_by('order', 'type', 'label')
    wb = Workbook()
    ws = wb.active
    ws.title = "Postes Budgetaires"
    
    headers = [
        'ID', 'Label', 'Type', 'Order', 'Description', 'Parent_ID', 'Parent_Nom',
        'Depense_Categories_IDs', 'Payment_Categories_IDs'
    ]
    ws.append(headers)
    
    for p in postes:
        depense_cats = ",".join([str(c.id) for c in p.depense_categories.all()])
        payment_cats = ",".join([str(c.id) for c in p.payment_categories.all()])
        
        ws.append([
            p.id,
            p.label,
            p.type,
            p.order,
            p.description,
            p.parent.id if p.parent else '',
            p.parent.label if p.parent else '',
            depense_cats,
            payment_cats
        ])
    
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    response = FileResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="postes_budgetaires.xlsx"'
    return response

@login_required(login_url='login')
def import_postes_budgetaires(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        filename = file.name.lower()
        data = []
        
        try:
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                wb = openpyxl.load_workbook(file)
                ws = wb.active
                headers = [cell.value for cell in ws[1]]
                for row in ws.iter_rows(min_row=2, values_only=True):
                    if not any(row): continue
                    data.append(dict(zip(headers, row)))
            elif filename.endswith('.json'):
                data = json.load(file)
            else:
                return JsonResponse({'status': 'error', 'message': 'Format non supporté.'})
            
            # Pass 1: Create or Update items (without parent/categories for now)
            item_map = {}
            for row in data:
                item_id = row.get('ID') or row.get('id')
                label = row.get('Label') or row.get('label')
                p_type = row.get('Type') or row.get('type')
                order = row.get('Order') or row.get('order') or 0
                desc = row.get('Description') or row.get('description') or ''
                
                poste, created = PostesBudgetaire.objects.update_or_create(
                    id=item_id if item_id else None,
                    defaults={
                        'label': label,
                        'type': p_type,
                        'order': int(order),
                        'description': desc
                    }
                )
                item_map[item_id or poste.id] = (poste, row)

            # Pass 2: Link Parents and Categories
            for item_id, (poste, row) in item_map.items():
                parent_id = row.get('Parent_ID') or row.get('parent_id')
                depense_cats_str = str(row.get('Depense_Categories_IDs') or row.get('depense_categories_ids') or '')
                payment_cats_str = str(row.get('Payment_Categories_IDs') or row.get('payment_categories_ids') or '')

                if parent_id:
                    poste.parent = PostesBudgetaire.objects.filter(id=parent_id).first()
                else:
                    poste.parent = None
                
                poste.save()

                if depense_cats_str:
                    ids = [int(i.strip()) for i in depense_cats_str.split(',') if i.strip().isdigit()]
                    poste.depense_categories.set(GlobalDepensesCategory.objects.filter(id__in=ids))
                else:
                    poste.depense_categories.clear()

                if payment_cats_str:
                    ids = [int(i.strip()) for i in payment_cats_str.split(',') if i.strip().isdigit()]
                    poste.payment_categories.set(GlobalPaymentCategory.objects.filter(id__in=ids))
                else:
                    poste.payment_categories.clear()

            return JsonResponse({'status': 'success', 'message': f'{len(data)} postes budgétaires traités avec succès.'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"Erreur lors de l'import : {str(e)}"})
            
    return JsonResponse({'status': 'error', 'message': 'Requête invalide.'})
