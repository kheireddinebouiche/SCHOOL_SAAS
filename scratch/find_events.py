import re

with open('templates/tenant_folder/crm/preinscrits/liste-des-preinscrits.html', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if "$('#filter-promo" in line and "on('change'" in line:
        print(f"Line {i+1}: {line}")
    elif "$('#month-filter" in line and "on('change'" in line:
        print(f"Line {i+1}: {line}")
