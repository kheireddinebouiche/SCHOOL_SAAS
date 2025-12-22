from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json



@login_required(login_url="institut_app:login")
def PageProduits(request):
    return render(request, 'tenant_folder/comptabilite/produits/liste_categories_produits.html')

@login_required(login_url="institut_app:login")
def ApiListeCategoriesProduits(request):
    """API endpoint to list all payment categories in hierarchical structure"""
    # Get all categories with parent relationship
    all_categories = PaymentCategory.objects.all().prefetch_related('children')

    # Build a hierarchical structure
    category_tree = []

    # Create a mapping of all categories by ID
    category_map = {}
    for cat in all_categories:
        category_map[cat.id] = {
            'id': cat.id,
            'name': cat.name,
            'parent_id': cat.parent.id if cat.parent else None,
            'children_count': cat.children.count(),
            'is_active': True,
            'is_parent': cat.parent is None,
            'created_at': cat.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(cat, 'created_at') else '-',
            'children': []
        }

    # Group children under their parents
    for cat_id, cat_data in category_map.items():
        if cat_data['parent_id'] and cat_data['parent_id'] in category_map:
            # This is a child category, add it to its parent
            category_map[cat_data['parent_id']]['children'].append(cat_data)
        elif cat_data['parent_id'] is None:
            # This is a parent category with no parent, add it to the root
            category_tree.append(cat_data)

    # Sort the root categories and their children by name
    category_tree.sort(key=lambda x: x['name'])
    for cat in category_tree:
        cat['children'].sort(key=lambda x: x['name'])

    return JsonResponse({'data': category_tree}, safe=False)

@login_required(login_url="institut_app:login")
def ApiCreerCategorieProduit(request):
    """API endpoint to create a new payment category"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            parent_id = data.get('parent_id')

            if not name:
                return JsonResponse({'error': 'Le nom de la catégorie est requis'}, status=400)

            parent = None
            if parent_id:
                parent = PaymentCategory.objects.get(id=parent_id)

            category = PaymentCategory.objects.create(
                name=name,
                parent=parent
            )

            return JsonResponse({
                'success': True,
                'message': 'Catégorie créée avec succès',
                'id': category.id,
                'name': category.name
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required(login_url="institut_app:login")
def ApiModifierCategorieProduit(request):
    """API endpoint to update a payment category"""
    if request.method == 'POST':  # Changed to POST for consistency
        try:
            data = json.loads(request.body)
            category_id = data.get('id')
            name = data.get('name')
            parent_id = data.get('parent_id')

            if not category_id or not name:
                return JsonResponse({'error': 'ID et nom de la catégorie sont requis'}, status=400)

            category = PaymentCategory.objects.get(id=category_id)

            parent = None
            if parent_id:
                parent = PaymentCategory.objects.get(id=parent_id)

            category.name = name
            category.parent = parent
            category.save()

            return JsonResponse({
                'success': True,
                'message': 'Catégorie modifiée avec succès'
            })
        except PaymentCategory.DoesNotExist:
            return JsonResponse({'error': 'Catégorie non trouvée'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required(login_url="institut_app:login")
def ApiSupprimerCategorieProduit(request):
    """API endpoint to delete a payment category"""
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            category_id = data.get('id')

            if not category_id:
                return JsonResponse({'error': 'ID de la catégorie est requis'}, status=400)

            category = PaymentCategory.objects.get(id=category_id)
            category.delete()

            return JsonResponse({
                'success': True,
                'message': 'Catégorie supprimée avec succès'
            })
        except PaymentCategory.DoesNotExist:
            return JsonResponse({'error': 'Catégorie non trouvée'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required(login_url="institut_app:login")
def ApiGetCategorieProduit(request, pk):
    """API endpoint to get details of a specific payment category"""
    try:
        category = PaymentCategory.objects.get(id=pk)

        return JsonResponse({
            'id': category.id,
            'name': category.name,
            'parent_id': category.parent.id if category.parent else None,
            'parent_name': category.parent.name if category.parent else None
        })
    except PaymentCategory.DoesNotExist:
        return JsonResponse({'error': 'Catégorie non trouvée'}, status=404)

@login_required(login_url="institut_app:login")
def PageCategoriesProduits(request):
    """Page to manage payment categories"""
    return render(request, 'tenant_folder/comptabilite/produits/liste_categories_produits.html')