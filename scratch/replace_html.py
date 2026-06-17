import re
html = open('scratch/crm_locks_ui.html', encoding='utf-8').read()
content = open('templates/tenant_folder/configuration/general_settings.html', encoding='utf-8').read()

pattern = re.compile(r'<div class="setting-item shadow-sm mb-3">\s*<div class="d-flex align-items-center justify-content-between">\s*<div class="d-flex align-items-center">\s*<div class="icon-box bg-info bg-opacity-10 text-info">\s*<i class="ri-shield-check-line"></i>\s*</div>\s*<div>\s*<h6 class="fw-bold mb-1">Validation des onglets CRM</h6>[\s\S]*?</div>\s*</div>\s*</div>', re.MULTILINE)

new_content = pattern.sub(html, content)
open('templates/tenant_folder/configuration/general_settings.html', 'w', encoding='utf-8').write(new_content)
print('Done replacement.')
