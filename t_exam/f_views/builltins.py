from institut_app.decorators import module_permission_required
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
@module_permission_required('exa', 'view')
def PageListeSessionExam(request):
    return render(request, 'tenant_folder/exams/builltins/liste.html')


@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'view')
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
@module_permission_required('exa', 'view')
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
@module_permission_required('exa', 'view')
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
@module_permission_required('exa', 'view')
def StudentBulletin(request, session_line_id, student_id):
    """
    Display the bulletin (relevé de notes) for a specific student in a session
    """
    try:
        # Get the session exam line
        session_line = SessionExamLine.objects.get(id=session_line_id)
        
        # Get the student
        student = Prospets.objects.get(id=student_id)
        
        # Get all session lines for this group and semester to compile complete results
        session_lines = SessionExamLine.objects.filter(
            groupe=session_line.groupe,
            semestre=session_line.semestre
        )
        
        # Get all exam planifications for these session lines
        exam_planifications = ExamPlanification.objects.filter(
            exam_line__in=session_lines
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
        
        # Cache NoteBloc IDs for the bulletin to avoid database hits in loops
        bulletin_bloc_ids = set(NoteBloc.objects.filter(
            Q(in_pv_deliberation=True) | Q(in_builltin_note=True)
        ).values_list('id', flat=True))
        
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
            exam_types = [
                et for et in pv.exam_types_notes.all()
                if et.bloc_id in bulletin_bloc_ids
            ]
            exam_types.sort(key=lambda x: x.ordre)
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
                # Get exam types notes that should appear in bulletin using prefetched cache
                exam_types_notes = [
                    etn for etn in pv.exam_types_notes.all()
                    if etn.bloc_id in bulletin_bloc_ids
                ]
                exam_types_notes_set = set(exam_types_notes)
                
                # Get notes for this student from this PV using prefetched cache
                notes = [
                    n for n in pv.notes.all()
                    if n.etudiant_id == student.id and n.type_note in exam_types_notes_set
                ]
                all_notes_for_module.extend(notes)
                
                # Get decisions for this student from this PV using prefetched cache
                decision = next((d for d in pv.decisions.all() if d.etudiant_id == student.id), None)
                if decision:
                    all_decisions_for_module.append(decision)
            
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

        # Get saved deliberation decision and observation for this student in this session line
        deliberation = DeliberationEtudiant.objects.filter(
            session_line=session_line,
            etudiant=student
        ).first()
        
        context = {
            'student': student,
            'session_line': session_line,
            'groupe': session_line.groupe,
            'modules_data': modules_data,
            'note_types_list': note_types_list,
            'moyenne_semestre': moyenne_semestre,
            'total_coef': total_coef,
            'total_points': round(total_points, 2),
            'deliberation': deliberation,
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




@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'view')
def PrintBulletinPDF(request, session_line_id, student_id):
    from pdf_editor.models import DocumentTemplate
    from pdf_editor.utils import render_template_with_context
    from django.utils import timezone
    from django.http import HttpResponse

    try:
        session_line = SessionExamLine.objects.get(id=session_line_id)
        student = Prospets.objects.get(id=student_id)
        
        session_lines = SessionExamLine.objects.filter(groupe=session_line.groupe, semestre=session_line.semestre)
        exam_planifications = ExamPlanification.objects.filter(exam_line__in=session_lines).select_related('module', 'pv')
        
        pvs = PvExamen.objects.filter(exam_planification__in=exam_planifications).select_related('exam_planification__module', 'exam_planification').prefetch_related(
            'exam_types_notes__bloc',
            'notes__type_note',
            'notes__sous_notes',
            'decisions'
        )
        
        bulletin_bloc_ids = set(NoteBloc.objects.filter(Q(in_pv_deliberation=True) | Q(in_builltin_note=True)).values_list('id', flat=True))
        
        modules_dict = {}
        for pv in pvs:
            module = pv.exam_planification.module
            if module.id not in modules_dict:
                modules_dict[module.id] = {'module': module, 'pvs': []}
            modules_dict[module.id]['pvs'].append(pv)
            
        all_note_types = set()
        for pv in pvs:
            exam_types = [et for et in pv.exam_types_notes.all() if et.bloc_id in bulletin_bloc_ids]
            exam_types.sort(key=lambda x: x.ordre)
            for et in exam_types:
                bloc_ordre = et.bloc.ordre if et.bloc else 0
                bloc_label = et.bloc.label if et.bloc else ""
                all_note_types.add((et.code, et.libelle, et.ordre, bloc_ordre, bloc_label))
        
        sorted_note_types = sorted(list(all_note_types), key=lambda x: (x[3], x[2]))
        note_types_list = [{'code': code, 'libelle': libelle, 'bloc_label': bloc_label} for code, libelle, ordre, bloc_ordre, bloc_label in sorted_note_types]
        
        modules_data = []
        total_points = 0
        total_coef = 0
        
        for module_id, module_info in modules_dict.items():
            module = module_info['module']
            pvs_list = module_info['pvs']
            all_notes_for_module = []
            all_decisions_for_module = []
            for pv in pvs_list:
                exam_types_notes = [etn for etn in pv.exam_types_notes.all() if etn.bloc_id in bulletin_bloc_ids]
                exam_types_notes_set = set(exam_types_notes)
                notes = [n for n in pv.notes.all() if n.etudiant_id == student.id and n.type_note in exam_types_notes_set]
                all_notes_for_module.extend(notes)
                decision = next((d for d in pv.decisions.all() if d.etudiant_id == student.id), None)
                if decision:
                    all_decisions_for_module.append(decision)
            
            notes_by_type = {}
            for note in all_notes_for_module:
                if note.type_note.code not in notes_by_type:
                    notes_by_type[note.type_note.code] = note
                elif note.valeur and note.valeur > 0:
                    if not notes_by_type[note.type_note.code].valeur or notes_by_type[note.type_note.code].valeur == 0:
                        notes_by_type[note.type_note.code] = note
            
            best_decision = None
            for decision in all_decisions_for_module:
                if not best_decision:
                    best_decision = decision
                elif decision.moyenne and decision.moyenne > 0:
                    if not best_decision.moyenne or best_decision.moyenne == 0:
                        best_decision = decision
                    elif decision.moyenne > best_decision.moyenne:
                        best_decision = decision
            
            coef = module.coef if module.coef else 1
            moy_coef = 0
            if best_decision and best_decision.moyenne:
                moy_coef = best_decision.moyenne * coef
                total_points += moy_coef
                total_coef += coef
            
            modules_data.append({
                'module': module,
                'decision': best_decision,
                'moy_coef': round(moy_coef, 2),
                'notes_by_type': notes_by_type
            })
            
        moyenne_semestre = round(total_points / total_coef, 2) if total_coef > 0 else 0
        deliberation = DeliberationEtudiant.objects.filter(session_line=session_line, etudiant=student).first()

        context_data = {
            'date_impression': timezone.now().date().strftime("%d/%m/%Y"),
            'entreprise': {
                'designation': getattr(request.tenant, 'nom', 'Institut'),
                'adresse': getattr(request.tenant, 'adresse', ''),
            },
            'etudiant': {
                'nom': student.nom,
                'prenom': student.prenom,
                'matricule': student.matricule or '',
                'date_naissance': student.date_naissance.strftime("%d/%m/%Y") if student.date_naissance else '',
                'lieu_naissance': student.lieu_naissance or ''
            },
            'session_line': {
                'session': {'nom_session': session_line.session.label},
                'semestre': session_line.get_semestre_display() if hasattr(session_line, 'get_semestre_display') else session_line.semestre
            },
            'groupe': {'nom_groupe': session_line.groupe.nom if session_line.groupe else ''},
            'moyenne_semestre': str(moyenne_semestre),
            'total_points': str(round(total_points, 2)),
            'total_coef': str(total_coef),
            'deliberation': {
                'decision_jury': getattr(deliberation, 'decision_jury', ''),
                'observation': getattr(deliberation, 'observation', '')
            },
            'note_types_list': note_types_list,
            'modules_data': []
        }
        
        for m_data in modules_data:
            module = m_data['module']
            decision = m_data['decision']
            
            # Map notes directly to a list ordered by note_types_list so we don't need custom filters in the isolated Django Engine
            notes_list = []
            for nt in note_types_list:
                note_obj = m_data['notes_by_type'].get(nt['code'])
                if note_obj and note_obj.valeur is not None:
                    notes_list.append(str(round(note_obj.valeur, 2)))
                else:
                    notes_list.append('')
                    
            context_data['modules_data'].append({
                'module': {'code': getattr(module, 'code_interne', None) or getattr(module, 'code', '-'), 'label': getattr(module, 'label', '')},
                'matiere': getattr(module, 'label', ''),
                'professeur': '',
                'coef': module.coef or 1,
                'moyenne_matiere': str(round(decision.moyenne, 2)) if decision and getattr(decision, 'moyenne', None) else '0',
                'total_points': str(m_data['moy_coef']),
                'observation': getattr(decision, 'observation', '') if decision else '',
                'decision': {'statut': decision.statut if decision else '', 'moyenne': decision.moyenne if decision else 0},
                'notes_list': notes_list
            })

        # Update the HTML template to exactly match the modal
        html_content_default = """<style>
  @page { margin: 0.5cm; }
  :root {
    --primary-color: #000000;
    --accent-color: #000000;
    --light-bg: transparent;
    --border-color: #000000;
  }
  .bulletin-container {
    background: transparent;
    padding: 1.5rem;
    width: 100%;
    margin: 0 auto;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    box-sizing: border-box;
    font-size: 11px;
    color: #000;
  }
  .bulletin-header {
    border-bottom: 1pt solid #000;
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .bulletin-title {
    font-family: 'Georgia', serif;
    color: #000;
    font-size: 1.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 0.2rem 0;
  }
  .bulletin-subtitle {
    color: #000;
    font-size: 0.9rem;
    margin: 0;
  }
  .student-details { margin-bottom: 1.5rem; display: flex; gap: 15px; }
  .detail-col { flex: 1; }
  .academic-year {
    background-color: transparent;
    padding: 0.8rem;
    border: 0.5pt solid #000;
  }
  .detail-row {
    display: flex;
    margin-bottom: 0.3rem;
    align-items: baseline;
  }
  .detail-label {
    width: 90px;
    font-weight: 600;
    color: #000;
    text-transform: uppercase;
    font-size: 0.7rem;
    letter-spacing: 0.5px;
  }
  .detail-value {
    color: #000;
    font-weight: 500;
    font-size: 0.85rem;
  }
  .custom-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1.5rem;
  }
  .custom-table th {
    background-color: transparent !important;
    color: #000 !important;
    text-transform: uppercase;
    font-size: 0.6rem;
    letter-spacing: 0.2px;
    padding: 0.6rem 0.4rem;
    font-weight: 600;
    border: 0.5pt solid #000;
    text-align: center;
  }
  .custom-table th:nth-child(1) { text-align: left; }
  .custom-table th:nth-child(2) { text-align: left; }
  .custom-table td {
    padding: 0.6rem 0.4rem;
    border: 0.5pt solid #000;
    vertical-align: middle;
    color: #000;
    font-size: 0.7rem;
  }
  .module-code { font-family: 'Courier New', monospace; font-weight: 600; color: #000; font-size: 0.65rem; }
  .module-label { font-weight: 600; font-size: 0.7rem; }
  .note-cell { text-align: center; font-family: 'Consolas', monospace; font-weight: 500; font-size: 0.7rem; }
  .average-cell { background-color: transparent !important; font-weight: 700; color: #000; text-align: center; font-size: 0.75rem; }
  .total-row td { background-color: transparent !important; color: #000 !important; font-weight: 700; border: 0.5pt solid #000; font-size: 0.7rem;}
  
  .status-badge {
    padding: 0.2em 0.5em; font-size: 0.6em; font-weight: 600; border: 0.5pt solid #000; text-transform: uppercase; color: #000 !important; background-color: transparent !important;
  }
</style>

<div class="bulletin-container">
  <div class="bulletin-header">
    <div>
      <h1 class="bulletin-title">Bulletin de Notes</h1>
      <p class="bulletin-subtitle">Session: {{ session_line.session.nom_session|upper }}</p>
    </div>
    <div style="text-align: right;">
        <h2 style="margin:0; font-size: 1rem; color: #000;">{{ entreprise.designation }}</h2>
        <p style="margin:0; font-size: 0.75rem; color: #000;">{{ entreprise.adresse }}</p>
    </div>
  </div>

  <div class="student-details">
    <div class="detail-col">
      <div class="detail-row"><div class="detail-label">Étudiant</div><div class="detail-value text-uppercase" style="font-size:1rem;">{{ etudiant.nom }} {{ etudiant.prenom }}</div></div>
      <div class="detail-row"><div class="detail-label">Matricule</div><div class="detail-value">{{ etudiant.matricule }}</div></div>
      <div class="detail-row"><div class="detail-label">Date Nais.</div><div class="detail-value">{{ etudiant.date_naissance }}</div></div>
    </div>
    <div class="detail-col">
      <div class="academic-year">
        <div class="detail-row"><div class="detail-label">Formation</div><div class="detail-value">{{ groupe.nom_groupe }}</div></div>
        <div class="detail-row"><div class="detail-label">Semestre</div><div class="detail-value text-uppercase font-monospace">Semestre {{ session_line.semestre }}</div></div>
        <div class="detail-row"><div class="detail-label">Édité le</div><div class="detail-value">{{ date_impression }}</div></div>
      </div>
    </div>
  </div>

  <table class="custom-table">
    <thead>
      <tr>
        <th>Code</th>
        <th>Unité d'Enseignement</th>
        {% for note_type in note_types_list %}
        <th>
          {{ note_type.libelle }}
        </th>
        {% endfor %}
        <th>Moy./20</th>
        <th>Coef.</th>
        <th>Total</th>
        <th>Décision</th>
      </tr>
    </thead>
    <tbody>
      {% for module_item in modules_data %}
      <tr>
        <td class="module-code">{{ module_item.module.code }}</td>
        <td class="module-label">{{ module_item.module.label }}</td>
        
        {% for note in module_item.notes_list %}
          <td class="note-cell">
              {% if note != '' %}
                {{ note }}
              {% else %}
                <span style="color:#adb5bd;">-</span>
              {% endif %}
          </td>
        {% endfor %}
        
        <td class="note-cell average-cell">{{ module_item.moyenne_matiere }}</td>
        <td class="note-cell">{{ module_item.coef }}</td>
        <td class="note-cell average-cell">{{ module_item.total_points }}</td>
        <td class="text-center">
            {% if module_item.decision.statut == 'valide' %}
              <span class="status-badge status-success">Admis</span>
            {% elif module_item.decision.statut == 'rattrapage' %}
              <span class="status-badge status-warning">Rattrapage</span>
            {% elif module_item.decision.statut == 'rach' %}
              <span class="status-badge status-info">Rachat</span>
            {% elif module_item.decision.statut == 'ajou' %}
              <span class="status-badge status-danger">Ajourné</span>
            {% else %}
              <span style="color:#adb5bd; font-size:0.7rem;">-</span>
            {% endif %}
        </td>
      </tr>
      {% endfor %}
      
      <tr class="total-row">
        <td colspan="{{ note_types_list|length|add:2 }}" style="text-align:right; text-transform:uppercase; padding-right: 1.5rem;">
          Moyenne Générale du Semestre
        </td>
        <td class="text-center" style="font-size: 0.8rem;">{{ moyenne_semestre }}</td>
        <td class="text-center">
          <div style="font-size: 0.5rem; opacity: 0.8;">COEF TOTAL</div>
          <span style="font-size: 0.75rem;">{{ total_coef }}</span>
        </td>
        <td colspan="2" class="text-center" style="font-size: 0.8rem;">
          <div style="font-size: 0.5rem; opacity: 0.8; font-weight: normal;">TOTAL POINTS</div>
          {{ total_points }}
        </td>
      </tr>
    </tbody>
  </table>

  {% if deliberation %}
  <div style="display:flex; gap: 15px; margin-top: 1.5rem; border-top: 0.5pt solid #000; padding-top: 1rem;">
    <div style="flex:1; background-color: transparent; padding: 10px; border: 0.5pt solid #000;">
      <h6 style="text-transform: uppercase; font-weight: bold; color: #000; font-size: 0.65rem; margin: 0 0 5px 0;">Décision du Jury</h6>
      <div style="font-size: 1rem; font-weight: 600; color: #000;">
        {% if deliberation.decision_jury == 'valide' %}Semestre validé
        {% elif deliberation.decision_jury == 'valide_dette' %}Semestre validé avec dette
        {% elif deliberation.decision_jury == 'non_valide' %}Semestre non validé
        {% else %}<span style="color:#000; font-size:0.8rem; font-weight:normal;">Non spécifiée</span>
        {% endif %}
      </div>
    </div>
    <div style="flex:1; background-color: transparent; padding: 10px; border: 0.5pt solid #000;">
      <h6 style="text-transform: uppercase; font-weight: bold; color: #000; font-size: 0.65rem; margin: 0 0 5px 0;">Observation</h6>
      <div style="font-size: 1rem; font-weight: 600; color: #000;">
        {% if deliberation.observation == 'admis' %}Admis(e)
        {% elif deliberation.observation == 'ajourne' %}Ajourné(e)
        {% elif deliberation.observation == 'radie' %}Radié(e)
        {% else %}<span style="color:#000; font-size:0.8rem; font-weight:normal;">Aucune observation</span>
        {% endif %}
      </div>
    </div>
  </div>
  {% endif %}
</div>
"""
        template = DocumentTemplate.objects.filter(template_type='bulletin', is_active=True).first()
        if template:
            # Force update to the exact modal layout just for this test, so it replaces the previous one
            template.content = html_content_default
            template.save()
        else:
            template = DocumentTemplate.objects.create(
                slug="bulletin-de-notes-standard",
                title="Bulletin de Notes Standard (Pro)",
                template_type="bulletin",
                content=html_content_default,
                description="Modèle professionnel identique à l'aperçu web.",
                is_active=True
            )
            
        html_content, error = render_template_with_context(template.content, context_data)
        if error:
            return HttpResponse(f"Erreur de rendu du modèle: {error}", status=500)
            
        try:
            from weasyprint import HTML
            from io import BytesIO
            from django.template.loader import render_to_string
            
            class MockDocument:
                def __init__(self, content, tpl):
                    self.rendered_content = content
                    self.template = tpl
                    
            mock_doc = MockDocument(html_content, template)
            
            full_html = render_to_string('documents/pdf_base.html', {
                'document': mock_doc,
                'entreprise': context_data['entreprise']
            })
            
            pdf_file = BytesIO()
            HTML(string=full_html, base_url=request.build_absolute_uri('/')).write_pdf(pdf_file)
            pdf_file.seek(0)
            
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="bulletin_{student.id}.pdf"'
            return response
            
        except ImportError:
            return HttpResponse(html_content)

    except Exception as e:
        return HttpResponse(f"Erreur: {str(e)}", status=500)
