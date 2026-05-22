import re

file_path = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\saas_admin_app\saas_tenant_data_explorer.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add the missing confirmDeleteDataExplorer function
missing_func = '''
    // Workflow: Single Item Deletion API
    function confirmDeleteDataExplorer(itemId, modelName) {
        Swal.fire({
            title: "Êtes-vous sûr ?",
            text: "Vous allez supprimer cet élément. Cette action est irréversible !",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            confirmButtonText: "Oui, supprimer !",
            cancelButtonText: "Annuler",
            customClass: {
                popup: 'rounded-4',
                confirmButton: 'btn btn-danger rounded-pill px-4',
                cancelButton: 'btn btn-light rounded-pill px-4 ms-2'
            },
            buttonsStyling: false
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`{% url 'saas_admin_app:saas_bulk_delete_action' institut.id %}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{{ csrf_token }}'
                    },
                    body: JSON.stringify({ 'ids': [itemId], 'model': modelName })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        Swal.fire({
                            title: 'Supprimé !',
                            text: data.message,
                            icon: 'success',
                            confirmButtonClass: 'btn btn-primary rounded-pill px-4',
                            buttonsStyling: false
                        }).then(() => {
                            window.location.reload();
                        });
                    } else {
                        Swal.fire('Erreur', data.message || 'Une erreur est survenue', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    Swal.fire('Erreur', 'Erreur de connexion', 'error');
                });
            }
        });
    }
'''

if "function confirmDeleteDataExplorer" not in content:
    # Append before the closing script tag
    content = content.replace('</script>\n{% endblock extra_js %}', missing_func + '\n</script>\n{% endblock extra_js %}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added confirmDeleteDataExplorer function.")
