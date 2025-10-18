from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import *
from .models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from t_groupe.models import *

@login_required(login_url="institut_app:login")
def ListeDesEmploie(request):
    groupes = Groupe.objects.all()
    emploies = Timetable.objects.all()
    context = {
        'groupes' : groupes,
        'timetables' : emploies,
    }
    return render(request, 'tenant_folder/timetable/liste_des_emploies.html', context)

@login_required(login_url="institut_app:login")
def CreateTimeTable(request):
    if request.method == 'POST':
        # Get the form data from the modal
        label = request.POST.get('label')
        groupe_id = request.POST.get('groupe')
        semestre = request.POST.get('semestre')
        description = request.POST.get('description', '')
        
        # Validate required fields
        if not label or not groupe_id or not semestre:
            return JsonResponse({'status': 'error','message': 'Veuillez remplir tous les champs obligatoires.'})
        
        try:
            # Get the Groupe instance
            groupe = Groupe.objects.get(id=groupe_id)
            
            # Create the Timetable instance
            timetable = Timetable.objects.create(
                label=label,
                groupe=groupe,
                semestre=semestre,
                description=description,
                cree_par=request.user
            )
            
            # Success response - the frontend will redirect after receiving this
            return JsonResponse({
                'status': 'success',
                'message': 'Emploi du temps créé avec succès.',
                'timetable_id': timetable.id
            })
            
        except Groupe.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Le groupe sélectionné n\'existe pas.'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Une erreur est survenue lors de la création de l\'emploi du temps: {str(e)}'
            })
    
    # For GET requests, redirect to the list page
    return redirect('t_timetable:ListeDesEmploie')


@login_required(login_url="institut_app:login")
def timetable_view(request, pk):
    pass

@login_required(login_url="institut_app:login")
def timetable_edit(request, pk):
    pass


@login_required(login_url="institut_app:login")
def timetable_configure(request, pk):
    object = Timetable.objects.get(id = pk)
    jours = Jour.objects.filter(timetable = object)
    horaires = Horaire.objects.filter(timetable = object)
    context = {
        'timetable' : object,
        'jours' : jours,
        'horaires': horaires,
    }
    if object.is_configured:
        return render(request,'tenant_folder/timetable/configure_timetable_cours.html', context)
    else:
        return render(request, 'tenant_folder/timetable/configuration_emploie.html', context)

@login_required(login_url="institut_app:login")
def save_session(request):
    pass

@login_required(login_url="institut_app:login")
def ApiMakeTimetableDone(request):
    id_emploie = request.GET.get('id_emploie')
    obj = Timetable.objects.get(id = id_emploie)
    obj.is_configured = True
    obj.save()
    return JsonResponse({"status": "success"})

@login_required(login_url="institut_app:login")
def save_day(request):
    if request.method == 'POST':
        # Get selected days from the POST request
        selected_days = request.POST.getlist('selected_days')
        timetable_id = request.POST.get('timetable_id')
        
        if not selected_days:
            return JsonResponse({'status': 'error', 'message': 'Veuillez sélectionner au moins un jour.'})
        
        try:
            created_count = 0
            
            # If timetable_id is provided, associate days with the specific timetable
            timetable = None
            if timetable_id:
                try:
                    timetable = Timetable.objects.get(id=timetable_id)
                except Timetable.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'L\'emploi du temps spécifié n\'existe pas.'})
            
            # Create Day objects for each selected day
            for day_name in selected_days:
                # Create the Day instance, associating it with the timetable if provided
                Jour.objects.get_or_create(
                    nom=day_name,
                    timetable=timetable  # Associate with the specific timetable if provided
                )
                created_count += 1
            
            return JsonResponse({
                'status': 'success',
                'message': f'{created_count} jour(s) ajouté(s) avec succès.'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Une erreur est survenue lors de l\'ajout des jours: {str(e)}'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée.'
    })

@login_required(login_url="institut_app:login")
def update_day(request):
    pass

@login_required(login_url="institut_app:login")
def delete_day(request):
    if request.method == "POST":
        pk = request.POST.get('id')
        jours = Jour.objects.get(id = pk)
        jours.delete()
        return JsonResponse({'status' : "success","message" : "Le jours à été supprimer avec succès"})
    else:
        return JsonResponse({'status' : "error","message" : "Methode non autoriser"})


@login_required(login_url="institut_app:login")
def save_horaire(request):
    if request.method == 'POST':
        # Get data from the POST request
        nom = request.POST.get('nom')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        est_actif = request.POST.get('est_actif', 'true').lower() == 'true'
        timetable_id = request.POST.get('timetable_id')
        
        if not all([nom, heure_debut, heure_fin]):
            return JsonResponse({
                'status': 'error',
                'message': 'Veuillez remplir tous les champs obligatoires (nom, heure de début, heure de fin).'
            })
        
        try:
            # Convert time strings to time objects
            from datetime import time
            import datetime
            # Parse the time values - assuming they come in HH:MM format
            debut_parts = heure_debut.split(':')
            fin_parts = heure_fin.split(':')
            
            heure_debut_obj = time(int(debut_parts[0]), int(debut_parts[1]))
            heure_fin_obj = time(int(fin_parts[0]), int(fin_parts[1]))
            
            # Check that end time is after start time
            if heure_fin_obj <= heure_debut_obj:
                return JsonResponse({
                    'status': 'error',
                    'message': 'L\'heure de fin doit être après l\'heure de début.'
                })
            
            # If timetable_id is provided, associate with specific timetable
            timetable = None
            if timetable_id:
                try:
                    timetable = Timetable.objects.get(id=timetable_id)
                except Timetable.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'L\'emploi du temps spécifié n\'existe pas.'
                    })
            
            # Create the Horaire instance
            horaire = Horaire.objects.create(
                nom=nom,
                heure_debut=heure_debut_obj,
                heure_fin=heure_fin_obj,
                est_actif=est_actif,
                timetable=timetable
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Horaire ajouté avec succès.',
                'horaire_id': horaire.id
            })
            
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': 'Format d\'heure invalide. Utilisez HH:MM.'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Une erreur est survenue lors de l\'ajout de l\'horaire: {str(e)}'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée.'
    })

@login_required(login_url="institut_app:login")
def update_horaire(request):
    pass

@login_required(login_url="institut_app:login")
def delete_horaire(request):
    if request.method == "POST":
        pk = request.POST.get('id')
        try:
            horaire = Horaire.objects.get(id=pk)
            horaire.delete()
            return JsonResponse({'status': "success", "message": "L'horaire a été supprimé avec succès"})
        except Horaire.DoesNotExist:
            return JsonResponse({'status': "error", "message": "L'horaire spécifié n'existe pas"})
    else:
        return JsonResponse({'status': "error", "message": "Méthode non autorisée"})