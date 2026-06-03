import re

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove table-layout and word-break from .custom-table
old_table_css = """  .custom-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1.5rem;
    table-layout: fixed;
    word-break: break-word;
  }"""
new_table_css = """  .custom-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1.5rem;
  }"""
content = content.replace(old_table_css, new_table_css)

# 2. Remove hardcoded widths from nth-child
old_nth_css = """  .custom-table th:nth-child(1) { width: 8%; text-align: left; }
  .custom-table th:nth-child(2) { width: 28%; text-align: left; }"""
new_nth_css = """  .custom-table th:nth-child(1) { text-align: left; }
  .custom-table th:nth-child(2) { text-align: left; }"""
content = content.replace(old_nth_css, new_nth_css)

# 3. Remove inline widths from the th tags in the html
old_th1 = '<th style="width: 8%;">Moy./20</th>'
new_th1 = '<th>Moy./20</th>'
content = content.replace(old_th1, new_th1)

old_th2 = '<th style="width: 6%;">Coef.</th>'
new_th2 = '<th>Coef.</th>'
content = content.replace(old_th2, new_th2)

old_th3 = '<th style="width: 8%;">Total</th>'
new_th3 = '<th>Total</th>'
content = content.replace(old_th3, new_th3)

old_th4 = '<th style="width: 10%;">Décision</th>'
new_th4 = '<th>Décision</th>'
content = content.replace(old_th4, new_th4)

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Table layout fixed.")
