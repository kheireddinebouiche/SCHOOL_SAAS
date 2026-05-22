import sys

file_path = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\saas_admin_app\saas_tenant_data_explorer.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

offcanvas_html = '''
<!-- Offcanvas Details Panel -->
<div class="offcanvas offcanvas-end" tabindex="-1" id="detailsOffcanvas" aria-labelledby="detailsOffcanvasLabel" style="width: 400px; border-radius: 20px 0 0 20px; box-shadow: -10px 0 30px rgba(0,0,0,0.1); background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(20px);">
  <div class="offcanvas-header border-bottom border-light">
    <h5 class="offcanvas-title fw-bold text-primary" id="detailsOffcanvasLabel"><i class="ri-information-line me-2"></i>Détails de l'élément</h5>
    <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <div class="text-center my-4">
        <div class="avatar-lg bg-primary bg-opacity-10 rounded-circle d-flex align-items-center justify-content-center mx-auto mb-3" style="width: 80px; height: 80px;">
            <i class="ri-file-text-line text-primary fs-1"></i>
        </div>
        <h4 class="fw-bold mb-1" id="offcanvasItemId">ID : --</h4>
        <p class="text-muted" id="offcanvasItemType">Type</p>
    </div>
    
    <div class="card border-0 bg-light rounded-4 p-3 mb-3">
        <h6 class="fw-bold text-muted mb-3 text-uppercase" style="letter-spacing: 1px; font-size: 0.75rem;">Informations Rapides</h6>
        <div id="offcanvasContent">
            <!-- Dynamic content will go here -->
            <p class="text-muted text-center mb-0">Chargement...</p>
        </div>
    </div>
    
    <div class="d-grid gap-2">
        <button class="btn btn-outline-primary rounded-pill"><i class="ri-edit-line me-1"></i> Modifier</button>
        <button class="btn btn-danger rounded-pill" id="offcanvasDeleteBtn"><i class="ri-delete-bin-line me-1"></i> Supprimer</button>
    </div>
  </div>
</div>
'''

js_offcanvas = '''
    // Workflow: Offcanvas Details
    function viewDetails(id, type, detailsObj) {
        $('#offcanvasItemId').text('ID : ' + id);
        $('#offcanvasItemType').text(type);
        
        let htmlContent = '<ul class="list-unstyled mb-0">';
        for (const [key, value] of Object.entries(detailsObj)) {
            htmlContent += `
                <li class="d-flex justify-content-between mb-2 pb-2 border-bottom border-light">
                    <span class="text-muted">${key}</span>
                    <span class="fw-medium text-end">${value || '-'}</span>
                </li>`;
        }
        htmlContent += '</ul>';
        
        $('#offcanvasContent').html(htmlContent);
        
        // Setup delete button
        $('#offcanvasDeleteBtn').off('click').on('click', function() {
            var modelKey = type.toLowerCase().replace(' ', '_').normalize("NFD").replace(/[\u0300-\u036f]/g, "");
            confirmDeleteDataExplorer(id, modelKey);
        });
        
        var offcanvas = new bootstrap.Offcanvas(document.getElementById('detailsOffcanvas'));
        offcanvas.show();
    }
'''

# Inject offcanvas HTML just before the modal
target_html = "<!-- Modal Modification Spécialité -->"
if offcanvas_html not in content and target_html in content:
    content = content.replace(target_html, offcanvas_html + "\n" + target_html)

# Inject JS
target_js = "// === Global Search & Filters ==="
if "function viewDetails" not in content and target_js in content:
    content = content.replace(target_js, js_offcanvas + "\n    " + target_js)

# Add "View Details" button to the new tables (ex: Remboursements)
# For remboursements:
rem_old = '''<button class="btn btn-soft-danger btn-sm rounded-circle p-0 avatar-xs" onclick="confirmDeleteDataExplorer('{{ item.id }}', 'remboursement')" title="Supprimer">'''
rem_new = '''<button class="btn btn-soft-info btn-sm rounded-circle p-0 avatar-xs me-1" onclick="viewDetails('{{ item.id }}', 'Remboursement', {'Motif': '{{ item.motif|escapejs }}', 'Montant': '{{ item.montant }}'})" title="Détails">
                                                    <i class="ri-eye-line"></i>
                                                </button>
                                                <button class="btn btn-soft-danger btn-sm rounded-circle p-0 avatar-xs" onclick="confirmDeleteDataExplorer('{{ item.id }}', 'remboursement')" title="Supprimer">'''
if rem_old in content:
    content = content.replace(rem_old, rem_new)

# For Operations bancaires:
ob_old = '''<button class="btn btn-soft-danger btn-sm rounded-circle p-0 avatar-xs" onclick="confirmDeleteDataExplorer('{{ item.id }}', 'operation_bancaire')" title="Supprimer">'''
ob_new = '''<button class="btn btn-soft-info btn-sm rounded-circle p-0 avatar-xs me-1" onclick="viewDetails('{{ item.id }}', 'Operation Bancaire', {'Compte': '{{ item.compte_bancaire|escapejs }}'})" title="Détails">
                                                    <i class="ri-eye-line"></i>
                                                </button>
                                                <button class="btn btn-soft-danger btn-sm rounded-circle p-0 avatar-xs" onclick="confirmDeleteDataExplorer('{{ item.id }}', 'operation_bancaire')" title="Supprimer">'''
if ob_old in content:
    content = content.replace(ob_old, ob_new)

# For Demandes Remboursement
dmp_old = '''<button class="btn btn-soft-danger btn-sm rounded-circle p-0 avatar-xs" onclick="confirmDeleteDataExplorer('{{ item.id }}', 'demande_paiement')" title="Supprimer">'''
dmp_new = '''<button class="btn btn-soft-info btn-sm rounded-circle p-0 avatar-xs me-1" onclick="viewDetails('{{ item.id }}', 'Demande Paiement', {'Client': '{{ item.client|escapejs }}', 'Date': '{{ item.date_demande }}'})" title="Détails">
                                                    <i class="ri-eye-line"></i>
                                                </button>
                                                <button class="btn btn-soft-danger btn-sm rounded-circle p-0 avatar-xs" onclick="confirmDeleteDataExplorer('{{ item.id }}', 'demande_paiement')" title="Supprimer">'''
if dmp_old in content:
    content = content.replace(dmp_old, dmp_new)

# For Autres Produits
ap_old = '''<button class="btn btn-soft-danger btn-sm rounded-circle p-0 avatar-xs" onclick="confirmDeleteDataExplorer('{{ item.id }}', 'autre_produit')" title="Supprimer">'''
ap_new = '''<button class="btn btn-soft-info btn-sm rounded-circle p-0 avatar-xs me-1" onclick="viewDetails('{{ item.id }}', 'Autre Produit', {'Label': '{{ item.label|escapejs }}', 'Numéro': '{{ item.num }}'})" title="Détails">
                                                    <i class="ri-eye-line"></i>
                                                </button>
                                                <button class="btn btn-soft-danger btn-sm rounded-circle p-0 avatar-xs" onclick="confirmDeleteDataExplorer('{{ item.id }}', 'autre_produit')" title="Supprimer">'''
if ap_old in content:
    content = content.replace(ap_old, ap_new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Offcanvas and Details buttons injected successfully')
