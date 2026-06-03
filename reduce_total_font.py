import re

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace CSS
old_css = ".total-row td { background-color: #333 !important; color: white !important; font-weight: 700; border: none; font-size: 0.85rem;}"
new_css = ".total-row td { background-color: #333 !important; color: white !important; font-weight: 700; border: none; font-size: 0.7rem;}"
content = content.replace(old_css, new_css)

# Replace HTML
old_html = """      <tr class="total-row">
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
      </tr>"""

new_html = """      <tr class="total-row">
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
      </tr>"""

content = content.replace(old_html, new_html)

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Total row font sizes reduced.")
