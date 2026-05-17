from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from t_tresorerie.models import SpecialiteCompte, PaymentCategory
from t_formations.models import Specialites


@login_required(login_url="institut_app:login")
def PageImputationComptable(request):
    return render(request, 'tenant_folder/comptabilite/comptabilite/imputation_comptable.html')

@login_required
def LoadSpecialiteComptes(request):
    """
    Charge la liste des associations spécialité-compte
    """
    associations = SpecialiteCompte.objects.select_related('specialite__formation', 'compte').all()
    
    data = []
    for assoc in associations:
        data.append({
            'id': assoc.id,
            'specialite': assoc.specialite.id if assoc.specialite else None,
            'specialite__label': assoc.specialite.label if assoc.specialite else "N/A",
            'specialite__formation__nom': assoc.specialite.formation.nom if (assoc.specialite and assoc.specialite.formation) else "Sans formation",
            'compte': assoc.compte.id if assoc.compte else None,
            'compte__name': assoc.compte.name if assoc.compte else "N/A",
            'created_at': assoc.created_at.strftime('%Y-%m-%d') if assoc.created_at else None,
        })
    
    return JsonResponse(data, safe=False)


@login_required
def LoadSpecialites(request):
    """
    Charge la liste des spécialités avec leur statut d'assignation
    """
    specialites = Specialites.objects.select_related('formation').all()
    assigned_specialite_ids = SpecialiteCompte.objects.values_list('specialite_id', flat=True)
    
    data = []
    for specialite in specialites:
        data.append({
            'id': specialite.id,
            'label': specialite.label,
            'code': specialite.code,
            'is_assigned': specialite.id in assigned_specialite_ids,
            'formation_id': specialite.formation.id if specialite.formation else None,
            'formation_nom': specialite.formation.nom if specialite.formation else "Sans formation",
        })
    
    return JsonResponse(data, safe=False)


@login_required
def LoadComptes(request):
    """
    Charge la liste des comptes comptables (PaymentCategory)
    """
    # On ne prend que les catégories qui n'ont pas d'enfants (les feuilles de l'arbre)
    # ou on prend tout selon le besoin. Ici, on prend tout mais on pourrait filtrer.
    comptes = PaymentCategory.objects.all().order_by('name')
    
    data = []
    for compte in comptes:
        data.append({
            'id': compte.id,
            'name': compte.name,
        })
    
    return JsonResponse(data, safe=False)


@login_required
@csrf_exempt
def CreateSpecialiteCompte(request):
    """
    Crée une ou plusieurs nouvelles associations spécialité-compte
    """
    if request.method == 'POST':
        specialite_ids = request.POST.getlist('specialite_ids[]')
        compte_id = request.POST.get('compte_id')
        
        if not specialite_ids:
            # Fallback for single ID if needed
            specialite_id = request.POST.get('specialite_id')
            if specialite_id:
                specialite_ids = [specialite_id]

        if not specialite_ids or not compte_id:
            return JsonResponse({
                'status': 'error',
                'message': 'Données manquantes!'
            })
            
        try:
            compte = PaymentCategory.objects.get(id=compte_id)
            created_count = 0
            skipped_count = 0
            
            for spec_id in specialite_ids:
                # Vérifier si l'association existe déjà
                existing_assoc = SpecialiteCompte.objects.filter(
                    specialite_id=spec_id,
                    compte_id=compte_id
                ).exists()
                
                if not existing_assoc:
                    specialite = Specialites.objects.get(id=spec_id)
                    SpecialiteCompte.objects.create(
                        specialite=specialite,
                        compte=compte
                    )
                    created_count += 1
                else:
                    skipped_count += 1
            
            msg = f"{created_count} association(s) créée(s) avec succès!"
            if skipped_count > 0:
                msg += f" ({skipped_count} déjà existante(s))"
                
            return JsonResponse({
                'status': 'success',
                'message': msg
            })
            
        except PaymentCategory.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Compte non trouvé!'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erreur lors de la création: {str(e)}'
            })


@login_required
@csrf_exempt
def UpdateSpecialiteCompte(request):
    """
    Met à jour une association spécialité-compte existante
    """
    if request.method == 'POST':
        association_id = request.POST.get('id')
        specialite_id = request.POST.get('specialite_id')
        compte_id = request.POST.get('compte_id')
        
        try:
            association = SpecialiteCompte.objects.get(id=association_id)
            
            # Vérifier si la nouvelle association existe déjà (autre que celle en cours de modification)
            existing_assoc = SpecialiteCompte.objects.filter(
                specialite_id=specialite_id,
                compte_id=compte_id
            ).exclude(id=association_id).first()
            
            if existing_assoc:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Cette association existe déjà!'
                })
            
            association.specialite_id = specialite_id
            association.compte_id = compte_id
            association.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Association mise à jour avec succès!'
            })
            
        except SpecialiteCompte.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Association non trouvée!'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erreur lors de la mise à jour: {str(e)}'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée!'
    })


@login_required
@csrf_exempt
def DeleteSpecialiteCompte(request):
    """
    Supprime une association spécialité-compte
    """
    if request.method == 'POST':
        association_id = request.POST.get('id')
        
        try:
            association = SpecialiteCompte.objects.get(id=association_id)
            association.delete()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Association supprimée avec succès!'
            })
            
        except SpecialiteCompte.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Association non trouvée!'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erreur lors de la suppression: {str(e)}'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée!'
    })