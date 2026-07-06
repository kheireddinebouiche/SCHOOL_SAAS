import re

file_path = 'templates/tenant_folder/crm/preinscrits/prospects_incomplets.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace <div class="card-body"> with <div class="card-body p-2">
content = content.replace('class="card-body"', 'class="card-body p-2"')

# Replace mb-3 with mb-2 inside stat cards
content = content.replace('<div class="d-flex align-items-center justify-content-between mb-3">', '<div class="d-flex align-items-center justify-content-between mb-2">')

# Reduce h3 to h4
content = content.replace('<h3 class="fw-bold mb-1">', '<h4 class="fw-bold mb-0">')
content = content.replace('</h3>', '</h4>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated KPIs in prospects_incomplets.html")
