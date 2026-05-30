import re

files = [
    r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\comptabilite\echeancier\details-suivie-echeancier.html',
    r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\comptabilite\echeancier\details-suivie-echeancier-double.html'
]

ids_to_remove = [
    'remboursementTraiteDetailsModal'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for element_id in ids_to_remove:
        while True:
            match = re.search(r'<([a-zA-Z0-9]+)[^>]*?id=[\'\"]' + element_id + r'[\'\"][^>]*>', content)
            if not match:
                break
            
            tag_name = match.group(1)
            start_idx = match.start()
            
            open_tags = 0
            end_idx = start_idx
            
            tag_pattern = re.compile(r'<\s*' + tag_name + r'\b[^>]*>|<\s*/\s*' + tag_name + r'\s*>', re.IGNORECASE)
            
            for m in tag_pattern.finditer(content, start_idx):
                tag_text = m.group(0)
                if tag_text.startswith('</'):
                    open_tags -= 1
                else:
                    if not tag_text.endswith('/>'):
                        open_tags += 1
                
                if open_tags <= 0:
                    end_idx = m.end()
                    break
            
            if end_idx > start_idx:
                content = content[:start_idx] + content[end_idx:]
            else:
                break
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Processed', file_path)
