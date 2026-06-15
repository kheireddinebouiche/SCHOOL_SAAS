import re

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the HTML content block
start_marker = 'html_content_default = """'
end_marker = '        template = DocumentTemplate.objects.filter(template_type=\'bulletin\', is_active=True).first()'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find boundaries")
    exit(1)

new_html = """html_content_default = \"\"\"<style>
  :root {
    --primary-color: #2c3e50;
    --accent-color: #3498db;
    --light-bg: #f8f9fa;
    --border-color: #e9ecef;
  }
  .bulletin-container {
    background: white;
    padding: 1.5rem;
    width: 100%;
    margin: 0 auto;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    box-sizing: border-box;
    font-size: 11px;
  }
  .bulletin-header {
    border-bottom: 2px solid var(--primary-color);
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .bulletin-title {
    font-family: 'Georgia', serif;
    color: var(--primary-color);
    font-size: 1.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 0.2rem 0;
  }
  .bulletin-subtitle {
    color: #6c757d;
    font-size: 0.9rem;
    margin: 0;
  }
  .student-details { margin-bottom: 1.5rem; display: flex; gap: 15px; }
  .detail-col { flex: 1; }
  .academic-year {
    background-color: var(--light-bg);
    padding: 0.8rem;
    border-left: 3px solid var(--accent-color);
    border-radius: 4px;
  }
  .detail-row {
    display: flex;
    margin-bottom: 0.3rem;
    align-items: baseline;
  }
  .detail-label {
    width: 90px;
    font-weight: 600;
    color: #495057;
    text-transform: uppercase;
    font-size: 0.7rem;
    letter-spacing: 0.5px;
  }
  .detail-value {
    color: #212529;
    font-weight: 500;
    font-size: 0.85rem;
  }
  .custom-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1.5rem;
    table-layout: fixed;
    word-break: break-word;
  }
  .custom-table th {
    background-color: #eee !important;
    color: black !important;
    text-transform: uppercase;
    font-size: 0.6rem;
    letter-spacing: 0.2px;
    padding: 0.6rem 0.4rem;
    font-weight: 600;
    border: none;
    text-align: center;
  }
  .custom-table th:nth-child(1) { width: 8%; text-align: left; }
  .custom-table th:nth-child(2) { width: 28%; text-align: left; }
  .custom-table td {
    padding: 0.6rem 0.4rem;
    border-bottom: 1px solid var(--border-color);
    vertical-align: middle;
    color: #212529;
    font-size: 0.7rem;
  }
  .module-code { font-family: 'Courier New', monospace; font-weight: 600; color: var(--accent-color); font-size: 0.65rem; }
  .module-label { font-weight: 600; font-size: 0.7rem; }
  .note-cell { text-align: center; font-family: 'Consolas', monospace; font-weight: 500; font-size: 0.7rem; }
  .average-cell { background-color: #f8f9fa !important; font-weight: 700; color: var(--primary-color); text-align: center; font-size: 0.75rem; }
  .total-row td { background-color: #333 !important; color: white !important; font-weight: 700; border: none; font-size: 0.85rem;}
  
  .status-badge {
    padding: 0.2em 0.5em; font-size: 0.6em; font-weight: 600; border-radius: 4px; text-transform: uppercase;
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
        <h2 style="margin:0; font-size: 1rem; color: #2c3e50;">{{ entreprise.designation }}</h2>
        <p style="margin:0; font-size: 0.75rem; color: #6c757d;">{{ entreprise.adresse }}</p>
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
          <div style="font-size: 0.55rem; opacity: 0.8; margin-bottom: 2px;">{{ note_type.bloc_label|default:"" }}</div>
          {{ note_type.libelle }}
        </th>
        {% endfor %}
        <th style="width: 8%;">Moy./20</th>
        <th style="width: 6%;">Coef.</th>
        <th style="width: 8%;">Total</th>
        <th style="width: 10%;">Décision</th>
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
        <td class="text-center" style="font-size: 1rem;">{{ moyenne_semestre }}</td>
        <td class="text-center">
          <div style="font-size: 0.6rem; opacity: 0.8;">COEF TOTAL</div>
          {{ total_coef }}
        </td>
        <td colspan="2" class="text-center" style="font-size: 1rem;">
          <div style="font-size: 0.6rem; opacity: 0.8; font-weight: normal;">TOTAL POINTS</div>
          {{ total_points }}
        </td>
      </tr>
    </tbody>
  </table>

  {% if deliberation %}
  <div style="display:flex; gap: 15px; margin-top: 1.5rem; border-top: 1px solid #dee2e6; padding-top: 1rem;">
    <div style="flex:1; background-color: #f8f9fa; padding: 10px; border-radius: 6px; border: 1px solid #dee2e6;">
      <h6 style="text-transform: uppercase; font-weight: bold; color: #6c757d; font-size: 0.65rem; margin: 0 0 5px 0;">Décision du Jury</h6>
      <div style="font-size: 1rem; font-weight: 600; color: #2c3e50;">
        {% if deliberation.decision_jury == 'valide' %}Semestre validé
        {% elif deliberation.decision_jury == 'valide_dette' %}Semestre validé avec dette
        {% elif deliberation.decision_jury == 'non_valide' %}Semestre non validé
        {% else %}<span style="color:#6c757d; font-size:0.8rem; font-weight:normal;">Non spécifiée</span>
        {% endif %}
      </div>
    </div>
    <div style="flex:1; background-color: #f8f9fa; padding: 10px; border-radius: 6px; border: 1px solid #dee2e6;">
      <h6 style="text-transform: uppercase; font-weight: bold; color: #6c757d; font-size: 0.65rem; margin: 0 0 5px 0;">Observation</h6>
      <div style="font-size: 1rem; font-weight: 600; color: #212529;">
        {% if deliberation.observation == 'admis' %}Admis(e)
        {% elif deliberation.observation == 'ajourne' %}Ajourné(e)
        {% elif deliberation.observation == 'radie' %}Radié(e)
        {% else %}<span style="color:#6c757d; font-size:0.8rem; font-weight:normal;">Aucune observation</span>
        {% endif %}
      </div>
    </div>
  </div>
  {% endif %}
</div>
\"\"\"\n"""

new_content = content[:start_idx] + new_html + content[end_idx:]

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Styles updated successfully.")
