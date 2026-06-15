import re

file_path = 'c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/templates/tenant_folder/menu.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

def replacer(match):
    urls = match.group(1)
    if 'DetailsProspectConseil' in urls:
        urls = urls.replace('DetailsProspectConseil', '').replace('  ', ' ').strip()
        return "in '" + urls + "' or request.resolver_match.url_name == 'DetailsProspectConseil'"
    return match.group(0)

content = re.sub(r"in\s+'([^']+)'", replacer, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
