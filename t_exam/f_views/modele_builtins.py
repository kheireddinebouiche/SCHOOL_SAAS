from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import ModelBuilltins, BuiltinTypeNote, BuiltinSousNote, BuiltinTypeNoteDependency, NoteBloc
from t_formations.models import Formation
from django.db import transaction
import json
from django.contrib.auth.decorators import login_required

@login_required(login_url="institut_app:login")
def ModelBuilltinPage(request):
    """Page principale pour la gestion des modèles de bulletins"""
    formations = Formation.objects.all()
    context = {
        'tenant': request.tenant,
        'formations': formations
    }
    return render(request, 'tenant_folder/exams/model-builtins.html', context)

@login_required(login_url="institut_app:login")
def ApiListModeleBuilltins(request):
    """API pour lister tous les modèles de bulletins"""
    obj = ModelBuilltins.objects.all().values('id', 'label', 'formation__nom', 'is_default')
    data = []
    for item in obj:
        data.append({
            'id': item['id'],
            'label': item['label'],
            'formation': item['formation__nom'] if item['formation__nom'] else 'Toutes les formations',
            'is_default': 'Oui' if item['is_default'] else 'Non'
        })
    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
def NewModelBuilltin(request):
    """Vue pour créer un nouveau modèle de bulletin"""
    if request.method == "POST":
        label = request.POST.get('label')
        formation_id = request.POST.get('formation')
        is_default = request.POST.get('is_default') == 'on'

        # Si un modèle est défini comme par défaut, on désactive les autres
        if is_default:
            ModelBuilltins.objects.filter(is_default=True).update(is_default=False)

        formation = None
        if formation_id and formation_id != 'null' and formation_id != '':
            formation = Formation.objects.get(id=formation_id)  # Correction: utiliser id au lieu de code

        model = ModelBuilltins.objects.create(
            label=label,
            formation=formation,
            is_default=is_default
        )

        return JsonResponse({'statut': 'success', 'id': model.id})
    else:
        formations = Formation.objects.all()
        context = {
            'formations': formations,
            'tenant': request.tenant
        }
        return render(request, 'tenant_folder/exams/template-modele-builtins.html', context)

@login_required(login_url="institut_app:login")
def ApiDeleteModelBuitltin(request):
    """API pour supprimer un modèle de bulletin"""
    id = request.GET.get('id')
    obj = ModelBuilltins.objects.get(id=id)
    obj.delete()
    return JsonResponse({'status': 'success', 'message': 'Le modèle de bulletin a été supprimé avec succès.'})

