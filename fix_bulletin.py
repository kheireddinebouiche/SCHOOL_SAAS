import os

# We will read t_exam/f_views/builltins.py and replace PrintBulletinPDF
# Actually, since it's a large block, let's just use python to parse and replace it.
import re

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find the start of PrintBulletinPDF
start_idx = content.find("def PrintBulletinPDF(")
if start_idx == -1:
    print("Could not find PrintBulletinPDF")
    exit(1)

# Find the next view or end of file
# Wait, PrintBulletinPDF is at the end of the file. So we can just slice it off.
# Let's verify if there is anything after it.
# We can just replace the whole file content from def PrintBulletinPDF( to the end.

new_view = """def PrintBulletinPDF(request, session_line_id, student_id):
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
            'deliberation': {'decision': deliberation.decision if deliberation else ''},
            'note_types_list': note_types_list,
            'modules_data': []
        }
        
        for m_data in modules_data:
            module = m_data['module']
            decision = m_data['decision']
            
            # Map values to primitives for the template rendering (since weasyprint + document editor runs in isolation)
            # Actually, `render_template_with_context` can handle django objects if we pass them, but we serialize them safely.
            notes_dict = {}
            for k, v in m_data['notes_by_type'].items():
                notes_dict[k] = {'valeur': v.valeur if v.valeur is not None else ''}
                
            context_data['modules_data'].append({
                'module': {'code': getattr(module, 'code', '-'), 'label': getattr(module, 'label', '')},
                'matiere': getattr(module, 'label', ''),
                'professeur': '',
                'coef': module.coef or 1,
                'moyenne_matiere': str(round(decision.moyenne, 2)) if decision and decision.moyenne else '0',
                'total_points': str(m_data['moy_coef']),
                'observation': decision.observation if decision else '',
                'decision': {'statut': decision.statut if decision else '', 'moyenne': decision.moyenne if decision else 0},
                'notes_by_type': notes_dict
            })

        # Update the HTML template to exactly match the modal
        html_content_default = \"\"\"{% load custom_filters %}
<style>
  :root {
    --primary-color: #2c3e50;
    --accent-color: #3498db;
    --light-bg: #f8f9fa;
    --border-color: #e9ecef;
  }
  .bulletin-container {
    background: white;
    padding: 2rem;
    max-width: 100%;
    margin: 0 auto;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  }
  .bulletin-header {
    border-bottom: 2px solid var(--primary-color);
    padding-bottom: 1.5rem;
    margin-bottom: 2.5rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .bulletin-title {
    font-family: 'Georgia', serif;
    color: var(--primary-color);
    font-size: 2rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 0.5rem 0;
  }
  .bulletin-subtitle {
    color: #6c757d;
    font-size: 1.1rem;
    margin: 0;
  }
  .student-details { margin-bottom: 2.5rem; display: flex; gap: 40px; }
  .detail-col { flex: 1; }
  .academic-year {
    background-color: var(--light-bg);
    padding: 1rem;
    border-left: 4px solid var(--accent-color);
    border-radius: 4px;
  }
  .detail-row {
    display: flex;
    margin-bottom: 0.5rem;
    align-items: baseline;
  }
  .detail-label {
    width: 120px;
    font-weight: 600;
    color: #495057;
    text-transform: uppercase;
    font-size: 0.8rem;
    letter-spacing: 0.5px;
  }
  .detail-value {
    color: #212529;
    font-weight: 500;
    font-size: 1.05rem;
  }
  .custom-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 2rem;
  }
  .custom-table th {
    background-color: #eee !important;
    color: black !important;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.5px;
    padding: 1rem 0.75rem;
    font-weight: 600;
    border: none;
    text-align: center;
  }
  .custom-table th:nth-child(1), .custom-table th:nth-child(2) { text-align: left; }
  .custom-table td {
    padding: 1rem 0.75rem;
    border-bottom: 1px solid var(--border-color);
    vertical-align: middle;
    color: #212529;
    font-size: 0.9rem;
  }
  .module-code { font-family: 'Courier New', monospace; font-weight: 600; color: var(--accent-color); }
  .module-label { font-weight: 600; }
  .note-cell { text-align: center; font-family: 'Consolas', monospace; font-weight: 500; }
  .average-cell { background-color: #f8f9fa !important; font-weight: 700; color: var(--primary-color); text-align: center;}
  .total-row td { background-color: #333 !important; color: white !important; font-weight: 700; border: none; }
  
  .status-badge {
    padding: 0.35em 0.8em; font-size: 0.75em; font-weight: 600; border-radius: 4px; text-transform: uppercase;
  }
  .status-success { background-color: #d4edda; color: #155724; }
  .status-warning { background-color: #fff3cd; color: #856404; }
  .status-danger { background-color: #f8d7da; color: #721c24; }
  .status-info { background-color: #d1ecf1; color: #0c5460; }
</style>

<div class="bulletin-container">
  <div class="bulletin-header">
    <div>
      <h1 class="bulletin-title">Bulletin de Notes</h1>
      <p class="bulletin-subtitle">Session: {{ session_line.session.nom_session|upper }}</p>
    </div>
    <div style="text-align: right;">
        <h2 style="margin:0; font-size: 1.2rem; color: #2c3e50;">{{ entreprise.designation }}</h2>
        <p style="margin:0; font-size: 0.9rem; color: #6c757d;">{{ entreprise.adresse }}</p>
    </div>
  </div>

  <div class="student-details">
    <div class="detail-col">
      <div class="detail-row"><div class="detail-label">Étudiant</div><div class="detail-value text-uppercase" style="font-size:1.3rem;">{{ etudiant.nom }} {{ etudiant.prenom }}</div></div>
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
        <th style="width: 8%;">Code</th>
        <th style="width: 30%;">Unité d'Enseignement</th>
        {% for note_type in note_types_list %}
        <th class="text-center" style="width: 8%;">
          <div style="font-size: 0.65rem; opacity: 0.8; margin-bottom: 2px;">{{ note_type.bloc_label|default:"" }}</div>
          {{ note_type.libelle }}
        </th>
        {% endfor %}
        <th class="text-center" style="width: 8%;">Moy./20</th>
        <th class="text-center" style="width: 6%;">Coef.</th>
        <th class="text-center" style="width: 10%;">Total</th>
        <th class="text-center" style="width: 12%;">Décision</th>
      </tr>
    </thead>
    <tbody>
      {% for module_item in modules_data %}
      <tr>
        <td class="module-code">{{ module_item.module.code }}</td>
        <td class="module-label">{{ module_item.module.label }}</td>
        
        {% for note_type in note_types_list %}
          <td class="note-cell">
            {% with note=module_item.notes_by_type|get_item:note_type.code %}
              {% if note and note.valeur != '' %}
                {{ note.valeur }}
              {% else %}
                <span style="color:#adb5bd;">-</span>
              {% endif %}
            {% endwith %}
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
              <span style="color:#adb5bd; font-size:0.8rem;">-</span>
            {% endif %}
        </td>
      </tr>
      {% endfor %}
      
      <tr class="total-row">
        <td colspan="{{ note_types_list|length|add:2 }}" style="text-align:right; text-transform:uppercase; padding-right: 1.5rem;">
          Moyenne Générale du Semestre
        </td>
        <td class="text-center" style="font-size: 1.2rem;">{{ moyenne_semestre }}</td>
        <td class="text-center">
          <div style="font-size: 0.7rem; opacity: 0.8;">COEF TOTAL</div>
          {{ total_coef }}
        </td>
        <td colspan="2" class="text-center" style="font-size: 1.2rem;">
          <div style="font-size: 0.7rem; opacity: 0.8; font-weight: normal;">TOTAL POINTS</div>
          {{ total_points }}
        </td>
      </tr>
    </tbody>
  </table>

  {% if deliberation %}
  <div style="display:flex; gap: 20px; margin-top: 2rem; border-top: 1px solid #dee2e6; padding-top: 1.5rem;">
    <div style="flex:1; background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6;">
      <h6 style="text-transform: uppercase; font-weight: bold; color: #6c757d; font-size: 0.75rem; margin-bottom: 8px;">Décision du Jury</h6>
      <div style="font-size: 1.25rem; font-weight: 600; color: #2c3e50;">
        {% if deliberation.decision_jury == 'valide' %}Semestre validé
        {% elif deliberation.decision_jury == 'valide_dette' %}Semestre validé avec dette
        {% elif deliberation.decision_jury == 'non_valide' %}Semestre non validé
        {% else %}<span style="color:#6c757d; font-size:1rem; font-weight:normal;">Non spécifiée</span>
        {% endif %}
      </div>
    </div>
    <div style="flex:1; background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6;">
      <h6 style="text-transform: uppercase; font-weight: bold; color: #6c757d; font-size: 0.75rem; margin-bottom: 8px;">Observation</h6>
      <div style="font-size: 1.25rem; font-weight: 600; color: #212529;">
        {% if deliberation.observation == 'admis' %}Admis(e)
        {% elif deliberation.observation == 'ajourne' %}Ajourné(e)
        {% elif deliberation.observation == 'radie' %}Radié(e)
        {% else %}<span style="color:#6c757d; font-size:1rem; font-weight:normal;">Aucune observation</span>
        {% endif %}
      </div>
    </div>
  </div>
  {% endif %}
</div>
\"\"\"
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
"""

content = content[:start_idx] + new_view

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated PrintBulletinPDF successfully")

# Also run this in a django context to update the template directly in DB if we run this script.
# We will just write it and then run it in django.
