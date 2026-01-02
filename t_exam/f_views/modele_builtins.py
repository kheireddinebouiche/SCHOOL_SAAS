from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import ModelBuilltins, BuiltinTypeNote, BuiltinSousNote
from t_formations.models import Formation
from django.db import transaction
import json


def ModelBuilltinPage(request):
    """Page principale pour la gestion des modèles de bulletins"""
    formations = Formation.objects.all()
    context = {
        'tenant': request.tenant,
        'formations': formations
    }
    return render(request, 'tenant_folder/exams/model-builtins.html', context)


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


def ApiDeleteModelBuitltin(request):
    """API pour supprimer un modèle de bulletin"""
    id = request.GET.get('id')
    obj = ModelBuilltins.objects.get(id=id)
    obj.delete()
    return JsonResponse({'status': 'success', 'message': 'Le modèle de bulletin a été supprimé avec succès.'})


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

        builtin = ModelBuilltins.objects.get(id=model_id)

        type_note = BuiltinTypeNote.objects.create(
            builtin=builtin,
            code=code,
            libelle=libelle,
            max_note=float(max_note),
            has_sous_notes=has_sous_notes,
            is_rattrapage=is_rattrapage,
            is_rachat=is_rachat,
            nb_sous_notes=int(nb_sous_notes),
            ordre=int(ordre)
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Type de note ajouté avec succès',
            'id': type_note.id
        })

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


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

        type_note = BuiltinTypeNote.objects.get(id=type_note_id)
        type_note.code = code
        type_note.libelle = libelle
        type_note.max_note = float(max_note)
        type_note.has_sous_notes = has_sous_notes
        type_note.is_rattrapage = is_rattrapage
        type_note.is_rachat = is_rachat
        type_note.nb_sous_notes = int(nb_sous_notes)
        type_note.ordre = int(ordre)
        type_note.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Type de note mis à jour avec succès'
        })

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


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