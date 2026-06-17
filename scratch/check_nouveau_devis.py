import re
content = open('templates/tenant_folder/conseil/nouveau-devis.html', encoding='utf-8', errors='ignore').read()
matches = re.findall(r'<button[^>]*>[^<]*prospect[^<]*</button>', content, re.IGNORECASE)
for m in matches:
    print(m)

matches2 = re.findall(r'<div[^>]*modal[^>]*>[\s\S]{0,300}prospect[\s\S]{0,300}', content, re.IGNORECASE)
for m in matches2:
    print(m)
