from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from t_exam.models import SessionExam, SessionExamLine, ExamPlanification, PvExamen, ExamTypeNote, ExamNote, ExamDecisionEtudiant
from t_groupe.models import Groupe, GroupeLine
from t_etudiants.models import Prospets
from t_formations.models import Modules
from django.db.models import Prefetch


@login_required(login_url="institut_app:login")
def groupe_deliberation_results_view(request, pk):
    """
    Display results for all students in all modules for a specific session exam
    """
    session_exam = get_object_or_404(SessionExam, id=pk)

    # Get all session exam lines for this session
    session_lines = SessionExamLine.objects.filter(session=session_exam).select_related(
        'groupe'
    ).prefetch_related(
        'exam_planification__module'
    )
    
    # Get all PVs related to exam plans in this session
    exam_plan_ids = []
    for line in session_lines:
        for exam_plan in line.exam_planification.all():
            exam_plan_ids.append(exam_plan.id)
    
    # Prefetch PV data separately
    pv_data = PvExamen.objects.filter(
        exam_planification__in=exam_plan_ids
    ).select_related(
        'exam_planification__module'
    ).prefetch_related(
        'exam_types_notes',
        'notes__type_note',
        'decisions__etudiant'
    )

    # Get all groups and students involved in this session
    groupes = []
    all_students = set()
    groupe_students = {}

    for line in session_lines:
        if line.groupe not in groupes:
            groupes.append(line.groupe)
            # Get students from GroupeLine model
            groupe_lines = GroupeLine.objects.filter(groupe=line.groupe).select_related('student')
            students = []
            for gline in groupe_lines:
                # Create a student object with group information
                student_obj = gline.student
                # Temporarily attach the group to the student for template use
                student_obj.groupe = gline.groupe
                students.append(student_obj)
                all_students.add(student_obj)
            groupe_students[line.groupe.id] = students

    # Get all modules for this session
    all_modules = set()
    for line in session_lines:
        for exam_plan in line.exam_planification.all():
            if exam_plan.module:
                all_modules.add(exam_plan.module)

    # Prepare data structure for template
    results_data = []
    grouped_modules = []

    # Group modules by exam type (normal, rachat, rattrapage)
    for module in all_modules:
        module_data = {
            'module': module,
            'normal_exam': None,
            'rachat_exam': None,
            'rattrapage_exam': None,
            'normal_note_count': 0,
            'rachat_note_count': 0,
            'rattrapage_note_count': 0
        }

        # Find exam plans for this module by type
        for line in session_lines:
            for exam_plan in line.exam_planification.all():
                if exam_plan.module and exam_plan.module.id == module.id:
                    if exam_plan.type_examen == 'rachat':
                        module_data['rachat_exam'] = exam_plan
                        # Check if there's a PV for this exam plan
                        pv_for_plan = pv_data.filter(exam_planification=exam_plan).first()
                        if pv_for_plan:
                            # Count only notes that are allowed in PV deliberation
                            all_types = pv_for_plan.exam_types_notes.all()
                            filtered_types = [note_type for note_type in all_types if note_type.bloc and note_type.bloc.in_pv_deliberation]
                            module_data['rachat_note_count'] = len(filtered_types)
                    elif exam_plan.type_examen == 'rattrage':  # rattrapage
                        module_data['rattrapage_exam'] = exam_plan
                        # Check if there's a PV for this exam plan
                        pv_for_plan = pv_data.filter(exam_planification=exam_plan).first()
                        if pv_for_plan:
                            # Count only notes that are allowed in PV deliberation
                            all_types = pv_for_plan.exam_types_notes.all()
                            filtered_types = [note_type for note_type in all_types if note_type.bloc and note_type.bloc.in_pv_deliberation]
                            module_data['rattrapage_note_count'] = len(filtered_types)
                    else:  # normal
                        module_data['normal_exam'] = exam_plan
                        # Check if there's a PV for this exam plan
                        pv_for_plan = pv_data.filter(exam_planification=exam_plan).first()
                        if pv_for_plan:
                            # Count only notes that are allowed in PV deliberation
                            all_types = pv_for_plan.exam_types_notes.all()
                            filtered_types = [note_type for note_type in all_types if note_type.bloc and note_type.bloc.in_pv_deliberation]
                            module_data['normal_note_count'] = len(filtered_types)

        grouped_modules.append(module_data)

    # Prepare student results
    for student in all_students:
        student_result = {
            'student': student,
            'results': []
        }

        for module_data in grouped_modules:
            result = {
                'module': module_data['module'],
                'normal_result': None,
                'rachat_result': None,
                'rattrapage_result': None
            }

            # Get normal exam result
            if module_data['normal_exam']:
                # Check if there's a PV for this exam plan
                pv = pv_data.filter(exam_planification=module_data['normal_exam']).first()
                if pv:
                    notes = pv.notes.filter(etudiant=student).select_related('type_note')
                    try:
                        decision = pv.decisions.get(etudiant=student)
                        decision_statut = decision.statut
                        avg_note = decision.moyenne or 0
                    except ExamDecisionEtudiant.DoesNotExist:
                        decision_statut = None
                        avg_note = 0

                    # Filter notes based on bloc's in_pv_deliberation setting
                    filtered_notes = [note for note in notes if note.type_note.bloc and note.type_note.bloc.in_pv_deliberation]

                    result['normal_result'] = {
                        'exam_plan': module_data['normal_exam'],
                        'structured_notes': filtered_notes,
                        'decision_statut': decision_statut,
                        'avg_note': avg_note,
                        'pv': pv
                    }

            # Get rachat exam result
            if module_data['rachat_exam']:
                # Check if there's a PV for this exam plan
                pv = pv_data.filter(exam_planification=module_data['rachat_exam']).first()
                if pv:
                    notes = pv.notes.filter(etudiant=student).select_related('type_note')
                    try:
                        decision = pv.decisions.get(etudiant=student)
                        decision_statut = decision.statut
                        avg_note = decision.moyenne or 0
                    except ExamDecisionEtudiant.DoesNotExist:
                        decision_statut = None
                        avg_note = 0

                    # Filter notes based on bloc's in_pv_deliberation setting
                    filtered_notes = [note for note in notes if note.type_note.bloc and note.type_note.bloc.in_pv_deliberation]

                    result['rachat_result'] = {
                        'exam_plan': module_data['rachat_exam'],
                        'structured_notes': filtered_notes,
                        'decision_statut': decision_statut,
                        'avg_note': avg_note,
                        'pv': pv
                    }

            # Get rattrapage exam result
            if module_data['rattrapage_exam']:
                # Check if there's a PV for this exam plan
                pv = pv_data.filter(exam_planification=module_data['rattrapage_exam']).first()
                if pv:
                    notes = pv.notes.filter(etudiant=student).select_related('type_note')
                    try:
                        decision = pv.decisions.get(etudiant=student)
                        decision_statut = decision.statut
                        avg_note = decision.moyenne or 0
                    except ExamDecisionEtudiant.DoesNotExist:
                        decision_statut = None
                        avg_note = 0

                    # Filter notes based on bloc's in_pv_deliberation setting
                    filtered_notes = [note for note in notes if note.type_note.bloc and note.type_note.bloc.in_pv_deliberation]

                    result['rattrapage_result'] = {
                        'exam_plan': module_data['rattrapage_exam'],
                        'structured_notes': filtered_notes,
                        'decision_statut': decision_statut,
                        'avg_note': avg_note,
                        'pv': pv
                    }

            student_result['results'].append(result)

        results_data.append(student_result)

    # Determine if we need to show rachat or rattrapage tables
    has_rachat = any(mod_data['rachat_exam'] for mod_data in grouped_modules)
    has_rattrapage = any(mod_data['rattrapage_exam'] for mod_data in grouped_modules)

    context = {
        'session_exam': session_exam,
        'groupes': groupes,
        'results_data': results_data,
        'grouped_modules': grouped_modules,
        'has_rachat': has_rachat,
        'has_rattrapage': has_rattrapage,
        'groupe': groupes[0] if groupes else None  # For template compatibility
    }

    return render(request, 'tenant_folder/exams/groupe_deliberation_results.html', context)