import re
with open('c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/templates/t_ressource_humaine/fiche_paie_list_formateur.html', 'r', encoding='utf-8') as f:
    content = f.read()

tabs_pattern = r'            <!-- Entity Tabs -->\n.*?</div>\n            </div>'
tabs_match = re.search(tabs_pattern, content, flags=re.DOTALL)
if tabs_match:
    tabs_str = tabs_match.group(0)
    # Remove from current location
    content = content.replace(tabs_str, '')
    
    insert_target = '            <div class="row">\n                <div class="col-lg-12">\n                    <div class="glass-card border-0 overflow-hidden">\n                        <div class="card-header bg-transparent'
    insert_point = content.find(insert_target)
    
    if insert_point != -1:
        content = content[:insert_point] + tabs_str + '\n\n' + content[insert_point:]
        with open('c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/templates/t_ressource_humaine/fiche_paie_list_formateur.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print('Success')
    else:
        print('Insert target not found')
else:
    print('Tabs not found')
