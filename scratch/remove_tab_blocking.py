import re

files = ['templates/tenant_folder/crm/preinscrits/details-preinscrit.html', 'templates/tenant_folder/crm/preinscrits/details_preinscript_double.html']
for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Disable the show.bs.tab interception logic
    pattern = re.compile(r'if \(!validateTab\(tabHref\)\) \{.*?return false;\s*\}', re.DOTALL)
    new_content = pattern.sub('// Tab navigation autorisée, pas de blocage ici', content)
    
    # Disable the nextTabBtn blocking logic
    new_content = new_content.replace('if (!validateCurrentTab()) return;', '// if (!validateCurrentTab()) return;')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

print('Tab navigation blocking removed')
