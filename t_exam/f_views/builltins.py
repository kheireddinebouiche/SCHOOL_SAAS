from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import *
from ..forms import *
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from t_etudiants.models import *
from t_groupe.models import *
from t_formations.models import Promos
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q



@login_required(login_url="institut_app:login")
def PageListeSessionExam(request):
    return render(request, 'tenant_folder/exams/builltins/liste.html')


@login_required(login_url="institut_app:login")
def ApiListeDesGroupes(request):
    if request.method == "GET":
        
        groupes = (
            Groupe.objects
            .annotate(nb_etudiants=Count('groupe_line_groupe'))
        )

        groupe_data = []
        for i in groupes:
            groupe_data.append({
                'id' : i.id,
                'nom' : i.nom,
                'code' : i.code_partenaire if i.code_partenaire else 'N/A',
                'created_at' : i.date_creation,
                'anness_scolaire' : i.annee_scolaire,
                'nb_etudiants': i.nb_etudiants,
            })
        return JsonResponse(groupe_data, safe=False)
    else:
        return JsonResponse({"status":"error"})
    
@login_required(login_url="institut_app:login")
def ApiListeGroupeSession(request):
    if request.method == "GET":
        id_groupe = request.GET.get('id')

        if not id_groupe:
            return JsonResponse({"status" : "error",'message':"Informations manquantes"})
        
        sessions = SessionExamLine.objects.filter(groupe_id = id_groupe)

        data = []
        for i in sessions:
            data.append({
                'id' : i.id,
                'semestre' : i.semestre,
                'date_debut' : i.date_debut,
                'date_fin' : i.date_fin,
                'created_at' : i.created_at,
            })
        return JsonResponse(data, safe=False)

    else:
        return JsonResponse({"status":"error"})
    

@login_required(login_url="institut_app:login")
def ListeDesEtudiants(request, pk):
    try:
        # Get the session exam line using the pk parameter
        session_exam_line = SessionExamLine.objects.get(id=pk)

        # Get the group associated with this session
        groupe = session_exam_line.groupe

        # Get all students in this group through GroupeLine along with their inscription dates
        groupe_lines = GroupeLine.objects.filter(groupe=groupe).select_related('student')

        # Prepare student data with inscription date
        student_data = []
        for groupe_line in groupe_lines:
            student_info = {
                'student': groupe_line.student,
                'date_inscription': groupe_line.date_inscription
            }
            student_data.append(student_info)

        context = {
            'student_data': student_data,
            'session_exam_line': session_exam_line,
            'groupe': groupe,
        }

    except SessionExamLine.DoesNotExist:
        # Handle case where session exam line doesn't exist
        context = {
            'student_data': [],
            'session_exam_line': None,
            'groupe': None,
        }

    return render(request, 'tenant_folder/exams/builltins/liste_des_etudiants.html', context)


