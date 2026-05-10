
$(document).ready(function () {
    // Variables pour la pagination
    let currentPage = 1;
    const recordsPerPage = 10;
    
    // Charger les promos pour le filtre
    function loadPromosForFilter() {
        $.ajax({
            url: "{% url 't_tresorerie:ApiLoadPromo' %}",
            type: "GET",
            success: function(data) {
                let options = '<option value="all">Toutes les promos</option>';
                data.forEach(function(p) {
                    if (p.id) {
                        let label = p.label || p.code || `Promotion #${p.id}`;
                        options += `<option value="${p.id}">${label}</option>`;
                    }
                });
                $('#filterPromo').html(options);
            }
        });
    }
    loadPromosForFilter();

    // Charger la liste des échéanciers
    function loadEcheanciers(page = 1) {
        currentPage = page;
        
        $.ajax({
            url: "{% url 't_tresorerie:ApiLoadEcheanciersConfigures' %}",
            dataType: "JSON",
            type: "GET",
            success: function(data) {
                if (Array.isArray(data)) {
                    // Appliquer les filtres
                    const showActive = $('#filterActive').is(':checked');
                    const showInactive = $('#filterInactive').is(':checked');
                    const promoFilter = $('#filterPromo').val();
                    
                    let filteredData = data.filter(item => {
                        // Filtre de disponibilité
                        let stateMatch = item.is_active ? showActive : showInactive;
                        
                        // Filtre de promo
                        let promoMatch = (promoFilter === 'all' || item.promo_id == promoFilter);
                        
                        return stateMatch && promoMatch;
                    });
                    
                    displayEcheanciers(filteredData, page);
                } else if (data.status === 'error') {
                    console.error("Server error:", data.message);
                    $('#listeEcheanciers').html('<tr><td colspan="9" class="text-center text-danger">Erreur serveur: ' + data.message + '</td></tr>');
                } else {
                    console.error("Unexpected response format:", data);
                    $('#listeEcheanciers').html('<tr><td colspan="9" class="text-center">Erreur de format de données</td></tr>');
                }
            },
            error: function(xhr, status, error) {
                console.log("Error loading échéanciers: " + error);
                $('#listeEcheanciers').html('<tr><td colspan="9" class="text-center">Erreur lors du chargement des données</td></tr>');
            }
        });
    }
    
    // Afficher les échéanciers dans le tableau avec groupement par promo
    function displayEcheanciers(data, page) {
        // Trier par promo puis par modèle
        data.sort((a, b) => {
            let promoComp = (a.promo_label || "").localeCompare(b.promo_label || "");
            if (promoComp !== 0) return promoComp;
            return (a.model_label || "").localeCompare(b.model_label || "");
        });
        
        const startIndex = (page - 1) * recordsPerPage;
        const endIndex = startIndex + recordsPerPage;
        const paginatedData = data.slice(startIndex, endIndex);
        const totalRecords = data.length;
        
        let row = "";
        let currentPromo = null;
        let currentModel = null;

        if(paginatedData.length > 0) {
            $.each(paginatedData, function(index, item) {
                // Ajouter un en-tête de groupe par promo
                if (item.promo_label !== currentPromo) {
                    currentPromo = item.promo_label;
                    currentModel = null; // Réinitialiser le modèle quand la promo change
                    row += `<tr class="bg-light bg-opacity-50">
                                <td colspan="10" class="py-2 px-4 border-bottom">
                                    <div class="d-flex align-items-center">
                                        <i class="ri-calendar-event-line text-primary me-2"></i>
                                        <span class="fw-bold text-primary text-uppercase small" style="letter-spacing: 0.1em;">
                                            Promotion: ${currentPromo || "N/A"}
                                        </span>
                                    </div>
                                </td>
                            </tr>`;
                }

                // Ajouter un en-tête de groupe par modèle
                if (item.model_label !== currentModel) {
                    currentModel = item.model_label;
                    row += `<tr class="bg-info bg-opacity-10">
                                <td colspan="10" class="py-1 px-5 border-bottom">
                                    <div class="d-flex align-items-center">
                                        <i class="ri-layout-grid-line text-info me-2 small"></i>
                                        <span class="fw-bold text-info small">
                                            Modèle: ${currentModel || "N/A"}
                                        </span>
                                    </div>
                                </td>
                            </tr>`;
                }

                // Déterminer le badge d'état
                let statusBadge = '';
                
                // Format the date
                var createdDate = new Date(item.created_at);
                var formattedDate = createdDate.toLocaleDateString('fr-FR', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric'
                });
                
                // Formation with specialties in tooltip
                let formationCell = "";
                if (item.is_double) {
                    formationCell = `
                        <div class="d-flex flex-column gap-1">
                            <span class="badge badge-soft-primary px-2 py-1" style="width: fit-content; font-size: 0.65rem;">
                                <i class="ri-double-quotes-l me-1"></i>DOUBLE DIPLOMATION
                            </span>
                            <div class="fw-bold text-dark d-flex align-items-center flex-wrap gap-1">
                                <span>${item.spec1 || "Spécialité 1"}</span>
                                <span class="text-muted fw-normal mx-1">&</span>
                                <span>${item.spec2 || "Spécialité 2"}</span>
                            </div>
                        </div>
                    `;
                } else {
                    formationCell = `<div class="fw-medium text-dark">${item.formation_nom}</div>`;
                }
                if (item.specialties_list) {
                    formationCell += ` <i class="ri-information-line text-info cursor-pointer" 
                                          data-bs-toggle="tooltip" 
                                          data-bs-placement="top" 
                                          title="${item.specialties_list}"></i>`;
                }
                
                row += '<tr class="align-middle echeancier-row" data-id="'+item.id+'">';
                row += '<td><div class="form-check custom-checkbox"><input type="checkbox" class="form-check-input echeancier-checkbox" data-id="'+item.id+'"></div></td>';
                row += "<td><div class='d-flex align-items-center'><div class='flex-grow-1 fw-bold text-primary'>" + item.model_label + "</div></div></td>";
                row += "<td>" + formationCell + "</td>";
                row += "<td><span class='fw-bold'>" + parseFloat(item.tarif_formation || 0).toLocaleString() + " DZD</span></td>";
                row += "<td>" + item.nombre_tranches + "</td>";
                row += "<td><span class='fw-bold'>" + parseFloat(item.frais_inscription || 0).toLocaleString() + " DZD</span></td>";
                
                let remiseText = parseFloat(item.remise || 0).toLocaleString();
                if (item.type_remise === 'pourcentage') {
                    remiseText = item.remise + " %";
                } else {
                    remiseText = remiseText + " DZD";
                }
                
                let majorationText = parseFloat(item.majoration || 0).toLocaleString();
                if (item.type_majoration === 'pourcentage') {
                    majorationText = item.majoration + " %";
                } else {
                    majorationText = majorationText + " DZD";
                }
                
                row += "<td><span class='text-danger fw-bold'>-" + remiseText + "</span></td>";
                row += "<td><span class='text-primary fw-bold'>+" + majorationText + "</span></td>";
                
                let disponibleBadge = item.is_active ? 
                    '<span class="badge bg-success-subtle text-success px-2 py-1"><i class="ri-check-line"></i></span>' : 
                    '<span class="badge bg-danger-subtle text-danger px-2 py-1"><i class="ri-close-line"></i></span>';
                
                row += "<td>" + disponibleBadge + "</td>";
                row += "<td>" + formattedDate + "</td>";
                row += '<td class="text-end">';
                row += '<div class="dropdown d-inline-block">';
                row += '<button class="btn btn-soft-info btn-sm dropdown shadow-none" type="button" data-bs-toggle="dropdown" aria-expanded="false">';
                row += '<i class="ri-more-2-fill"></i>';
                row += '</button>';
                row += '<ul class="dropdown-menu dropdown-menu-end border-0 shadow-sm">';
                row += '<li><button class="btn-detail-echeancier dropdown-item d-flex align-items-center px-3 py-2" data-id="'+item.id+'">';
                row += '<i class="ri-eye-line text-info me-2"></i>Voir détails</button></li>';
                row += '<li><button class="btn-edit-echeancier dropdown-item d-flex align-items-center px-3 py-2" data-is_default='+item.is_default+' data-status="'+item.is_active+'" data-id="'+item.id+'">';
                row += '<i class="ri-edit-line text-primary me-2"></i>Modifier</button></li>';
                
                if(item.is_active) {
                    row += '<li><button class="btn-toggle-availability dropdown-item d-flex align-items-center px-3 py-2 text-danger" data-id="'+item.id+'" data-available="false">';
                    row += '<i class="ri-close-circle-line me-2"></i>Rendre indisponible</button></li>';
                } else {
                    row += '<li><button class="btn-toggle-availability dropdown-item d-flex align-items-center px-3 py-2 text-success" data-id="'+item.id+'" data-available="true">';
                    row += '<i class="ri-checkbox-circle-line me-2"></i>Rendre disponible</button></li>';
                }
                
                row += '<li><hr class="dropdown-divider my-1"></li>';
                if(!item.is_archived) {
                    row += '<li><button class="btn-archive-echeancier dropdown-item d-flex align-items-center px-3 py-2 text-warning" data-id="'+item.id+'">';
                    row += '<i class="ri-archive-line me-2"></i>Archiver</button></li>';
                } else {
                    row += '<li><button class="btn-unarchive-echeancier dropdown-item d-flex align-items-center px-3 py-2 text-success" data-id="'+item.id+'">';
                    row += '<i class="ri-unarchive-line me-2"></i>Désarchiver</button></li>';
                }
                row += '<li><button class="btn-delete-echeancier dropdown-item d-flex align-items-center px-3 py-2 text-danger" data-id="'+item.id+'">';
                row += '<i class="ri-delete-bin-line me-2"></i>Supprimer</button></li>';
                row += '</ul>';
                row += '</div>';
                row += '</td>';
                row += '</tr>';
            });
        } else {
            row += '<tr><td colspan="10" class="text-center py-4">';
            row += '<div class="d-flex flex-column align-items-center">';
            row += '<i class="ri-calendar-check-line ri-2x text-muted mb-2"></i>';
            row += '<p class="text-muted mb-0">Aucun échéancier configuré pour le moment</p>';
            row += '<p class="text-muted small mb-0">Créez un échéancier pour le voir apparaître ici</p>';
            row += '</div>';
            row += '</td></tr>';
        }

        $('#listeEcheanciers').html(row);
        
        // Initialiser les tooltips Bootstrap
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
          return new bootstrap.Tooltip(tooltipTriggerEl)
        })
        
        // Mettre à jour les informations de pagination
        $('#startRecord').text(startIndex + 1);
        $('#endRecord').text(Math.min(endIndex, totalRecords));
        $('#totalRecords').text(totalRecords);
        
        // Générer les contrôles de pagination
        generatePagination(Math.ceil(totalRecords / recordsPerPage), page);
    }


    var globalEntites = [];
    function loadEntiteLegal(callback){
      $.ajax({
        url : '{% url "t_tresorerie:ApiLoadEntiteLegal" %}',
        dataType : "GET",
        type: "GET",
        success : function(data){
          globalEntites = data;
          var option = "<option value='0'>Sélectionnez une entite</option>";
          $.each(data, function(index, p){
            option += "<option value="+p.id+">"+p.designation+"</option>";
          });
          $('#editEcheancierEntite').html(option);
          
          if (callback && typeof callback === "function") {
            callback();
          }
        },
        error: function() {
          console.error("Erreur lors du chargement des entités légales");
          if (callback && typeof callback === "function") {
            callback();
          }
        }
      })
    }
    
    // Générer les contrôles de pagination
    function generatePagination(totalPages, currentPage) {
        let paginationHtml = '';
        
        if(totalPages > 1) {
            // Bouton précédent
            if(currentPage > 1) {
                paginationHtml += '<li class="page-item"><a class="page-link" href="#" data-page="' + (currentPage - 1) + '">Précédent</a></li>';
            } else {
                paginationHtml += '<li class="page-item disabled"><span class="page-link">Précédent</span></li>';
            }
            
            // Pages
            for(let i = 1; i <= totalPages; i++) {
                if(i === currentPage) {
                    paginationHtml += '<li class="page-item active"><span class="page-link">' + i + '</span></li>';
                } else {
                    paginationHtml += '<li class="page-item"><a class="page-link" href="#" data-page="' + i + '">' + i + '</a></li>';
                }
            }
            
            // Bouton suivant
            if(currentPage < totalPages) {
                paginationHtml += '<li class="page-item"><a class="page-link" href="#" data-page="' + (currentPage + 1) + '">Suivant</a></li>';
            } else {
                paginationHtml += '<li class="page-item disabled"><span class="page-link">Suivant</span></li>';
            }
        }
        
        $('#paginationControls').html(paginationHtml);
    }
    
    // Gestion des clics sur la pagination
    $(document).on('click', '#paginationControls .page-link', function(e) {
        e.preventDefault();
        const page = $(this).data('page');
        if(page) {
            loadEcheanciers(page);
        }
    });
    
    // Charger les échéanciers au démarrage
    loadEcheanciers();
    
    // Recherche dans le tableau
    $('#table-filter').on('keyup', function() {
        const searchTerm = $(this).val().toLowerCase();
        $("#listeEcheanciers tr").each(function() {
            const rowText = $(this).text().toLowerCase();
            if(rowText.indexOf(searchTerm) === -1 && searchTerm !== '') {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });
    
    // Appliquer les filtres
    $('#applyFilters').on('click', function() {
        // Pour l'instant, on recharge tous les échéanciers
        // Dans une implémentation complète, on enverrait les filtres au serveur
        loadEcheanciers();
    });
    
    // Voir les détails d'un échéancier
    $(document).on('click', '.btn-detail-echeancier', function() {
        var echeancierId = $(this).data('id');
        
        loadEntiteLegal(function() {
            $.ajax({
                url: "{% url 't_tresorerie:ApiLoadEcheancierDetails' %}",
                type: 'GET',
                data: { 'id': echeancierId },
                dataType: 'JSON',
            success: function(response) {
                if(response.status === 'success') {
                    var data = response.data;
                    
                    // Remplir les informations générales
                    $('#detailEcheancierModele').text(data.model_label);
                    $('#detailEcheancierFormation').text(data.formation_label || '-');
                    $('#detailEcheancierIDBadge').text('#ID-' + data.id);
                    $('#detailEcheancierTypeBadge').text(data.type_model);
                    
                    // Déterminer le badge d'état
                    let statusBadge = '';
                    if(data.is_active && !data.is_archived) {
                        statusBadge = '<span class="badge bg-success text-white px-3 py-1 rounded-pill"><i class="ri-checkbox-circle-line me-1"></i>Actif</span>';
                    } else if(!data.is_active && !data.is_archived) {
                        statusBadge = '<span class="badge bg-danger text-white px-3 py-1 rounded-pill"><i class="ri-close-circle-line me-1"></i>Inactif</span>';
                    } else {
                        statusBadge = '<span class="badge bg-warning text-white px-3 py-1 rounded-pill"><i class="ri-archive-line me-1"></i>Archivé</span>';
                    }
                    $('#summaryStatus').html(statusBadge);
                    
                    $('#detailEcheancierEntite').text(data.entite_label || 'Non définie');
                    $('#detailEcheancierFraisInscription').text(parseFloat(data.frais_inscription).toLocaleString() + ' DA');
                    
                    var tarif = parseFloat(data.tarif_formation) || 0;
                    var remise = parseFloat(data.remise) || 0;
                    var typeRemise = data.type_remise;
                    var majoration = parseFloat(data.majoration) || 0;
                    var typeMajoration = data.type_majoration;
                    
                    var actualDiscount = (typeRemise === 'pourcentage') ? (tarif * remise / 100) : remise;
                    var actualMajoration = (typeMajoration === 'pourcentage') ? (tarif * majoration / 100) : majoration;
                    var netToPay = tarif - actualDiscount + actualMajoration;

                    $('#detailEcheancierRemise').text('-' + actualDiscount.toLocaleString() + ' DA');
                    $('#summaryRemise').text(actualDiscount.toLocaleString() + ' DA');
                    
                    $('#detailEcheancierTarif').text(tarif.toLocaleString() + ' DA');
                    $('#detailEcheancierNet').text(netToPay.toLocaleString() + ' DA');
                    $('#summaryNet').text(netToPay.toLocaleString() + ' DA');
                    
                    // Remplir les tranches
                    var tranchesRow = "";
                    $('#trancheCountBadge').text(data.tranches.length + ' tranches');

                    if(data.tranches.length > 0) {
                        $.each(data.tranches, function(index, tranche) {
                            // Format the date
                            var dateEcheance = tranche.date_echeancier ? new Date(tranche.date_echeancier).toLocaleDateString('fr-FR') : '-';
                            
                            var entiteText = '<span class="text-muted small">Par défaut</span>';
                            if (tranche.entite_id && globalEntites) {
                                var ent = globalEntites.find(e => e.id == tranche.entite_id);
                                if (ent) {
                                    entiteText = `<span class="text-primary fw-medium small">${ent.designation}</span>`;
                                }
                            }
                            
                            tranchesRow += '<tr>';
                            tranchesRow += '<td class="ps-4 fw-medium text-dark">'+tranche.value+'</td>';
                            tranchesRow += '<td><span class="badge bg-primary bg-opacity-10 text-primary fw-bold">'+tranche.taux+' %</span></td>';
                            tranchesRow += '<td class="fw-bold text-dark">'+parseFloat(tranche.montant_tranche).toLocaleString()+' DA</td>';
                            tranchesRow += '<td>'+entiteText+'</td>';
                            
                            var dayLabel = "";
                            if (tranche.date_echeancier) {
                                var dParts = tranche.date_echeancier.split('-');
                                var d = new Date(dParts[0], dParts[1] - 1, dParts[2]);
                                var day = d.getDay();
                                if (day === 5 || day === 6) {
                                    var dayName = (day === 5) ? "Vendredi" : "Samedi";
                                    dayLabel = ` <span class="badge bg-danger text-white ms-1" style="font-size: 0.6rem; vertical-align: middle;">${dayName}</span>`;
                                }
                            }

                            tranchesRow += '<td class="pe-4">'+dateEcheance + dayLabel + '</td>';
                            tranchesRow += '</tr>';
                        });
                    } else {
                        tranchesRow += '<tr><td colspan="5" class="text-center py-4 text-muted small">Aucune tranche définie</td></tr>';
                    }
                    
                    $('#detailTranchesList').html(tranchesRow);
                    
                    // Afficher la modale
                    $('#detailsEcheancierModal').modal('show');
                } else {
                    alertify.error(response.message);
                }
            },
            error: function() {
                alertify.error("Erreur lors de la communication avec le serveur");
            }
            });
        });
    });
    
    
    // Archiver un échéancier
    $(document).on('click', '.btn-archive-echeancier', function() {
        var echeancierId = $(this).data('id');
        // Stocker l'ID de l'échéancier à archiver
        $('#archiveModalLabel').data('echeancierId', echeancierId);
        // Afficher la modale de confirmation
        $('.archiveModal').modal('show');
    });
    
    // Confirmer l'archivage
    $('#confirmArchiveBtn').on('click', function() {
        var echeancierId = $('#archiveModalLabel').data('echeancierId');
        // À implémenter : appel AJAX pour archiver l'échéancier
        alertify.success("Échéancier archivé avec succès");
        $('.archiveModal').modal('hide');
        loadEcheanciers();
    });
    
    // Désarchiver un échéancier
    $(document).on('click', '.btn-unarchive-echeancier', function() {
        var echeancierId = $(this).data('id');
        alertify.confirm("Désarchiver l'échéancier", "Êtes-vous sûr de vouloir désarchiver cet échéancier ?", 
            function() {
                // À implémenter : appel AJAX pour désarchiver l'échéancier
                alertify.success("Échéancier désarchivé avec succès");
                loadEcheanciers();
            },
            function() {
                // Annulation
            }
        );
    });
    
    // Supprimer un échéancier
    $(document).on('click', '.btn-delete-echeancier', function() {
        var echeancierId = $(this).data('id');
        
        
        $('#deleteModalLabel').data('echeancierId', echeancierId);
        // Afficher la modale de confirmation
        $('.deleteModal').modal('show');
    });
    
    // Confirmer la suppression
    $('#confirmDeleteBtn').on('click', function() {
        var echeancierId = $('#deleteModalLabel').data('echeancierId');
        // À implémenter : appel AJAX pour supprimer l'échéancier

        $.ajax({
          url : "{% url 't_tresorerie:ApiDeleteEcheancier' %}",
          dataType : "JSON",
          type : "POST",
          data : {
            'echeancierId' : echeancierId,
            'csrfmiddlewaretoken': '{{ csrf_token }}',
             
          },
          success: function(response){
            if (response.status === "success"){
                alertify.success("Échéancier supprimé avec succès");
                $('.deleteModal').modal('hide');
                loadEcheanciers();
            }else{
                alertify.error(response.message);
            }
          }
        });

        
    });


    $(document).on('click', '.btn-make-default', function(){
        var echeancierId = $(this).data('id');
        
        // Store the echeancier ID in the hidden input
        $('#echeancierIdToSetDefault').val(echeancierId);
        
        // Show the confirmation modal
        $('#setEcheancierDefaultModal').modal('show');
    });
    
    // Handle the confirmation button click
    $('#confirmSetDefaultBtn').on('click', function() {
        var echeancierId = $('#echeancierIdToSetDefault').val();
        
        // Hide the modal
        $('#setEcheancierDefaultModal').modal('hide');
        
        // Proceed with setting as default
        $.ajax({
            url: "{% url 't_tresorerie:ApiSetEcheancierDefault' %}",
            type: 'POST',
            data: {
                'id': echeancierId,
                'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            success: function(response) {
                if(response.status === 'success') {
                    alertify.success(response.message || "L'échéancier a été défini comme par défaut");
                    loadEcheanciers(); // Reload the list to update the UI
                } else {
                    alertify.error(response.message || "Erreur lors de la mise à jour");
                }
            },
            error: function() {
                alertify.error("Erreur de connexion au serveur");
            }
        });
    });

    // Toggle availability
    $(document).on('click', '.btn-toggle-availability', function() {
        var echeancierId = $(this).data('id');
        var available = $(this).data('available');
        
        $.ajax({
            url: "{% url 't_tresorerie:ApiToggleEcheancierAvailability' %}",
            type: 'POST',
            data: {
                'id': echeancierId,
                'available': available,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(response) {
                if(response.status === 'success') {
                    alertify.success(response.message);
                    loadEcheanciers();
                } else {
                    alertify.error(response.message);
                }
            },
            error: function() {
                alertify.error("Erreur de connexion au serveur");
            }
        });
    });

    // Modal for active echeancier editing restriction
    $(document).on('click', '.btn-edit-echeancier', function() {
      var echeancierId = $(this).data('id');
      var is_default = $(this).data('is_default');

      if(is_default == false || is_default === "false"){
        loadEcheancierForEdit(echeancierId);
      }else{
        $('#echeancierActiveModal').modal('show');
      }
    });
    
    // Function to load echeancier data for editing
    function loadEcheancierForEdit(echeancierId) {
        // First load entities, then load echeancier details
        loadEntiteLegal(function() {
            $.ajax({
                url: "{% url 't_tresorerie:ApiLoadEcheancierDetails' %}",
                type: 'GET',
                data: { 'id': echeancierId },
                dataType: 'JSON',
                success: function(response) {
                    if(response.status === 'success') {
                        var data = response.data;
                        
                        // Fill the form with data
                        $('#editEcheancierId').val(data.id);
                        $('#editEcheancierStatus').val(data.is_active ? 1 : 0);
                        
                        // Display model and formation as read-only
                        $('#editModelLabel').text(data.model_label);
                        $('#editFormationLabel').text(data.formation_label);
                        
                        // Set the entity value (now that options are loaded)
                        if (data.entite) {
                            $('#editEcheancierEntite').val(data.entite);
                        } else {
                            $('#editEcheancierEntite').val(0);
                        }

                        // Set the summary values
                        $('#editSummaryTarif').text(parseFloat(data.tarif_formation).toLocaleString() + ' DA');
                        $('#editSummaryNet').text(parseFloat(data.total_after_adjustments).toLocaleString() + ' DA');
                        
                        // Set registration fees
                        $('#editEcheancierFraisInscription').val(data.frais_inscription);
                        $('#editEcheancierRemise').val(data.remise);
                        $('#editEcheancierTypeRemise').val(data.type_remise);
                        $('#editEcheancierMajoration').val(data.majoration);
                        $('#editEcheancierTypeMajoration').val(data.type_majoration);
                        
                        // Fill the tranches - allow editing libellé and dates
                        var tranchesHtml = '';
                        if(data.tranches.length > 0) {
                            $.each(data.tranches, function(index, tranche) {
                                var dateEcheance = tranche.date_echeancier ? new Date(tranche.date_echeancier).toISOString().split('T')[0] : '';
                                
                                tranchesHtml += '<tr class="tranche-row" data-index="' + index + '">';
                                tranchesHtml += '<td><input type="text" class="form-control fw-medium border-0 bg-light rounded-2 px-3 py-2 tranche-libelle" value="' + tranche.value + '" data-id="' + (tranche.id || '') + '"></td>';
                                tranchesHtml += '<td><span class="badge bg-primary bg-opacity-10 text-primary fw-bold">' + parseFloat(tranche.taux) + ' %</span></td>';
                                tranchesHtml += '<td class="fw-bold text-dark">' + parseFloat(tranche.montant_tranche).toLocaleString() + ' DA</td>';
                                
                                // Entity Select
                                tranchesHtml += '<td>';
                                tranchesHtml += '<select class="form-select border-0 bg-light rounded-2 tranche-entite" style="font-size: 0.8rem; font-weight: 500;">';
                                tranchesHtml += '<option value="0">Global</option>';
                                $.each(globalEntites, function(i, ent) {
                                    var selected = (tranche.entite_id == ent.id) ? 'selected' : '';
                                    tranchesHtml += '<option value="' + ent.id + '" ' + selected + '>' + ent.designation + '</option>';
                                });
                                tranchesHtml += '</select>';
                                tranchesHtml += '</td>';

                                tranchesHtml += '<td>';
                                tranchesHtml += '  <div class="d-flex align-items-center gap-2">';
                                tranchesHtml += '    <input type="date" class="form-control edit-tranche-date border-0 bg-light rounded-2" value="' + dateEcheance + '" data-id="' + (tranche.id || '') + '" style="font-weight: 600;">';
                                tranchesHtml += '    <span class="edit-weekend-warning badge bg-danger text-white d-none shadow-sm" style="font-size: 0.65rem; font-weight: 700; padding: 4px 6px;"></span>';
                                tranchesHtml += '  </div>';
                                tranchesHtml += '</td>';
                                tranchesHtml += '</tr>';
                            });
                        } else {
                            tranchesHtml += '<tr><td colspan="5" class="text-center py-5 text-muted small">Aucune tranche définie</td></tr>';
                        }
                        
                        $('#editTranchesList').html(tranchesHtml);
                        
                        // Initial check for all dates
                        $('#editTranchesList .edit-tranche-date').each(function() {
                            checkEditTrancheWeekend($(this));
                        });
                        
                        // Show the modal
                        $('#editEcheancierModal').modal('show');
                    } else {
                        alertify.error("Erreur lors du chargement des données de l'échéancier");
                    }
                },
                error: function() {
                    alertify.error("Erreur lors de la communication avec le serveur");
                }
            });
        });
    }

    $(document).on('change', '.edit-tranche-date', function() {
        checkEditTrancheWeekend($(this));
    });

    function checkEditTrancheWeekend($input) {
        var dateVal = $input.val();
        var $warningContainer = $input.closest('td').find('.edit-weekend-warning');
        
        if (!dateVal) {
            $warningContainer.addClass('d-none');
            return;
        }
        
        var dateParts = dateVal.split('-');
        var date = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]);
        var day = date.getDay();
        
        if (day === 5 || day === 6) {
            var dayName = (day === 5) ? "Vendredi" : "Samedi";
            $warningContainer.html(`<i class="ri-error-warning-line"></i> ${dayName}`).removeClass('d-none');
        } else {
            $warningContainer.addClass('d-none');
        }
    }
    
    // Save echeancier changes
    $('#saveEcheancierChanges').on('click', function() {
        var echeancierId = $('#editEcheancierId').val();
        var is_active = $('#editEcheancierStatus').val();
        var entite = $('#editEcheancierEntite').val();
        var frais_inscription = $('#editEcheancierFraisInscription').val();
        var remise = $('#editEcheancierRemise').val();
        var type_remise = $('#editEcheancierTypeRemise').val();
        var majoration = $('#editEcheancierMajoration').val();
        var type_majoration = $('#editEcheancierTypeMajoration').val();
        
        // Collect tranche data (libellé and date)
        var trancheUpdates = [];
        $('#editTranchesList .tranche-row').each(function() {
            var trancheLibelleInput = $(this).find('.tranche-libelle');
            var trancheDateInput = $(this).find('.edit-tranche-date');
            var trancheEntiteSelect = $(this).find('.tranche-entite');
            var trancheId = trancheLibelleInput.data('id');
            var libelle = trancheLibelleInput.val();
            var date = trancheDateInput.val();
            var entite_id = trancheEntiteSelect.val();
            
            if(trancheId) {
                trancheUpdates.push({
                    id: trancheId,
                    value: libelle,
                    date: date,
                    entite_id: entite_id
                });
            }
        });
        
        // Prepare data for submission
        var formData = new FormData();
        formData.append('id', echeancierId);
        formData.append('is_active', is_active);
        formData.append('entite', entite);
        formData.append('frais_inscription', frais_inscription);
        formData.append('remise', remise);
        formData.append('type_remise', type_remise);
        formData.append('majoration', majoration);
        formData.append('type_majoration', type_majoration);
        formData.append('tranche_updates', JSON.stringify(trancheUpdates));
        formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
        
        // Show loading indicator
        $(this).prop('disabled', true).html('<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Enregistrement...');
        
        // Send the update request
        $.ajax({
            url: "{% url 't_tresorerie:ApiUpdateEcheancier' %}",
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            success: function(response) {
                if(response.status === 'success') {
                    alertify.success(response.message || "Échéancier mis à jour avec succès");
                    $('#editEcheancierModal').modal('hide');
                    loadEcheanciers(); // Reload the list
                } else {
                    alertify.error(response.message || "Erreur lors de la mise à jour de l'échéancier");
                }
            },
            error: function(xhr, status, error) {
                console.log("Error: ", xhr.responseText);
                alertify.error("Erreur lors de la mise à jour de l'échéancier");
            },
            complete: function() {
                // Re-enable the button
                $('#saveEcheancierChanges').prop('disabled', false).html('<i class="ri-save-line me-2"></i>Enregistrer les modifications');
            }
        });
    });


    function CheckEcheancierState(id_echeancier, callback){
        $.ajax({
          url : "{% url 't_tresorerie:ApiCheckEcheancierState' %}",
          dataType :"JSON",
          type : "GET",
          data :{
            'id_echeancier' : id_echeancier,
          },
          headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
          },
          success : function(response){
            if(response.status === "has_due_paiement"){
              callback(true);
            } else {
              callback(false);
            }
          },
          error: function() {
            callback(false); // en cas d'erreur on considère comme inactif
          }
        });
    }
    
    // Logique pour la barre d'actions groupées
    function updateBulkActionBar() {
        const selectedCount = $('.echeancier-checkbox:checked').length;
        if (selectedCount > 0) {
            $('#selectedCount').text(selectedCount);
            $('#bulkActionBar').removeClass('d-none').addClass('d-block fade-in');
        } else {
            $('#bulkActionBar').removeClass('d-block').addClass('d-none');
            $('#selectAllEcheanciers').prop('checked', false);
        }
    }

    // Sélectionner tout
    $(document).on('change', '#selectAllEcheanciers', function() {
        $('.echeancier-checkbox:not(:disabled)').prop('checked', $(this).prop('checked'));
        updateBulkActionBar();
    });

    // Sélection individuelle
    $(document).on('change', '.echeancier-checkbox', function() {
        updateBulkActionBar();
    });

    // Annuler la sélection
    $('#btnCancelSelection').on('click', function() {
        $('.echeancier-checkbox').prop('checked', false);
        $('#selectAllEcheanciers').prop('checked', false);
        updateBulkActionBar();
    });

    // Suppression groupée - Ouverture de la modale
    $('#btnBulkDelete').on('click', function() {
        const selectedCount = $('.echeancier-checkbox:checked').length;
        if (selectedCount === 0) return;
        
        $('#bulkDeleteCountText').text(selectedCount);
        $('#bulkDeleteModal').modal('show');
    });

    // Confirmation de la suppression groupée
    $('#confirmBulkDeleteBtn').on('click', function() {
        const selectedIds = $('.echeancier-checkbox:checked').map(function() {
            return $(this).data('id');
        }).get();

        if (selectedIds.length === 0) return;

        // Désactiver le bouton pendant le chargement
        $(this).prop('disabled', true).html('<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Suppression...');

        $.ajax({
            url: "{% url 't_tresorerie:ApiBulkDeleteEcheanciers' %}",
            type: 'POST',
            data: {
                'ids': JSON.stringify(selectedIds),
                'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            success: function(response) {
                if (response.status === 'success') {
                    alertify.success(response.message || "Échéanciers supprimés avec succès");
                    $('#bulkDeleteModal').modal('hide');
                    updateBulkActionBar();
                    loadEcheanciers(currentPage);
                } else {
                    alertify.error(response.message || "Une erreur est survenue lors de la suppression");
                }
            },
            error: function() {
                alertify.error("Erreur de connexion au serveur");
            },
            complete: function() {
                $('#confirmBulkDeleteBtn').prop('disabled', false).html('<i class="ri-delete-bin-line me-2"></i>Confirmer la suppression');
            }
        });
    });

});
