fields = {
    'Identité': ['nom_arabe', 'prenom_arabe', 'date_naissance', 'lieu_naissance', 'nin', 'secu', 'groupe_sanguin', 'nationnalite'],
    'Parents': ['prenom_pere', 'tel_pere', 'indicatif_pere', 'nom_mere', 'prenom_mere', 'tel_mere', 'indicatif_mere', 'tuteur_legal', 'tel_tuteur', 'indicatif_tuteur'],
    'Médical': ['has_handicap', 'type_handicap'],
    'Adresse': ['adresse_prospect', 'commune', 'wilaya', 'pays', 'code_zip'],
    'Académique': ['niveau_scolaire', 'filiere_prospect', 'diplome', 'specialite_diplome', 'etablissement_diplome', 'annee_diplome']
}

html = []
html.append('''                                    <div class="setting-item shadow-sm mb-3">
                                        <div class="d-flex justify-content-between align-items-center mb-3">
                                            <div class="d-flex align-items-center">
                                                <div class="icon-shape icon-sm bg-warning text-white rounded-circle me-3">
                                                    <i class="ri-lock-line"></i>
                                                </div>
                                                <div>
                                                    <h6 class="mb-0 fw-bold">Verrouillage des champs CRM</h6>
                                                    <p class="text-muted small mb-0">Sélectionnez les champs à verrouiller (griser) dans la fiche pré-inscrit.</p>
                                                </div>
                                            </div>
                                            <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#crmFieldLocksConfig">
                                                <i class="ri-settings-4-line"></i> Configurer
                                            </button>
                                        </div>
                                        <div class="collapse" id="crmFieldLocksConfig">
                                            <div class="card card-body bg-light border-0 p-3 mt-3">
                                                <div class="row g-3">''')

for group, f_list in fields.items():
    html.append(f'''                                                    <div class="col-md-6">
                                                        <h6 class="text-primary small fw-bold mb-2">{group}</h6>
                                                        <div class="vstack gap-2">''')
    for f in f_list:
        label = f.replace('_', ' ').title()
        html.append(f'''                                                            <div class="form-check form-switch">
                                                                <input class="form-check-input" type="checkbox" id="lock_{f}" 
                                                                       {{% if config.crm_field_locks.{f} %}}checked{{% endif %}}
                                                                       onchange="updateSetting('crm_field_locks__{f}', this.checked)">
                                                                <label class="form-check-label small" for="lock_{f}">{label}</label>
                                                            </div>''')
    html.append('''                                                        </div>
                                                    </div>''')

html.append('''                                                </div>
                                            </div>
                                        </div>
                                    </div>''')

with open('scratch/crm_locks_ui.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(html))
