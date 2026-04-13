import os

filepath = 'templates/tenant_folder/crm/inscription_particulier.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add JS logic before {% endblock content %}
new_js = """
<script>
    $(document).ready(function() {
        const searchInput = $('#quick-search-input');
        const resultsDropdown = $('#search-results-dropdown');
        let searchTimeout;

        searchInput.on('input', function() {
            clearTimeout(searchTimeout);
            const query = $(this).val();

            if (query.length < 3) {
                resultsDropdown.hide();
                return;
            }

            searchTimeout = setTimeout(() => {
                $.ajax({
                    url: "{% url 't_crm:ApiQuickSearchExistingContact' %}",
                    data: { 'query': query },
                    success: function(response) {
                        if (response.status === 'success' && response.results.length > 0) {
                            let html = '';
                            response.results.forEach(item => {
                                html += `
                                    <button class="dropdown-item p-3 border-bottom rounded-3 select-contact-btn" 
                                            type="button"
                                            data-id="${item.id}"
                                            data-nom="${item.nom || ''}"
                                            data-prenom="${item.prenom || ''}"
                                            data-email="${item.email || ''}"
                                            data-tel="${item.telephone || ''}"
                                            data-nin="${item.nin || ''}"
                                            data-adresse="${item.adresse || ''}"
                                            data-wilaya="${item.wilaya || ''}"
                                            data-commune="${item.commune || ''}">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <div>
                                                <div class="fw-bold text-dark">${item.nom} ${item.prenom}</div>
                                                <div class="text-muted small">
                                                    <i class="ri-mail-line me-1"></i>${item.email || 'N/A'} | 
                                                    <i class="ri-phone-line me-1"></i>${item.telephone || 'N/A'}
                                                </div>
                                            </div>
                                            <span class="badge bg-soft-info text-info rounded-pill">${item.statut || 'Prospect'}</span>
                                        </div>
                                    </button>`;
                            });
                            resultsDropdown.html(html).show();
                        } else {
                            resultsDropdown.html('<div class="p-3 text-center text-muted">Aucun résultat trouvé</div>').show();
                        }
                    }
                });
            }, 300);
        });

        $(document).on('click', '.select-contact-btn', function() {
            const btn = $(this);
            
            // Auto-fill form
            $('#id_last_name').val(btn.data('nom'));
            $('#id_first_name').val(btn.data('prenom'));
            $('input[name="email"]').val(btn.data('email'));
            $('input[name="telephone"]').val(btn.data('tel'));
            $('input[name="nin"]').val(btn.data('nin'));
            $('textarea[name="adresse"]').val(btn.data('adresse'));
            $('input[name="wilaya"]').val(btn.data('wilaya'));
            $('input[name="commune"]').val(btn.data('commune'));
            
            // Set link to existing prospect
            $('#id_related_prospect_id').val(btn.data('id'));

            resultsDropdown.hide();
            searchInput.val('');

            // Highlight form sections with a visual cue
            $('.form-section').css('border-color', '#10b981').css('box-shadow', '0 0 0 4px rgba(16, 185, 129, 0.1)');
            setTimeout(() => {
                $('.form-section').css('border-color', '').css('box-shadow', '');
            }, 1000);
            
            Swal.fire({
                icon: 'success',
                title: 'Données importées',
                text: 'Les informations ont été chargées.',
                timer: 2000,
                showConfirmButton: false
            });
        });

        // Close dropdown when clicking outside
        $(document).click(function(event) {
            if (!$(event.target).closest('.search-group, #search-results-dropdown').length) {
                resultsDropdown.hide();
            }
        });
    });
</script>
"""

if '{% endblock content %}' in content:
    new_content = content.replace('{% endblock content %}', new_js + '\n{% endblock content %}')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Success")
else:
    print("Tag not found")
