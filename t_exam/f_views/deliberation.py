from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from t_exam.models import SessionExam, SessionExamLine, ExamPlanification, PvExamen, ExamTypeNote, ExamNote, ExamSousNote, ExamDecisionEtudiant, NoteBloc
from t_groupe.models import Groupe, GroupeLine
from t_etudiants.models import Prospets
from t_formations.models import Modules
from django.db.models import Prefetch


@login_required(login_url="institut_app:login")
def groupe_deliberation_results_view(request, pk):

    session_line = get_object_or_404(SessionExamLine, id=pk)
    groupe = session_line.groupe

    # Get all exam planifications for this session line
    exam_planifications = ExamPlanification.objects.filter(
        exam_line=session_line
    ).select_related('module', 'pv')

    # Get all PVs for these exam planifications
    pvs = PvExamen.objects.filter(
        exam_planification__in=exam_planifications
    ).select_related('exam_planification__module').prefetch_related(
        'exam_types_notes__bloc',  # Get the bloc with in_pv_deliberation field
        'notes__etudiant',
        'notes__type_note',
        'notes__sous_notes',
        'decisions__etudiant'
    )

    # Get all students in the group
    groupe_lines = GroupeLine.objects.filter(groupe=groupe).select_related('student')
    etudiants = [gl.student for gl in groupe_lines]

    # Group PVs by module
    modules_data = {}
    for pv in pvs:
        module = pv.exam_planification.module
        if module.id not in modules_data:
            modules_data[module.id] = {
                'module': module,
                'pvs': [],
                'all_exam_types_notes': [],
                'all_notes': [],
                'all_decisions': []
            }
        modules_data[module.id]['pvs'].append(pv)

    # Process each module to combine data from all its PVs
    pv_data = []
    for module_id, module_info in modules_data.items():
        module = module_info['module']
        pvs_list = module_info['pvs']

        # Collect all exam types notes from all PVs for this module
        exam_types_notes_dict = {}  # Use dict to avoid duplicates by code
        all_notes = []
        all_decisions = []

        for pv in pvs_list:
            # Get exam types notes that should appear in PV deliberation
            exam_types_notes = pv.exam_types_notes.filter(
                bloc__in=NoteBloc.objects.filter(in_pv_deliberation=True)
            ).order_by('ordre')

            for etn in exam_types_notes:
                if etn.code not in exam_types_notes_dict:
                    exam_types_notes_dict[etn.code] = etn

            # Get all notes for these exam types
            notes = pv.notes.filter(
                type_note__in=exam_types_notes
            ).select_related('etudiant', 'type_note').prefetch_related('sous_notes')
            all_notes.extend(notes)

            # Get decisions for this PV
            decisions = pv.decisions.all().select_related('etudiant')
            all_decisions.extend(decisions)

        # Convert exam_types_notes_dict to ordered list
        exam_types_notes_list = sorted(exam_types_notes_dict.values(), key=lambda x: x.ordre)

        # Organize notes by student and type for easier access in template
        notes_by_student = {}
        for note in all_notes:
            student_id = note.etudiant.id
            type_note_code = note.type_note.code
            if student_id not in notes_by_student:
                notes_by_student[student_id] = {}
            
            # If there are multiple notes for same student and type (from different PVs),
            # we keep the latest or combine them based on your business logic
            if type_note_code not in notes_by_student[student_id]:
                notes_by_student[student_id][type_note_code] = []
            notes_by_student[student_id][type_note_code].append(note)

        # Organize decisions by student for easier access in template
        decisions_by_student = {}
        for decision in all_decisions:
            student_id = decision.etudiant.id
            # If student already has a decision, keep the one with non-zero moyenne
            # or the one with the highest moyenne (for rachat/rattrapage)
            if student_id in decisions_by_student:
                existing_decision = decisions_by_student[student_id]
                # Prioritize non-zero moyenne, or take the higher one
                if decision.moyenne and decision.moyenne > 0:
                    if not existing_decision.moyenne or existing_decision.moyenne == 0:
                        decisions_by_student[student_id] = decision
                    elif decision.moyenne > existing_decision.moyenne:
                        decisions_by_student[student_id] = decision
            else:
                decisions_by_student[decision.etudiant.id] = decision

        pv_data.append({
            'module': module,
            'pvs': pvs_list,
            'exam_types_notes': exam_types_notes_list,
            'notes': all_notes,
            'notes_by_student': notes_by_student,
            'decisions': all_decisions,
            'decisions_by_student': decisions_by_student
        })

    context = {
        'session_line': session_line,  # Pass the session line object
        'groupe': groupe,  # Pass the main group
        'etudiants': etudiants,
        'pv_data': pv_data,
    }

    return render(request, 'tenant_folder/exams/groupe_deliberation_results.html', context)

