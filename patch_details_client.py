import re

file_path = 'templates/tenant_folder/conseil/clients/details_client.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

table_html = """
                                <!-- Contacts de l'entreprise -->
                                {% if client.type_prospect == 'entreprise' %}
                                <div class="col-12">
                                    <div class="card glass-card shadow-none border mt-2">
                                        <div class="card-header border-0 bg-transparent px-4 py-3 d-flex justify-content-between align-items-center">
                                            <h5 class="fw-bold mb-0">Contacts de l'entreprise</h5>
                                            <button type="button" class="btn btn-primary btn-sm rounded-pill shadow-sm" onclick="$('#addContactModal').modal('show')">
                                                <i class="ri-add-line me-1"></i>Ajouter Contact
                                            </button>
                                        </div>
                                        <div class="card-body p-4 pt-0">
                                            <div class="table-responsive">
                                                <table class="table table-premium align-middle mb-0">
                                                    <thead>
                                                        <tr>
                                                            <th>Type</th>
                                                            <th>Nom & Prénom</th>
                                                            <th>Poste</th>
                                                            <th>Téléphone</th>
                                                            <th>Email</th>
                                                            <th class="text-end">Actions</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody id="contacts_entreprise_list">
                                                        <tr><td colspan="6" class="text-center text-muted">Chargement des contacts...</td></tr>
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                {% endif %}
"""

# Fixed: appending `content[match.end():]`
tab_end_marker = r'(\s*)</div>\s*<!-- Opportunities Tab -->'
match = re.search(tab_end_marker, content)
if match:
    content = content[:match.start()] + table_html + match.group(1) + '</div>\n                        <!-- Opportunities Tab -->' + content[match.end():]
else:
    print("Could not find insertion point for table")


modal_html = """
<!-- Modal Ajouter Contact Entreprise -->
<div class="modal fade" id="addContactModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-card border-0">
            <div class="modal-header border-0 bg-primary bg-opacity-10">
                <h5 class="modal-title fw-semibold text-primary mb-0">Ajouter un Contact</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body p-4">
                <form id="addContactForm">
                    <input type="hidden" name="prospect_id" value="{{ client.id }}">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Nom <span class="text-danger">*</span></label>
                            <input type="text" class="form-control" name="nom" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Prénom <span class="text-danger">*</span></label>
                            <input type="text" class="form-control" name="prenom" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Téléphone</label>
                            <input type="text" class="form-control" name="telephone">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" name="email">
                        </div>
                        <div class="col-12">
                            <label class="form-label">Poste / Fonction</label>
                            <input type="text" class="form-control" name="poste">
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer border-0">
                <button type="button" class="btn btn-light btn-rounded" data-bs-dismiss="modal">Annuler</button>
                <button type="button" class="btn btn-primary btn-rounded shadow-sm" id="saveContactBtn">Enregistrer</button>
            </div>
        </div>
    </div>
</div>

<!-- Modal Edit Contact Entreprise -->
<div class="modal fade" id="editContactModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-card border-0">
            <div class="modal-header border-0 bg-warning bg-opacity-10">
                <h5 class="modal-title fw-semibold text-warning mb-0">Modifier le Contact</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body p-4">
                <form id="editContactForm">
                    <input type="hidden" name="contact_id" id="edit_contact_id">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Nom <span class="text-danger">*</span></label>
                            <input type="text" class="form-control" name="nom" id="edit_contact_nom" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Prénom <span class="text-danger">*</span></label>
                            <input type="text" class="form-control" name="prenom" id="edit_contact_prenom" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Téléphone</label>
                            <input type="text" class="form-control" name="telephone" id="edit_contact_telephone">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" name="email" id="edit_contact_email">
                        </div>
                        <div class="col-12">
                            <label class="form-label">Poste / Fonction</label>
                            <input type="text" class="form-control" name="poste" id="edit_contact_poste">
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer border-0">
                <button type="button" class="btn btn-light btn-rounded" data-bs-dismiss="modal">Annuler</button>
                <button type="button" class="btn btn-warning btn-rounded shadow-sm" id="updateContactBtn">Enregistrer</button>
            </div>
        </div>
    </div>
</div>
"""
if 'id="addContactModal"' not in content:
    content = content.replace('<!-- Bank Account Modal -->', modal_html + '\n<!-- Bank Account Modal -->')


