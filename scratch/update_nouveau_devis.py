import re

filename = 'templates/tenant_folder/conseil/nouveau-devis.html'
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the old Modal HTML block
modal_start = content.find('<!-- Modal Nouveau Prospect Premium Style -->')
modal_end = content.find('</div>\n</div>\n</div>', modal_start) + len('</div>\n</div>\n</div>')

if modal_start != -1 and modal_end != -1:
    new_content = content[:modal_start] + "{% include 'tenant_folder/conseil/modal_prospect.html' %}\n" + content[modal_end:]
else:
    print("Could not find old modal")
    exit(1)

# 2. Replace the JS logic:
# Find `saveProspectBtn.addEventListener('click', function() {`
# to its closing `});`
# And replace with `window.submitNewProspect = function() { ... }`

js_start = new_content.find('saveProspectBtn.addEventListener(\'click\', function() {')
if js_start != -1:
    # Find the end of this block
    # It ends with:
    #             });
    #         });
    #     });
    # </script>
    
    # Let's replace the whole modal logic block to be safe.
    logic_start = new_content.find('// Modal Logic', js_start - 300)
    logic_end = new_content.find('});\n</script>', logic_start)
    
    new_logic = '''// Modal Logic
        const clientSelect = document.getElementById('{{ form.client.id_for_label }}');

        window.submitNewProspect = function() {
            const quickProspectForm = document.getElementById('quickProspectForm');
            const prospectError = document.getElementById('prospectError');
            const errorText = document.getElementById('errorText');
            const saveProspectBtn = document.getElementById('saveProspectBtn');

            if (!quickProspectForm.checkValidity()) {
                quickProspectForm.reportValidity();
                return;
            }

            const formData = new FormData(quickProspectForm);
            
            const originalBtnText = saveProspectBtn.innerHTML;
            saveProspectBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
            saveProspectBtn.disabled = true;
            if (prospectError) prospectError.classList.add('d-none');
            
            formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

            fetch("{% url 't_conseil:ApiQuickCreateProspect' %}", {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Close Modal using Bootstrap 5
                    const modalEl = document.getElementById('newProspectModal');
                    const modalInstance = bootstrap.Modal.getInstance(modalEl);
                    if (modalInstance) {
                        modalInstance.hide();
                    }
                    
                    const label = data.prospect.entreprise ? `${data.prospect.entreprise} (Entreprise)` : `${data.prospect.nom} ${data.prospect.prenom || ''}`;
                    const option = new Option(label, data.prospect.id, true, true);
                    clientSelect.add(option, undefined);
                    $(clientSelect).trigger('change');
                    quickProspectForm.reset();
                    
                    if (typeof alertify !== 'undefined') {
                        alertify.success(data.message || 'Prospect ajouté avec succès');
                    }
                } else {
                    if (errorText) errorText.textContent = data.message || 'Erreur inconnue.';
                    if (prospectError) prospectError.classList.remove('d-none');
                }
            })
            .catch(err => {
                console.error(err);
                if (errorText) errorText.textContent = 'Erreur serveur.';
                if (prospectError) prospectError.classList.remove('d-none');
            })
            .finally(() => {
                saveProspectBtn.innerHTML = originalBtnText;
                saveProspectBtn.disabled = false;
            });
        };
'''
    new_content = new_content[:logic_start] + new_logic + new_content[logic_end:]

with open(filename, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated nouveau-devis.html successfully.")
