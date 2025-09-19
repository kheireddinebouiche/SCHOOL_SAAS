from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


@login_required(login_url="institut_app:login")
def ListeEcheancierSpecial(request):
    # Fetch all special echeanciers with related prospect data
    echeanciers = EcheancierSpecial.objects.select_related('prospect').all().order_by('-created_at')
    
    # Prepare data for the template
    echeanciers_data = []
    for echeancier in echeanciers:
        echeanciers_data.append({
            'id': echeancier.id,
            'nombre_tranche': echeancier.nombre_tranche,
            'prospect': {
                'id': echeancier.prospect.id,
                'nom': echeancier.prospect.nom,
                'prenom': echeancier.prospect.prenom,
            },
            'is_validate': echeancier.is_validate,
            'is_approuved': echeancier.is_approuved,
            'created_at': echeancier.created_at.strftime('%Y-%m-%d %H:%M:%S') if echeancier.created_at else None,
            'updated_at': echeancier.updated_at.strftime('%Y-%m-%d %H:%M:%S') if echeancier.updated_at else None,
        })
    
    return render(request, 'tenant_folder/comptabilite/tresorerie/liste_echeancier_special.html', {
        'echeanciers': echeanciers_data
    })

@login_required(login_url="institut_app:login")
def ApiListEcheancierSpecial(request):
    try:
        # Fetch all special echeanciers with related prospect data
        echeanciers = EcheancierSpecial.objects.select_related('prospect').all().order_by('-created_at')
        
        # Calculate statistics
        total_count = echeanciers.count()
        approved_count = echeanciers.filter(is_approuved=True).count()
        pending_count = echeanciers.filter(is_approuved=False).count()
        validated_count = echeanciers.filter(is_validate=True).count()
        
        # Prepare data for JSON response
        echeanciers_data = []
        for echeancier in echeanciers:
            # Get related echeancier lines
            lines = EcheancierPaiementSpecialLine.objects.filter(echeancier=echeancier)
            lines_data = []
            for line in lines:
                lines_data.append({
                    'id': line.id,
                    'taux': line.taux,
                    'value': line.value,
                    'montant_tranche': str(line.montant_tranche),
                    'date_echeancier': line.date_echeancier.strftime('%Y-%m-%d') if line.date_echeancier else None,
                    'created_at': line.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': line.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                })
            
            echeanciers_data.append({
                'id': echeancier.id,
                'nombre_tranche': echeancier.nombre_tranche,
                'prospect': {
                    'id': echeancier.prospect.id,
                    'nom': echeancier.prospect.nom,
                    'prenom': echeancier.prospect.prenom,
                },
                'is_validate': echeancier.is_validate,
                'is_approuved': echeancier.is_approuved,
                'created_at': echeancier.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': echeancier.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'lines': lines_data
            })
        
        return JsonResponse({
            'status': 'success',
            'echeanciers': echeanciers_data,
            'statistics': {
                'total': total_count,
                'approved': approved_count,
                'pending': pending_count,
                'validated': validated_count
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erreur lors de la récupération des échéanciers: {str(e)}'
        })

@login_required(login_url="institut_app:login")
def ApiValidateEcheancierSpecial(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            echeancier_id = data.get('echeancier_id')
            
            if not echeancier_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'ID de l\'échéancier manquant'
                })
            
            # Update the echeancier to set is_validate to True
            echeancier = EcheancierSpecial.objects.get(id=echeancier_id)
            echeancier.is_validate = True
            echeancier.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Échéancier validé avec succès'
            })
        except EcheancierSpecial.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Échéancier non trouvé'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erreur lors de la validation: {str(e)}'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée'
    })

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiApproveEcheancierSpecial(request):
    if request.method == "GET":
        echeancierId = request.GET.get('echeancierId')
        obj = EcheancierSpecial.objects.get(id = echeancierId)
        obj.is_approuved = True
        obj.save()

        return JsonResponse({"status" : "success"})
    else:

        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
def ApiRejectEcheancierSpecial(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            echeancier_id = data.get('echeancier_id')
            
            if not echeancier_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'ID de l\'échéancier manquant'
                })
            
            echeancier = EcheancierSpecial.objects.get(id=echeancier_id)
            echeancier.is_approuved = False
            echeancier.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Échéancier rejeté avec succès'
            })
        except EcheancierSpecial.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Échéancier non trouvé'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erreur lors du rejet: {str(e)}'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée'
    })

@login_required(login_url="institut_app:login")
@csrf_exempt
@transaction.atomic
def ApiStoreEcheancierSpecial(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract data from request
            prospect_id = data.get('prospect_id')
            nombre_tranches = data.get('nombre_tranches')
            echeancier_lines = data.get('echeancier_lines')
            
            # Validate required fields
            if not prospect_id or not nombre_tranches or not echeancier_lines:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Données incomplètes'
                })
            
            # Create EcheancierSpecial
            echeancier_special = EcheancierSpecial.objects.create(
                prospect_id=prospect_id,
                nombre_tranche=nombre_tranches,
                is_validate=False,
                is_approuved=False
            )
            
            # Create EcheancierPaiementSpecialLine for each line
            for line in echeancier_lines:
                # Convert montant_tranche to Decimal safely
                montant_tranche = line.get('montant_tranche', 0)
                if isinstance(montant_tranche, str):
                    montant_tranche = montant_tranche.replace(',', '.')  # Handle comma as decimal separator
                    montant_tranche = Decimal(montant_tranche)
                elif isinstance(montant_tranche, (int, float)):
                    montant_tranche = Decimal(str(montant_tranche))
                else:
                    montant_tranche = Decimal('0')
                
                EcheancierPaiementSpecialLine.objects.create(
                    echeancier=echeancier_special,
                    taux=line.get('taux', ''),
                    value=line.get('value', ''),
                    montant_tranche=montant_tranche,
                    date_echeancier=line.get('date_echeancier')
                )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Échéancier spécial enregistré avec succès',
                'echeancier_id': echeancier_special.id
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erreur lors de l\'enregistrement: {str(e)}'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée'
    })