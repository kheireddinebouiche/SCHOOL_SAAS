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
    associations = SpecialiteCompte.objects.select_related('specialite', 'compte').all()
    
    data = []
    for assoc in associations:
        data.append({
            'id': assoc.id,
            'specialite': assoc.specialite.id if assoc.specialite else None,
            'specialite__label': assoc.specialite.label if assoc.specialite else "N/A",
            'compte': assoc.compte.id if assoc.compte else None,
            'compte__name': assoc.compte.name if assoc.compte else "N/A",
            'created_at': assoc.created_at.strftime('%Y-%m-%d') if assoc.created_at else None,
        })
    
    return JsonResponse(data, safe=False)


@login_required
def LoadSpecialites(request):
    """
    Charge la liste des spécialités
    """
    specialites = Specialites.objects.all()
    
    data = []
    for specialite in specialites:
        data.append({
            'id': specialite.id,
            'label': specialite.label,
            'code': specialite.code,
        })
    
    return JsonResponse(data, safe=False)


@login_required
def LoadComptes(request):
    """
    Charge la liste des comptes comptables
    """
    comptes = PaymentCategory.objects.all()
    
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
    Crée une nouvelle association spécialité-compte
    """
    if request.method == 'POST':
        specialite_id = request.POST.get('specialite_id')
        compte_id = request.POST.get('compte_id')
        
        try:
            # Vérifier si l'association existe déjà
            existing_assoc = SpecialiteCompte.objects.filter(
                specialite_id=specialite_id,
                compte_id=compte_id
            ).first()
            
            if existing_assoc:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Cette association existe déjà!'
                })
            
            # Créer la nouvelle association
            specialite = Specialites.objects.get(id=specialite_id)
            compte = PaymentCategory.objects.get(id=compte_id)
            
            association = SpecialiteCompte.objects.create(
                specialite=specialite,
                compte=compte
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Association créée avec succès!',
                'id': association.id
            })
            
        except Specialites.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Spécialité non trouvée!'
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
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée!'
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