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
    ).prefetch_related(
        'exam_types_notes__bloc',  # Get the bloc with in_pv_deliberation field
        'notes__etudiant',
        'notes__type_note',
        'notes__sous_notes',
        'decisions__etudiant'
    )

    # Get all students in the group
    groupe_lines = GroupeLine.objects.filter(groupe=groupe).select_related('student')
    etudiants = [gl.student for gl in groupe_lines]

    # Prepare data structure for the template
    pv_data = []
    for pv in pvs:
        # Get exam types notes that should appear in PV deliberation (where bloc.in_pv_deliberation is True)
        exam_types_notes = pv.exam_types_notes.filter(
            bloc__in=NoteBloc.objects.filter(in_pv_deliberation=True)
        ).order_by('ordre')

        # Get all notes for these exam types
        notes = pv.notes.filter(
            type_note__in=exam_types_notes
        ).select_related('etudiant', 'type_note').prefetch_related('sous_notes')

        # Get decisions for this PV
        decisions = pv.decisions.all().select_related('etudiant')

        # Organize notes by student and type for easier access in template
        notes_by_student = {}
        for note in notes:
            student_id = note.etudiant.id
            if student_id not in notes_by_student:
                notes_by_student[student_id] = {}
            notes_by_student[student_id][note.type_note.id] = note

        # Organize decisions by student for easier access in template
        decisions_by_student = {}
        for decision in decisions:
            decisions_by_student[decision.etudiant.id] = decision

        pv_data.append({
            'pv': pv,
            'exam_types_notes': exam_types_notes,
            'notes': notes,
            'notes_by_student': notes_by_student,
            'decisions': decisions,
            'decisions_by_student': decisions_by_student
        })

    context = {
        'session_line': session_line,  # Pass the session line object
        'groupe': groupe,  # Pass the main group
        'etudiants': etudiants,
        'pv_data': pv_data,
    }

    return render(request, 'tenant_folder/exams/groupe_deliberation_results.html', context)

