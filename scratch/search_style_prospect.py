import os

files = [
    r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\crm\details_prospect.html",
    r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\crm\details_prospect_double.html"
]

for file_path in files:
    print(f"Searching in {file_path}")
    if not os.path.exists(file_path):
        print("File not found")
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if '.style' in line:
                print(f"{i}: {line.strip()}")
