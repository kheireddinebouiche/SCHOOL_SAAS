import sys

file_path = 'templates/tenant_folder/menu.html'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '<!-- Conseil -->' in line:
        if start_idx == -1:
            start_idx = i
        else:
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    new_content = lines[:start_idx + 1]
    
    new_content.append('                    <li class="nav-item">\n')
    new_content.append('                        <a class="nav-link menu-link rounded-2 mx-2 mb-1 {% if request.resolver_match.url_name in \'ConseilDashboard ListeGroupesConseil NouveauGroupeConseil DetailsGroupeConseil ListeDAS PipelineConseil ConfigurationConseil configure-devis DetailsDevis ListeDesDevis prospectInstance ListeDesClients DetailsClient ListeThematique AddNewDevis ArchiveThematique ListeDesFactures AddNewFacture configure-facture DetailsFacture ListeDesAvoirs PaiementsConseilListe ListeConsultants HistoriqueConsultant\' or request.resolver_match.url_name == \'DetailsProspectConseil\' %}active{% endif %}" href="{% url \'t_conseil:ConseilDashboard\' %}">\n')
    new_content.append('                            <i class=\'bx bx-briefcase-alt-2 fs-5\'></i> <span data-key="t-authentication" class="ms-1">Executive Education</span>\n')
    new_content.append('                        </a>\n')
    new_content.append('                    </li>\n')
    new_content.append(lines[end_idx])
    new_content.extend(lines[end_idx + 1:])
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_content)
    print('Successfully updated menu.html')
else:
    print('Could not find <!-- Conseil --> markers')
