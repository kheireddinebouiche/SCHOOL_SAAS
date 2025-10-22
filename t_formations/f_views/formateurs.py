from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import *
from ..forms import *
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django_tenants.utils import get_tenant_model, schema_context
from django.http import JsonResponse
from django.db.models import Q



login_required(login_url="institut_app:login")
def PageFormateurs(request):
    liste = Formateurs.objects.all()
    context = {
        "formateurs" : liste
    }
    return render(request, 'tenant_folder/formateur/liste_des_formateur.html', context)

@login_required(login_url="institut_app:login")
@transaction.atomic
def create_formateur(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        diplome = request.POST.get('diplome')

        Formateurs.objects.create(
            nom = nom,
            prenom = prenom,
            telephone = telephone,
            email = email,
            diplome = diplome,
        )
        messages.success(request,'Les données du formateur ont été sauvegarder avec succès.')
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({"status" : "error","message":"Method non autoriser"})


@login_required(login_url="institut_app:login")
@transaction.atomic
def update_formateur(request):
    if request.method == "POST":
        formateur_id = request.POST.get('id')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        diplome = request.POST.get('diplome')

        try:
            formateur = Formateurs.objects.get(id=formateur_id)
            formateur.nom = nom
            formateur.prenom = prenom
            formateur.telephone = telephone
            formateur.email = email
            formateur.diplome = diplome

            formateur.save()
            messages.success(request,'Les données du formateur ont été mises à jour avec succès.')
            return JsonResponse({'status': 'success'})
        except Formateurs.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Le formateur spécifié n\'existe pas.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})


def delete_formateur(request):
    if request.method == "POST":
        formateur_id = request.POST.get('id')

        try:
            formateur = Formateurs.objects.get(id=formateur_id)
            formateur.delete()
            messages.success(request, 'Le formateur a été supprimé avec succès.')
            return JsonResponse({'status': 'success'})
        except Formateurs.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Le formateur spécifié n\'existe pas.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
def ApiGetFormateurs(request):
    try:
        formateurs = Formateurs.objects.all()
        formateurs_data = []
        
        for formateur in formateurs:
            formateurs_data.append({
                'id': formateur.id,
                'nom': formateur.nom,
                'prenom': formateur.prenom,
                'telephone': formateur.telephone,
                'email': formateur.email,
                'diplome': formateur.diplome,
            })
        
        return JsonResponse(formateurs_data, safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


def load_module_teachers(request):
    module_id = request.GET.get('module_id')
    if module_id:
        try:
            # Get all trainers assigned to this module
            teacher_modules = EnseignantModule.objects.filter(module_id=module_id).select_related('formateur')
            teachers_data = []
            
            for tm in teacher_modules:
                formateur = tm.formateur
                teachers_data.append({
                    'id': formateur.id,
                    'nom': formateur.nom,
                    'prenom': formateur.prenom,
                    'telephone': formateur.telephone,
                    'email': formateur.email,
                    'diplome': formateur.diplome,
                })
            
            return JsonResponse(teachers_data, safe=False)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'ID du module requis'})


