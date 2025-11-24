from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import *
from ..forms import *
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django_tenants.utils import get_tenant_model, schema_context
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
import json



@login_required(login_url="institut_app:login")
def PageAssociation(request):
    return render(request,'tenant_folder/formations/double_diplomation/association.html')


@login_required(login_url="institut_app:login")
def ApiSaveDouble(request):
    if request.method == 'POST':
        try:
            # Récupérer les données envoyées
            specialite1_id = request.POST.get('specialite1_id')
            specialite2_id = request.POST.get('specialite2_id')
            label = request.POST.get('label', '')  # Le label est maintenant fourni par l'utilisateur
            description = request.POST.get('description', '')

            # Validation des données
            if not specialite1_id or not specialite2_id:
                return JsonResponse({
                    'success': False,
                    'message': 'Veuillez sélectionner deux spécialités.'
                }, status=400)

            if not label:
                return JsonResponse({
                    'success': False,
                    'message': 'Le libellé est requis.'
                }, status=400)

            # Vérifier que les spécialités sont différentes
            if specialite1_id == specialite2_id:
                return JsonResponse({
                    'success': False,
                    'message': 'Les deux spécialités doivent être différentes.'
                }, status=400)

            # Récupérer les objets spécialités
            try:
                specialite1 = Specialites.objects.get(id=specialite1_id)
                specialite2 = Specialites.objects.get(id=specialite2_id)
            except Specialites.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Une ou plusieurs spécialités sélectionnées n\'existent pas.'
                }, status=400)

            # Vérifier si une combinaison existe déjà entre ces deux spécialités
            combinaison_existe = DoubleDiplomation.objects.filter(
                Q(specialite1=specialite1, specialite2=specialite2) |
                Q(specialite1=specialite2, specialite2=specialite1)
            ).exists()

            if combinaison_existe:
                return JsonResponse({
                    'success': False,
                    'message': f'Une combinaison existe déjà entre "{specialite1.label}" et "{specialite2.label}".'
                }, status=400)

            # Créer la combinaison dans la base de données
            with transaction.atomic():
                combinaison = DoubleDiplomation.objects.create(
                    specialite1=specialite1,
                    specialite2=specialite2,
                    label=label
                )

            # Retourner une réponse de succès
            return JsonResponse({
                'success': True,
                'message': 'La combinaison a été enregistrée avec succès.',
                'combinaison_id': combinaison.id
            })

        except Exception as e:
            # En cas d'erreur serveur
            print(f"Erreur dans ApiSaveDouble: {str(e)}")  # Pour le débogage
            return JsonResponse({
                'success': False,
                'message': 'Une erreur est survenue lors de l\'enregistrement de la combinaison.'
            }, status=500)

    else:
        # Si la requête n'est pas POST
        return JsonResponse({
            'success': False,
            'message': 'Méthode non autorisée.'
        }, status=405)


@login_required(login_url="institut_app:login")
def ApiLoadDoubleDiplomation(request):
    if request.method == 'GET':
        try:
            # Récupérer toutes les combinaisons de double diplomation avec les informations nécessaires
            combinaisons = DoubleDiplomation.objects.select_related(
                'specialite1__formation',
                'specialite2__formation'
            ).all()

            # Préparer la liste des combinaisons avec les détails nécessaires
            liste_combinaisons = []
            for combinaison in combinaisons:
                combinaison_data = {
                    'id': combinaison.id,
                    'label': combinaison.label,
                    'specialite1_id': combinaison.specialite1.id if combinaison.specialite1 else None,
                    'specialite1_label': combinaison.specialite1.label if combinaison.specialite1 else 'N/A',
                    'specialite1_formation': combinaison.specialite1.formation.nom if combinaison.specialite1 and combinaison.specialite1.formation else 'N/A',
                    'specialite1_formation_id': combinaison.specialite1.formation.id if combinaison.specialite1 and combinaison.specialite1.formation else None,
                    'specialite2_id': combinaison.specialite2.id if combinaison.specialite2 else None,
                    'specialite2_label': combinaison.specialite2.label if combinaison.specialite2 else 'N/A',
                    'specialite2_formation': combinaison.specialite2.formation.nom if combinaison.specialite2 and combinaison.specialite2.formation else 'N/A',
                    'specialite2_formation_id': combinaison.specialite2.formation.id if combinaison.specialite2 and combinaison.specialite2.formation else None,
                    'created_at': combinaison.created_at.strftime('%d %b %Y') if combinaison.created_at else 'N/A',
                    'description': getattr(combinaison, 'description', ''),  # In case description field exists in future
                }
                liste_combinaisons.append(combinaison_data)

            return JsonResponse({
                'success': True,
                'combinaisons': liste_combinaisons
            })

        except Exception as e:
            print(f"Erreur dans ApiLoadDoubleDiplomation: {str(e)}")  # Pour le débogage
            return JsonResponse({
                'success': False,
                'message': 'Une erreur est survenue lors du chargement des combinaisons.'
            }, status=500)

    else:
        return JsonResponse({
            'success': False,
            'message': 'Méthode non autorisée.'
        }, status=405)


