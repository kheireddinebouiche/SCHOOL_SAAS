content = open('templates/tenant_folder/configuration/general_settings.html', encoding='utf-8').read()

idx1 = content.find('<h6 class="mb-0 fw-bold">Verrouillage des champs CRM</h6>')
if idx1 != -1:
    idx1 = content.rfind('<div class="setting-item shadow-sm mb-3">', 0, idx1)
    idx2 = content.find('<div class="setting-item shadow-sm mb-3">', idx1 + 100)
    
    new_content = content[:idx1] + content[idx2:]
    open('templates/tenant_folder/configuration/general_settings.html', 'w', encoding='utf-8').write(new_content)
    print("Removed old block")
else:
    print("Could not find old block")
