import re

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the notes_dict logic
old_notes_logic = """            # Map values to primitives for the template rendering (since weasyprint + document editor runs in isolation)
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
            })"""

new_notes_logic = """            # Map notes directly to a list ordered by note_types_list so we don't need custom filters in the isolated Django Engine
            notes_list = []
            for nt in note_types_list:
                note_obj = m_data['notes_by_type'].get(nt['code'])
                if note_obj and note_obj.valeur is not None:
                    notes_list.append(str(round(note_obj.valeur, 2)))
                else:
                    notes_list.append('')
                    
            context_data['modules_data'].append({
                'module': {'code': getattr(module, 'code', '-'), 'label': getattr(module, 'label', '')},
                'matiere': getattr(module, 'label', ''),
                'professeur': '',
                'coef': module.coef or 1,
                'moyenne_matiere': str(round(decision.moyenne, 2)) if decision and decision.moyenne else '0',
                'total_points': str(m_data['moy_coef']),
                'observation': decision.observation if decision else '',
                'decision': {'statut': decision.statut if decision else '', 'moyenne': decision.moyenne if decision else 0},
                'notes_list': notes_list
            })"""

content = content.replace(old_notes_logic, new_notes_logic)

# Replace the HTML template logic
old_html = """        # Update the HTML template to exactly match the modal
        html_content_default = \"\"\"{% load custom_filters %}"""

new_html = """        # Update the HTML template to exactly match the modal
        html_content_default = \"\"\""""

content = content.replace(old_html, new_html)

old_table_td = """        {% for note_type in note_types_list %}
          <td class="note-cell">
            {% with note=module_item.notes_by_type|get_item:note_type.code %}
              {% if note and note.valeur != '' %}
                {{ note.valeur }}
              {% else %}
                <span style="color:#adb5bd;">-</span>
              {% endif %}
            {% endwith %}
          </td>
        {% endfor %}"""

new_table_td = """        {% for note in module_item.notes_list %}
          <td class="note-cell">
              {% if note != '' %}
                {{ note }}
              {% else %}
                <span style="color:#adb5bd;">-</span>
              {% endif %}
          </td>
        {% endfor %}"""

content = content.replace(old_table_td, new_table_td)

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Template fixed.")