@login_required(login_url="institut_app:login")
def ApiUpdateDoubleDiplomation(request):
    if request.method == 'POST':
        try:
            # Récupérer les données envoyées
            combinaison_id = request.POST.get('combinaison_id')
            specialite1_id = request.POST.get('specialite1_id')
            specialite2_id = request.POST.get('specialite2_id')
            label = request.POST.get('label', '')
            description = request.POST.get('description', '')

            # Validation des données
            if not combinaison_id or not specialite1_id or not specialite2_id or not label:
                return JsonResponse({
                    'success': False,
                    'message': 'Tous les champs requis doivent être remplis.'
                }, status=400)

            # Vérifier que les spécialités sont différentes
            if specialite1_id == specialite2_id:
                return JsonResponse({
                    'success': False,
                    'message': 'Les deux spécialités doivent être différentes.'
                }, status=400)

            # Récupérer les objets spécialités
            try:
                specialite1 = Specialites.objects.get(id=specialite1_id)
                specialite2 = Specialites.objects.get(id=specialite2_id)
                combinaison = DoubleDiplomation.objects.get(id=combinaison_id)
            except Specialites.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Une ou plusieurs spécialités sélectionnées n\'existent pas.'
                }, status=400)
            except DoubleDiplomation.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'La combinaison spécifiée n\'existe pas.'
                }, status=400)

            # Vérifier si une combinaison existe déjà entre ces deux spécialités (autre que celle en cours de modification)
            combinaison_existe = DoubleDiplomation.objects.filter(
                Q(specialite1=specialite1, specialite2=specialite2) |
                Q(specialite1=specialite2, specialite2=specialite1)
            ).exclude(id=combinaison_id).exists()

            if combinaison_existe:
                return JsonResponse({
                    'success': False,
                    'message': f'Une combinaison existe déjà entre "{specialite1.label}" et "{specialite2.label}".'
                }, status=400)

            # Mettre à jour la combinaison dans la base de données
            with transaction.atomic():
                combinaison.specialite1 = specialite1
                combinaison.specialite2 = specialite2
                combinaison.label = label
                # Note: We don't update description in the model since it's not in the model yet
                combinaison.save()

            # Retourner une réponse de succès
            return JsonResponse({
                'success': True,
                'message': 'La combinaison a été mise à jour avec succès.',
                'combinaison_id': combinaison.id
            })

        except Exception as e:
            # En cas d'erreur serveur
            print(f"Erreur dans ApiUpdateDoubleDiplomation: {str(e)}")  # Pour le débogage
            return JsonResponse({
                'success': False,
                'message': 'Une erreur est survenue lors de la mise à jour de la combinaison.'
            }, status=500)

    else:
        # Si la requête n'est pas POST
        return JsonResponse({
            'success': False,
            'message': 'Méthode non autorisée.'
        }, status=405)


@login_required(login_url="institut_app:login")
def ApiDeleteDoubleDiplomation(request):
    if request.method == 'POST':
        try:
            # Récupérer l'ID de la combinaison à supprimer
            combinaison_id = request.POST.get('combinaison_id')

            # Validation des données
            if not combinaison_id:
                return JsonResponse({
                    'success': False,
                    'message': 'L\'ID de la combinaison est requis.'
                }, status=400)

            try:
                # Récupérer la combinaison
                combinaison = DoubleDiplomation.objects.get(id=combinaison_id)
            except DoubleDiplomation.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'La combinaison spécifiée n\'existe pas.'
                }, status=400)

            # Supprimer la combinaison
            combinaison.delete()

            # Retourner une réponse de succès
            return JsonResponse({
                'success': True,
                'message': 'La combinaison a été supprimée avec succès.'
            })

        except Exception as e:
            # En cas d'erreur serveur
            print(f"Erreur dans ApiDeleteDoubleDiplomation: {str(e)}")  # Pour le débogage
            return JsonResponse({
                'success': False,
                'message': 'Une erreur est survenue lors de la suppression de la combinaison.'
            }, status=500)

    else:
        return JsonResponse({
            'success': False,
            'message': 'Méthode non autorisée.'
        }, status=405)
    

@login_required(login_url="institut_app:login")
def ApiLoadSelestDoubleDiplomation(request):
    if request.method == "GET":
        liste = DoubleDiplomation.objects.all().values('id','label')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status":"error"})