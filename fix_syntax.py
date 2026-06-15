import re

file_path = 'templates/tenant_folder/conseil/clients/details_client.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# First, remove the bad patch_js.
bad_patch = r'\}\s*if \(data\.type_prospect === \'entreprise\' \&\& data\.contacts\) \{[\s\S]*?\$\(\'#contacts_entreprise_list\'\)\.html\(contactsHtml\);\s*\}'
content = re.sub(bad_patch, '', content)

# Now, insert it correctly inside the success block, before the closing brace.
good_patch = """
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
            }
"""

content = re.sub(r"\$\('#ets_code_zip_input'\)\.val\(data\.code_zip\);\s*\}?", "$('#ets_code_zip_input').val(data.code_zip);" + good_patch, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed!')
