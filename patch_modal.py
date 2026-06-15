import re

file_path = 'templates/tenant_folder/conseil/prospect/details_prospect.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

modal_html = """
            <!-- Modal Ajouter Contact Entreprise -->
            <div class="modal fade" id="addContactModal" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content rounded-4 shadow-lg border-0">
                        <div class="modal-header border-0 bg-primary bg-opacity-10 px-4 py-3">
                            <div class="d-flex align-items-center">
                                <div class="bg-primary bg-opacity-10 rounded-3 p-2 me-3">
                                    <i class="ri-user-add-line text-primary fs-4"></i>
                                </div>
                                <div>
                                    <h5 class="modal-title fw-semibold text-primary mb-0">Ajouter un Contact</h5>
                                    <small class="text-muted">Nouveau contact pour l'entreprise</small>
                                </div>
                            </div>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body p-4">
                            <form id="addContactForm">
                                <input type="hidden" name="prospect_id" id="contact_prospect_id" value="{{ pk }}">
                                <div class="row g-3">
                                    <div class="col-md-6">
                                        <label class="form-label fw-medium">Nom <span class="text-danger">*</span></label>
                                        <input type="text" class="form-control border-light bg-light" name="nom" required>
                                    </div>
                                    <div class="col-md-6">
                                        <label class="form-label fw-medium">Prénom <span class="text-danger">*</span></label>
                                        <input type="text" class="form-control border-light bg-light" name="prenom" required>
                                    </div>
                                    <div class="col-md-6">
                                        <label class="form-label fw-medium">Téléphone</label>
                                        <input type="text" class="form-control border-light bg-light" name="telephone">
                                    </div>
                                    <div class="col-md-6">
                                        <label class="form-label fw-medium">Email</label>
                                        <input type="email" class="form-control border-light bg-light" name="email">
                                    </div>
                                    <div class="col-12">
                                        <label class="form-label fw-medium">Poste / Fonction</label>
                                        <input type="text" class="form-control border-light bg-light" name="poste" placeholder="ex: Directeur Technique">
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer border-0 bg-light px-4 py-3">
                            <button type="button" class="btn btn-light px-4 py-2 btn-rounded" data-bs-dismiss="modal">
                                Annuler
                            </button>
                            <button type="button" class="btn btn-primary px-4 py-2 btn-rounded shadow-sm" id="saveContactBtn">
                                <i class="ri-save-line me-1"></i> Enregistrer
                            </button>
                        </div>
                    </div>
                </div>
            </div>
"""

js_code = """
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
                        loadPersonalInfos(); // reload list
                    } else {
                        alertify.error(response.message);
                    }
                },
                error: function(xhr) {
                    let msg = "Erreur lors de l'enregistrement.";
                    if(xhr.responseJSON && xhr.responseJSON.message) {
                        msg = xhr.responseJSON.message;
                    }
                    alertify.error(msg);
                }
            });
        });
"""

if '<script>' in content:
    content = content.replace('<script>', modal_html + '\n<script>')

match = re.search(r'\s*\}\);\s*</script>', content)
if match:
    content = content[:match.start()] + js_code + content[match.start():]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully.")
