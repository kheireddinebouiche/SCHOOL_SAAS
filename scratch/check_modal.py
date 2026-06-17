import re
content = open('templates/tenant_folder/crm/preinscrits/details-preinscrit.html', encoding='utf-8').read()
match = re.search(r'id="additionalInfoModal"[^>]*>([\s\S]{0,1000})', content)
if match:
    print(match.group(0))
