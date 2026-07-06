import sys

file_path = 'templates/tenant_folder/menu.html'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '<!-- Configuration -->' in line:
        if start_idx == -1:
            start_idx = i
        else:
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    new_content = lines[:start_idx + 1]
    
    new_content.append('                    <li class="nav-item">\n')
    new_content.append('                        <a class="nav-link menu-link rounded-2 mx-2 mb-1 {% if request.resolver_match.url_name in \'ConfigurationDashboard general_settings liste_entreprise new_entreprise create_template edit_template template_list details_entreprise UsersListePage Role_Attribution ModulesPages roles_page user_action_log_list active_sessions DeviceManagementPage\' %}active{% endif %}" href="{% url \'institut_app:ConfigurationDashboard\' %}">\n')
    new_content.append('                            <i class="bx bx-cog fs-5"></i> <span class="ms-1">Configuration</span>\n')
    new_content.append('                        </a>\n')
    new_content.append('                    </li>\n')
    new_content.append(lines[end_idx])
    new_content.extend(lines[end_idx + 1:])
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_content)
    print('Successfully updated menu.html for Configuration')
else:
    print('Could not find <!-- Configuration --> markers')
