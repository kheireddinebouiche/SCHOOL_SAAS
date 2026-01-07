from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Avg, Count
from t_exam.models import *
from t_groupe.models import Groupe, GroupeLine
from t_etudiants.models import Prospets
from t_formations.models import Modules


@login_required
def groupe_deliberation_results_view(request, session_line_id):
    """
    View to display group deliberation results in a modal
    Note: groupe_id is actually the SessionExamLine ID
    """
    try:
        # Get the SessionExamLine using the groupe_id parameter
        session_exam_line = SessionExamLine.objects.get(id=session_line_id)
        groupe = session_exam_line.groupe  # Get the associated group

        # Get all exam planifications for this session exam line
        exam_planifications = ExamPlanification.objects.filter(
            exam_line=session_exam_line
        ).select_related('module', 'exam_line__session', 'pv').order_by('module__id', 'type_examen')

        # Get all students in the group through GroupeLine
        groupe_lines = GroupeLine.objects.filter(groupe=groupe).select_related('student')
        students = [groupe_line.student for groupe_line in groupe_lines]

        # Group exam planifications by module
        modules_dict = {}
        for exam_plan in exam_planifications:
            module_id = exam_plan.module.id
            if module_id not in modules_dict:
                modules_dict[module_id] = {
                    'module': exam_plan.module,
                    'normal_exam': None,
                    'rachat_exam': None,
                    'rattrapage_exam': None,
                    'normal_note_count': 0,
                    'rachat_note_count': 0,
                    'rattrapage_note_count': 0
                }

            if exam_plan.type_examen == 'normal':
                modules_dict[module_id]['normal_exam'] = exam_plan
                # Count the number of note types for this exam
                modules_dict[module_id]['normal_note_count'] = exam_plan.pv.exam_types_notes.count()
            elif exam_plan.type_examen == 'rachat':
                modules_dict[module_id]['rachat_exam'] = exam_plan
                # Count the number of note types for this exam
                modules_dict[module_id]['rachat_note_count'] = exam_plan.pv.exam_types_notes.count()
            elif exam_plan.type_examen == 'rattrage':
                modules_dict[module_id]['rattrapage_exam'] = exam_plan
                # Count the number of note types for this exam
                modules_dict[module_id]['rattrapage_note_count'] = exam_plan.pv.exam_types_notes.count()

        # Convert to list for template
        grouped_modules = list(modules_dict.values())

        # Prepare data for the template
        results_data = []

        for student in students:
            student_data = {
                'student': student,
                'results': []
            }

            for module_data in grouped_modules:
                result_entry = {
                    'module': module_data['module'],
                    'normal_result': None,
                    'rattrapage_result': None
                }

                # Handle normal exam if exists
                if module_data['normal_exam']:
                    normal_exam_plan = module_data['normal_exam']
                    normal_decision = ExamDecisionEtudiant.objects.filter(
                        pv=normal_exam_plan.pv,
                        etudiant=student
                    ).first()

                    normal_notes = ExamNote.objects.filter(
                        pv=normal_exam_plan.pv,
                        etudiant=student
                    ).select_related('type_note')

                    # Calculate average note for normal exam
                    normal_avg_note = 0
                    if normal_notes.exists():
                        total_notes = 0
                        count_notes = 0
                        for note in normal_notes:
                            if note.valeur is not None:
                                total_notes += note.valeur
                                count_notes += 1
                        if count_notes > 0:
                            normal_avg_note = round(total_notes / count_notes, 2)

                    # Organize normal notes by type
                    normal_notes_by_type = {}
                    for note in normal_notes:
                        normal_notes_by_type[note.type_note.id] = note

                    # Create structured normal notes
                    normal_structured_notes = []
                    if normal_exam_plan.pv.exam_types_notes.exists():
                        for note_type in normal_exam_plan.pv.exam_types_notes.all():
                            note_value = normal_notes_by_type.get(note_type.id)
                            normal_structured_notes.append({
                                'type_note': note_type,
                                'note': note_value,
                                'valeur': note_value.valeur if note_value else '-'
                            })

                    result_entry['normal_result'] = {
                        'exam_plan': normal_exam_plan,
                        'decision': normal_decision,
                        'notes': normal_notes,
                        'notes_by_type': normal_notes_by_type,
                        'structured_notes': normal_structured_notes,
                        'avg_note': normal_avg_note
                    }

                # Handle rachat exam if exists
                if module_data['rachat_exam']:
                    rachat_exam_plan = module_data['rachat_exam']
                    rachat_decision = ExamDecisionEtudiant.objects.filter(
                        pv=rachat_exam_plan.pv,
                        etudiant=student
                    ).first()

                    rachat_notes = ExamNote.objects.filter(
                        pv=rachat_exam_plan.pv,
                        etudiant=student
                    ).select_related('type_note')

                    # Calculate average note for rachat exam
                    rachat_avg_note = 0
                    if rachat_notes.exists():
                        total_notes = 0
                        count_notes = 0
                        for note in rachat_notes:
                            if note.valeur is not None:
                                total_notes += note.valeur
                                count_notes += 1
                        if count_notes > 0:
                            rachat_avg_note = round(total_notes / count_notes, 2)

                    # Organize rachat notes by type
                    rachat_notes_by_type = {}
                    for note in rachat_notes:
                        rachat_notes_by_type[note.type_note.id] = note

                    # Create structured rachat notes
                    rachat_structured_notes = []
                    if rachat_exam_plan.pv.exam_types_notes.exists():
                        for note_type in rachat_exam_plan.pv.exam_types_notes.all():
                            note_value = rachat_notes_by_type.get(note_type.id)
                            rachat_structured_notes.append({
                                'type_note': note_type,
                                'note': note_value,
                                'valeur': note_value.valeur if note_value else '-'
                            })

                    result_entry['rachat_result'] = {
                        'exam_plan': rachat_exam_plan,
                        'decision': rachat_decision,
                        'notes': rachat_notes,
                        'notes_by_type': rachat_notes_by_type,
                        'structured_notes': rachat_structured_notes,
                        'avg_note': rachat_avg_note
                    }

                # Handle rattrapage exam if exists
                if module_data['rattrapage_exam']:
                    rattrapage_exam_plan = module_data['rattrapage_exam']
                    rattrapage_decision = ExamDecisionEtudiant.objects.filter(
                        pv=rattrapage_exam_plan.pv,
                        etudiant=student
                    ).first()

                    rattrapage_notes = ExamNote.objects.filter(
                        pv=rattrapage_exam_plan.pv,
                        etudiant=student
                    ).select_related('type_note')

                    # Calculate average note for rattrapage exam
                    rattrapage_avg_note = 0
                    if rattrapage_notes.exists():
                        total_notes = 0
                        count_notes = 0
                        for note in rattrapage_notes:
                            if note.valeur is not None:
                                total_notes += note.valeur
                                count_notes += 1
                        if count_notes > 0:
                            rattrapage_avg_note = round(total_notes / count_notes, 2)

                    # Organize rattrapage notes by type
                    rattrapage_notes_by_type = {}
                    for note in rattrapage_notes:
                        rattrapage_notes_by_type[note.type_note.id] = note

                    # Create structured rattrapage notes
                    rattrapage_structured_notes = []
                    if rattrapage_exam_plan.pv.exam_types_notes.exists():
                        for note_type in rattrapage_exam_plan.pv.exam_types_notes.all():
                            note_value = rattrapage_notes_by_type.get(note_type.id)
                            rattrapage_structured_notes.append({
                                'type_note': note_type,
                                'note': note_value,
                                'valeur': note_value.valeur if note_value else '-'
                            })

                    result_entry['rattrapage_result'] = {
                        'exam_plan': rattrapage_exam_plan,
                        'decision': rattrapage_decision,
                        'notes': rattrapage_notes,
                        'notes_by_type': rattrapage_notes_by_type,
                        'structured_notes': rattrapage_structured_notes,
                        'avg_note': rattrapage_avg_note
                    }

                student_data['results'].append(result_entry)

            results_data.append(student_data)

        # Check if there are any rachat or rattrapage exams
        has_rachat = any(module_data['rachat_exam'] for module_data in grouped_modules)
        has_rattrapage = any(module_data['rattrapage_exam'] for module_data in grouped_modules)

        context = {
            'groupe': groupe,
            'session_exam_line': session_exam_line,
            'results_data': results_data,
            'grouped_modules': grouped_modules,
            'students': students,
            'has_rachat': has_rachat,
            'has_rattrapage': has_rattrapage
        }

        # Check if the request is AJAX to return only the modal content
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string('tenant_folder/exams/groupe_deliberation_results.html', context, request=request)
            return JsonResponse({'html': html, 'status': 'success'})

        return render(request, 'tenant_folder/exams/groupe_deliberation_results.html', context)

    except SessionExamLine.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Session d\'examen non trouvée', 'status': 'error'}, status=404)
        else:
            return JsonResponse({'error': 'Session d\'examen non trouvée'}, status=404)
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e), 'status': 'error'}, status=500)
        else:
            return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_groupe_deliberation_results_ajax(request):
    """
    AJAX view to get group deliberation results data
    """
    try:
        session_exam_line_id = request.GET.get('groupe_id')  # Using groupe_id but it's actually session exam line ID
        if not session_exam_line_id:
            return JsonResponse({'error': 'Session d\'examen ID manquant'}, status=400)

        session_exam_line = SessionExamLine.objects.get(id=session_exam_line_id)
        groupe = session_exam_line.groupe  # Get the associated group

        # Get all exam planifications for this session exam line
        exam_planifications = ExamPlanification.objects.filter(
            exam_line=session_exam_line
        ).select_related('module', 'exam_line__session', 'pv').order_by('module__id', 'type_examen')

        # Get all students in the group through GroupeLine
        groupe_lines = GroupeLine.objects.filter(groupe=groupe).select_related('student')
        students = [groupe_line.student for groupe_line in groupe_lines]

        # Group exam planifications by module
        modules_dict = {}
        for exam_plan in exam_planifications:
            module_id = exam_plan.module.id
            if module_id not in modules_dict:
                modules_dict[module_id] = {
                    'module': exam_plan.module,
                    'normal_exam': None,
                    'rachat_exam': None,
                    'rattrapage_exam': None,
                    'normal_note_count': 0,
                    'rachat_note_count': 0,
                    'rattrapage_note_count': 0
                }

            if exam_plan.type_examen == 'normal':
                modules_dict[module_id]['normal_exam'] = exam_plan
                # Count the number of note types for this exam
                modules_dict[module_id]['normal_note_count'] = exam_plan.pv.exam_types_notes.count()
            elif exam_plan.type_examen == 'rachat':
                modules_dict[module_id]['rachat_exam'] = exam_plan
                # Count the number of note types for this exam
                modules_dict[module_id]['rachat_note_count'] = exam_plan.pv.exam_types_notes.count()
            elif exam_plan.type_examen == 'rattrage':
                modules_dict[module_id]['rattrapage_exam'] = exam_plan
                # Count the number of note types for this exam
                modules_dict[module_id]['rattrapage_note_count'] = exam_plan.pv.exam_types_notes.count()

        # Convert to list for template
        grouped_modules = list(modules_dict.values())

        # Prepare data for JSON response
        results_data = []

        for student in students:
            student_data = {
                'id': student.id,
                'matricule': student.matricule,
                'nom': student.nom,
                'prenom': student.prenom,
                'results': []
            }

            for module_data in grouped_modules:
                result_entry = {
                    'module_id': module_data['module'].id,
                    'module_label': module_data['module'].libelle,
                    'normal_result': None,
                    'rachat_result': None,
                    'rattrapage_result': None
                }

                # Handle normal exam if exists
                if module_data['normal_exam']:
                    normal_exam_plan = module_data['normal_exam']
                    normal_decision = ExamDecisionEtudiant.objects.filter(
                        pv=normal_exam_plan.pv,
                        etudiant=student
                    ).first()

                    normal_notes = ExamNote.objects.filter(
                        pv=normal_exam_plan.pv,
                        etudiant=student
                    ).select_related('type_note')

                    # Calculate average note for normal exam
                    normal_avg_note = 0
                    if normal_notes.exists():
                        total_notes = 0
                        count_notes = 0
                        for note in normal_notes:
                            if note.valeur is not None:
                                total_notes += note.valeur
                                count_notes += 1
                        if count_notes > 0:
                            normal_avg_note = round(total_notes / count_notes, 2)

                    # Organize normal notes by type
                    normal_notes_by_type = {}
                    for note in normal_notes:
                        normal_notes_by_type[note.type_note.id] = note

                    # Create structured normal notes
                    normal_structured_notes = []
                    if normal_exam_plan.pv.exam_types_notes.exists():
                        for note_type in normal_exam_plan.pv.exam_types_notes.all():
                            note_value = normal_notes_by_type.get(note_type.id)
                            normal_structured_notes.append({
                                'type_note': note_type,
                                'note': note_value,
                                'valeur': note_value.valeur if note_value else '-'
                            })

                    result_entry['normal_result'] = {
                        'exam_plan_id': normal_exam_plan.id,
                        'date': normal_exam_plan.date.strftime('%Y-%m-%d') if normal_exam_plan.date else '',
                        'decision_statut': normal_decision.statut if normal_decision else '',
                        'decision_moyenne': normal_decision.moyenne if normal_decision else '',
                        'notes': [{'type': note.type_note.libelle, 'valeur': note.valeur, 'type_note_id': note.type_note.id} for note in normal_notes],
                        'structured_notes': normal_structured_notes,
                        'avg_note': normal_avg_note
                    }

                # Handle rachat exam if exists
                if module_data['rachat_exam']:
                    rachat_exam_plan = module_data['rachat_exam']
                    rachat_decision = ExamDecisionEtudiant.objects.filter(
                        pv=rachat_exam_plan.pv,
                        etudiant=student
                    ).first()

                    rachat_notes = ExamNote.objects.filter(
                        pv=rachat_exam_plan.pv,
                        etudiant=student
                    ).select_related('type_note')

                    # Calculate average note for rachat exam
                    rachat_avg_note = 0
                    if rachat_notes.exists():
                        total_notes = 0
                        count_notes = 0
                        for note in rachat_notes:
                            if note.valeur is not None:
                                total_notes += note.valeur
                                count_notes += 1
                        if count_notes > 0:
                            rachat_avg_note = round(total_notes / count_notes, 2)

                    # Organize rachat notes by type
                    rachat_notes_by_type = {}
                    for note in rachat_notes:
                        rachat_notes_by_type[note.type_note.id] = note

                    # Create structured rachat notes
                    rachat_structured_notes = []
                    if rachat_exam_plan.pv.exam_types_notes.exists():
                        for note_type in rachat_exam_plan.pv.exam_types_notes.all():
                            note_value = rachat_notes_by_type.get(note_type.id)
                            rachat_structured_notes.append({
                                'type_note': note_type,
                                'note': note_value,
                                'valeur': note_value.valeur if note_value else '-'
                            })

                    result_entry['rachat_result'] = {
                        'exam_plan_id': rachat_exam_plan.id,
                        'date': rachat_exam_plan.date.strftime('%Y-%m-%d') if rachat_exam_plan.date else '',
                        'decision_statut': rachat_decision.statut if rachat_decision else '',
                        'decision_moyenne': rachat_decision.moyenne if rachat_decision else '',
                        'notes': [{'type': note.type_note.libelle, 'valeur': note.valeur, 'type_note_id': note.type_note.id} for note in rachat_notes],
                        'structured_notes': rachat_structured_notes,
                        'avg_note': rachat_avg_note
                    }

                # Handle rattrapage exam if exists
                if module_data['rattrapage_exam']:
                    rattrapage_exam_plan = module_data['rattrapage_exam']
                    rattrapage_decision = ExamDecisionEtudiant.objects.filter(
                        pv=rattrapage_exam_plan.pv,
                        etudiant=student
                    ).first()

                    rattrapage_notes = ExamNote.objects.filter(
                        pv=rattrapage_exam_plan.pv,
                        etudiant=student
                    ).select_related('type_note')

                    # Calculate average note for rattrapage exam
                    rattrapage_avg_note = 0
                    if rattrapage_notes.exists():
                        total_notes = 0
                        count_notes = 0
                        for note in rattrapage_notes:
                            if note.valeur is not None:
                                total_notes += note.valeur
                                count_notes += 1
                        if count_notes > 0:
                            rattrapage_avg_note = round(total_notes / count_notes, 2)

                    # Organize rattrapage notes by type
                    rattrapage_notes_by_type = {}
                    for note in rattrapage_notes:
                        rattrapage_notes_by_type[note.type_note.id] = note

                    # Create structured rattrapage notes
                    rattrapage_structured_notes = []
                    if rattrapage_exam_plan.pv.exam_types_notes.exists():
                        for note_type in rattrapage_exam_plan.pv.exam_types_notes.all():
                            note_value = rattrapage_notes_by_type.get(note_type.id)
                            rattrapage_structured_notes.append({
                                'type_note': note_type,
                                'note': note_value,
                                'valeur': note_value.valeur if note_value else '-'
                            })

                    result_entry['rattrapage_result'] = {
                        'exam_plan_id': rattrapage_exam_plan.id,
                        'date': rattrapage_exam_plan.date.strftime('%Y-%m-%d') if rattrapage_exam_plan.date else '',
                        'decision_statut': rattrapage_decision.statut if rattrapage_decision else '',
                        'decision_moyenne': rattrapage_decision.moyenne if rattrapage_decision else '',
                        'notes': [{'type': note.type_note.libelle, 'valeur': note.valeur, 'type_note_id': note.type_note.id} for note in rattrapage_notes],
                        'structured_notes': rattrapage_structured_notes,
                        'avg_note': rattrapage_avg_note
                    }

                student_data['results'].append(result_entry)

            results_data.append(student_data)

        # Check if there are any rachat or rattrapage exams
        has_rachat = any(module_data['rachat_exam'] for module_data in grouped_modules)
        has_rattrapage = any(module_data['rattrapage_exam'] for module_data in grouped_modules)

        response_data = {
            'status': 'success',
            'groupe': {
                'id': groupe.id,
                'code': groupe.code,
                'label': groupe.libelle
            },
            'session_exam_line': {
                'id': session_exam_line.id,
            },
            'has_rachat': has_rachat,
            'has_rattrapage': has_rattrapage,
            'results_data': results_data,
            'exam_planifications': [
                {
                    'id': ep.id,
                    'module_label': ep.module.libelle if ep.module else '',
                    'date': ep.date.strftime('%Y-%m-%d') if ep.date else ''
                }
                for ep in exam_planifications
            ]
        }

        return JsonResponse(response_data)

    except SessionExamLine.DoesNotExist:
        return JsonResponse({'error': 'Session d\'examen non trouvée'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)