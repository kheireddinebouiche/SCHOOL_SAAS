import os

paths = [
    'templates/tenant_folder/administration/permissions/attribution_des_roles.html',
    'templates/tenant_folder/administration/permissions/modules.html',
    'templates/tenant_folder/administration/permissions/roles.html',
    'templates/tenant_folder/administration/logs_list.html',
    'templates/tenant_folder/configuration/general_settings.html',
    'templates/tenant_folder/users/active_sessions.html',
    'templates/tenant_folder/users/device_management.html',
    'templates/tenant_folder/users/liste_users.html'
]

for p in paths:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'configuration_navbar.html' not in content:
            # We want to insert it right after <div class="container-fluid">
            # if multiple container-fluid, we take the first one after base.html inclusion
            if '<div class="container-fluid">' in content:
                content = content.replace('<div class="container-fluid">', '<div class="container-fluid">\n        {% include \'tenant_folder/configuration_navbar.html\' %}', 1)
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'Updated {p}')
            else:
                print(f'container-fluid not found in {p}')
        else:
            print(f'Already updated {p}')
    else:
        print(f'File not found: {p}')
