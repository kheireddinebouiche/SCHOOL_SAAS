import re

content = open('templates/tenant_folder/conseil/nouveau-devis.html', encoding='utf-8', errors='ignore').read()
match = re.search(r'<div class="modal[^>]+id="([^"]+)"[^>]*>[\s\S]{0,1000}id="quickProspectForm"', content)
if match:
    print('Modal ID is:', match.group(1))

# Let's find the trigger button that uses this Modal ID
match_btn = re.search(r'<button[^>]+data-bs-target="#' + match.group(1) + r'"[^>]*>[\s\S]*?</button>', content)
if match_btn:
    print('Button HTML:', match_btn.group(0))

# Also search for 'modal_prospect.html' in 'pipeline.html'
content_pipe = open('templates/tenant_folder/conseil/pipeline.html', encoding='utf-8', errors='ignore').read()
match_pipe = re.search(r'<button[^>]+data-bs-target="([^"]+)"[^>]*>[\s\S]*?</button>', content_pipe)
if match_pipe:
    print('Pipeline trigger button target:', match_pipe.group(1))
