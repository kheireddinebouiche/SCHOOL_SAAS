from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import ModelBuilltins, BuiltinTypeNote, BuiltinSousNote
from t_formations.models import Formation, Modules
from t_timetable.models import Salle
from t_exam.models import *
from t_groupe.models import Groupe,GroupeLine
from django.db import transaction, IntegrityError
import json
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required(login_url="institut_app:login")
def GeneratePvModal(request, pk):
    obj = ExamPlanification.objects.get(id=pk)
    groupe = SessionExamLine.objects.get(id=obj.exam_line.id)

    modeleBuiltin = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)

    # Get students from the group
    all_students = GroupeLine.objects.filter(groupe_id=groupe.groupe.id)

    # Get the commission results for the session if it exists
    commission_results = {}
    if groupe.session.commission:
        commission_results = {
            result.etudiants.id: result.result
            for result in CommisionResult.objects.filter(
                commission=groupe.session.commission,
                modules__id=obj.module.id  # Filter by the current module
            ).distinct()
        }

    # Filter students based on commission results and exam type
    exam_type = obj.type_examen
    filtered_students = []

    for student_line in all_students:
        student_id = student_line.student.id
        commission_result = commission_results.get(student_id, None)

        # Apply filtering based on exam type and commission result
        if exam_type == 'normal':
            # For normal exam, show ALL students regardless of commission result
            # But handle their status differently in the template
            filtered_students.append(student_line)
        elif exam_type == 'rachat':
            # For rachat exam, show students with 'rach' result
            if commission_result == 'rach':
                filtered_students.append(student_line)
        elif exam_type == 'rattrage':
            # For rattrapage exam, we need to find the original exam's PV to check ExamDecisionEtudiant
            # Look for the original normal exam for this module and group
            original_planification = ExamPlanification.objects.filter(
                exam_line=groupe,
                module=obj.module,
                type_examen='normal'  # Original normal exam
            ).first()

            if original_planification:
                original_pv = PvExamen.objects.filter(exam_planification=original_planification).first()
                if original_pv:
                    # Show students who have 'rattrapage' status in the original exam's decisions
                    if ExamDecisionEtudiant.objects.filter(pv=original_pv, etudiant=student_line.student, statut='rattrapage').exists():
                        filtered_students.append(student_line)
            else:
                # If no original exam found, check the current PV as fallback
                pv_examen, created = PvExamen.objects.get_or_create(exam_planification=obj)
                if ExamDecisionEtudiant.objects.filter(pv=pv_examen, etudiant=student_line.student, statut='rattrapage').exists():
                    filtered_students.append(student_line)
        else:
            # Default: show all students
            filtered_students.append(student_line)

    students = filtered_students

    session = groupe.session.get_type_session_display()
    date_debut = groupe.session.date_debut.date()
    date_fin = groupe.session.date_fin.date()
    module = obj.module.label
    note_eliminatoire = obj.module.n_elimate

    # Get or create the PvExamen record
    pv_examen, created = PvExamen.objects.get_or_create(exam_planification=obj)

    # If this is the first time creating the PV, create the ExamTypeNote records based on BuiltinTypeNote
    if created:
        for builtin_type_note in modeleBuiltin.types_notes.all().order_by('ordre'):
            exam_type_note = ExamTypeNote.objects.create(
                pv=pv_examen,
                bloc=builtin_type_note.bloc,  # Copy the bloc from the builtin type note
                code=builtin_type_note.code,
                libelle=builtin_type_note.libelle,
                max_note=builtin_type_note.max_note,
                has_sous_notes=builtin_type_note.has_sous_notes,
                nb_sous_notes=builtin_type_note.nb_sous_notes,
                ordre=builtin_type_note.ordre
            )

            # Create ExamNote records for each student for this type of note
            for student_line in students:
                exam_note = ExamNote.objects.create(
                    pv=pv_examen,
                    etudiant=student_line.student,
                    type_note=exam_type_note,
                    valeur=None
                )

                # If this type note has sous-notes, create them
                if builtin_type_note.has_sous_notes and builtin_type_note.nb_sous_notes > 0:
                    for builtin_sous_note in builtin_type_note.sous_notes.all().order_by('ordre'):
                        ExamSousNote.objects.create(
                            note=exam_note,
                            valeur=0.0  # Use 0.0 instead of None to avoid NOT NULL constraint
                        )

    # Get the builtin model to match the IDs used in the template
    modele_builtins = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)

    # Filter type notes based on exam type
    exam_type = obj.type_examen  # Get the actual type, not the display value
    if exam_type == 'normal':
        # For normal exam, show all types where both is_rattrapage and is_rachat are False
        all_types_notes = modele_builtins.types_notes.filter(is_rattrapage=False, is_rachat=False).order_by('ordre')
    elif exam_type == 'rattrage':
        # For rattrapage exam, show only types where is_rattrapage is True
        all_types_notes = modele_builtins.types_notes.filter(is_rattrapage=True).order_by('ordre')
    elif exam_type == 'rachat':
        # For rachat exam, show only types where is_rachat is True
        all_types_notes = modele_builtins.types_notes.filter(is_rachat=True).order_by('ordre')
    else:
        # Default case: show all type notes
        all_types_notes = modele_builtins.types_notes.all().order_by('ordre')

    # Separate type notes with sub-notes from those without sub-notes
    # Show types with sub-notes first, then types without sub-notes
    types_with_sous_notes = all_types_notes.filter(has_sous_notes=True, nb_sous_notes__gt=0).order_by('ordre')
    types_without_sous_notes = all_types_notes.filter(has_sous_notes=False).order_by('ordre')

    # Combine the two querysets: first with sub-notes, then without sub-notes
    filtered_types_notes = list(types_with_sous_notes) + list(types_without_sous_notes)

    # Group type notes by blocs for the template
    # Get all blocs associated with these type notes, ordered by bloc order
    blocs_with_types = {}
    bloc_order = {}  # To maintain bloc order

    for type_note in filtered_types_notes:
        bloc = type_note.bloc
        bloc_key = bloc.id if bloc else 'no_bloc'

        if bloc_key not in blocs_with_types:
            blocs_with_types[bloc_key] = {
                'bloc': bloc,
                'types': []
            }
            if bloc:
                bloc_order[bloc.id] = bloc.ordre

        blocs_with_types[bloc_key]['types'].append(type_note)

    # Sort blocs by order, with 'no_bloc' at the end
    sorted_bloc_keys = sorted([k for k in blocs_with_types.keys() if k != 'no_bloc'],
                             key=lambda x: bloc_order[x]) + (['no_bloc'] if 'no_bloc' in blocs_with_types else [])

    # Create ordered list of blocs with their types
    ordered_blocs_with_types = []
    for bloc_key in sorted_bloc_keys:
        ordered_blocs_with_types.append(blocs_with_types[bloc_key])

    # Create a mapping between builtin type note IDs and exam type note objects
    builtin_to_exam_mapping = {}
    for exam_type_note in pv_examen.exam_types_notes.all():
        # Find the corresponding builtin type note by code
        builtin_type_note = modele_builtins.types_notes.filter(code=exam_type_note.code).first()
        if builtin_type_note:
            builtin_to_exam_mapping[builtin_type_note.id] = exam_type_note

    # Prepare data for the template - use builtin IDs as keys to match template
    student_notes_data = {}
    for student_line in students:
        student_notes_data[student_line.student.id] = {}
        for builtin_type_note in filtered_types_notes:  # Use filtered types instead of all
            # Get the corresponding exam type note
            exam_type_note = builtin_to_exam_mapping.get(builtin_type_note.id)
            if exam_type_note:
                exam_note = ExamNote.objects.filter(
                    pv=pv_examen,
                    etudiant=student_line.student,
                    type_note=exam_type_note
                ).first()

                if exam_note:
                    sous_notes_list = list(exam_note.sous_notes.all())

                    student_notes_data[student_line.student.id][builtin_type_note.id] = {
                        'value': exam_note.valeur if exam_note.valeur is None else float(exam_note.valeur),
                        'sous_notes': [{'valeur': float(sn.valeur) if sn.valeur is not None else None} for sn in sous_notes_list] if exam_type_note.has_sous_notes else []
                    }
                else:
                    # If no exam note exists yet, create empty data structure
                    student_notes_data[student_line.student.id][builtin_type_note.id] = {
                        'value': None,
                        'sous_notes': []
                    }

    # Récupérer les décisions existantes pour ce PV
    decisions_existantes = {}

    # Récupérer les décisions pour ce PV spécifique
    for decision in ExamDecisionEtudiant.objects.filter(pv=pv_examen):
        decisions_existantes[decision.etudiant.id] = {
            'statut': decision.statut,
            'moyenne': decision.moyenne
        }

    # Pour les examens de rattrapage, on devrait chercher les décisions des examens originaux pour ce module et groupe
    if exam_type == 'rattrage':
        # Trouver les examens normaux originaux pour ce module et ce groupe
        original_planifications = ExamPlanification.objects.filter(
            exam_line=groupe,
            module=obj.module,
            type_examen='normal'  # Examen normal original
        )

        for original_plan in original_planifications:
            original_pv = PvExamen.objects.filter(exam_planification=original_plan).first()
            if original_pv:
                for decision in ExamDecisionEtudiant.objects.filter(pv=original_pv, statut='rattrapage'):
                    # Ajouter les décisions de rattrapage de l'examen original
                    decisions_existantes[decision.etudiant.id] = {
                        'statut': decision.statut,
                        'moyenne': decision.moyenne
                    }

    # Pass commission results to template for special handling
    context = {
        'pk': pk,
        'groupe': groupe,
        'modele': modeleBuiltin,
        'filtered_types_notes': filtered_types_notes,  # Pass the filtered types
        'ordered_blocs_with_types': ordered_blocs_with_types,  # Pass the grouped blocs with types
        'students': students,
        'pv_examen': pv_examen,
        'student_notes_data': student_notes_data,
        'session' : f"{session} - {date_debut}/{date_fin}",
        "module" : module,
        'note_eliminatoire' : note_eliminatoire,
        'decisions_existantes': decisions_existantes,
        'commission_results': commission_results,  # Pass commission results to template
        'exam_planification': obj,  # Pass the exam planification object to template
    }
    return render(request, 'tenant_folder/exams/remplissage_notes.html', context)