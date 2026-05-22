import re

file_path = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\saas_admin_app\saas_tenant_data_explorer.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

danger_zone = '''                </ul>
                <hr class="border-secondary opacity-25 my-3">
                <h5 class="mb-3 px-3 fw-bold text-danger"><i class="ri-error-warning-line me-2"></i>Zone de danger</h5>
                <button type="button" class="btn btn-danger w-100 rounded-pill shadow-sm" onclick="confirmResetTresorerie()">
                    <i class="ri-restart-line me-1"></i> Réinitialiser Trésorerie
                </button>
            </div>'''

if "confirmResetTresorerie()" not in content:
    content = content.replace("</ul>\n            </div>", danger_zone)
    
js_function = '''
    // Workflow: Reset Tresorerie
    function confirmResetTresorerie() {
        Swal.fire({
            title: 'Réinitialiser la Trésorerie ?',
            text: "Cette action va purger DÉFINITIVEMENT toutes les opérations bancaires, dépenses, dépôts, et remboursements de cet institut. Tapez 'CONFIRMER' pour valider.",
            input: 'text',
            icon: 'error',
            showCancelButton: true,
            confirmButtonText: 'Réinitialiser',
            cancelButtonText: 'Annuler',
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            customClass: {
                popup: 'rounded-4',
                confirmButton: 'btn btn-danger rounded-pill px-4',
                cancelButton: 'btn btn-light rounded-pill px-4 ms-2'
            },
            buttonsStyling: false,
            preConfirm: (inputValue) => {
                if (inputValue !== 'CONFIRMER') {
                    Swal.showValidationMessage("Veuillez taper 'CONFIRMER' pour valider.");
                    return false;
                }
                return true;
            }
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire({title: 'Purge en cours...', allowOutsideClick: false, didOpen: () => Swal.showLoading()});
                fetch(`{% url 'saas_admin_app:saas_reset_tresorerie_action' institut.id %}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{{ csrf_token }}'
                    }
                })
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'success') {
                        Swal.fire('Succès', data.message, 'success').then(() => location.reload());
                    } else {
                        Swal.fire('Erreur', data.message, 'error');
                    }
                })
                .catch(err => {
                    console.error(err);
                    Swal.fire('Erreur', 'Erreur de connexion serveur.', 'error');
                });
            }
        });
    }
'''

if "function confirmResetTresorerie(" not in content:
    content = content.replace('</script>\n{% endblock extra_js %}', js_function + '\n</script>\n{% endblock extra_js %}')
    
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added danger zone and js function to template.")
