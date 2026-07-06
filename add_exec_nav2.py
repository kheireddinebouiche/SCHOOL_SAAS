import os

def insert_navbar(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Check if already included
    for line in lines:
        if 'executive_education_navbar.html' in line:
            return
            
    out_lines = []
    inserted = False
    for line in lines:
        out_lines.append(line)
        if not inserted and 'container-fluid' in line:
            out_lines.append("        {% include 'tenant_folder/executive_education_navbar.html' %}\n")
            inserted = True
            
    if inserted:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(out_lines)
        print(f"Updated: {filepath}")
    else:
        # try after <div class="main-content">
        out_lines = []
        inserted = False
        for line in lines:
            out_lines.append(line)
            if not inserted and 'class="main-content"' in line:
                out_lines.append("        {% include 'tenant_folder/executive_education_navbar.html' %}\n")
                inserted = True
        
        if inserted:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(out_lines)
            print(f"Updated (main-content): {filepath}")
        else:
            print(f"Failed to find insertion point: {filepath}")

base_dir = r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\conseil"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            insert_navbar(filepath)