patch_js = """
                if (data.type_prospect === 'entreprise' && data.contacts) {
                    let contactsHtml = '';
                    if (data.contacts.length > 0) {
                        $.each(data.contacts, function(i, contact) {
                            let typeBadge = contact.is_primary 
                                ? '<span class="badge bg-success-subtle text-success px-2 py-1">Contact Principal</span>'
                                : '<span class="badge bg-secondary-subtle text-secondary px-2 py-1">Autre contact</span>';
                            contactsHtml += '<tr>';
                            contactsHtml += '<td>' + typeBadge + '</td>';
                            contactsHtml += '<td class="fw-medium">' + (contact.nom || '') + ' ' + (contact.prenom || '') + '</td>';
                            contactsHtml += '<td>' + (contact.poste || '-') + '</td>';
                            contactsHtml += '<td>' + (contact.telephone || '-') + '</td>';
                            contactsHtml += '<td>' + (contact.email || '-') + '</td>';
                            contactsHtml += '<td class="text-end">';
                            contactsHtml += '<button class="btn btn-sm btn-light btn-icon rounded-circle me-1 edit-contact-btn" ' +
                                            'data-id="' + contact.id + '" ' +
                                            'data-nom="' + (contact.nom || '') + '" ' +
                                            'data-prenom="' + (contact.prenom || '') + '" ' +
                                            'data-telephone="' + (contact.telephone || '') + '" ' +
                                            'data-email="' + (contact.email || '') + '" ' +
                                            'data-poste="' + (contact.poste || '') + '">' +
                                            '<i class="ri-pencil-line text-warning"></i></button>';
                            if (!contact.is_primary) {
                                contactsHtml += '<button class="btn btn-sm btn-light btn-icon rounded-circle delete-contact-btn" data-id="' + contact.id + '">' +
                                                '<i class="ri-delete-bin-line text-danger"></i></button>';
                            }
                            contactsHtml += '</td>';
                            contactsHtml += '</tr>';
                        });
                    } else {
                        contactsHtml = `<tr>
                            <td colspan="6" class="text-center py-4">
                                <div class="avatar-sm bg-light rounded-circle mx-auto mb-2 d-flex align-items-center justify-content-center">
                                    <i class="ri-user-add-line fs-4 text-muted"></i>
                                </div>
                                <h6 class="fw-semibold mb-1">Aucun contact enregistré</h6>
                                <p class="text-muted small mb-0">Veuillez ajouter un contact pour cette entreprise.</p>
                            </td>
                        </tr>`;
                    }
                    $('#contacts_entreprise_list').html(contactsHtml);
                }
"""

match_js = re.search(r"\$\('#ets_code_zip_input'\)\.val\(data\.code_zip\);\s*\}", content)
if match_js:
    content = content[:match_js.end()] + patch_js + content[match_js.end():]


js_logic = """
    // Contacts Entreprise Actions
    $('#saveContactBtn').on('click', function() {
        var formData = new FormData($('#addContactForm')[0]);
        formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
        
        $.ajax({
            url: "{% url 't_conseil:ApiAddContactEntreprise' %}",
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success') {
                    alertify.success(response.message);
                    $('#addContactModal').modal('hide');
                    $('#addContactForm')[0].reset();
                    loadPersonalInfos();
                } else {
                    alertify.error(response.message);
                }
            }
        });
    });

    $(document).on('click', '.edit-contact-btn', function() {
        var btn = $(this);
        $('#edit_contact_id').val(btn.data('id'));
        $('#edit_contact_nom').val(btn.data('nom'));
        $('#edit_contact_prenom').val(btn.data('prenom'));
        $('#edit_contact_telephone').val(btn.data('telephone'));
        $('#edit_contact_email').val(btn.data('email'));
        $('#edit_contact_poste').val(btn.data('poste'));
        $('#editContactModal').modal('show');
    });

    $('#updateContactBtn').on('click', function() {
        var formData = new FormData($('#editContactForm')[0]);
        formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
        
        $.ajax({
            url: "{% url 't_conseil:ApiEditContactEntreprise' %}",
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success') {
                    alertify.success(response.message);
                    $('#editContactModal').modal('hide');
                    loadPersonalInfos();
                } else {
                    alertify.error(response.message);
                }
            }
        });
    });

    $(document).on('click', '.delete-contact-btn', function() {
        var contact_id = $(this).data('id');
        alertify.confirm("Supprimer le contact", "Êtes-vous sûr de vouloir supprimer ce contact ?", 
            function() {
                $.ajax({
                    url: "{% url 't_conseil:ApiDeleteContactEntreprise' %}",
                    type: 'POST',
                    data: {
                        'contact_id': contact_id,
                        'csrfmiddlewaretoken': '{{ csrf_token }}'
                    },
                    success: function(response) {
                        if (response.status === 'success') {
                            alertify.success(response.message);
                            loadPersonalInfos();
                        } else {
                            alertify.error(response.message);
                        }
                    }
                });
            }, null
        ).set('labels', {ok:'Supprimer', cancel:'Annuler'});
    });
"""

if "ApiEditContactEntreprise" not in content:
    match_end = re.search(r'\s*// Workflow Stepper Logic', content)
    if match_end:
        content = content[:match_end.start()] + js_logic + content[match_end.start():]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated details_client.html successfully")
