import re

file_path = 'templates/tenant_folder/conseil/prospect/details_prospect.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We look for the end of loadPersonalInfos success function:
#                     $('#telephoneInputUpdate').val(data.telephone)
#                     ...
#                 }

patch = """
                    // Render contacts si c'est une entreprise
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
                                contactsHtml += '</tr>';
                            });
                        } else {
                            contactsHtml = '<tr><td colspan="5" class="text-center text-muted">Aucun contact enregistré</td></tr>';
                        }
                        $('#contacts_entreprise_list').html(contactsHtml);
                    }
"""

# Insert it before the end of the success function
# Find where the success function ends.
# A safe place is right after `$('#statut_prospectSelectUpdate').val(data.statut)` or just search for `$('#telephoneInputUpdate').val(data.telephone)`
# and insert after all the `.val()` assignments.

match = re.search(r"\$\('#statut_prospectSelectUpdate'\)\.val\(data\.statut\)\s*;", content)
if match:
    new_content = content[:match.end()] + patch + content[match.end():]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Patched JS successfully.")
else:
    print("Could not find insertion point")
    # try another
    match2 = re.search(r"\$\('#statut_prospectSelectUpdate'\)\.val\(data\.statut\)", content)
    if match2:
        new_content = content[:match2.end()] + patch + content[match2.end():]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Patched JS successfully. (No semicolon)")
    else:
        print("Failed both.")
