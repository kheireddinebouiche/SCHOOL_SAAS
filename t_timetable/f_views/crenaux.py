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
    context = {
        "modeles" : liste
    }
    return render(request, 'tenant_folder/timetable/crenaux/liste_model_crenau.html',context)

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
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        jours_travail = request.POST.getlist('jours_travail')
        
        # Récupérer les heures de début et de fin
        heures_debut = request.POST.getlist('heure_debut')
        heures_fin = request.POST.getlist('heure_fin')
        
        # Valider la correspondance des plages horaires
        if len(heures_debut) != len(heures_fin):
            return JsonResponse({ 'success': False,'message': "Les heures de début et de fin ne correspondent pas."})
        
        # Créer la liste des plages horaires
        plages_horaires = []
        for debut, fin in zip(heures_debut, heures_fin):
            if debut and fin: 
                plages_horaires.append({
                    'heure_debut': debut,
                    'heure_fin': fin
                })
        
        
        modele = get_object_or_404(ModelCrenau, pk=modele_id)
        
        modele.label = nom
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