@login_required(login_url="institut_app:login")
def ApiGetModelBuilltinDetails(request):
    """API pour obtenir les détails d'un modèle de bulletin avec ses types de notes et sous-notes"""
    model_id = request.GET.get('id')
    model = ModelBuilltins.objects.get(id=model_id)

    types_notes = BuiltinTypeNote.objects.filter(builtin=model).order_by('ordre')

    data = {
        'id': model.id,
        'label': model.label,
        'formation_id': model.formation.id if model.formation else None,
        'formation_nom': model.formation.nom if model.formation else 'Toutes les formations',
        'is_default': model.is_default,
        'types_notes': []
    }

    for type_note in types_notes:
        sous_notes = BuiltinSousNote.objects.filter(type_note=type_note).order_by('ordre')

        # Get dependencies for this type note
        dependencies = BuiltinTypeNoteDependency.objects.filter(parent=type_note)
        dependencies_data = [
            {
                'id': dep.id,
                'child_id': dep.child.id,
                'child_code': dep.child.code,
                'child_libelle': dep.child.libelle
            } for dep in dependencies
        ]

        data['types_notes'].append({
            'id': type_note.id,
            'code': type_note.code,
            'libelle': type_note.libelle,
            'max_note': type_note.max_note,
            'has_sous_notes': type_note.has_sous_notes,
            'is_rattrapage': type_note.is_rattrapage,
            'is_rachat': type_note.is_rachat,
            'nb_sous_notes': type_note.nb_sous_notes,
            'ordre': type_note.ordre,
            'is_calculee': type_note.is_calculee,
            'type_calcul': type_note.type_calcul,
            'bloc_id': type_note.bloc.id if type_note.bloc else None,
            'bloc_label': type_note.bloc.label if type_note.bloc else None,
            'dependencies': dependencies_data,
            'sous_notes': [
                {
                    'id': sn.id,
                    'label': sn.label,
                    'max_note' : sn.max_note,
                    'ordre': sn.ordre
                } for sn in sous_notes
            ]
        })

    return JsonResponse(data)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateModelBuilltin(request):
    """API pour mettre à jour un modèle de bulletin"""
    if request.method == 'POST':
        model_id = request.POST.get('id')
        label = request.POST.get('label')
        formation_id = request.POST.get('formation')
        is_default = request.POST.get('is_default') == 'on'
        
        model = ModelBuilltins.objects.get(id=model_id)
        
        # Si ce modèle devient le défaut, on désactive les autres
        if is_default and not model.is_default:
            ModelBuilltins.objects.filter(is_default=True).update(is_default=False)
        
        formation = None
        if formation_id and formation_id != 'null' and formation_id != '':
            formation = Formation.objects.get(id=formation_id)
        
        model.label = label
        model.formation = formation
        model.is_default = is_default
        model.save()
        
        return JsonResponse({'status': 'success', 'message': 'Modèle mis à jour avec succès'})
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@login_required(login_url="institut_app:login")
def ApiGetTypeNotes(request):
    """API pour obtenir les types de notes d'un modèle"""
    model_id = request.GET.get('model_id')
    types_notes = BuiltinTypeNote.objects.filter(builtin_id=model_id).order_by('ordre')

    data = []
    for type_note in types_notes:
        data.append({
            'id': type_note.id,
            'code': type_note.code,
            'libelle': type_note.libelle,
            'max_note': type_note.max_note,
            'has_sous_notes': type_note.has_sous_notes,
            'is_rattrapage': type_note.is_rattrapage,
            'is_rachat': type_note.is_rachat,
            'nb_sous_notes': type_note.nb_sous_notes,
            'ordre': type_note.ordre
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiAddTypeNote(request):
    """API pour ajouter un type de note à un modèle"""
    if request.method == 'POST':
        model_id = request.POST.get('model_id')
        code = request.POST.get('code')
        libelle = request.POST.get('libelle')
        max_note = request.POST.get('max_note')
        has_sous_notes = request.POST.get('has_sous_notes') == 'on'
        is_rattrapage = request.POST.get('is_rattrapage') == 'on'
        is_rachat = request.POST.get('is_rachat') == 'on'
        nb_sous_notes = request.POST.get('nb_sous_notes', 0)
        ordre = request.POST.get('ordre', 0)
        is_calculee = request.POST.get('is_calculee') == 'on'
        type_calcul = request.POST.get('type_calcul', 'NONE')
        bloc_id = request.POST.get('bloc_id')

        builtin = ModelBuilltins.objects.get(id=model_id)

        bloc = None
        if bloc_id and bloc_id != 'null' and bloc_id != '':
            bloc = NoteBloc.objects.get(id=bloc_id)

        type_note = BuiltinTypeNote.objects.create(
            builtin=builtin,
            bloc=bloc,
            code=code,
            libelle=libelle,
            max_note=float(max_note),
            has_sous_notes=has_sous_notes,
            is_rattrapage=is_rattrapage,
            is_rachat=is_rachat,
            nb_sous_notes=int(nb_sous_notes),
            ordre=int(ordre),
            is_calculee=is_calculee,
            type_calcul=type_calcul
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Type de note ajouté avec succès',
            'id': type_note.id
        })

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateTypeNote(request):
    """API pour mettre à jour un type de note"""
    if request.method == 'POST':
        type_note_id = request.POST.get('type_note_id')
        code = request.POST.get('code')
        libelle = request.POST.get('libelle')
        max_note = request.POST.get('max_note')
        has_sous_notes = request.POST.get('has_sous_notes') == 'on'
        is_rattrapage = request.POST.get('is_rattrapage') == 'on'
        is_rachat = request.POST.get('is_rachat') == 'on'
        nb_sous_notes = request.POST.get('nb_sous_notes', 0)
        ordre = request.POST.get('ordre', 0)
        is_calculee = request.POST.get('is_calculee') == 'on'
        type_calcul = request.POST.get('type_calcul', 'NONE')
        bloc_id = request.POST.get('bloc_id')

        type_note = BuiltinTypeNote.objects.get(id=type_note_id)

        # Update bloc
        if bloc_id and bloc_id != 'null' and bloc_id != '':
            bloc = NoteBloc.objects.get(id=bloc_id)
            type_note.bloc = bloc
        else:
            type_note.bloc = None

        type_note.code = code
        type_note.libelle = libelle
        type_note.max_note = float(max_note)
        type_note.has_sous_notes = has_sous_notes
        type_note.is_rattrapage = is_rattrapage
        type_note.is_rachat = is_rachat
        type_note.nb_sous_notes = int(nb_sous_notes)
        type_note.ordre = int(ordre)
        type_note.is_calculee = is_calculee
        type_note.type_calcul = type_calcul
        type_note.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Type de note mis à jour avec succès'
        })

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiDeleteTypeNote(request):
    """API pour supprimer un type de note"""
    type_note_id = request.GET.get('id')
    type_note = BuiltinTypeNote.objects.get(id=type_note_id)
    type_note.delete()
    return JsonResponse({
        'status': 'success', 
        'message': 'Type de note supprimé avec succès'
    })

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiAddSousNote(request):
    """API pour ajouter une sous-note à un type de note"""
    if request.method == 'POST':
        type_note_id = request.POST.get('type_note_id')
        label = request.POST.get('label')
        max_note = request.POST.get('max_note')
        ordre = request.POST.get('ordre', 0)

        type_note = BuiltinTypeNote.objects.get(id=type_note_id)

        sous_note = BuiltinSousNote.objects.create(
            type_note=type_note,
            label=label,
            max_note=float(max_note) if max_note else None,
            ordre=int(ordre)
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Sous-note ajoutée avec succès',
            'id': sous_note.id
        })

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@transaction.atomic
def ApiUpdateSousNote(request):
    """API pour mettre à jour une sous-note"""
    if request.method == 'POST':
        sous_note_id = request.POST.get('sous_note_id')
        label = request.POST.get('label')
        max_note = request.POST.get('max_note')
        ordre = request.POST.get('ordre', 0)

        sous_note = BuiltinSousNote.objects.get(id=sous_note_id)
        sous_note.label = label
        sous_note.max_note = float(max_note) if max_note else None
        sous_note.ordre = int(ordre)
        sous_note.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Sous-note mise à jour avec succès'
        })

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@transaction.atomic
def ApiDeleteSousNote(request):
    """API pour supprimer une sous-note"""
    sous_note_id = request.GET.get('id')
    sous_note = BuiltinSousNote.objects.get(id=sous_note_id)
    sous_note.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Sous-note supprimée avec succès'
    })

