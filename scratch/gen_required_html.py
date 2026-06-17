fields = {
    'Identité': ['nom_arabe', 'prenom_arabe', 'date_naissance', 'lieu_naissance', 'nin', 'secu', 'groupe_sanguin', 'nationnalite'],
    'Parents': ['prenom_pere', 'tel_pere', 'indicatif_pere', 'nom_mere', 'prenom_mere', 'tel_mere', 'indicatif_mere', 'tuteur_legal', 'tel_tuteur', 'indicatif_tuteur'],
    'Médical': ['has_handicap', 'type_handicap'],
    'Adresse': ['adresse_prospect', 'commune', 'wilaya', 'pays', 'code_zip'],
    'Académique': ['niveau_scolaire', 'filiere_prospect', 'diplome', 'specialite_diplome', 'etablissement_diplome', 'annee_diplome']
}

html = []
html.append('''
                                    <div class="setting-item shadow-sm mb-3">
                                        <div class="d-flex justify-content-between align-items-center mb-3">
                                            <div class="d-flex align-items-center">
                                                <div class="icon-shape icon-sm bg-info text-white rounded-circle me-3">
                                                    <i class="ri-checkbox-circle-line"></i>
                                                </div>
                                                <div>
                                                    <h6 class="mb-0 fw-bold">Validation des champs obligatoires CRM</h6>
                                                    <p class="text-muted small mb-0">Sélectionnez les champs requis pour la validation de la fiche selon le profil du prospect.</p>
                                                </div>
                                            </div>
                                            <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#crmRequiredFieldsConfig">
                                                <i class="ri-settings-4-line"></i> Configurer
                                            </button>
                                        </div>
                                        <div class="collapse" id="crmRequiredFieldsConfig">
                                            <div class="card card-body bg-light border-0 p-3 mt-3">
                                                
                                                <ul class="nav nav-pills mb-3" id="pills-tab-required" role="tablist">
                                                    <li class="nav-item" role="presentation">
                                                        <button class="nav-link active" id="pills-national-tab" data-bs-toggle="pill" data-bs-target="#pills-national" type="button" role="tab">National</button>
                                                    </li>
                                                    <li class="nav-item" role="presentation">
                                                        <button class="nav-link" id="pills-etranger-tab" data-bs-toggle="pill" data-bs-target="#pills-etranger" type="button" role="tab">Étranger</button>
                                                    </li>
                                                    <li class="nav-item" role="presentation">
                                                        <button class="nav-link" id="pills-double-tab" data-bs-toggle="pill" data-bs-target="#pills-double" type="button" role="tab">Double Diplomation</button>
                                                    </li>
                                                </ul>

                                                <div class="tab-content" id="pills-tabContent-required">
''')

profiles = {
    'national': 'crm_required_fields_national',
    'etranger': 'crm_required_fields_etranger',
    'double': 'crm_required_fields_double'
}

for i, (profile_key, config_key) in enumerate(profiles.items()):
    active_class = "show active" if i == 0 else ""
    html.append(f'''                                                    <div class="tab-pane fade {active_class}" id="pills-{profile_key}" role="tabpanel">
                                                        <div class="row g-3">''')
    for group, f_list in fields.items():
        html.append(f'''                                                            <div class="col-md-6">
                                                                <h6 class="text-primary small fw-bold mb-2">{group}</h6>
                                                                <div class="vstack gap-2">''')
        for f in f_list:
            label = f.replace('_', ' ').title()
            html.append(f'''                                                                    <div class="form-check form-switch">
                                                                        <input class="form-check-input" type="checkbox" id="req_{profile_key}_{f}" 
                                                                               {{% if config.{config_key}.{f} %}}checked{{% endif %}}
                                                                               onchange="updateSetting('{config_key}__{f}', this.checked)">
                                                                        <label class="form-check-label small" for="req_{profile_key}_{f}">{label}</label>
                                                                    </div>''')
        html.append('''                                                                </div>
                                                            </div>''')
    html.append('''                                                        </div>
                                                    </div>''')

html.append('''                                                </div>
                                            </div>
                                        </div>
                                    </div>''')

import re
content = open('templates/tenant_folder/configuration/general_settings.html', encoding='utf-8').read()

# find crmFieldLocksConfig end
idx = content.find('id="crmFieldLocksConfig"')
if idx != -1:
    idx2 = content.find('<div class="setting-item shadow-sm mb-3">', idx)
    new_content = content[:idx2] + '\n'.join(html) + '\n' + content[idx2:]
    open('templates/tenant_folder/configuration/general_settings.html', 'w', encoding='utf-8').write(new_content)
    print("Done")
