import os

files = [
    r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\crm\preinscrits\details-preinscrit.html",
    r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\crm\preinscrits\details_preinscript_double.html"
]

for file_path in files:
    print(f"Searching in {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if '.style' in line:
                print(f"{i}: {line.strip()}")
