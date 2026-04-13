import re

filepath = 't_crm/views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for InscriptionParticulier save (lines 349-350)
pattern = r'(donnee\.type_prospect = "particulier"\s+)(donnee\.save\(\))'
replacement = r'\1\n            # Linking to previous journey\n            related_id = request.POST.get("related_prospect_id")\n            if related_id:\n                donnee.related_prospect_id = related_id\n\n            \2'

if re.search(pattern, content):
    new_content = re.sub(pattern, replacement, content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Success")
else:
    print("Pattern not found")
