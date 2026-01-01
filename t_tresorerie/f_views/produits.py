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

@login_required(login_url="institut_app:login")
def PageAutrePaiements(request):
    """Page to manage other payments"""
    return render(request, 'tenant_folder/comptabilite/paiements/liste_autre_paiements.html')

@login_required(login_url="institut_app:login")
def PageNouveauAutrePaiement(request):
    """Page to create a new other payment"""
    return render(request, 'tenant_folder/comptabilite/paiements/nouveau_autre_paiement.html')

@login_required(login_url="institut_app:login")
def ApiStoreAutrePaiement(request):
    """API endpoint to create a new other payment"""

    data = json.loads(request.body)
    label = data.get('label')
    montant_paiement = data.get('montant_paiement')
    mode_paiement = data.get('mode_paiement')
    date_operation = data.get('date_operation')
    reference = data.get('reference')
    date_paiement = data.get('date_paiement')
    compte_id = data.get('compte')

    if not label or not montant_paiement or not mode_paiement or not date_operation or not date_paiement:
        return JsonResponse({'error': 'Tous les champs obligatoires doivent être remplis'}, status=400)

    # Get the PaymentCategory if provided
    compte = None
    if compte_id:
        compte = PaymentCategory.objects.get(id=compte_id)

    # Create the AutreProduit instance
    autre_paiement = AutreProduit.objects.create(
        label=label,
        montant_paiement=montant_paiement,
        mode_paiement=mode_paiement,
        date_operation=date_operation,
        reference=reference,
        date_paiement=date_paiement,
        compte=compte
    )

    return JsonResponse({
        'success': True,
        'message': 'Paiement enregistré avec succès',
        'id': autre_paiement.id
    })
      


@login_required(login_url="institut_app:login")
def ApiListeAutrePaiements(request):
    """API endpoint to list all other payments"""
    
    autre_paiements = AutreProduit.objects.all().values('id')

    print(autre_paiements)

    return JsonResponse(list(autre_paiements), safe=False)
    

@login_required(login_url="institut_app:login")
def ApiGetAutrePaiement(request, pk):
    """API endpoint to get details of a specific other payment"""
    try:
        paiement = AutreProduit.objects.get(id=pk)

        return JsonResponse({
            'id': paiement.id,
            'label': paiement.label,
            'montant_paiement': float(paiement.montant_paiement) if paiement.montant_paiement else 0,
            'mode_paiement': paiement.mode_paiement,
            'date_operation': paiement.date_operation.strftime('%Y-%m-%d') if paiement.date_operation else '-',
            'reference': paiement.reference or '-',
            'date_paiement': paiement.date_paiement.strftime('%Y-%m-%d') if paiement.date_paiement else '-',
            'compte_id': paiement.compte.id if paiement.compte else None
        })
    except AutreProduit.DoesNotExist:
        return JsonResponse({'error': 'Paiement non trouvé'}, status=404)

@login_required(login_url="institut_app:login")
def ApiUpdateAutrePaiement(request):
    """API endpoint to update an other payment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            paiement_id = data.get('id')
            label = data.get('label')
            montant_paiement = data.get('montant_paiement')
            mode_paiement = data.get('mode_paiement')
            date_operation = data.get('date_operation')
            reference = data.get('reference')
            date_paiement = data.get('date_paiement')
            compte_id = data.get('compte')

            if not paiement_id or not label or not montant_paiement or not mode_paiement or not date_operation or not date_paiement:
                return JsonResponse({'error': 'Tous les champs obligatoires doivent être remplis'}, status=400)

            paiement = AutreProduit.objects.get(id=paiement_id)

            # Get the PaymentCategory if provided
            compte = None
            if compte_id:
                compte = PaymentCategory.objects.get(id=compte_id)

            # Update the AutreProduit instance
            paiement.label = label
            paiement.montant_paiement = montant_paiement
            paiement.mode_paiement = mode_paiement
            paiement.date_operation = date_operation
            paiement.reference = reference
            paiement.date_paiement = date_paiement
            paiement.compte = compte
            paiement.save()

            return JsonResponse({
                'success': True,
                'message': 'Paiement mis à jour avec succès'
            })
        except AutreProduit.DoesNotExist:
            return JsonResponse({'error': 'Paiement non trouvé'}, status=404)
        except PaymentCategory.DoesNotExist:
            return JsonResponse({'error': 'Catégorie de paiement non trouvée'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required(login_url="institut_app:login")
def ApiDeleteAutrePaiement(request):
    """API endpoint to delete an other payment"""
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            paiement_id = data.get('id')

            if not paiement_id:
                return JsonResponse({'error': 'ID du paiement est requis'}, status=400)

            paiement = AutreProduit.objects.get(id=paiement_id)
            paiement.delete()

            return JsonResponse({
                'success': True,
                'message': 'Paiement supprimé avec succès'
            })
        except AutreProduit.DoesNotExist:
            return JsonResponse({'error': 'Paiement non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required(login_url="institut_app:login")
def api_liste_clients(request):
    if request.method == "GET":
        pass
    else:
        return JsonResponse({"status" : "error"})
    

@login_required(login_url="institu_app:login")
def CreateClientFromTresorerie(request):
    if request.method == "POST":
        nom  = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        nin = request.POST.get('nin')
        telephone = request.POST.get('telephone')


        if not nom or not prenom or not nin or not telephone:
            return JsonResponse({"status" : "error"})
        
        Prospets.objects.create(
            
        )

    else:
        return JsonResponse({"status" : "error"})