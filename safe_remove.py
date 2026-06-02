import re

files = [
    r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\comptabilite\echeancier\details-suivie-echeancier.html',
    r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\comptabilite\echeancier\details-suivie-echeancier-double.html'
]

ids_to_remove = [
    'remboursementEnAttenteNotification',
    'remboursementTraiteNotification',
    'btnRefundRequestModal',
    'remboursementDetailsModal',
    'remboursementDetailsDangerModal',
    'confirmationRemboursementModal',
    'refundModal',
    'remboursementTraiteDetailsModal'
]

def remove_html_block_by_id(content, element_id):
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
    return content

def remove_js_block(content, start_pattern):
    while True:
        match = re.search(start_pattern, content)
        if not match:
            break
        
        start_idx = match.start()
        
        first_brace = content.find('{', start_idx)
        if first_brace == -1:
            break
            
        open_braces = 0
        end_idx = -1
        in_string = False
        string_char = ''
        escape = False
        
        for i in range(first_brace, len(content)):
            char = content[i]
            
            if escape:
                escape = False
                continue
                
            if char == '\\':
                escape = True
                continue
                
            if char in ['\"', '\'', '`']:
                if not in_string:
                    in_string = True
                    string_char = char
                elif string_char == char:
                    in_string = False
                continue
                
            if not in_string:
                if char == '{':
                    open_braces += 1
                elif char == '}':
                    open_braces -= 1
                    if open_braces == 0:
                        end_idx = i + 1
                        break
        
        if end_idx != -1:
            if content[end_idx:end_idx+2] == ');':
                end_idx += 2
            elif content[end_idx:end_idx+1] == ';':
                end_idx += 1
            content = content[:start_idx] + content[end_idx:]
        else:
            break
    return content

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for element_id in ids_to_remove:
        content = remove_html_block_by_id(content, element_id)
        
    content = re.sub(r'<h6[^>]*>Bouton "Remboursement"</h6>\s*<p[^>]*>.*?</p>', '', content, flags=re.DOTALL)
    content = re.sub(r'<span[^>]*>Si une demande de remboursement est créée.*?</span>', '', content, flags=re.DOTALL)
    
    content = remove_js_block(content, r'\$\(document\)\.on\(\'click\',\s*\'#confirmerRemboursementBtn\'')
    content = remove_js_block(content, r'\$\(document\)\.on\(\'click\',\s*\'#btnRefundRequestModal\'')
    content = remove_js_block(content, r'\$\(\'#confirmationRemboursementModal\'\)\.on\(\'shown\.bs\.modal\'')
    content = remove_js_block(content, r'function DetailsRembourssementAvantTraitement\s*\(')
    content = remove_js_block(content, r'function DetailsRefundTraite\s*\(')
    
    content = re.sub(r'document\.getElementById\([\'"]btnRefundRequestModal[\'"]\).*?;', '', content)
    content = re.sub(r'\$\([\'"]#refundModal[\'"]\).*?;', '', content)
    content = re.sub(r'\$\([\'"]#remboursementDetailsModal[\'"]\).*?;', '', content)
    content = re.sub(r'\$\([\'"]#remboursementDetailsDangerModal[\'"]\).*?;', '', content)
    content = re.sub(r'\$\([\'"]#confirmationRemboursementModal[\'"]\).*?;', '', content)
    content = re.sub(r'DetailsRefundTraite\(.*?\);', '', content)
    content = re.sub(r'DetailsRembourssementAvantTraitement\(.*?\);', '', content)
    content = re.sub(r'\$\(\'#remboursementStatut\'\)\.text\(.*?\);', '', content)
    content = re.sub(r'\$\(\'#remboursementDateValidation\'\)\.text\(.*?\);', '', content)
    content = re.sub(r'\$\(\'#remboursementMotifDanger\'\)\.text\(.*?\);', '', content)
    content = re.sub(r'\$\(\'#remboursementObservations\'\)\.text\(.*?\);', '', content)
    content = re.sub(r'\$\(\'#confirmMontantRemboursement\'\)\.text\(.*?\);', '', content)
    content = re.sub(r'document\.getElementById\([\'"]remboursementTraiteNotification[\'"]\).*?;', '', content)
    content = re.sub(r'document\.getElementById\([\'"]remboursementEnAttenteNotification[\'"]\).*?;', '', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Safely processed', file_path)
