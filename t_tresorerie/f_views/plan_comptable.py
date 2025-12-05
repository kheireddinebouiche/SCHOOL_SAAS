from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.serializers import serialize
import json


@login_required
def PagePlanComptable(request):
    """
    Affiche la page du plan comptable avec une interface harmonisée
    avec les autres pages de la section de trésorerie
    Le plan comptable suit la structure du Plan Comptable Général Algérien (PCGA)
    avec 8 classes de comptes : 1-Capitaux, 2-Immobilisations, 3-Stocks, 4-Tiers, 5-Financier, 6-Charges, 7-Produits, 8-Comptes spéciaux
    """
    context = {
        'titre_page': 'Plan Comptable',
        'titre_section': 'Comptabilité',
        'sous_titre': 'Gestion du plan comptable'
    }
    return render(request, 'tenant_folder/comptabilite/comptabilite/plan_comptable.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def CreateCompteModal(request):
    """
    Vue pour afficher ou traiter la modal de création d'un compte comptable
    selon le plan comptable général algérien (PCGA)
    """
    if request.method == 'POST':
        # Récupérer les données du formulaire
        numero = request.POST.get('code')  # Using 'code' from form but mapping to 'numero' in model
        intitule = request.POST.get('intitule')
        type_compte = request.POST.get('type_compte')

        # Validation basique
        errors = []
        if not numero:
            errors.append('Le numéro du compte est requis')
        if not intitule:
            errors.append('L\'intitulé du compte est requis')
        if not type_compte:
            errors.append('Le type du compte est requis')
        if not numero.isdigit() and len(numero) > 0:
            errors.append('Le numéro du compte doit être un nombre ou une combinaison de chiffres')

        # Vérifier que le numéro commence par un chiffre entre 1 et 8 (classes du PCGA algérien)
        if numero and len(numero) >= 1:
            premier_chiffre = numero[0]
            if premier_chiffre not in ['1', '2', '3', '4', '5', '6', '7', '8']:
                errors.append('Le numéro du compte doit commencer par un chiffre entre 1 et 8 conformément au Plan Comptable Général Algérien')

        # Vérifier que le type_compte est dans les choix valides
        type_compte_choices = [choice[0] for choice in PlanComptable._meta.get_field('type_compte').choices]
        if type_compte and type_compte not in type_compte_choices:
            errors.append(f'Le type de compte doit être parmi : {", ".join([choice[1] for choice in PlanComptable._meta.get_field("type_compte").choices])}')

        if errors:
            messages.error(request, '; '.join(errors))
            return JsonResponse({'success': False, 'errors': errors})

        try:
            # Vérifier si un compte avec le même numéro existe déjà
            if PlanComptable.objects.filter(numero=numero).exists():
                return JsonResponse({'success': False, 'errors': ['Un compte avec ce numéro existe déjà']})

            # Extraire la classe du numéro (premier chiffre)
            classe = numero[0] if numero else ''

            # Créer le nouveau compte
            compte = PlanComptable.objects.create(
                numero=numero,
                intitule=intitule,
                classe=classe,
                type_compte=type_compte
            )

            messages.success(request, 'Compte créé avec succès')
            return JsonResponse({
                'success': True,
                'message': 'Compte créé avec succès',
                'compte': {
                    'id': compte.id,
                    'numero': compte.numero,
                    'intitule': compte.intitule,
                    'classe': compte.classe,
                    'type_compte': compte.get_type_compte_display()  # Utilise la méthode get_FOO_display pour obtenir le label
                }
            })

        except Exception as e:
            messages.error(request, f'Erreur lors de la création du compte: {str(e)}')
            return JsonResponse({'success': False, 'errors': [str(e)]})

    # Si c'est une requête GET, afficher la modal
    else:
        # Récupérer les comptes existants pour permettre de créer des comptes enfants
        # On va organiser les comptes par classe pour une meilleure hiérarchie
        comptes_parents = PlanComptable.objects.filter(
            type_compte__in=['actif', 'passif', 'charge', 'produit']
        ).order_by('numero')

        # Créer des structures pour aider à la création hiérarchique
        classes_disponibles = []
        for i in range(1, 9):  # Classes 1 à 8 du PCGA
            if PlanComptable.objects.filter(numero__startswith=str(i)).exists():
                classes_disponibles.append(str(i))

        context = {
            'comptes_parents': comptes_parents,
            'classes_disponibles': classes_disponibles,
        }
        return render(request, 'tenant_folder/comptabilite/comptabilite/modal_create_compte.html', context)


@login_required
def PlanComptableAPI(request):
    """
    API endpoint to fetch all PlanComptable data for the table
    Returns JSON data in the format expected by the frontend
    """
    try:
        # Fetch all PlanComptable records
        comptes = PlanComptable.objects.all().order_by('numero')

        # Convert to the format expected by the frontend
        comptes_data = []
        for compte in comptes:
            # Determine the level based on the length of the account number
            niveau = len(compte.numero)

            # Map type_compte to French display values
            type_mapping = {
                'actif': 'Actif',
                'passif': 'Passif',
                'charge': 'Charge',
                'produit': 'Produit',
                'hors_bilan': 'Hors bilan'
            }

            compte_dict = {
                'code': compte.numero,
                'intitule': compte.intitule,
                'type': type_mapping.get(compte.type_compte, compte.type_compte),
                'categorie': compte.get_type_compte_display(),  # Using the choice display value
                'niveau': niveau,
                'classe': compte.classe
            }

            comptes_data.append(compte_dict)

        return JsonResponse({
            'success': True,
            'comptes': comptes_data,
            'count': len(comptes_data)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

