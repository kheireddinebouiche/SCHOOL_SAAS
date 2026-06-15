import re

file_path = 'templates/tenant_folder/conseil/prospect/details_prospect.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The section starts at:
#             <!-- Première rangée : Informations personnelles et Fiche de Voeux -->
#             <div class="row mb-4">
# and ends right before:
#             {% if prospect.opportunites.all %}

start_marker = r'<!-- Première rangée : Informations personnelles et Fiche de Voeux -->\s*<div class="row mb-4">'
end_marker = r'\s*\{% if prospect.opportunites.all %\}'

match = re.search(f'({start_marker}.*?)(?={end_marker})', content, flags=re.DOTALL)
if not match:
    print("Could not find the section")
    exit(1)

original_row = match.group(1)

new_structure = f"""<!-- Première rangée : Informations personnelles et Fiche de Voeux -->
            {{% if prospect.type_prospect == 'entreprise' %}}
            <div class="row mb-4">
                <!-- Informations Entreprise (col-lg-4) -->
                <div class="col-lg-4">
                    <div class="card glass-card h-100 overflow-hidden">
                        <div class="card-header border-0 bg-info bg-opacity-10 px-4 py-3">
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="d-flex align-items-center">
                                    <div class="bg-info bg-opacity-10 rounded-3 p-2 me-3">
                                        <i class="ri-building-line text-info fs-4"></i>
                                    </div>
                                    <div>
                                        <h5 class="card-title fw-bold text-info mb-0">Entreprise</h5>
                                    </div>
                                </div>
                                <button type="button" class="btn btn-info btn-sm btn-rounded shadow-sm text-white" id="updateEtsDetails">
                                    <i class="ri-edit-line me-1"></i> Modifier
                                </button>
                            </div>
                        </div>
                        <div class="card-body p-4">
                            <div class="mb-4 d-flex align-items-start">
                                <div class="icon-circle bg-info bg-opacity-10 rounded-circle p-2 me-3">
                                    <i class="ri-building-line text-info"></i>
                                </div>
                                <div>
                                    <small class="text-muted d-block mb-1">Désignation</small>
                                    <span class="fw-semibold" id="entreprise_nom">-</span>
                                </div>
                            </div>
                            <div class="mb-4 d-flex align-items-start">
                                <div class="icon-circle bg-success bg-opacity-10 rounded-circle p-2 me-3">
                                    <i class="ri-phone-line text-success"></i>
                                </div>
                                <div>
                                    <small class="text-muted d-block mb-1">Téléphone</small>
                                    <span class="fw-semibold" id="phone">-</span>
                                </div>
                            </div>
                            <div class="mb-4 d-flex align-items-start">
                                <div class="icon-circle bg-primary bg-opacity-10 rounded-circle p-2 me-3">
                                    <i class="ri-mail-line text-primary"></i>
                                </div>
                                <div>
                                    <small class="text-muted d-block mb-1">Email</small>
                                    <span class="fw-semibold" id="email">-</span>
                                </div>
                            </div>
                            <div class="mb-4 d-flex align-items-start">
                                <div class="icon-circle bg-secondary bg-opacity-10 rounded-circle p-2 me-3">
                                    <i class="ri-map-pin-line text-secondary"></i>
                                </div>
                                <div>
                                    <small class="text-muted d-block mb-1">Adresse</small>
                                    <span class="fw-semibold" id="ets_adresse">-</span>
                                    <small class="text-muted d-block" id="ets_wilaya_zip"></small>
                                </div>
                            </div>
                            <div class="mb-4 d-flex align-items-start">
                                <div class="icon-circle bg-warning bg-opacity-10 rounded-circle p-2 me-3">
                                    <i class="ri-flag-line text-warning"></i>
                                </div>
                                <div>
                                    <small class="text-muted d-block mb-1">Statut</small>
                                    <span class="fw-semibold" id="statut_prospect">-</span>
                                </div>
                            </div>
                            <!-- Hidden inputs for JS to map -->
                            <div class="d-none" id="nom_prenom"></div>
                        </div>
                    </div>
                </div>

                <!-- Section Contacts (col-lg-8) -->
                <div class="col-lg-8">
                    <div class="card glass-card h-100 overflow-hidden">
                        <div class="card-header border-0 bg-primary bg-opacity-10 px-4 py-3">
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="d-flex align-items-center">
                                    <div class="bg-primary bg-opacity-10 rounded-3 p-2 me-3">
                                        <i class="ri-group-line text-primary fs-4"></i>
                                    </div>
                                    <div>
                                        <h5 class="card-title fw-bold text-primary mb-0">Contacts de l'entreprise</h5>
                                    </div>
                                </div>
                                <!-- Modal for adding contact can be added if needed, but not requested immediately. Maybe a placeholder for now -->
                                <div></div>
                            </div>
                        </div>
                        <div class="card-body p-4">
                            <div class="table-responsive">
                                <table class="table table-hover align-middle mb-0">
                                    <thead class="table-light">
                                        <tr>
                                            <th>Type</th>
                                            <th>Nom & Prénom</th>
                                            <th>Poste</th>
                                            <th>Téléphone</th>
                                            <th>Email</th>
                                        </tr>
                                    </thead>
                                    <tbody id="contacts_entreprise_list">
                                        <tr><td colspan="5" class="text-center text-muted">Chargement des contacts...</td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {{% else %}}
{original_row}
            {{% endif %}}
"""

new_content = content[:match.start()] + new_structure + content[match.end():]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Template updated successfully.")
