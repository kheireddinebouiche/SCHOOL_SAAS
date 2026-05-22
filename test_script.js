

    // === Logic for Bulk Selection and Actions ===
    let selectedIds = [];
    let currentModel = ''; // 'due_paiement' or 'paiement'

    function updateBulkBar() {
        const bar = document.getElementById('bulkActionBar');
        const countSpan = document.getElementById('selectedCount');
        if (bar && countSpan) {
            if (selectedIds.length > 0) {
                countSpan.innerText = selectedIds.length;
                bar.classList.add('show');
            } else {
                bar.classList.remove('show');
            }
        }
    }

    function syncSelectedIds(selector) {
        selectedIds = [];
        $(selector + ':checked').each(function() {
            selectedIds.push($(this).val());
        });
        updateBulkBar();
    }

    $(document).ready(function() {
        $('#selectAllDuePaiements').on('change', function() {
            const isChecked = $(this).is(':checked');
            $('.select-due-paiement').prop('checked', isChecked);
            currentModel = 'due_paiement';
            syncSelectedIds('.select-due-paiement');
        });

        $(document).on('change', '.select-due-paiement', function() {
            currentModel = 'due_paiement';
            $('.select-paiement').prop('checked', false);
            syncSelectedIds('.select-due-paiement');
        });

        $('#selectAllPaiements').on('change', function() {
            const isChecked = $(this).is(':checked');
            $('.select-paiement').prop('checked', isChecked);
            currentModel = 'paiement';
            syncSelectedIds('.select-paiement');
        });

        $(document).on('change', '.select-paiement', function() {
            currentModel = 'paiement';
            $('.select-due-paiement').prop('checked', false);
            syncSelectedIds('.select-paiement');
        });

        
        function deselectAllOthers(exceptClass) {
            const allClasses = ['.select-due-paiement', '.select-paiement', '.select-operation-bancaire', '.select-demande-paiement', '.select-remboursement', '.select-autre-produit'];
            allClasses.forEach(cls => {
                if (cls !== exceptClass) $(cls).prop('checked', false);
            });
            const allSelectAllIds = ['#selectAllDuePaiements', '#selectAllPaiements', '#selectAllOperationsBancaire', '#selectAllDemandesPaiement', '#selectAllRemboursements', '#selectAllAutresProduits'];
            allSelectAllIds.forEach(id => {
                if (!exceptClass.includes(id.replace('#selectAll', '').toLowerCase())) {
                    $(id).prop('checked', false);
                }
            });
        }

        $('#selectAllOperationsBancaire').on('change', function() {
            deselectAllOthers('.select-operation-bancaire');
            $('.select-operation-bancaire').prop('checked', $(this).is(':checked'));
            currentModel = 'operation_bancaire';
            syncSelectedIds('.select-operation-bancaire');
        });
        $(document).on('change', '.select-operation-bancaire', function() {
            deselectAllOthers('.select-operation-bancaire');
            currentModel = 'operation_bancaire';
            syncSelectedIds('.select-operation-bancaire');
        });

        $('#selectAllDemandesPaiement').on('change', function() {
            deselectAllOthers('.select-demande-paiement');
            $('.select-demande-paiement').prop('checked', $(this).is(':checked'));
            currentModel = 'demande_paiement';
            syncSelectedIds('.select-demande-paiement');
        });
        $(document).on('change', '.select-demande-paiement', function() {
            deselectAllOthers('.select-demande-paiement');
            currentModel = 'demande_paiement';
            syncSelectedIds('.select-demande-paiement');
        });

        $('#selectAllRemboursements').on('change', function() {
            deselectAllOthers('.select-remboursement');
            $('.select-remboursement').prop('checked', $(this).is(':checked'));
            currentModel = 'remboursement';
            syncSelectedIds('.select-remboursement');
        });
        $(document).on('change', '.select-remboursement', function() {
            deselectAllOthers('.select-remboursement');
            currentModel = 'remboursement';
            syncSelectedIds('.select-remboursement');
        });

        $('#selectAllAutresProduits').on('change', function() {
            deselectAllOthers('.select-autre-produit');
            $('.select-autre-produit').prop('checked', $(this).is(':checked'));
            currentModel = 'autre_produit';
            syncSelectedIds('.select-autre-produit');
        });
        $(document).on('change', '.select-autre-produit', function() {
            deselectAllOthers('.select-autre-produit');
            currentModel = 'autre_produit';
            syncSelectedIds('.select-autre-produit');
        });

\n        $('#cancelSelection').on('click', function() {
            $('.select-due-paiement, .select-paiement, #selectAllDuePaiements, #selectAllPaiements').prop('checked', false);
            selectedIds = [];
            updateBulkBar();
        });

        $('#bulkDeleteBtn').on('click', function() {
            if (selectedIds.length === 0) return;
            Swal.fire({
                title: 'Êtes-vous sûr ?',
                text: `Vous allez supprimer ${selectedIds.length} éléments. Cette action est irréversible !`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#ef4444',
                cancelButtonColor: '#64748b',
                confirmButtonText: 'Oui, supprimer tout',
                cancelButtonText: 'Annuler',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    $.ajax({
                        url: ""DJANGO"",
                        type: "POST",
                        data: {
                            'model': currentModel,
                            'ids': JSON.stringify(selectedIds),
                            'csrfmiddlewaretoken': '"DJANGO"'
                        },
                        success: function(response) {
                            if (response.status === 'success') {
                                Swal.fire('Supprimé !', response.message, 'success').then(() => location.reload());
                            } else {
                                Swal.fire('Erreur', response.message, 'error');
                            }
                        },
                        error: function() {
                            Swal.fire('Erreur', 'Une erreur est survenue lors de la suppression.', 'error');
                        }
                    });
                }
            });
        });
    });

    // === Prospect Actions ===
    const prospectModal = new bootstrap.Modal(document.getElementById('editProspectModal'));
    function openEditProspectModal(id, name, etat, statut) {
        document.getElementById('editProspectId').value = id;
        document.getElementById('editProspectName').innerText = name;
        document.getElementById('editProspectEtat').value = etat || "en_attente";
        document.getElementById('editProspectStatut').value = statut || "visiteur";
        prospectModal.show();
    }

    function saveProspectChange() {
        const id = document.getElementById('editProspectId').value;
        const etat = document.getElementById('editProspectEtat').value;
        const statut = document.getElementById('editProspectStatut').value;
        const btn = document.getElementById('saveProspectBtn');
        btn.disabled = true;
        const fd = new FormData();
        fd.append('etat', etat);
        fd.append('statut', statut);
        fd.append('csrfmiddlewaretoken', '"DJANGO"');

        fetch(`/saas-admin/api/tenant/"DJANGO"/prospect/${id}/update/`, { method: 'POST', body: fd })
            .then(r => r.json()).then(data => {
                if (data.status === 'success') location.reload();
                else Swal.fire('Erreur', data.message, 'error');
            }).finally(() => btn.disabled = false);
    }

    function confirmDeleteProspect(id) {
        Swal.fire({
            title: 'Supprimer le prospect ?',
            text: "Toutes les données associées seront supprimées.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#ef4444',
            confirmButtonText: 'Oui, supprimer !'
        }).then((res) => {
            if (res.isConfirmed) {
                const fd = new FormData();
                fd.append('action', 'delete');
                fd.append('csrfmiddlewaretoken', '"DJANGO"');
                fetch(`/saas-admin/api/tenant/"DJANGO"/prospect/${id}/update/`, { method: 'POST', body: fd })
                    .then(r => r.json()).then(() => location.reload());
            }
        });
    }

    function confirmResetProspect(id, name) {
        Swal.fire({
            title: `Réinitialiser ${name} ?`,
            text: "Cela supprimera tous les paiements et montants dus, et remettra le statut à 'Pré-inscrit'.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#f59e0b',
            confirmButtonText: 'Oui, réinitialiser !',
            cancelButtonText: 'Annuler'
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire({ title: 'Réinitialisation en cours...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
                $.ajax({
                    url: `/saas-admin/api/tenant/"DJANGO"/prospect/${id}/reset/`,
                    type: "POST",
                    data: { 'csrfmiddlewaretoken': '"DJANGO"' },
                    success: function(response) {
                        if (response.status === 'success') Swal.fire('Réinitialisé !', response.message, 'success').then(() => location.reload());
                        else Swal.fire('Erreur', response.message, 'error');
                    },
                    error: function() {
                        Swal.fire('Erreur', 'Une erreur est survenue lors de la réinitialisation.', 'error');
                    }
                });
            }
        });
    }

    // === Voeux Actions ===
    const voeuModal = new bootstrap.Modal(document.getElementById('editVoeuModal'));
    function openEditVoeuModal(id, type, currentSpecId, prospectName, currentPromoId, isConfirmed) {
        document.getElementById('editVoeuId').value = id;
        document.getElementById('editVoeuType').value = type;
        document.getElementById('editVoeuProspectName').innerText = prospectName;
        document.getElementById('editVoeuSpecialiteSelect').value = currentSpecId;
        document.getElementById('editVoeuPromoSelect').value = currentPromoId || "";
        document.getElementById('editVoeuConfirmedSelect').value = (isConfirmed === 'true' || isConfirmed === true) ? 'true' : 'false';
        voeuModal.show();
    }

    function saveVoeuChange() {
        const id = document.getElementById('editVoeuId').value;
        const type = document.getElementById('editVoeuType').value;
        const btn = document.getElementById('saveVoeuBtn');
        btn.disabled = true;
        const fd = new FormData();
        fd.append('action', 'update_specialite');
        fd.append('voeu_type', type);
        fd.append('specialite_id', document.getElementById('editVoeuSpecialiteSelect').value);
        fd.append('promo_id', document.getElementById('editVoeuPromoSelect').value);
        fd.append('is_confirmed', document.getElementById('editVoeuConfirmedSelect').value);
        fd.append('csrfmiddlewaretoken', '"DJANGO"');

        fetch(`/saas-admin/api/tenant/"DJANGO"/voeu/${id}/update/`, { method: 'POST', body: fd })
            .then(r => r.json()).then(data => {
                if (data.status === 'success') location.reload();
                else Swal.fire('Erreur', data.message, 'error');
            }).finally(() => btn.disabled = false);
    }

    function confirmDeleteVoeu(id, type) {
        Swal.fire({ title: 'Supprimer ce vœu ?', icon: 'warning', showCancelButton: true, confirmButtonColor: '#ef4444' }).then(res => {
            if (res.isConfirmed) {
                const fd = new FormData(); fd.append('action', 'delete'); fd.append('voeu_type', type); fd.append('csrfmiddlewaretoken', '"DJANGO"');
                fetch(`/saas-admin/api/tenant/"DJANGO"/voeu/${id}/update/`, { method: 'POST', body: fd })
                    .then(r => r.json()).then(() => location.reload());
            }
        });
    }

    // === Due Paiements Actions ===
    const dpModal = new bootstrap.Modal(document.getElementById('editDuePaiementModal'));
    function openEditDuePaiementModal(id, label, montant, restant, date) {
        document.getElementById('editDpId').value = id;
        document.getElementById('editDpLabel').value = label;
        document.getElementById('editDpMontantDue').value = montant;
        document.getElementById('editDpMontantRestant').value = restant;
        document.getElementById('editDpDate').value = date;
        dpModal.show();
    }

    function saveDuePaiementChange() {
        const id = document.getElementById('editDpId').value;
        const btn = document.getElementById('saveDuePaiementBtn');
        btn.disabled = true;
        const fd = new FormData(document.getElementById('editDuePaiementForm'));
        fd.append('action', 'update');
        fd.append('csrfmiddlewaretoken', '"DJANGO"');
        fetch(`/saas-admin/api/tenant/"DJANGO"/due-paiement/${id}/update/`, { method: 'POST', body: fd })
            .then(r => r.json()).then(data => location.reload()).finally(() => btn.disabled = false);
    }

    function confirmDeleteDuePaiement(id) {
        Swal.fire({ title: 'Supprimer ce montant dû ?', icon: 'warning', showCancelButton: true, confirmButtonColor: '#ef4444' }).then(res => {
            if (res.isConfirmed) {
                const fd = new FormData(); fd.append('action', 'delete'); fd.append('csrfmiddlewaretoken', '"DJANGO"');
                fetch(`/saas-admin/api/tenant/"DJANGO"/due-paiement/${id}/update/`, { method: 'POST', body: fd })
                    .then(r => r.json()).then(data => Swal.fire('Succès', data.message, 'success').then(() => location.reload()));
            }
        });
    }

    // === Paiements Actions ===
    const pModal = new bootstrap.Modal(document.getElementById('editPaiementModal'));
    function openEditPaiementModal(id, montant, date, obs) {
        document.getElementById('editPId').value = id;
        document.getElementById('editPMontant').value = montant;
        document.getElementById('editPDate').value = date;
        document.getElementById('editPObservation').value = obs;
        pModal.show();
    }

    function savePaiementChange() {
        const id = document.getElementById('editPId').value;
        const btn = document.getElementById('savePaiementBtn');
        btn.disabled = true;
        const fd = new FormData();
        fd.append('action', 'update');
        fd.append('montant_paye', document.getElementById('editPMontant').value);
        fd.append('date_paiement', document.getElementById('editPDate').value);
        fd.append('observation', document.getElementById('editPObservation').value);
        fd.append('csrfmiddlewaretoken', '"DJANGO"');
        fetch(`/saas-admin/api/tenant/"DJANGO"/paiement/${id}/update/`, { method: 'POST', body: fd })
            .then(r => r.json()).then(data => location.reload()).finally(() => btn.disabled = false);
    }

    function confirmDeletePaiement(id) {
        Swal.fire({ title: 'Supprimer ce paiement ?', text: "Le montant dû sera rétabli.", icon: 'warning', showCancelButton: true, confirmButtonColor: '#ef4444' }).then(res => {
            if (res.isConfirmed) {
                const fd = new FormData(); fd.append('action', 'delete'); fd.append('csrfmiddlewaretoken', '"DJANGO"');
                fetch(`/saas-admin/api/tenant/"DJANGO"/paiement/${id}/update/`, { method: 'POST', body: fd })
                    .then(r => r.json()).then(data => Swal.fire('Succès', data.message, 'success').then(() => location.reload()));
            }
        });
    }

    
    // Workflow: Offcanvas Details
    $(document).on('click', '.btn-view-details', function(e) {
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
            var modelKey = type.toLowerCase().replace(' ', '_').normalize("NFD").replace(/[\u0300-\u036f]/g, "");
            confirmDeleteDataExplorer(id, modelKey);
        });
        
        var offcanvas = new bootstrap.Offcanvas(document.getElementById('detailsOffcanvas'));
        offcanvas.show();
    });

    // === Global Search & Filters ===
    document.addEventListener('DOMContentLoaded', function() {
        const urlParams = new URLSearchParams(window.location.search);
        let activeTabId = urlParams.get('tab') || 'prospects';
        
        // Fallback for backward compatibility if tab param is missing
        if (!urlParams.has('tab')) {
            if (urlParams.has('v_page')) activeTabId = 'voeux';
            else if (urlParams.has('vd_page')) activeTabId = 'voeux_double';
            else if (urlParams.has('f_page')) activeTabId = 'formations';
            else if (urlParams.has('s_page')) activeTabId = 'specialites';
            else if (urlParams.has('dp_page')) activeTabId = 'due_paiements';
            else if (urlParams.has('pa_page')) activeTabId = 'paiements';
        }
        
        const tabEl = document.querySelector(`a[href="#${activeTabId}"]`);
        if (tabEl) (new bootstrap.Tab(tabEl)).show();

        const filterTable = (tableId) => {
            const table = document.getElementById(tableId);
            if (!table) return;
            const searchInput = document.querySelector(`.explorer-search[data-target="${tableId}"]`);
            const searchTerm = (searchInput ? searchInput.value : '').toLowerCase();
            const selectFilter = document.querySelector(`.explorer-filter[data-target="${tableId}"]`);
            const filterTerm = (selectFilter ? selectFilter.value : '').toLowerCase();
            const filterColumn = parseInt(selectFilter ? selectFilter.dataset.column : -1);

            table.querySelectorAll('tbody tr').forEach(row => {
                if (row.querySelector('.empty-state-container')) return;
                const text = row.innerText.toLowerCase();
                const matchesSearch = text.includes(searchTerm);
                let matchesFilter = true;
                if (filterTerm && filterColumn !== -1) {
                    if (filterTerm === 'doublon') matchesFilter = row.dataset.isDuplicate === 'true';
                    else matchesFilter = row.cells[filterColumn].innerText.toLowerCase().includes(filterTerm);
                }
                row.style.display = (matchesSearch && matchesFilter) ? '' : 'none';
            });
        };

        document.querySelectorAll('.explorer-search, .explorer-filter').forEach(el => {
            el.addEventListener(el.tagName === 'SELECT' ? 'change' : 'input', function() {
                filterTable(this.dataset.target);
            });
        });
    });

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
                fetch(`"DJANGO"`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '"DJANGO"'
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


