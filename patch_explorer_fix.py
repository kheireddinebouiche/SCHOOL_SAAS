import re

file_path = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\saas_admin_app\saas_tenant_data_explorer.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace inline onclicks with data attributes
# 1. Remboursements
rem_old = r"onclick=\"viewDetails\('\{\{ item.id \}\}', 'Remboursement', \{'Motif': '\{\{ item.motif\|escapejs \}\}', 'Montant': '\{\{ item.montant \}\}'\}\)\""
rem_new = "class=\"btn-view-details btn btn-soft-info btn-sm rounded-circle p-0 avatar-xs me-1\" data-id=\"{{ item.id }}\" data-type=\"Remboursement\" data-motif=\"{{ item.motif }}\" data-montant=\"{{ item.montant }}\""
content = re.sub(r'class="btn btn-soft-info[^"]*"\s*' + rem_old, rem_new, content)

# 2. Operations Bancaires
ob_old = r"onclick=\"viewDetails\('\{\{ item.id \}\}', 'Operation Bancaire', \{'Compte': '\{\{ item.compte_bancaire\|escapejs \}\}'\}\)\""
ob_new = "class=\"btn-view-details btn btn-soft-info btn-sm rounded-circle p-0 avatar-xs me-1\" data-id=\"{{ item.id }}\" data-type=\"Operation Bancaire\" data-compte=\"{{ item.compte_bancaire }}\""
content = re.sub(r'class="btn btn-soft-info[^"]*"\s*' + ob_old, ob_new, content)

# 3. Demandes Paiement
dmp_old = r"onclick=\"viewDetails\('\{\{ item.id \}\}', 'Demande Paiement', \{'Client': '\{\{ item.client\|escapejs \}\}', 'Date': '\{\{ item.date_demande \}\}'\}\)\""
dmp_new = "class=\"btn-view-details btn btn-soft-info btn-sm rounded-circle p-0 avatar-xs me-1\" data-id=\"{{ item.id }}\" data-type=\"Demande Paiement\" data-client=\"{{ item.client }}\" data-date=\"{{ item.date_demande }}\""
content = re.sub(r'class="btn btn-soft-info[^"]*"\s*' + dmp_old, dmp_new, content)

# 4. Autres Produits
ap_old = r"onclick=\"viewDetails\('\{\{ item.id \}\}', 'Autre Produit', \{'Label': '\{\{ item.label\|escapejs \}\}', 'Numéro': '\{\{ item.num \}\}'\}\)\""
ap_new = "class=\"btn-view-details btn btn-soft-info btn-sm rounded-circle p-0 avatar-xs me-1\" data-id=\"{{ item.id }}\" data-type=\"Autre Produit\" data-label=\"{{ item.label }}\" data-num=\"{{ item.num }}\""
content = re.sub(r'class="btn btn-soft-info[^"]*"\s*' + ap_old, ap_new, content)

# Update JS to use event listener instead of global function
js_old = '''    function viewDetails(id, type, detailsObj) {
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
    }'''

js_new = '''    $(document).on('click', '.btn-view-details', function(e) {
        e.preventDefault();
        var id = $(this).data('id');
        var type = $(this).data('type');
        
        var detailsObj = {};
        if (type === 'Remboursement') {
            detailsObj = {'Motif': $(this).data('motif'), 'Montant': $(this).data('montant')};
        } else if (type === 'Operation Bancaire') {
            detailsObj = {'Compte': $(this).data('compte')};
        } else if (type === 'Demande Paiement') {
            detailsObj = {'Client': $(this).data('client'), 'Date': $(this).data('date')};
        } else if (type === 'Autre Produit') {
            detailsObj = {'Label': $(this).data('label'), 'Numéro': $(this).data('num')};
        }

        $('#offcanvasItemId').text('ID : ' + id);
        $('#offcanvasItemType').text(type);
        
        let htmlContent = '<ul class="list-unstyled mb-0">';
        for (const [key, value] of Object.entries(detailsObj)) {
            let valStr = (value === null || value === undefined || value === 'None' || value === '') ? '-' : value;
            htmlContent += '<li class="d-flex justify-content-between mb-2 pb-2 border-bottom border-light">' +
                           '<span class="text-muted">' + key + '</span>' +
                           '<span class="fw-medium text-end">' + valStr + '</span></li>';
        }
        htmlContent += '</ul>';
        
        $('#offcanvasContent').html(htmlContent);
        
        // Setup delete button
        $('#offcanvasDeleteBtn').off('click').on('click', function() {
            var modelKey = type.toLowerCase().replace(' ', '_').normalize("NFD").replace(/[\\u0300-\\u036f]/g, "");
            confirmDeleteDataExplorer(id, modelKey);
        });
        
        var offcanvas = new bootstrap.Offcanvas(document.getElementById('detailsOffcanvas'));
        offcanvas.show();
    });'''

if js_old in content:
    content = content.replace(js_old, js_new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated to use data attributes and removed inline backticks.")
