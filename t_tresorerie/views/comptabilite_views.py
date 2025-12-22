from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction
from ..models import TypePaiement
import json


@login_required
def liste_categories_produits(request):
    """
    Vue pour afficher la liste des catégories de paiement (TypePaiement)
    """
    categories = TypePaiement.objects.all().order_by('-created_at')
    context = {
        'categories': categories
    }
    return render(request, 'tenant_folder/comptabilite/produits/liste_categories_produits.html', context)


def create_type_paiement(request):
    """
    Vue pour créer une nouvelle catégorie de paiement (TypePaiement)
    """
    if request.method == 'POST':
        try:
            label = request.POST.get('label')
            description = request.POST.get('description', '')
            is_active = request.POST.get('is_active', '0') == '1'
            
            # Validation des données
            if not label:
                return JsonResponse({'success': False, 'error': 'Le libellé est requis'})
            
            # Création de la nouvelle catégorie
            category = TypePaiement.objects.create(
                label=label,
                description=description,
                is_active=is_active
            )
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


def update_type_paiement(request):
    """
    Vue pour mettre à jour une catégorie de paiement existante (TypePaiement)
    """
    if request.method == 'POST':
        try:
            category_id = request.POST.get('category_id')
            label = request.POST.get('label')
            description = request.POST.get('description', '')
            is_active = request.POST.get('is_active', '0') == '1'
            
            # Validation des données
            if not category_id or not label:
                return JsonResponse({'success': False, 'error': 'Données incomplètes'})
            
            # Mise à jour de la catégorie
            category = get_object_or_404(TypePaiement, id=category_id)
            category.label = label
            category.description = description
            category.is_active = is_active
            category.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


def get_type_paiement(request):
    """
    Vue pour récupérer les détails d'une catégorie de paiement (TypePaiement)
    """
    try:
        category_id = request.GET.get('id')
        category = get_object_or_404(TypePaiement, id=category_id)
        
        data = {
            'id': category.id,
            'label': category.label,
            'description': category.description,
            'is_active': category.is_active,
            'created_at': category.created_at.strftime('%d/%m/%Y %H:%M'),
            'updated_at': category.updated_at.strftime('%d/%m/%Y %H:%M')
        }
        
        return JsonResponse({'success': True, 'category': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def delete_type_paiement(request):
    """
    Vue pour supprimer une catégorie de paiement (TypePaiement)
    """
    if request.method == 'POST':
        try:
            category_id = request.POST.get('id')
            category = get_object_or_404(TypePaiement, id=category_id)
            category.delete()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})