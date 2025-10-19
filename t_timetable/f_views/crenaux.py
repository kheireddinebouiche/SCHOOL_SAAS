from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..forms import *
from ..models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from t_groupe.models import *

@login_required(login_url="institut_app:login")
def ListeModel(request):
    liste = ModelCrenau.objects.all()
    context = {
        "modeles" : liste
    }
    return render(request, 'tenant_folder/timetable/crenaux/liste_model_crenau.html',context)

@login_required(login_url="institut_app:login")
def create_model(request):
    if request.method == 'POST':
        label = request.POST.get('label')
        # Since we're now sending multiple days as a JSON array, we need to handle that
        import json
        jours = request.POST.get('jours')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        
        try:
            # Validate required fields
            if not label or not jours or not heure_debut or not heure_fin:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Tous les champs sont obligatoires'
                })
            
            # Parse the jours JSON
            try:
                jours_list = json.loads(jours)
            except json.JSONDecodeError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Format de jours invalide'
                })
            
            if not jours_list:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Veuillez sélectionner au moins un jour'
                })
            
            # Validate that end time is after start time
            from datetime import time
            debut_h, debut_m = map(int, heure_debut.split(':'))
            fin_h, fin_m = map(int, heure_fin.split(':'))
            
            time_debut = time(debut_h, debut_m)
            time_fin = time(fin_h, fin_m)
            
            if time_fin <= time_debut:
                return JsonResponse({
                    'status': 'error',
                    'message': 'L\'heure de fin doit être postérieure à l\'heure de début'
                })
            
            # Create the ModelCrenau instance
            crenau = ModelCrenau.objects.create(
                label=label
            )
            
            # For now, we'll store the first day in the jour_data, but we could store all days
            # If needed, we could change the jour_data field to store multiple days
            jour_data = {
                "id": None,
                "nom": jours_list[0],  # Store first day for backward compatibility
                "jours": jours_list,   # Store all selected days
                "date_creation": None
            }
            crenau.jour_data = jour_data
            
            # Create the horaire_data dictionary
            horaire_data = {
                "id": None,
                "nom": f"{heure_debut}-{heure_fin}",
                "heure_debut": heure_debut,
                "heure_fin": heure_fin,
                "est_actif": True
            }
            crenau.horaire_data = horaire_data
            
            crenau.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Modèle de créneau créé avec succès!',
                'id': crenau.id
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erreur lors de la création du modèle de créneau: {str(e)}'
            })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Méthode non autorisée'
        })

@login_required(login_url="institut_app:login")
def get_horaires(request):
    # This view could return available time slots if there's a Horaire model
    # For now, returning an empty response since horaires are user-defined
    return JsonResponse({
        'status': 'success',
        'horaires': []
    })
