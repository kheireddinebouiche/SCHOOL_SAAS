import re

def update_liste_users(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject the Action link in the dropdown (Grid & List views)
    # We will search for: <li><a class="dropdown-item change-password"
    dropdown_link = '''                    <li><a class="dropdown-item configure-submenu" href="#" data-user-id="${user.id}"><i class="ri-function-line me-2 text-info"></i> Accès Finance</a></li>
'''
    content = re.sub(r'(<li><a class="dropdown-item change-password".*?</li>)', r'\1\n' + dropdown_link, content)
    
    # Grid view uses href="#" data-user-id... let's find the exact matches
    # The previous regex might match both, let's test if it did:
    
    # 2. Inject the Modal HTML
    # We will insert it before <!-- Modal de création d'utilisateur -->
    modal_html = '''<!-- Modal de Configuration Sous-Menus Finance -->
<div class="modal fade" id="submenuConfigModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header bg-soft-info">
        <div class="d-flex align-items-center">
          <div class="modal-icon-box bg-info text-white shadow-sm">
            <i class="ri-function-line fs-20"></i>
          </div>
          <div>
            <h5 class="modal-title fw-bold text-info mb-0">Accès Sous-Menus Finance</h5>
            <small class="text-muted">Configurer les sous-menus visibles pour l'utilisateur</small>
          </div>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body p-4">
        <div class="list-group" id="submenuList">
            <!-- Populated by JS -->
            <div class="text-center py-3"><div class="spinner-border text-info" role="status"></div></div>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-light" data-bs-dismiss="modal">Fermer</button>
      </div>
    </div>
  </div>
</div>
'''
    if 'submenuConfigModal' not in content:
        content = content.replace("<!-- Modal de création d'utilisateur -->", modal_html + "\n<!-- Modal de création d'utilisateur -->")
    
    # 3. Inject the JavaScript
    js_code = '''
    // Handle SubMenu Configuration click
    $(document).on('click', '.configure-submenu', function(e) {
      e.preventDefault();
      var userId = $(this).data('user-id');
      $('#submenuConfigModal').data('user-id', userId);
      $('#submenuList').html('<div class="text-center py-3"><div class="spinner-border text-info" role="status"></div></div>');
      $('#submenuConfigModal').modal('show');
      
      // Fetch current accesses
      $.ajax({
        url: "{% url 'institut_app:ApiGetSubMenuAccess' %}",
        type: 'GET',
        data: { id: userId, module_code: 'tre' },
        success: function(response) {
          if(response.status === 'success') {
            var accesses = response.data;
            var submenus = [
              {code: 'dashboard', name: 'Tableau de bord financier'},
              {code: 'tresorerie', name: 'Trésorerie'},
              {code: 'exec_edu', name: 'Executive Education'},
              {code: 'remboursement', name: 'Remboursements'},
              {code: 'remises', name: 'Remises'},
              {code: 'caisse', name: 'Caisse'},
              {code: 'banque', name: 'Banque'},
              {code: 'autres_paiements', name: 'Autres paiements'},
              {code: 'depenses', name: 'Dépenses'},
              {code: 'fournisseurs', name: 'Fournisseurs'},
              {code: 'factures', name: 'Factures'},
              {code: 'parametres', name: 'Paramètres Financiers'},
              {code: 'echeanciers', name: 'Échéanciers'}
            ];
            
            var html = '';
            submenus.forEach(function(item) {
                var isActive = accesses[item.code] ? 'checked' : '';
                html += `
                <label class="list-group-item d-flex justify-content-between align-items-center">
                    <span>${item.name}</span>
                    <div class="form-check form-switch">
                        <input class="form-check-input submenu-toggle" type="checkbox" data-submenu="${item.code}" ${isActive}>
                    </div>
                </label>`;
            });
            $('#submenuList').html(html);
          } else {
            alertify.error(response.message || "Erreur de chargement");
            $('#submenuConfigModal').modal('hide');
          }
        },
        error: function() {
          alertify.error("Erreur serveur");
          $('#submenuConfigModal').modal('hide');
        }
      });
    });

    // Handle toggle switch change
    $(document).on('change', '.submenu-toggle', function() {
        var userId = $('#submenuConfigModal').data('user-id');
        var submenuCode = $(this).data('submenu');
        var isActive = $(this).is(':checked');
        
        $.ajax({
            url: "{% url 'institut_app:ApiToggleSubMenuAccess' %}",
            type: 'POST',
            data: JSON.stringify({
                id: userId,
                module_code: 'tre',
                submenu_code: submenuCode,
                is_active: isActive
            }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            success: function(response) {
                if(response.status === 'success') {
                    alertify.success(response.message);
                } else {
                    alertify.error(response.message || "Erreur");
                    // Revert UI
                    $(this).prop('checked', !isActive);
                }
            }.bind(this),
            error: function() {
                alertify.error("Erreur de sauvegarde");
                $(this).prop('checked', !isActive);
            }.bind(this)
        });
    });
'''
    if 'ApiGetSubMenuAccess' not in content:
        content = content.replace("});\n  });\n</script>", js_code + "\n  });\n</script>")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
update_liste_users(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\users\liste_users.html')
print("Done updating liste_users.html")
