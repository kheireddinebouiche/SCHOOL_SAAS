import sys

file_path = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\saas_admin_app\saas_tenant_data_explorer.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('tab=paiements">Suivant</a></li>')
if idx != -1:
    print(repr(content[idx:idx+300]))
else:
    print('Not found')