@transaction.atomic
def ApiBulkUpdateSousNotes(request):
    """API pour mettre à jour plusieurs sous-notes à la fois"""
    if request.method == 'POST':
        type_note_id = request.POST.get('type_note_id')
        type_note = BuiltinTypeNote.objects.get(id=type_note_id)

        # Supprimer toutes les sous-notes existantes pour ce type de note
        BuiltinSousNote.objects.filter(type_note=type_note).delete()

        # Créer les nouvelles sous-notes
        sous_notes_data = []
        i = 0
        while f'sous_note_labels[{i}][label]' in request.POST:
            label = request.POST.get(f'sous_note_labels[{i}][label]')
            max_note = request.POST.get(f'sous_note_labels[{i}][max_note]')
            ordre = request.POST.get(f'sous_note_labels[{i}][ordre]', i)

            if label:  # Ne créer que si le label n'est pas vide
                sous_note = BuiltinSousNote.objects.create(
                    type_note=type_note,
                    label=label,
                    max_note=float(max_note) if max_note else None,
                    ordre=int(ordre)
                )
                sous_notes_data.append({
                    'id': sous_note.id,
                    'label': sous_note.label,
                    'max_note': sous_note.max_note,
                    'ordre': sous_note.ordre
                })
            i += 1

        return JsonResponse({
            'status': 'success',
            'message': 'Sous-notes mises à jour avec succès',
            'sous_notes': sous_notes_data
        })

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiAddTypeNoteDependency(request):
    """API pour ajouter une dépendance entre types de notes"""
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        child_id = request.POST.get('child_id')

        parent = BuiltinTypeNote.objects.get(id=parent_id)
        child = BuiltinTypeNote.objects.get(id=child_id)

        # Vérifier qu'on ne crée pas une boucle de dépendance
        if creates_cycle(parent, child):
            return JsonResponse({
                'status': 'error',
                'message': 'Cette dépendance créerait une boucle de dépendance'
            })

        dependency, created = BuiltinTypeNoteDependency.objects.get_or_create(
            parent=parent,
            child=child
        )

        if created:
            return JsonResponse({
                'status': 'success',
                'message': 'Dépendance ajoutée avec succès',
                'id': dependency.id
            })
        else:
            return JsonResponse({
                'status': 'success',
                'message': 'La dépendance existe déjà',
                'id': dependency.id
            })

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiDeleteTypeNoteDependency(request):
    """API pour supprimer une dépendance entre types de notes"""
    dependency_id = request.GET.get('id')
    dependency = BuiltinTypeNoteDependency.objects.get(id=dependency_id)
    dependency.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Dépendance supprimée avec succès'
    })

