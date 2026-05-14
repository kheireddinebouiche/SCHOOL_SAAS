import os

file_path = r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\crm\preinscrits\details-preinscrit.html"

print(f"Searching in {file_path}")
with open(file_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if 'style' in line.lower():
            if i > 3000: # Focus on JS
                print(f"{i}: {line.strip()}")