@login_required(login_url="institut_app:login")
@transaction.atomic
def assign_trainers_to_module(request):
    if request.method == "POST":
        try:
            # Get module ID and trainer IDs from the request
            module_id = request.POST.get('module_id')
            trainer_ids = request.POST.getlist('trainer_ids[]')  # For multiple trainer IDs
        
            if not module_id:
                return JsonResponse({'status': 'error', 'message': 'ID du module est requis'})
            
            if not trainer_ids:
                return JsonResponse({'status': 'error', 'message': 'Au moins un ID d\'enseignant est requis'})
            
            # Convert string IDs to integers and filter out invalid IDs
            valid_trainer_ids = []
            for id_str in trainer_ids:
                try:
                    valid_trainer_ids.append(int(id_str))
                except ValueError:
                    continue  # Skip invalid IDs
            
            if not valid_trainer_ids:
                return JsonResponse({'status': 'error', 'message': 'Aucun ID d\'enseignant valide'})
            
            # Validate module exists
            try:
                module = Modules.objects.get(id=module_id)
            except Modules.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Le module spécifié n\'existe pas'})
            
            # Validate all trainer IDs exist
            formateurs = Formateurs.objects.filter(id__in=valid_trainer_ids)
            found_ids = [f.id for f in formateurs]
            missing_ids = set(valid_trainer_ids) - set(found_ids)
            
            if missing_ids:
                return JsonResponse({'status': 'error', 'message': f'Les formateurs avec les IDs {list(missing_ids)} n\'existent pas'})
            
            # Remove existing associations for this module
            EnseignantModule.objects.filter(module=module).delete()
            
            # Create new associations
            assigned_count = 0
            for formateur in formateurs:
                EnseignantModule.objects.create(
                    module=module,
                    formateur=formateur
                )
                assigned_count += 1
                
            return JsonResponse({
                'status': 'success',
                'message': f'{assigned_count} enseignant(s) affecté(s) au module avec succès'
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
@transaction.atomic
def remove_trainer_from_module(request):
    if request.method == "POST":
        try:
            # Get module ID and trainer ID from the request
            trainer_id = request.POST.get('trainer_id')
            module_id = request.POST.get('module_id')
            
            if not module_id:
                return JsonResponse({'status': 'error', 'message': 'ID du module est requis'})
            
            if not trainer_id:
                return JsonResponse({'status': 'error', 'message': 'ID de l\'enseignant est requis'})
            
            # Validate module exists
            try:
                module = Modules.objects.get(id=module_id)
            except Modules.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Le module spécifié n\'existe pas'})
            
            # Validate trainer exists
            try:
                formateur = Formateurs.objects.get(id=trainer_id)
            except Formateurs.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'L\'enseignant spécifié n\'existe pas'})
            
            # Remove the specific association
            association = EnseignantModule.objects.filter(module=module, formateur=formateur).first()
            if association:
                association.delete()
                messages.success(request, f'L\'enseignant {formateur.nom} {formateur.prenom} a été retiré du module avec succès.')
                return JsonResponse({
                    'status': 'success',
                    'message': f'Enseignant retiré du module avec succès'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Aucune association trouvée entre cet enseignant et ce module'
                })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
@transaction.atomic
def update_module_details(request):
    if request.method == "POST":
        try:
            # Get module ID and updated details from the request
            module_id = request.POST.get('id')
            code = request.POST.get('code')
            label = request.POST.get('label')
            duree = request.POST.get('duree')
            coef = request.POST.get('coef')
            n_elimate = request.POST.get('n_elimate')
            systeme_eval = request.POST.get('systeme_eval')
            
            if not module_id:
                return JsonResponse({'status': 'error', 'message': 'ID du module est requis'})
            
            # Validate module exists
            try:
                module = Modules.objects.get(id=module_id)
            except Modules.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Le module spécifié n\'existe pas'})
            
            # Update the module details
            if code is not None:
                module.code = code
            if label is not None:
                module.label = label
            if duree is not None:
                module.duree = duree
            if coef is not None:
                module.coef = coef
            if n_elimate is not None:
                module.n_elimate = n_elimate
            if systeme_eval is not None:
                module.systeme_eval = systeme_eval
            
            # Update the updated_by field if user is available
            if hasattr(request, 'user') and request.user.is_authenticated:
                module.updated_by = request.user
            
            module.save()
            
            messages.success(request, f'Les détails du module {module.label} ont été mis à jour avec succès.')
            return JsonResponse({
                'status': 'success',
                'message': 'Détails du module mis à jour avec succès'
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
def validate_module(request):
    if request.method == "POST":
        try:
            module_id = request.POST.get('module_id')
            
            if not module_id:
                return JsonResponse({'status': 'error', 'message': 'ID du module est requis'})
            
            # Validate module exists
            try:
                module = Modules.objects.get(id=module_id)
            except Modules.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Le module spécifié n\'existe pas'})
            
            # Update the validation status
            module.est_valider = True
            module.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Module validé avec succès'
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})