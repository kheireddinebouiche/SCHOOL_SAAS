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
from django.db.models import Count
import json

@login_required(login_url="institut_app:login")
def PageAffectation(request):

    modules = Modules.objects.annotate(nombre_formateur = Count('affect_module'))
    specialite = Specialites.objects.all()
    formateurs = Formateurs.objects.all().values('id', 'nom', 'prenom', 'email')

    affectations = EnseignantModule.objects.values('formateur_id', 'module_id')
    affectations_list = list(affectations)

    context = {
        'modules' : modules,
        'specialites' : specialite,
        'formateurs_json': json.dumps(list(formateurs)),
        'affectations_json': json.dumps(affectations_list),
    }
    return render(request, 'tenant_folder/formateur/affectation_modules.html', context)


@login_required(login_url="institut_app:login")
def LoadFormateurs(request):
    if request.method == "GET":
        formateur = Formateurs.objects.all().values('id','nom','prenom','email','telephone')
        return JsonResponse(list(formateur), safe=False)
    else:
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
def ApiLoadFormation(request):
    if request.method == "GET":
        formations = Formation.objects.all().values('id','code','nom')

        return JsonResponse(list(formations), safe=False)

    return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
def ApiFilterSpecialite(request):
    if request.method == "GET":
        formation = request.GET.get('id')

        specialite = Specialites.objects.filter(formation__code = formation).values('id','code','version','label')

        return JsonResponse(list(specialite), safe=False)
    else:
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="institut_app:login")
def ApiFilterModules(request):
    if request.method == "GET":
        specialite = request.GET.get('id')

        liste_module = Modules.objects.filter(specialite__code = specialite).values('id','code','label')
        return JsonResponse(list(liste_module), safe=False)

    else:
        return JsonResponse({"status" : "error"})
    

@login_required(login_url="institut_app:login")
def ApiLoaAffectation(request):
    if request.method == "GET":
        formateurId = request.GET.get('formateurId')

        modules = EnseignantModule.objects.filter(formateur_id = formateurId).values('id','module__id','module__label','module__code')

        return JsonResponse(list(modules), safe=False)
    else:

        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
def ApiGetAffectations(request):
    affectations = list(EnseignantModule.objects.values('id', 'formateur_id', 'module_id'))
    return JsonResponse({'affectations': affectations})

@login_required(login_url="institut_app:login")
def ApiLoadModules(request):
    modules = Modules.objects.annotate(nombre_formateur = Count('affect_module')).values('id','label','code','specialite__label', 'nombre_formateur')

    return JsonResponse(list(modules), safe=False)


@login_required(login_url="institut_app:login")
def LoadAssignedProf(request):
    if request.method == "GET":
        moduleId = request.GET.get('moduleId')
        if not moduleId:
            return JsonResponse({"status" : "error" , "messages" : "Erreur ! ID module indisponible"})

        liste = EnseignantModule.objects.filter(module_id = moduleId).values('id','formateur__nom','formateur__prenom','formateur__email')

        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
def LoadAffectation(request):
    """
    Vue pour charger les affectations avec le bouton de suppression
    """
    if request.method == "GET":
        # Charger toutes les affectations avec les informations du formateur et du module
        affectations = EnseignantModule.objects.select_related('formateur', 'module').values(
            'id',
            'formateur__id',
            'formateur__nom',
            'formateur__prenom',
            'formateur__email',
            'module__id',
            'module__code',
            'module__label'
        )

        # Ajouter les boutons d'action à chaque affectation
        affectations_avec_boutons = []
        for affectation in affectations:
            affectation_avec_bouton = {
                'id': affectation['id'],
                'formateur_id': affectation['formateur__id'],
                'formateur_nom': f"{affectation['formateur__nom']} {affectation['formateur__prenom']}",
                'formateur_email': affectation['formateur__email'],
                'module_id': affectation['module__id'],
                'module_code': affectation['module__code'],
                'module_label': affectation['module__label'],
                'actions': f"""
                    <button type="button" class="btn btn-danger btn-sm supprimer-affectation"
                            data-affectation-id="{affectation['id']}"
                            title="Supprimer cette affectation">
                        <i class="ri-delete-bin-line"></i> Supprimer
                    </button>
                """
            }
            affectations_avec_boutons.append(affectation_avec_bouton)

        return JsonResponse(list(affectations_avec_boutons), safe=False)
    else:
        return JsonResponse({"status" : "error", "message" : "Méthode non autorisée"})
    
@login_required(login_url="insitut_app:login")
@transaction.atomic
def ApiAffectTrainer(request):
    if request.method == "POST":
        moduleId = request.POST.get('module_id')
        trainerId = request.POST.get('formateur_id')

        if not trainerId and not moduleId:
            return JsonResponse({"status" : "error", "message" : "Des données sont manquante lors du traitement de la requete"})
        try:
            EnseignantModule.objects.get_or_create(
                module_id=moduleId,
                formateur_id = trainerId
            )
            return JsonResponse({"status" : "success", "message" : "L'enseignant à été affecter avec succès"})
        except Exception as e:
            return JsonResponse({"status":"error",'message' : "Le module a été déja affecter a l'enseignant."})
    else:
        return JsonResponse({"status" : "error", "message" : "Methode non autoriser"})
    


##### Fonction qui permet de verifier si un module affecter a un enseignant enseigne deja ####
def CheckIfModuleIsPlanned(moduleId, trainerId):
    return TimetableEntry.objects.filter(
        cours_id = moduleId,
        formateur_id = trainerId,
    ).exclude(
        timetable__status="ter" 
    ).exists()

@login_required(login_url="institut_app:login")
def ApiDeaffectTrainer(request):
    if request.method == "POST":
        moduleId = request.POST.get('module_id')
        trainerId = request.POST.get('formateur_id')

        if not trainerId or not moduleId:
            return JsonResponse({"status" : "error", "message" : "Des données sont manquante lors du traitement de la requete"})
        
        if CheckIfModuleIsPlanned(moduleId, trainerId):
            return JsonResponse({"status":"error-suppress"})
        
        try:
            object = EnseignantModule.objects.get(module_id=moduleId, formateur_id=trainerId)
            object.delete()
            return JsonResponse({"status" : "success", "message" : "L'affectation a été supprimée avec succès"})
        except EnseignantModule.DoesNotExist:
            return JsonResponse({"status" : "error", "message" : "L'affectation n'existe pas"})
    else:
        return JsonResponse({"status" : "error", "message" : "Methode non autorisée"})

@login_required(login_url="institut_app:login")
def ApiDeleteAffectation(request):
    """
    Vue pour supprimer une affectation spécifique via une action dans une fenêtre modale
    """
    if request.method == "POST":
        affectation_id = request.POST.get('affectation_id')

        if not affectation_id:
            return JsonResponse({"status" : "error", "message" : "ID d'affectation manquant"})

        try:
            affectation = EnseignantModule.objects.get(id=affectation_id)
            formateur_nom = f"{affectation.formateur.nom} {affectation.formateur.prenom}"
            module_label = affectation.module.label

            affectation.delete()

            return JsonResponse({
                "status" : "success",
                "message" : f"L'affectation de {formateur_nom} au module {module_label} a été supprimée avec succès"
            })
        except EnseignantModule.DoesNotExist:
            return JsonResponse({"status" : "error", "message" : "L'affectation n'existe pas"})
    else:
        return JsonResponse({"status" : "error", "message" : "Méthode non autorisée"})