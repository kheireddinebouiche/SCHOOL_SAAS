from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from ..forms import *
from ..models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from t_groupe.models import *
from django.views.decorators.http import require_http_methods

@login_required(login_url="institut_app:login")
def ListeModel(request):
    liste = ModelCrenau.objects.all()
    modeles_actifs = ModelCrenau.objects.filter(is_active=True).count()
    
    # Calculate the number of unique days configured across all models
    jours_uniques = set()
    for modele in liste:
        if modele.jour_data and 'jours_travail' in modele.jour_data:
            jours_uniques.update(modele.jour_data['jours_travail'])
    
    # Calculate the number of different configurations (for types count)
    # This might be based on different combinations of hours, or other attributes
    # For now, using a simple approach - you might want to customize this based on your business logic
    types_count = liste.count()  # or some other logic based on your requirements
    
    context = {
        "modeles": liste,
        "model_crenaux": liste,  # For the total count in stats
        "days_count": len(jours_uniques),
        "types_count": types_count,
        "actifs_count": modeles_actifs
    }
    return render(request, 'tenant_folder/timetable/crenaux/liste_model_crenau.html', context)

@login_required(login_url="institut_app:login")
def create_model(request):
    if request.method == 'POST':
        label = request.POST.get('nom')
        description = request.POST.get('description')
        # Since we're now sending multiple days as a JSON array, we need to handle that
        try:
            # Validate required fields
            if not label :
                return JsonResponse({
                    'status': 'error',
                    'message': 'Le champs label est obligatoire'
                })
              
            # Create the ModelCrenau instance
            ModelCrenau.objects.create(
                label=label,
                description = description
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Modèle de créneau créé avec succès!',
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
def model_creneau_detail(request, pk):
    pass

@login_required(login_url="institut_app:login")
def model_creneau_edit(request, pk):
    """
    Vue pour éditer un modèle de créneau existant
    """
    modele = get_object_or_404(ModelCrenau, pk=pk)
    
    # Jours de la semaine
    jours_semaine = [
        {"jour_semaine": "lundi", "nom": "Lundi"},
        {"jour_semaine": "mardi", "nom": "Mardi"},
        {"jour_semaine": "mercredi", "nom": "Mercredi"},
        {"jour_semaine": "jeudi", "nom": "Jeudi"},
        {"jour_semaine": "vendredi", "nom": "Vendredi"},
        {"jour_semaine": "samedi", "nom": "Samedi"},
        {"jour_semaine": "dimanche", "nom": "Dimanche"},
    ]
    
    # Déterminer quels jours sont sélectionnés
    jours_selectionnes = modele.jour_data.get('jours_travail', []) if modele.jour_data else []
    
    # Ajouter une indication si chaque jour est sélectionné
    for jour in jours_semaine:
        jour['est_selectionne'] = jour['jour_semaine'] in jours_selectionnes
    
    # Récupérer les plages horaires stockées
    plages_horaires = []
    if modele.horaire_data and 'plages_horaires' in modele.horaire_data:
        plages_horaires = modele.horaire_data['plages_horaires']
    
    context = {
        'modele': modele,
        'jours': jours_semaine,
        'jours_selectionnes': jours_selectionnes,
        'plages_horaires': plages_horaires,
        # Variables pour chaque jour pour faciliter l'affichage dans le template
        'jour_lundi_selectionne': 'lundi' in jours_selectionnes,
        'jour_mardi_selectionne': 'mardi' in jours_selectionnes,
        'jour_mercredi_selectionne': 'mercredi' in jours_selectionnes,
        'jour_jeudi_selectionne': 'jeudi' in jours_selectionnes,
        'jour_vendredi_selectionne': 'vendredi' in jours_selectionnes,
        'jour_samedi_selectionne': 'samedi' in jours_selectionnes,
        'jour_dimanche_selectionne': 'dimanche' in jours_selectionnes,
    }
    
    return render(request, 'tenant_folder/timetable/crenaux/edit_model_crenau.html', context)

@login_required(login_url="institut_app:login")
def get_horaires(request):
    # This view could return available time slots if there's a Horaire model
    # For now, returning an empty response since horaires are user-defined
    return JsonResponse({
        'status': 'success',
        'horaires': []
    })

@require_http_methods(["POST"])
def save_model_crenau(request):
   
    try:
        modele_id = request.POST.get('modele_id')
        nom_model = request.POST.get('nom_model')
        description = request.POST.get('description')
        jours_travail = request.POST.getlist('jours_travail')
        
        # Récupérer les heures de début, de fin et les noms de créneau
        heures_debut = request.POST.getlist('heure_debut')
        heures_fin = request.POST.getlist('heure_fin')
        noms_creneau = request.POST.getlist('nom_creneau')
        
        # Valider la correspondance des plages horaires
        if len(heures_debut) != len(heures_fin) or len(heures_debut) != len(noms_creneau):
            return JsonResponse({ 'success': False,'message': "Les heures de début, de fin et les noms de créneau ne correspondent pas."})
        
        # Créer la liste des plages horaires
        plages_horaires = []
        for debut, fin, nom in zip(heures_debut, heures_fin, noms_creneau):
            if debut and fin: 
                plages_horaires.append({
                    'heure_debut': debut,
                    'heure_fin': fin,
                    'nom_creneau': nom if nom else f"{debut} - {fin}"  # Default name if empty
                })
        
        
        modele = get_object_or_404(ModelCrenau, pk=modele_id)
        
        modele.label = nom_model
        modele.description = description
        modele.jour_data = {'jours_travail': jours_travail}
        modele.horaire_data = {'plages_horaires': plages_horaires}
        
        modele.save()
        
        return JsonResponse({
            'success': True,
            'message': "Le modèle de créneau a été mis à jour avec succès."
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Une erreur est survenue lors de la sauvegarde : {str(e)}"
        })

@login_required(login_url="institut_app:login")
@require_http_methods(["POST"])
def activate_model_crenau(request):
    try:
        model_id = request.POST.get('model_id')
        
        if not model_id:
            return JsonResponse({
                'success': False,
                'message': "ID du modèle manquant"
            })
        
        # Get the model
        modele = get_object_or_404(ModelCrenau, pk=model_id)
        
        # Check if the model is already activated
        if modele.is_active:
            return JsonResponse({
                'success': False,
                'message': "Le modèle est déjà activé"
            })
        
        # Activate the model
        modele.is_active = True
        modele.save()
        
        return JsonResponse({
            'success': True,
            'message': "Le modèle de créneau a été activé avec succès."
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Une erreur est survenue lors de l'activation : {str(e)}"
        })