@login_required(login_url="institut_app:login")
def ApiGetTypeNoteDependencies(request):
    """API pour obtenir toutes les dépendances d'un type de note"""
    parent_id = request.GET.get('parent_id')
    parent = BuiltinTypeNote.objects.get(id=parent_id)

    dependencies = BuiltinTypeNoteDependency.objects.filter(parent=parent)

    data = []
    for dep in dependencies:
        data.append({
            'id': dep.id,
            'parent_id': dep.parent.id,
            'parent_code': dep.parent.code,
            'parent_libelle': dep.parent.libelle,
            'child_id': dep.child.id,
            'child_code': dep.child.code,
            'child_libelle': dep.child.libelle
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
def ApiGetTypeNoteAvailableDependencies(request):
    """API pour obtenir tous les types de notes disponibles pour les dépendances"""
    model_id = request.GET.get('model_id')
    parent_id = request.GET.get('parent_id')

    # Récupérer tous les types de notes du modèle sauf le parent lui-même
    available_types = BuiltinTypeNote.objects.filter(builtin_id=model_id).exclude(id=parent_id)

    # Exclure les types de notes qui sont déjà dépendants du parent (pour éviter les boucles)
    parent = BuiltinTypeNote.objects.get(id=parent_id)
    dependencies = BuiltinTypeNoteDependency.objects.filter(parent=parent)
    excluded_ids = [dep.child.id for dep in dependencies]
    available_types = available_types.exclude(id__in=excluded_ids)

    data = []
    for type_note in available_types:
        data.append({
            'id': type_note.id,
            'code': type_note.code,
            'libelle': type_note.libelle
        })

    return JsonResponse(data, safe=False)

def creates_cycle(parent, child):
    """
    Fonction pour vérifier si l'ajout d'une dépendance créerait une boucle
    """
    # Vérifier si le child dépend déjà du parent (directement ou indirectement)
    visited = set()
    stack = [child]

    while stack:
        current = stack.pop()
        if current.id == parent.id:
            return True  # Une boucle serait créée
        if current.id in visited:
            continue
        visited.add(current.id)

        # Ajouter tous les parents de current à la pile
        parents = BuiltinTypeNoteDependency.objects.filter(child=current).values_list('parent', flat=True)
        for parent_id in parents:
            parent_obj = BuiltinTypeNote.objects.get(id=parent_id)
            if parent_obj.id not in visited:
                stack.append(parent_obj)

    return False

def ApiGetSousNotesForType(request):
    """API pour obtenir toutes les sous-notes d'un type de note"""
    type_note_id = request.GET.get('type_note_id')
    type_note = BuiltinTypeNote.objects.get(id=type_note_id)

    sous_notes = BuiltinSousNote.objects.filter(type_note=type_note).order_by('ordre')

    data = []
    for sous_note in sous_notes:
        data.append({
            'id': sous_note.id,
            'label': sous_note.label,
            'max_note': sous_note.max_note,
            'ordre': sous_note.ordre
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
def ApiGetAllBlocs(request):
    """API pour obtenir tous les blocs de notes"""
    blocs = NoteBloc.objects.all().order_by('ordre')

    data = []
    for bloc in blocs:
        data.append({
            'id': bloc.id,
            'label': bloc.label,
            'code': bloc.code,
            'ordre': bloc.ordre
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiAddBloc(request):
    """API pour ajouter un nouveau bloc de notes"""
    if request.method == 'POST':
        label = request.POST.get('label')
        code = request.POST.get('code')
        ordre = request.POST.get('ordre', 0)

        # Check if code already exists
        if NoteBloc.objects.filter(code=code).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Un bloc avec ce code existe déjà'
            })

        bloc = NoteBloc.objects.create(
            label=label,
            code=code,
            ordre=int(ordre)
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Bloc ajouté avec succès',
            'id': bloc.id,
            'label': bloc.label,
            'code': bloc.code,
            'ordre': bloc.ordre
        })

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})