@login_required(login_url="institut_app:login")
def StudentBulletin(request, session_line_id, student_id):
    """
    Display the bulletin (relevé de notes) for a specific student in a session
    """
    try:
        # Get the session exam line
        session_line = SessionExamLine.objects.get(id=session_line_id)
        
        # Get the student
        student = Prospets.objects.get(id=student_id)
        
        # Get all exam planifications for this session line
        exam_planifications = ExamPlanification.objects.filter(
            exam_line=session_line
        ).select_related('module', 'pv')
        
        # Get all PVs with related data
        pvs = PvExamen.objects.filter(
            exam_planification__in=exam_planifications
        ).select_related('exam_planification__module', 'exam_planification').prefetch_related(
            'exam_types_notes__bloc',
            'notes__type_note',
            'notes__sous_notes',
            'decisions'
        )
        
        # Group PVs by module (like in deliberation.py)
        modules_dict = {}
        for pv in pvs:
            module = pv.exam_planification.module
            if module.id not in modules_dict:
                modules_dict[module.id] = {
                    'module': module,
                    'pvs': [],
                }
            modules_dict[module.id]['pvs'].append(pv)
        
        # Get all types of notes that should appear in bulletin
        # We'll collect all unique note types across all PVs
        all_note_types = set()
        for pv in pvs:
            exam_types = pv.exam_types_notes.filter(
                bloc__in=NoteBloc.objects.filter(Q(in_pv_deliberation=True) | Q(in_builltin_note=True))
            ).order_by('ordre')
            for et in exam_types:
                bloc_ordre = et.bloc.ordre if et.bloc else 0
                bloc_label = et.bloc.label if et.bloc else ""
                all_note_types.add((et.code, et.libelle, et.ordre, bloc_ordre, bloc_label))
        
        # Sort note types by bloc ordre then note type ordre
        sorted_note_types = sorted(list(all_note_types), key=lambda x: (x[3], x[2]))
        
        note_types_list = [{'code': code, 'libelle': libelle, 'bloc_label': bloc_label} for code, libelle, ordre, bloc_ordre, bloc_label in sorted_note_types]
        
        # Organize data by module
        modules_data = []
        total_points = 0
        total_coef = 0
        
        # Process each module and combine data from all its PVs
        for module_id, module_info in modules_dict.items():
            module = module_info['module']
            pvs_list = module_info['pvs']
            
            # Collect all notes from all PVs for this module
            all_notes_for_module = []
            all_decisions_for_module = []
            
            for pv in pvs_list:
                # Get exam types notes that should appear in bulletin
                exam_types_notes = pv.exam_types_notes.filter(
                    bloc__in=NoteBloc.objects.filter(Q(in_pv_deliberation=True) | Q(in_builltin_note=True))
                ).order_by('ordre')
                
                # Get notes for this student from this PV
                notes = pv.notes.filter(
                    etudiant=student,
                    type_note__in=exam_types_notes
                ).select_related('type_note').prefetch_related('sous_notes')
                all_notes_for_module.extend(notes)
                
                # Get decisions for this student from this PV
                try:
                    decision = pv.decisions.get(etudiant=student)
                    all_decisions_for_module.append(decision)
                except ExamDecisionEtudiant.DoesNotExist:
                    pass
            
            # Organize notes by type code
            notes_by_type = {}
            for note in all_notes_for_module:
                # If there are multiple notes for the same type (from different PVs),
                # we keep the latest one with non-zero value
                if note.type_note.code not in notes_by_type:
                    notes_by_type[note.type_note.code] = note
                elif note.valeur and note.valeur > 0:
                    # Prioritize non-zero values
                    if not notes_by_type[note.type_note.code].valeur or notes_by_type[note.type_note.code].valeur == 0:
                        notes_by_type[note.type_note.code] = note
            
            # Get the best decision (prioritize non-zero moyenne)
            best_decision = None
            for decision in all_decisions_for_module:
                if not best_decision:
                    best_decision = decision
                elif decision.moyenne and decision.moyenne > 0:
                    if not best_decision.moyenne or best_decision.moyenne == 0:
                        best_decision = decision
                    elif decision.moyenne > best_decision.moyenne:
                        best_decision = decision
            
            # Calculate Moy x Coef for this module
            coef = module.coef if module.coef else 1
            moy_coef = 0
            if best_decision and best_decision.moyenne:
                moy_coef = best_decision.moyenne * coef
                total_points += moy_coef
                total_coef += coef
            
            modules_data.append({
                'module': module,
                'notes_by_type': notes_by_type,
                'decision': best_decision,
                'moy_coef': round(moy_coef, 2)
            })
        
        # Calculate semester average
        moyenne_semestre = round(total_points / total_coef, 2) if total_coef > 0 else 0
        
        context = {
            'student': student,
            'session_line': session_line,
            'groupe': session_line.groupe,
            'modules_data': modules_data,
            'note_types_list': note_types_list,
            'moyenne_semestre': moyenne_semestre,
            'total_coef': total_coef,
            'total_points': round(total_points, 2)
        }
        
    except (SessionExamLine.DoesNotExist, Prospets.DoesNotExist):
        context = {
            'student': None,
            'session_line': None,
            'groupe': None,
            'modules_data': [],
        }
    
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    context['is_ajax'] = is_ajax
    context['base_template'] = 'tenant_folder/base_ajax.html' if is_ajax else 'tenant_folder/base.html'
    return render(request, 'tenant_folder/exams/builltins/student_bulletin.html', context)


