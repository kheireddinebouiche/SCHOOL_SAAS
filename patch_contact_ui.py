import re

file_path = 'templates/tenant_folder/conseil/prospect/details_prospect.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add "<th>Actions</th>" to the table header.
# We search for: <th>Email</th>\n                                        </tr>
# and replace with: <th>Email</th>\n                                            <th>Actions</th>\n                                        </tr>

header_search = r'<th>Email</th>\s*</tr>'
header_replace = '<th>Email</th>\n                                            <th class="text-end">Actions</th>\n                                        </tr>'
content = re.sub(header_search, header_replace, content, count=1)

# 2. Modify `loadPersonalInfos` to include the buttons in the row, and `colspan="6"` for the empty state.
# Let's find: contactsHtml += '<td>' + (contact.email || '-') + '</td>';\n                                contactsHtml += '</tr>';
# Replace with buttons

row_search = r"contactsHtml \+= '<td>' \+ \(contact\.email \|\| '-'\) \+ '</td>';\s*contactsHtml \+= '</tr>';"
row_replace = """contactsHtml += '<td>' + (contact.email || '-') + '</td>';
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
                                contactsHtml += '</tr>';"""
content = re.sub(row_search, row_replace, content)

# 3. Fix the empty state colspan (colspan="5" -> colspan="6")
empty_search = r'colspan="5" class="text-center py-4"'
empty_replace = 'colspan="6" class="text-center py-4"'
content = content.replace(empty_search, empty_replace)

empty_search_2 = r'colspan="5" class="text-center text-muted"'
empty_replace_2 = 'colspan="6" class="text-center text-muted"'
content = content.replace(empty_search_2, empty_replace_2)


# 4. Add `editContactModal` and JS
modal_html = """
            <!-- Modal Edit Contact Entreprise -->
            <div class="modal fade" id="editContactModal" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content rounded-4 shadow-lg border-0">
                        <div class="modal-header border-0 bg-warning bg-opacity-10 px-4 py-3">
                            <div class="d-flex align-items-center">
                                <div class="bg-warning bg-opacity-10 rounded-3 p-2 me-3">
                                    <i class="ri-edit-line text-warning fs-4"></i>
                                </div>
                                <div>
                                    <h5 class="modal-title fw-semibold text-warning mb-0">Modifier le Contact</h5>
                                    <small class="text-muted">Mise à jour des informations</small>
                                </div>
                            </div>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body p-4">
                            <form id="editContactForm">
                                <input type="hidden" name="contact_id" id="edit_contact_id">
                                <div class="row g-3">
                                    <div class="col-md-6">
                                        <label class="form-label fw-medium">Nom <span class="text-danger">*</span></label>
                                        <input type="text" class="form-control border-light bg-light" name="nom" id="edit_contact_nom" required>
                                    </div>
                                    <div class="col-md-6">
                                        <label class="form-label fw-medium">Prénom <span class="text-danger">*</span></label>
                                        <input type="text" class="form-control border-light bg-light" name="prenom" id="edit_contact_prenom" required>
                                    </div>
                                    <div class="col-md-6">
                                        <label class="form-label fw-medium">Téléphone</label>
                                        <input type="text" class="form-control border-light bg-light" name="telephone" id="edit_contact_telephone">
                                    </div>
                                    <div class="col-md-6">
                                        <label class="form-label fw-medium">Email</label>
                                        <input type="email" class="form-control border-light bg-light" name="email" id="edit_contact_email">
                                    </div>
                                    <div class="col-12">
                                        <label class="form-label fw-medium">Poste / Fonction</label>
                                        <input type="text" class="form-control border-light bg-light" name="poste" id="edit_contact_poste">
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer border-0 bg-light px-4 py-3">
                            <button type="button" class="btn btn-light px-4 py-2 btn-rounded" data-bs-dismiss="modal">
                                Annuler
                            </button>
                            <button type="button" class="btn btn-warning px-4 py-2 btn-rounded shadow-sm" id="updateContactBtn">
                                <i class="ri-save-line me-1"></i> Enregistrer
                            </button>
                        </div>
                    </div>
                </div>
            </div>
"""

js_code = """
        // Edit contact button click
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

        // Update contact form submission
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
                },
                error: function(xhr) {
                    let msg = "Erreur lors de la modification.";
                    if(xhr.responseJSON && xhr.responseJSON.message) msg = xhr.responseJSON.message;
                    alertify.error(msg);
                }
            });
        });

        // Delete contact button click
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
                        },
                        error: function(xhr) {
                            let msg = "Erreur lors de la suppression.";
                            if(xhr.responseJSON && xhr.responseJSON.message) msg = xhr.responseJSON.message;
                            alertify.error(msg);
                        }
                    });
                }, null
            ).set('labels', {ok:'Supprimer', cancel:'Annuler'});
        });
"""

if 'id="editContactModal"' not in content:
    content = content.replace('<!-- Modal Ajouter Contact Entreprise -->', modal_html + '\n<!-- Modal Ajouter Contact Entreprise -->')

if 'ApiDeleteContactEntreprise' not in content:
    match = re.search(r'\s*\}\);\s*</script>', content)
    if match:
        content = content[:match.start()] + js_code + content[match.start():]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("UI Updated successfully.")
