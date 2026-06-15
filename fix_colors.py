import re

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the style block
start_style = 'html_content_default = """<style>'
end_style = '</style>'

start_idx = content.find(start_style)
end_idx = content.find(end_style)

if start_idx == -1 or end_idx == -1:
    print("Could not find style")
    exit(1)

new_style = """html_content_default = \"\"\"<style>
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
    border-bottom: 2px solid #000;
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
    border: 1px solid #000;
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
    border: 1px solid #000;
    text-align: center;
  }
  .custom-table th:nth-child(1) { text-align: left; }
  .custom-table th:nth-child(2) { text-align: left; }
  .custom-table td {
    padding: 0.6rem 0.4rem;
    border: 1px solid #000;
    vertical-align: middle;
    color: #000;
    font-size: 0.7rem;
  }
  .module-code { font-family: 'Courier New', monospace; font-weight: 600; color: #000; font-size: 0.65rem; }
  .module-label { font-weight: 600; font-size: 0.7rem; }
  .note-cell { text-align: center; font-family: 'Consolas', monospace; font-weight: 500; font-size: 0.7rem; }
  .average-cell { background-color: transparent !important; font-weight: 700; color: #000; text-align: center; font-size: 0.75rem; }
  .total-row td { background-color: transparent !important; color: #000 !important; font-weight: 700; border: 1px solid #000; font-size: 0.7rem;}
  
  .status-badge {
    padding: 0.2em 0.5em; font-size: 0.6em; font-weight: 600; border: 1px solid #000; text-transform: uppercase; color: #000 !important; background-color: transparent !important;
  }
"""

content = content[:start_idx] + new_style + content[end_idx:]

# Also fix the bottom deliberation blocks HTML
old_deliberation = """  {% if deliberation %}
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
  {% endif %}"""

new_deliberation = """  {% if deliberation %}
  <div style="display:flex; gap: 15px; margin-top: 1.5rem; border-top: 1px solid #000; padding-top: 1rem;">
    <div style="flex:1; background-color: transparent; padding: 10px; border: 1px solid #000;">
      <h6 style="text-transform: uppercase; font-weight: bold; color: #000; font-size: 0.65rem; margin: 0 0 5px 0;">Décision du Jury</h6>
      <div style="font-size: 1rem; font-weight: 600; color: #000;">
        {% if deliberation.decision_jury == 'valide' %}Semestre validé
        {% elif deliberation.decision_jury == 'valide_dette' %}Semestre validé avec dette
        {% elif deliberation.decision_jury == 'non_valide' %}Semestre non validé
        {% else %}<span style="color:#000; font-size:0.8rem; font-weight:normal;">Non spécifiée</span>
        {% endif %}
      </div>
    </div>
    <div style="flex:1; background-color: transparent; padding: 10px; border: 1px solid #000;">
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
  {% endif %}"""

content = content.replace(old_deliberation, new_deliberation)

# Also fix the styling of header and texts
content = content.replace('color: #2c3e50;', 'color: #000;')
content = content.replace('color: #6c757d;', 'color: #000;')

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Colors removed and borders added.")
