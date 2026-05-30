import re

files = [
    r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\comptabilite\echeancier\details-suivie-echeancier.html',
    r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\comptabilite\echeancier\details-suivie-echeancier-double.html'
]

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The corrupted variable assignments that cause syntax errors
    content = re.sub(r'var amount =\s*\n', '', content)
    content = re.sub(r'var mode_rembourssement =\s*\n', '', content)
    content = re.sub(r'var id_refund =\s*\n', '', content)
    
    # Remove the whole event listener for confirmationRemboursementBtn
    content = re.sub(r'\$\(document\)\.on\(\'click\',\s*\'#confirmerRemboursementBtn\'.*?\}\);', '', content, flags=re.DOTALL)
    
    # Remove the whole event listener for confirmationRemboursementModal shown
    content = re.sub(r'\$\(\'#confirmationRemboursementModal\'\)\.on\(\'shown\.bs\.modal\'.*?\}\);', '', content, flags=re.DOTALL)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed', fpath)
