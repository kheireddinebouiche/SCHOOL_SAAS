
    // Configuration globale et robuste de PDF.js
    const PDF_WORKER_URL = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js';
    if (typeof pdfjsLib !== 'undefined') {
        pdfjsLib.GlobalWorkerOptions.workerSrc = PDF_WORKER_URL;
    }

    $(document).ready(function(){
        let id  = "true";
        const isTabValidationEnabled = true;
        let currentPdf = null;
        let pdfScale = 1.5;
        let currentFileUrl = "";
        var hasHandicap=null;
        let dergorationStatus = false;
        let inscription_validated = false;
        let has_completed_profile = false;
        
        // Initialisation de Select2 pour la nationalité
        $('.select2-nationality').select2({
            dropdownParent: $('#additionalInfoModal'),
            width: '100%'
        });


        // Fonction pour charger les notes
        function loadNotes(){
            $.ajax({
                url :"''",
                dataType: "JSON",
                type : 'GET',
                data:{'id_prospect' : id},
                success: function(data){
                    var html = "";

                    if (data.length > 0){
                        $.each(data, function(index, item){
                            html +='<div class="border-start border-4 border-warning ps-4 py-2 bg-white rounded-end">';
                            html +='<div class="d-flex justify-content-between align-items-start mb-2">';
                            html +='<div class="d-flex align-items-center">';
                            html +='<div class="avatar-sm me-3"><div class="avatar-title bg-warning bg-opacity-10 text-warning rounded-circle fs-5">JM</div></div>';
                            html +='<div><h6 class="mb-0 fw-semibold">'+item.created_by__username+'</h6><small class="text-muted">'+item.created_at+'</small></div>';
                            html +='</div>';
                            html +='<div class="dropdown">';
                            html +='<button class="btn btn-icon btn-sm btn-ghost-secondary" data-bs-toggle="dropdown"><i class="ri-more-2-fill"></i></button>';
                            html +='<ul class="dropdown-menu dropdown-menu-end border-0 shadow-sm">';
                            html +='<li><button class="dropdown-item d-flex align-items-center editNoteBtn" type="button" data-bs-toggle="modal" data-bs-target="#editNoteModal" data-id="'+item.id+'" data-note="'+item.note+'" data-tage="'+item.tage+'"><i class="ri-edit-line me-2"></i>Modifier</button></li>';
                            html +='<li><button class="dropdown-item d-flex align-items-center" type="button" data-bs-toggle="modal" data-id="'+item.id+'" id="deleteNoteBtn"><i class="ri-delete-bin-line me-2"></i>Supprimer</button></li>';
                            html +='</ul>';
                            html +='</div>';
                            html +='</div>';
                            html +='<p class="mb-3">'+item.note+'</p>';
                            html +='<div class="d-flex gap-2">';
                            html +='<span class="badge bg-warning-subtle text-warning">'+item.tage+'</span>';
                            html +='</div>';
                            html +='</div>';
                        });
                    }else{
                            html +='<button type="button" class="border-start border-4 border-dashed border-warning ps-4 py-4 bg-white rounded-end text-start w-100" data-bs-toggle="modal" data-bs-target="#addNoteModal">';
                            html +='<div class="d-flex align-items-center">';
                            html +='<div class="avatar-sm me-3">';
                            html +='<div class="avatar-title bg-warning bg-opacity-10 text-warning rounded-circle fs-5">';
                            html +='<i class="ri-add-line"></i>';
                            html +='</div>';
                            html +='</div>';
                            html +='<div>';
                            html +='<h6 class="fw-medium text-warning mb-0">Ajouter une note</h6>';
                            html +='<small class="text-muted">Cliquez pour ajouter une nouvelle note</small>';
                            html +='</div>';
                            html +='</div>';
                            html +='</button>';
                    }

                    $('#ListeDesNotes').html(html);
                }
            });
        }

        // Fonction pour charger la fiche de voeux
        function loadFicheVoeux(){
            $.ajax({
                url : "''",
                dataType : 'JSON',
                type : 'GET',
                data : {'id_prospect' : id},
                success : function(data){
                    var html="";
                    if (data.fiche_voeux.length > 0){
                        $.each(data.fiche_voeux, function(index, item){
                            html += '<div class="col-12 col-md-4 text-center mb-4 mb-md-0">';
                                    html += '<div class="avatar-lg mx-auto mb-4">';
                                        html += '<div class="avatar-title bg-info bg-opacity-10 text-info display-5 rounded-circle">';
                                            html += '<i class="ri-school-line"></i>';
                                        html += '</div>';
                                    html += '</div>';
                                    html += '<h6 class="fw-semibold mb-2">'+item.formation_label+'</h6>';
                                    html += '<h6 class="fw-semibold mb-2">Spécialité</h6>';
                                    html += '<p class="text-muted mb-0">'+item.specialite_label+'</p>';
                                     html += '<h6 class="fw-semibold mb-2 mt-3">Promotion/Session</h6>';
                                    html += '<p class="text-muted mb-0">'+item.promo+'</p>';
                                html += '</div>';
                                html += '<div class="col-12 col-md-8 d-flex align-items-center">';
                                    html += '<div class="vstack gap-4 w-100">';
                                        html += '<div class="d-flex align-items-center justify-content-center">';
                                            html += '<div class="d-flex align-items-center bg-light rounded-3 p-3 w-100">';
                                                html += '<div class="flex-shrink-0">';
                                                    html += '<div class="avatar-sm">';
                                                        html += '<div class="avatar-title bg-info bg-opacity-10 text-info rounded-circle">';
                                                            html += '<i class="ri-calendar-line fs-5"></i>';
                                                        html += '</div>';
                                                    html += '</div>';
                                                html += '</div>';
                                                html += '<div class="flex-grow-1 ms-3 text-center">';
                                                    html += '<h6 class="mb-1">Date de création</h6>';
                                                    html += '<small class="text-muted">'+item.created_at+'</small>';
                                                html += '</div>';
                                            html += '</div>';
                                        html += '</div>';

                                        html += '<div class="d-flex align-items-center justify-content-center">';
                                            html += '<div class="d-flex align-items-center bg-light rounded-3 p-3 w-100">';
                                                html += '<div class="flex-shrink-0">';
                                                    html += '<div class="avatar-sm">';
                                                        html += '<div class="avatar-title bg-info bg-opacity-10 text-info rounded-circle"><i class="ri-time-line fs-5"></i></div>';
                                                    html += '</div>';
                                                html += '</div>';
                                                html += '<div class="flex-grow-1 ms-3 text-center"><h6 class="mb-1">Dernière mise à jour</h6><small class="text-muted">'+item.updated_at+'</small></div>';
                                            html += '</div>';
                                        html += '</div>';
                                        
                                    html += '</div>';
                                html += '</div>';

                                $('#editVoeuxBtn').data('id',item.id);
                        });
                    }else{
                        html += '<div class="col-12 text-center py-5">';
                        html += '<div class="avatar-lg mx-auto mb-4">';
                        html += '<div class="avatar-title bg-light text-muted display-5 rounded-circle">';
                        html += '<i class="ri-file-search-line"></i>';
                        html += '</div>';
                        html += '</div>';
                        html += '<h5 class="mb-3">Aucune fiche de vœux disponible</h5>';
                        html += '<p class="text-muted mb-4">Ce prospect n\'a pas encore de fiche de vœux enregistrée.</p>';
                        html += '<button type="button" class="btn btn-soft-primary px-4 py-2" data-bs-toggle="modal" data-bs-target="#voeuxModal">';
                        html += '<i class="ri-add-line me-2"></i>Créer une fiche de vœux';
                        html += '</button>';
                        html += '</div>';
                    }

                    $('#preinscritVoeuxDetails').html(html);

                }
            });
        }

        // Fonction pour charger les informations personnelles
        function loadPersonalInfos(){
            
            $.ajax({
                url : "''",
                dataType : 'JSON',
                type : 'GET',
                data : {'id_prospect' : id},
                success : function(data){
                    $('#nom_prenom').text(data.nom + ' ' + data.prenom);
                    $('#email').text(data.email);
                    $('#phone').text(data.telephone);
                    $('#created_at').text(data.created_at);
                    $('#statut_preinscrit').text(data.statut);

                    if(data.statut_clean === "prinscrit"){
                        $('#date_changement').text(data.preinscri_date);

                    }else if(data.statut_clean === "instance"){
                        $('#date_changement').text(data.instance_date);

                    }else if(data.statut_clean === "convertit"){
                        $('#date_changement').text(data.convertit_date);
                    }else{
                        $('#date_changement').text("Aucune date trouvée");

                    }

                    $('#profile_nom_arabe').text(data.nom_arabe);
                    $('#profile_prenom_arabe').text(data.prenom_arabe);
                    $('#profile_date_naissance').text(data.date_naissance);
                    $('#profile_lieu_naissance').text(data.lieu_naissance);
                    $('#profile_pays').text(data.pays);
                    $('#profile_wilaya').text(data.wilaya);
                    $('#profile_code_zip').text(data.code_zip);
                    $('#profile_commune').text(data.commune);
                    $('#profile_nin').text(data.nin);
                    $('#profile_nationnalite').text(data.nationnalite);
                    
                    $('#profile_prenom_pere').text(data.prenom_pere);
                    $('#profile_tel_pere').text(data.indic_pere+''+data.tel_pere);
                    $('#profile_nom_mere').text(data.nom_mere);
                    $('#profile_prenom_mere').text(data.prenom_mere);
                    $('#profile_tel_mere').text(data.indic_mere+''+data.tel_mere);
                    $('#profile_tuteur_legal').text(data.tuteur_legal);
                    $('#profile_tel_tuteur').text(data.indic3+''+data.tel_tuteur);

                    if(data.has_endicap == true){
                        var p = "Oui";
                    }else{
                        var p = "Non";
                    }
                    $('#profile_has_handicap').text(p);
                    $('#profile_type_handicap').text(data.type_handicap);
                    $('#profile_groupe_sanguin').text(data.groupe_sanguin);
                    $('#profile_adresse').text(data.adresse);
                    $('#profile_niveau_scolaire').text(data.niveau_scolaire);
                    $('#profile_diplome').text(data.diplome);
                    $('#profile_specialite_diplome').text(data.specialite_obtenu || '-');
                    $('#profile_etablissement_diplome').text(data.etablissement);
                    $('#profile_annee_diplome').text(data.annee_obtention);
                    $('#profile_secu').text(data.secu);
                    
                    $('#nom_arabe').val(data.nom_arabe);
                    $('#prenom_arabe').val(data.prenom_arabe);
                    $('#date_naissance').val(data.date_naissance);
                    $('#nin').val(data.nin);
                    $('#nationnalite').val(data.nationnalite).trigger('change');
                    $('#prenom_pere').val(data.prenom_pere);
                    $('#tel_pere').val(data.tel_pere);
                    $('#indicatif_pere').val(data.indic_pere);
                    $('#indicatif_mere').val(data.indic_mere);
                    $('#nom_mere').val(data.nom_mere);
                    $('#prenom_mere').val(data.prenom_mere);
                    $('#tel_mere').val(data.tel_mere);
                    $('#type_handicap').val(data.type_handicap);
                    if(data.has_endicap == true){
                        var hand = "True";
                    }else{
                        var hand = "False";
                    }
                    $('#has_handicap').val(hand);
                    $('#groupe_sanguin').val(data.groupe_sanguin);
                    $('#adresse_prospect').val(data.adresse);
                    $('#niveau_scolaire').val(data.niveau_scolaire_pure);
                    $('#diplome').val(data.diplome);
                    $('#specialite_diplome').val(data.specialite_obtenu);
                    $('#etablissement_diplome').val(data.etablissement);
                    $('#pays').val(data.pays);
                    $('#wilaya').val(data.wilaya);
                    $('#code_zip').val(data.code_zip);
                    $('#lieu_naissance').val(data.lieu_naissance);
                    $('#commune').val(data.commune);
                    $('#annee_diplome').val(data.annee_obtention);
                    $('#secu').val(data.secu);
                    $('#filiere_prospect').val(data.filiere);

                    $('#profile_filiere').text(data.filiere || '-');

                    $('#tuteur_legal').val(data.tuteur_legal);
                    $('#tel_tuteur').val(data.tel_tuteur);
                    $('#indicatif_tuteur').val(data.indic3);

                    if(data.statut_key !== "prinscrit"){
                        document.getElementById("validatePreinscritBtn").disabled = true;
                    };

                    // Handle cancellation banner
                    if (data.motif_annulation) {
                        $('#cancellationBanner').show();
                        $('#cancellationReasonText').text(data.motif_annulation);
                        $('#btnOpenCancelModal').hide();
                    } else {
                        $('#cancellationBanner').hide();
                        if (data.statut_key === "prinscrit") {
                            $('#btnOpenCancelModal').show();
                        } else {
                            $('#btnOpenCancelModal').hide();
                        }
                    }

                    // Render History/Timeline
                    if (data.history && data.history.length > 0) {
                        $('#timeline-card').show();
                        var historyHtml = "";
                        $.each(data.history, function(index, item) {
                            var url = "";
                            if (["prinscrit", "instance", "convertit"].includes(item.statut_key)) {
                                url = "''".replace('0', item.id);
                            } else {
                                url = "''".replace('SLUG_PLACEHOLDER', item.slug);
                            }
                            
                            historyHtml += '<div class="timeline-item-v2">';
                            historyHtml += '    <div class="timeline-dot-v2"><i class="ri-checkbox-blank-circle-fill"></i></div>';
                            historyHtml += '    <a href="' + url + '" class="text-decoration-none">';
                            historyHtml += '        <div class="timeline-content-v2">';
                            historyHtml += '            <div class="timeline-date-v2">' + item.created_at + '</div>';
                            historyHtml += '            <div class="timeline-title-v2">' + item.statut + '</div>';
                            historyHtml += '            <div class="timeline-sub-v2">' + item.promo + '</div>';
                             if (item.is_double) {
                                historyHtml += '            <span class="badge bg-info-subtle text-info mt-1" style="font-size: 10px;">Double Diplomation</span>';
                            }
                            historyHtml += '        </div>';
                            historyHtml += '    </a>';
                            historyHtml += '</div>';
                        });
                        $('#linked-inscriptions-list').html(historyHtml);
                    } else {
                        $('#timeline-card').hide();
                    }
                }
            });
        }

        // Fonction pour charger les rappels/rendez-vous
        function loadRappelRendezVous(){
            $.ajax({
                url : "''",
                dataType: "JSON",
                type : "GET",
                data : {"id_prospect" : id},
                success : function(data){
                    var row = "";
                    if (data.length > 0){
                        $.each(data, function(index, item){
                            var statutBreak = "";
                            switch(item.statut){
                                case "nabouti":
                                    statutBreak = '<span class="badge bg-primary-subtle text-primary px-2 py-1"><i class="ri-time-line me-1"></i>' + item.status_label + '</span>';
                                break;

                                case "abouti":
                                    statutBreak = '<span class="badge bg-success-subtle text-success px-2 py-1"><i class="ri-time-line me-1"></i>' + item.status_label + '</span>';
                                break;

                                case "termine":
                                    statutBreak = '<span class="badge bg-danger-subtle text-danger px-2 py-1"><i class="ri-time-line me-1"></i>' + item.status_label + '</span>';
                                break;

                                case "nabouti":
                                    statutBreak = '<span class="badge bg-dark-subtle text-dark px-2 py-1"><i class="ri-time-line me-1"></i>' + item.status_label + '</span>';
                                break;

                                case "en_attent":
                                    statutBreak = '<span class="badge bg-warning-subtle text-warning px-2 py-1"><i class="ri-time-line me-1"></i>' + item.status_label + '</span>';
                                break;

                                case "annule":
                                    statutBreak = '<span class="badge bg-danger-subtle text-danger px-2 py-1"><i class="ri-time-line me-1"></i>' + item.status_label + '</span>';
                                break;

                            }
                            row += '<tr>';
                                row += '<td>';
                                    row += '<div class="d-flex align-items-center">';
                                        row += '<div class="icon-circle bg-primary bg-opacity-10 rounded-circle p-2 me-2">';
                                            row += (item.type =="appel") ? '<i class="ri-phone-line text-primary"></i>' : '<i class="ri-calendar-line text-primary"></i>';
                                        row += '</div>';
                                        row += '<span>' + item.type_label + '</span>';
                                    row += '</div>';
                                row += '</td>';
                                row += '<td>';
                                    row += '<div class="text-body">';
                                        row += '<i class="ri-time-line text-muted me-2"></i>' + item.date_rendez_vous +' '+item.heure_rendez_vous+'';

                                    row += '</div>';
                                row += '</td>';
                                row += '<td>';
                                    row += '<div class="text-wrap" style="max-width: 200px;">';
                                        row += '' + item.object + '';
                                    row += '</div>';
                                row += '</td>';
                                row += '<td>';
                                    row += ''+statutBreak+'';
                                row += '</td>';
                                row += '<td class="text-end">';
                                    row += '<div class="d-flex justify-content-end gap-2">';
                                        row += '<button class="btn btn-soft-primary btn-sm" data-bs-toggle="modal" id="editReminderBtn" data-id=' + item.id + '  title="Modifier">';
                                            row += '<i class="ri-edit-line"></i>';
                                        row += '</button>';
                                        row += '<button class="btn btn-soft-info btn-sm" data-bs-toggle="modal" id="detailsReminderBtn" data-id=' + item.id + '  title="Détails">';
                                            row += '<i class="ri-eye-line"></i>';
                                        row += '</button>';
                                        row += '<button class="btn btn-soft-success btn-sm" data-bs-toggle="modal" id="validateReminderBtn" data-id=' + item.id + '  title="Valider">';
                                            row += '<i class="ri-check-line"></i>';
                                        row += '</button>';
                                        row += '<button class="btn btn-soft-danger btn-sm" data-bs-toggle="modal" id="deleteReminderBtn" data-id=' + item.id + '  title="Supprimer">';
                                            row += '<i class="ri-delete-bin-line"></i>';
                                        row += '</button>';
                                    row += '</div>';
                                row += '</td>';
                            row += '</tr>';
                        });
                    }else{
                        row +="<tr>";
                            row += "<td colspan='5' class='text-center text-muted'>Aucun rappel ou rendez-vous trouvé</td>";
                        row += "</tr>";
                    }

                    $('#listeDesRendezVous').html(row);
                }
            });
        }
        
        // Fonction pour charger les documents
        function loadDocuments(){
            $.ajax({
                url : "''",
                dataType : "JSON",
                type: 'GET',
                data : {
                    'id_preinscrit' : id,
                },
                success : function(data){
                    var row = "";
                    if(data.length > 0){
                        $.each(data, function(index, item){
                            row += "<tr>";
                                row +="<td>"+item.label+"</td>";
                                row +="<td>"+item.id_document__label+"</td>";
                                row +="<td>"+item.created_at+"</td>";
                                row +="<td class='text-end'>";
                                    row +="<div class='d-flex justify-content-end gap-2'>";
                                        row +="<button data-url='"+item.file+"' class='btn btn-soft-info btn-sm view-doc' title='Voir'>";
                                            row +="<i class='ri-eye-line'></i>";
                                        row +="</button>";
                                        row +="<button class='btn btn-soft-success btn-sm download-doc' data-url='"+item.file+"' title='Télécharger'>";
                                            row +="<i class='ri-download-line'></i>";
                                        row +="</button>";
                                        row +="<button class='btn btn-soft-danger btn-sm delete-doc' data-id='"+item.id+"' title='Supprimer'>";
                                            row +="<i class='ri-delete-bin-line'></i>";
                                        row +="</button>";
                                    row +="</div>";
                                row +="</td>";

                            row += "</tr>";
                        });
                    }else{
                        var row = "<tr><td colspan='4' class='text-muted text-center'><div class='d-flex flex-column align-items-center justify-content-center py-5'>"+
                                        '<div class="avatar-sm mb-4">'+
                                            '<div class="avatar-title bg-light text-muted rounded-circle fs-1">'+
                                                '<i class="ri-file-paper-2-line"></i>'+
                                            '</div>'+
                                        '</div>'+
                                        '<h5 class="mb-2">Aucun document trouvé</h5>'+
                                        '<p class="text-muted mb-0">Il n\'y a aucun document enregistré pour le moment</p>'+
                                    '</div></td></tr>';
                    }
                    $('#listeDesDocuments').html(row);
                }
            });
        }

        function CheckCompletedInfos(){
            $.ajax({
                url : "''",
                dataType : "JSON",
                type : "GET",
                data : {'id_preinscrit' : id},
                success : function(response){
                    if(response.profile_completed.profile_completed  == "false"){
                        document.getElementById('incompleted_infos').hidden = false;
                        has_completed_profile = false;
                    }else{
                        document.getElementById('incompleted_infos').hidden = true;
                        has_completed_profile = true;
                        
                    }
                }
            });
        }

        CheckCompletedInfos();

        function loadSelectDocuement(){
            $.ajax({
                url : "''",
                dataType : "JSON",
                type : 'GET',
                data : {'id_preinscrit' : id},
                success : function(data){
                    var option ="<option value=''>Veuillez selection un type de document</option>";
                    $.each(data, function(index, item){
                        option += "<option value="+item.id+">"+item.label+"</option>"
                    });
                    $('#documentType').html(option);
                    
                },
            })
        }

        function handleDocs(){
             $.ajax({
                url: "''",
                dataType: "JSON",
                type: 'GET',
                data: {'id_prospect': id},
                success: function(data) {
                    var html = "";
                    
                    if (data.missing_docs && data.missing_docs.length > 0) {
                        document.getElementById('non_completed_docs').hidden = false;
                        document.getElementById('completed_docs').hidden = true;
                    } else {
                        document.getElementById('non_completed_docs').hidden = true;
                        document.getElementById('completed_docs').hidden = false;
                        
                    }
                    
                },
                error: function() {
                    $('#missingDocumentsList').html(
                        "<tr><td colspan='2' class='text-center text-danger'>Erreur lors du chargement des documents</td></tr>"
                    );
                }
            });
        }

        loadNotes();
        loadFicheVoeux();
        loadPersonalInfos();
        loadRappelRendezVous();
        loadDocuments();
        loadFinancialData(); // Charger les données financières

        $(document).on('click', '#btnReactivatePreinscrit', function() {
            var btn = $(this);
            btn.prop('disabled', true);
            
            $.ajax({
                url: "''",
                type: 'POST',
                data: {
                    'id_preinscrit': id,
                    'csrfmiddlewaretoken': 'true'
                },
                success: function(response) {
                    if (response.status === 'success') {
                        alertify.success(response.message);
                        setTimeout(function(){
                            location.reload();
                        }, 2000);
                    } else {
                        if (response.has_voeux === false) {
                            $('#reactivationNoVoeuxModal').modal('show');
                        } else {
                            alertify.error(response.message);
                        }
                        btn.prop('disabled', false);
                    }
                },
                error: function() {
                    alertify.error("Erreur lors de la communication avec le serveur.");
                    btn.prop('disabled', false);
                }
            });
        });
        
        // Initialiser l'état des boutons de navigation
        updateNavigationButtons();

        // Gestionnaires d'événements
        $(document).on('click', '#addNoteModalBtn', function(){
            $('#addNoteModal').modal('show');
        });

        $(document).on('click', '#addReminderBtn', function(){
            $('#addReminderModal').modal('show');
        });

        $(document).on('click', '#saveReminderBtn', function(){
            var type = $('#reminderType').val();
            var subject = $('#reminderSubject').val();
            var date = $('#reminderDate').val();
            var time = $('#reminderTime').val();
            var description = $('#reminderDescription').val();

            $.ajax({
                url: "''",
                dataType: 'JSON',
                type: 'POST',
                data: {
                    'type': type,
                    'subject': subject,
                    'date': date,
                    'time': time,
                    'description': description,
                    'id_prospect' : id,
                    'csrfmiddlewaretoken': 'true'
                },
                success: function(data) {
                    if (data.status === 'success') {
                        $('#addReminderModal').modal('hide');
                        loadRappelRendezVous();
                        alertify.success(data.message);
                    } else {
                        alertify.error(data.message);
                    }
                }
            });
        });

        $(document).on('click', '#saveNoteBtn', function(){
            var content = $('#content_note').val();
            var tags  = $('#note_tags').val();
            if (content === ""){
                alert("Le contenu de la note ne peut pas être vide.");
                return;
            }
            $.ajax({
                url : "''",
                dataType : 'JSON',
                type : 'POST',
                data : {
                    'id_prospect' : id,
                    'content' : content,
                    'tags' : tags,
                    'csrfmiddlewaretoken' : 'true'
                },
                success : function(data){
                    if (data.status === 'success'){
                        $('#addNoteModal').modal('hide');
                        alertify.success(response.message);
                    } else {
                        alertify.error(response.message);
                    }
                }
            });
        });



        
        // Gestion de la modification des notes
        $(document).on('click', '.editNoteBtn', function() {
            var noteId = $(this).data('id');
            var noteContent = $(this).data('note');
            var noteTage = $(this).data('tage');
            
            $('#edit_content_note').val(noteContent);
            $('#edit_note_tags').val(noteTage);
            $('#updateNoteBtn').data('id', noteId);
        });

        $('#updateNoteBtn').click(function(){
            var noteId = $(this).data('id');
            var content = $('#edit_content_note').val();
            var tage = $('#edit_note_tags').val();

            $.ajax({
                url: "''",
                type: 'POST',
                data: {
                    'id': noteId,
                    'note': content,
                    'tage': tage,
                    'csrfmiddlewaretoken': 'true'
                },
                success: function(response) {
                    if (response.status === 'success') {
                        $('#editNoteModal').modal('hide');
                        loadNotes();
loadNotes();
                        $('#content_note').val('');
                        alertify.success(data.message);
                    }else{
                        alert("Erreur lors de l'enregistrement de la note. Veuillez réessayer.");
                        alertify.error(data.message);
                    }
                }
            });
        });

        //bouton de validation de la préinscription
        $(document).on('click', '#validatePreinscritBtn', function(){
            // Vérifier si le profil et les documents sont complets avant de permettre la validation
            let profileCompleted = null;
            let documentsCompleted = null;
            
            if(dergorationStatus == false){
                // Vérifier la complétude du profil
                $.ajax({
                    url: "''",
                    dataType: "JSON",
                    type: "GET",
                    data: {'id_preinscrit': id},
                    success: function(response) {
                        profileCompleted = response.profile_completed.profile_completed  === "true";
                        updateValidationStatus(profileCompleted, documentsCompleted);
                    },
                    error: function() {
                        profileCompleted = false;
                        updateValidationStatus(profileCompleted, documentsCompleted);
                    }
                });
                
                // Vérifier la complétude des documents
                $.ajax({
                    url: "''",
                    dataType: "JSON",
                    type: 'GET',
                    data: {'id_prospect': id},
                    success: function(data) {
                        documentsCompleted = !(data.missing_docs && data.missing_docs.length > 0);
                        updateValidationStatus(profileCompleted, documentsCompleted);
                    },
                    error: function() {
                        documentsCompleted = false;
                        updateValidationStatus(profileCompleted, documentsCompleted);
                    }
                });
                
                // Fonction pour mettre à jour l'état de validation
                function updateValidationStatus(profileCompleted, documentsCompleted) {
                    // Mettre à jour l'interface de la modale de blocage
                    if (profileCompleted === true) {
                        $('#profileStatusIcon').removeClass('ri-close-circle-line text-danger').addClass('ri-checkbox-circle-line text-success');
                    } else if (profileCompleted === false) {
                        $('#profileStatusIcon').removeClass('ri-checkbox-circle-line text-success').addClass('ri-close-circle-line text-danger');
                    }
                    
                    if (documentsCompleted === true) {
                        $('#documentsStatusIcon').removeClass('ri-close-circle-line text-danger').addClass('ri-checkbox-circle-line text-success');
                    } else if (documentsCompleted === false) {
                        $('#documentsStatusIcon').removeClass('ri-checkbox-circle-line text-success').addClass('ri-close-circle-line text-danger');
                    }
                    
                    // Si les deux vérifications sont terminées
                    if (profileCompleted !== null && documentsCompleted !== null) {
                        if (profileCompleted && documentsCompleted) {
                            // Tous les critères sont remplis, afficher la modale de validation
                            $('#validatePreinscritModal').modal('show');
                        } else {
                            // Au moins un critère n'est pas rempli, afficher la modale de blocage
                            $('#validationBlockedModal').modal('show');
                        }
                    }
                }
            }else {
                 $('#validatePreinscritModal').modal('show');
            }
            


        });

        // Gestionnaire pour le bouton "Corriger les problèmes"
        $(document).on('click', '#fixIssuesBtn', function(){
            $('#validationBlockedModal').modal('hide');
            
            // Vérifier à nouveau les statuts pour déterminer où rediriger l'utilisateur
            $.ajax({
                url: "''",
                dataType: "JSON",
                type: "GET",
                data: {'id_preinscrit': id},
                success: function(response) {
                    let profileCompleted = response.profile_completed === "true";
                    
                    $.ajax({
                        url: "''",
                        dataType: "JSON",
                        type: 'GET',
                        data: {'id_prospect': id},
                        success: function(data) {
                            let documentsCompleted = !(data.missing_docs && data.missing_docs.length > 0);
                            
                            // Rediriger selon les problèmes identifiés
                            if (!profileCompleted && !documentsCompleted) {
                                // Les deux sont incomplets, demander à l'utilisateur ce qu'il veut corriger en premier
                                alertify.confirm(
                                    "Problèmes multiples",
                                    "Le profil et les documents sont incomplets. Voulez-vous d'abord compléter le profil ?",
                                    function(){
                                        // Oui, compléter le profil
                                        $('#completeAdditionalInfoBtn').click();
                                    },
                                    function(){
                                        // Non, voir les documents manquants
                                        $('#missingDocumentsModal').modal('show');
                                    }
                                ).set('labels', {ok:'Compléter le profil', cancel:'Voir documents manquants'});
                            } else if (!profileCompleted) {
                                // Seulement le profil est incomplet
                                $('#completeAdditionalInfoBtn').click();
                            } else if (!documentsCompleted) {
                                // Seulement les documents sont incomplets
                                $('#missingDocumentsModal').modal('show');
                            }
                        }
                    });
                }
            });
        });

        $(document).on('click', '#confirmeValidationBtn', function(){
            var btn = $(this); // référence du bouton
            btn.prop('disabled', true); // désactive le bouton

            // Optionnel : afficher un spinner pour indiquer le chargement
            var originalText = btn.html();
            btn.html(`
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Envoi en cours...
            `);
            $.ajax({
                url : "''",
                dataType : "JSON",
                type :"GET",
                data : {
                    'id_preinscrit' : id,
                },
                success : function(response){
                    if(response.status === "success"){
                        $('#validatePreinscritModal').modal('hide');
                        alertify.success("Pré-inscription validée avec succès");
                        $('#successFinalisationModal').modal('show');
                        loadPersonalInfos();
                    }else{
                        $('#validatePreinscritModal').modal('hide');
                        alertify.error(response.message);
                    }
                },
                complete: function() {
                    // Réactiver le bouton et restaurer son texte après la requête
                    btn.prop('disabled', false);
                    btn.html(originalText);
                }
            });              
        });

        $(document).on('click', '#editVoeuxBtn', function(){
            $('#editVoeuxModal').modal('show');
        });

        $(document).on('click', '#saveVoeuxBtn', function(){
            // Simulation d'enregistrement des voeux
            $('#editVoeuxModal').modal('hide');
            alertify.success("Fiche de voeux mise à jour avec succès");
        });

        // Gestion des documents
        $(document).on('click', '#addDocumentBtn', function(){
            loadSelectDocuement();
            $('#documentName').val(''); // Reset name
            $('#addDocumentModal').modal('show');
        });

        $(document).on('change', '#documentFile', function() {
            if (this.files && this.files[0]) {
                $('#documentName').val(this.files[0].name);
            }
        });

        // Gestion de la suppression des documents
        $(document).on('click', '.delete-doc', function(){
            documentIdToDelete = $(this).data('id');
            $('#deleteDocumentModal').modal('show');
            $('#confirmDeleteDocumentBtn').data('id', documentIdToDelete);
        });

        $(document).on('click', '#confirmDeleteDocumentBtn', function(){
            var confirmDeleteDocumentBtn = $(this).data('id')
            if(documentIdToDelete !== null){
                // Appel AJAX pour supprimer le document
                $.ajax({
                    url: "''",
                    dataType: "JSON",
                    type: 'POST',
                    data: {
                        'id_document': documentIdToDelete,
                        'csrfmiddlewaretoken': 'true'
                    },
                    success: function(response){
                        if(response.status === "success"){
                            alertify.success(response.message);
                            // Recharger la liste des documents
                            loadDocuments();
                            // Fermer la modale
                            $('#deleteDocumentModal').modal('hide');
                            // Réinitialiser l'ID du document à supprimer
                            documentIdToDelete = null;

                            handleDocs();
                        } else {
                            alertify.error(response.message);
                        }
                    },
                    error: function(){
                        alertify.error("Erreur lors de la suppression du document");
                    }
                });
            }
        });

        // Gestion du téléchargement des documents
        $(document).on('click', '.download-doc', function(){
            var documentUrl = $(this).data('url');
            // Créer un élément <a> temporaire pour déclencher le téléchargement
            var link = document.createElement('a');
            link.href = documentUrl;
            link.download = ''; // Le nom du fichier sera déterminé par le serveur
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });

        // Gestion des informations supplémentaires
        $(document).on('click', '#completeAdditionalInfoBtn', function(){
            $('#additionalInfoModal').modal('show');
        });

        $(document).on('click', '#showProfileAnywayBtn', function(){
            $('#profil_incomplet_modal').modal('hide');
            loadProfileDetails();
            $('#profileDetailsModal').modal('show');
        });

        function loadProfileDetails() {
            $.ajax({
                url: "''",
                dataType: "JSON",
                type: "GET",
                data: {'id_prospect': id},
                success: function(data) {
                    // Informations d'identité
                    $('#profile_nom_arabe').text(data.nom_arabe || '-');
                    $('#profile_prenom_arabe').text(data.prenom_arabe || '-');
                    $('#profile_date_naissance').text(data.date_naissance || '-');
                    $('#profile_nin').text(data.nin || '-');
                    $('#profile_nationnalite').text(data.nationnalite || '-');
                    
                    // Informations des parents
                    $('#profile_prenom_pere').text(data.prenom_pere || '-');
                    $('#profile_tel_pere').text(data.tel_pere || '-');
                    $('#profile_nom_mere').text(data.nom_mere || '-');
                    $('#profile_prenom_mere').text(data.prenom_mere || '-');
                    $('#profile_tel_mere').text(data.tel_mere || '-');
                    $('#indicatif_pere').val(data.indic_pere);

                    // Informations médicales
                    var hasHandicap = data.has_handicap === true ? 'Oui' : (data.has_handicap === false ? 'Non' : '-');
                    $('#profile_has_handicap').text(hasHandicap);
                    $('#profile_type_handicap').text(data.type_handicap || '-');
                    $('#profile_groupe_sanguin').text(data.groupe_sanguin || '-');
                    
                    // Informations de contact
                    $('#profile_adresse').text(data.adresse || '-');
                    
                    // Informations académiques
                    $('#profile_niveau_scolaire').text(data.niveau_scolaire || '-');
                    $('#profile_diplome').text(data.diplome || '-');
                    $('#profile_etablissement_diplome').text(data.etablissement_diplome || '-');
                    $('#profile_filiere').text(data.filiere || '-');
                },
                error: function() {
                    alertify.error("Erreur lors du chargement des détails du profil");
                }
            });
        }

        // Navigation entre les onglets avec les boutons Précédent/Suivant
        function updateNavigationButtons() {
            var activeTab = $('.nav-tabs .nav-link.active');
            var prevTab = activeTab.parent().prev('li').find('.nav-link');
            var nextTab = activeTab.parent().next('li').find('.nav-link');
            
            // Mettre à jour l'état des boutons
            if (prevTab.length === 0) {
                $('#prevTabBtn').prop('disabled', true);
            } else {
                $('#prevTabBtn').prop('disabled', false);
            }
            
            if (nextTab.length === 0) {
                $('#nextTabBtn').hide();
                $('#saveAdditionalInfoBtn').show();
            } else {
                $('#nextTabBtn').show();
                $('#saveAdditionalInfoBtn').hide();
            }
        }

        // Lorsque les onglets changent, mettre à jour les boutons
        $('a[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
            updateNavigationButtons();
        });

        function validateTab(tabId) {
            var isValid = true;
            var $tabPane = $('#additionalInfoModal ' + tabId);
            
            if ($tabPane.length === 0) return true;

            // Reset previous error states in this tab
            $tabPane.find('.is-invalid').removeClass('is-invalid');
            $tabPane.find('.select2-selection').removeClass('border-danger');

            // Find all inputs/selects in the tab pane
            $tabPane.find('input, select').each(function() {
                var field = $(this);
                var value = field.val();
                var id = field.attr('id');

                // Skip specific non-mandatory fields
                if (id === 'tuteur_legal' || id === 'indicatif_tuteur' || id === 'tel_tuteur' || id === 'type_handicap' || id === 'secu') {
                    return;
                }

                if (!value || value === "" || value === "0") {
                    isValid = false;
                    field.addClass('is-invalid');
                    if (field.hasClass('select2-hidden-accessible')) {
                        field.next('.select2-container').find('.select2-selection').addClass('border-danger');
                    }
                }
            });

            if (tabId === '#medical') {
                var hasHandicap = $('#has_handicap').val();
                if (hasHandicap === "True" && !$('#type_handicap').val()) {
                    isValid = false;
                    $('#type_handicap').addClass('is-invalid');
                }
            }

            return isValid;
        }

        function validateCurrentTab() {
            if (!isTabValidationEnabled) return true;
            var activeTabHref = $('#additionalInfoModal .nav-tabs .nav-link.active').attr('href');
            var isValid = validateTab(activeTabHref);
            if (!isValid) {
                alertify.error("Veuillez remplir tous les champs obligatoires de cet onglet");
            }
            return isValid;
        }

        // Interception robuste de TOUT changement d'onglet dans ce modal spécifique
        $('#additionalInfoModal').on('show.bs.tab', 'a[data-bs-toggle="tab"]', function (e) {
            if (!isTabValidationEnabled) return true;
            var $targetTab = $(e.target);
            var $previousTab = $(e.relatedTarget);
            
            if (!$previousTab.length) return; 

            var targetIndex = $targetTab.parent().index();
            var previousIndex = $previousTab.parent().index();
            
            if (targetIndex > previousIndex) {
                 var $tabs = $('#additionalInfoModal .nav-tabs .nav-link');
                 for (var i = previousIndex; i < targetIndex; i++) {
                     var tabHref = $($tabs[i]).attr('href');
                     if (!validateTab(tabHref)) {
                         alertify.error("Veuillez remplir tous les champs obligatoires avant d'avancer.");
                         e.preventDefault();
                         return false;
                     }
                 }
            }
        });

        $(document).on('click', '#nextTabBtn', function(){
            if (!validateCurrentTab()) return;

            var activeTab = $('.nav-tabs .nav-link.active');
            var nextTab = activeTab.parent().next('li').find('.nav-link');
            
            if (nextTab.length > 0) {
                nextTab.tab('show');
            }
            updateNavigationButtons();
        });

        $(document).on('click', '#prevTabBtn', function(){
            var activeTab = $('.nav-tabs .nav-link.active');
            var prevTab = activeTab.parent().prev('li').find('.nav-link');
            
            if (prevTab.length > 0) {
                prevTab.tab('show');
            }
            updateNavigationButtons();
        });

        // Gestion du clavier (touche Entrée) pour naviguer entre les onglets
        $('#additionalInfoModal').on('keydown', 'input, select, textarea', function(e) {
            if (e.which === 13) { // Touche Entrée
                e.preventDefault();
                $('#nextTabBtn').click();
            }
        });

        // Initialiser l'état des boutons quand la modale s'ouvre
        $('#additionalInfoModal').on('shown.bs.modal', function () {
            updateNavigationButtons();
        });

        $(document).on('click', '#saveAdditionalInfoBtn', function(){
            if (!validateCurrentTab()) return;

            // Récupération des valeurs de tous les champs
            var formData = {
                // Identité
                'nom_arabe': $('#nom_arabe').val(),
                'prenom_arabe': $('#prenom_arabe').val(),
                'date_naissance': $('#date_naissance').val(),
                'lieu_naissance' : $('#lieu_naissance').val(),
                'secu' : $('#secu').val(),
                'nin': $('#nin').val(),
                'nationnalite' : $('#nationnalite').val(),
                
                // Parents
                'prenom_pere': $('#prenom_pere').val(),
                'tel_pere': $('#tel_pere').val(),
                'indic_pere' : $('#indicatif_pere').val(),
                'nom_mere': $('#nom_mere').val(),
                'prenom_mere': $('#prenom_mere').val(),
                'tel_mere': $('#tel_mere').val(),
                'indic_mere' : $('#indicatif_mere').val(),

                'tuteur_legal' : $('#tuteur_legal').val(),
                'indic3' : $('#indicatif_tuteur').val(),
                'tel_tuteur' : $('#tel_tuteur').val(),

                
                // Médical
                'has_handicap': $('#has_handicap option:selected').text(),
                'type_handicap': $('#type_handicap').val(),
                'groupe_sanguin': $('#groupe_sanguin').val(),
                
                // Adresse
                'adresse': $('#adresse_prospect').val(),
                'commune' : $('#commune').val(),
                'pays' : $('#pays').val(),
                'wilaya' : $("#wilaya").val(),
                'code_zip' : $('#code_zip').val(),

                // Académique
                'niveau_scolaire': $('#niveau_scolaire').val(),
                'diplome': $('#diplome').val(),
                'specialite_obtenu': $('#specialite_diplome').val(),
                'etablissement_diplome': $('#etablissement_diplome').val(),
                'annee_diplome' : $('#annee_diplome').val(),
                'filiere' : $('#filiere_prospect').val(),
            };
            
            // Préparation des données pour l'affichage dans la modale de confirmation
            var confirmationHtml = "";
            
            // Identité
            confirmationHtml += '<div class="col-12"><h5 class="text-primary fw-bold border-bottom pb-2 mb-3">Informations personnelles</h5></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Nom en arabe</p><h6 class="mb-0">' + (formData.nom_arabe || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Prénom en arabe</p><h6 class="mb-0">' + (formData.prenom_arabe || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-3"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Date de naissance</p><h6 class="mb-0">' + (formData.date_naissance || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-3"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Lieu de naissance</p><h6 class="mb-0">' + (formData.lieu_naissance || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">N° identification national (NIN)</p><h6 class="mb-0">' + (formData.nin || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Nationnalite</p><h6 class="mb-0">' + (formData.nationnalite || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">N° Sécurite social</p><h6 class="mb-0">' + (formData.secu || '-') + '</h6></div></div>';
            
            // Parents
            confirmationHtml += '<div class="col-12 mt-3"><h5 class="text-success fw-bold border-bottom pb-2 mb-3">Informations des parents</h5></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Prénom père</p><h6 class="mb-0">' + (formData.prenom_pere || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Téléphone père</p><h6 class="mb-0">' + (formData.indic_pere || '-') + (formData.tel_pere || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-4"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Nom mère</p><h6 class="mb-0">' + (formData.nom_mere || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-4"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Prénom mère</p><h6 class="mb-0">' + (formData.prenom_mere || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-4"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Téléphone mère</p><h6 class="mb-0">' + (formData.indic_mere || '-') + (formData.tel_mere || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Tuteur légal</p><h6 class="mb-0">' + (formData.tuteur_legal || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Telephone</p><h6 class="mb-0">' + (formData.indic3 || '-') + (formData.tel_tuteur || '-') + '</h6></div></div>';
           
            // Médical
            confirmationHtml += '<div class="col-12 mt-3"><h5 class="text-warning fw-bold border-bottom pb-2 mb-3">Informations médicales</h5></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Handicap</p><h6 class="mb-0">' + (formData.has_handicap || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Type handicap</p><h6 class="mb-0">' + (formData.type_handicap || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-12"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Groupe sanguin</p><h6 class="mb-0">' + ($('#groupe_sanguin option:selected').text() || '-') + '</h6></div></div>';
            
            // Adresse
            confirmationHtml += '<div class="col-12 mt-3"><h5 class="text-info fw-bold border-bottom pb-2 mb-3">Informations de contact</h5></div>';
            confirmationHtml += '<div class="col-12"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Adresse</p><h6 class="mb-0">' + (formData.adresse || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-3"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Commune</p><h6 class="mb-0">' + (formData.commune || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-3"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Wilya</p><h6 class="mb-0">' + (formData.wilaya || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-3"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Pays</p><h6 class="mb-0">' + (formData.pays || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-3"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Code postal</p><h6 class="mb-0">' + (formData.code_zip || '-') + '</h6></div></div>';
            
            // Académique
            confirmationHtml += '<div class="col-12 mt-3"><h5 class="text-primary fw-bold border-bottom pb-2 mb-3">Informations académiques</h5></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Niveau scolaire</p><h6 class="mb-0">' + (formData.niveau_scolaire || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-6"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Filière</p><h6 class="mb-0">' + (formData.filiere || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-4"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Diplôme</p><h6 class="mb-0">' + (formData.diplome || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-md-4"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Spécialité</p><h6 class="mb-0">' + (formData.specialite_obtenu || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-8"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Etablissement d\'obtention</p><h6 class="mb-0">' + (formData.etablissement_diplome || '-') + '</h6></div></div>';
            confirmationHtml += '<div class="col-4"><div class="bg-light rounded-3 p-3 h-100"><p class="mb-1 text-muted">Année d\'obtention</p><h6 class="mb-0">' + (formData.annee_diplome || '-') + '</h6></div></div>';
            
            // Affichage des données dans la modale de confirmation
            $('#confirmationDetails').html(confirmationHtml);
            
            // Affichage de la modale de confirmation
            $('#additionalInfoModal').modal('hide');
            $('#confirmAdditionalInfoModal').modal('show');
        });

        function loadDataToUpdate(filiere,tuteur_legal,indicatif_tuteur,tel_tuteur,secu,annee_diplome,commune,wilaya,code_zip,pays,lieu_naissance,nom_arabe,prenom_arabe,date_naissance,nin,nationnalite,prenom_pere,tel_pere,nom_mere,prenom_mere,tel_mere,has_handicap,type_handicap,groupe_sanguin,adresse,niveau_scolaire,diplome,etablissement_diplome,indic_pere,indic_mere,specialite_obtenu){
            $.ajax({
                url : "''",
                dataType: "JSON",
                type : "POST",
                data : {
                    'nom_arabe' : nom_arabe,
                    'prenom_arabe' : prenom_arabe,
                    'date_naissance' : date_naissance,
                    'nin' : nin,
                    'nationnalite' : nationnalite,
                    'prenom_pere' : prenom_pere,
                    'tel_pere' : tel_pere,
                    'nom_mere' : nom_mere,
                    'prenom_mere' : prenom_mere,
                    'tel_mere' : tel_mere,
                    'has_handicap' : has_handicap,
                    'type_handicap' : type_handicap,
                    'groupe_sanguin' : groupe_sanguin,
                    'adresse' : adresse,
                    'niveau_scolaire' : niveau_scolaire,
                    'diplome' : diplome,
                    'specialite_obtenu' : specialite_obtenu,
                    'filiere' : filiere,
                    'etablissement_diplome' : etablissement_diplome,
                    'id_preinscrit' : id,
                    'pays' : pays,
                    'wilaya' : wilaya,
                    'code_zip' : code_zip,
                    'lieu_naissance' : lieu_naissance,
                    'indic_pere' : indic_pere,
                    'indic_mere' : indic_mere,
                    'secu' : secu,

                    'commune' : commune,
                    'annee_diplome' : annee_diplome,

                    'tuteur_legal' : tuteur_legal,
                    'indicatif_tuteur' : indicatif_tuteur,
                    'tel_tuteur' : tel_tuteur,

                    'csrfmiddlewaretoken': 'true',
                },

                success : function(response){
                if (response.status == "success"){
                        alertify.success(response.message);
                        $('#confirmAdditionalInfoModal').modal('hide');
                        loadPersonalInfos();
                        loadFinancialData(); 
                        CheckCompletedInfos();
                }else{
                    alertify.error("Une erreur c'est produite lors du traitement de la requête");
                }
            }
            })
        }
        
        $(document).on('click', '#confirmSaveAdditionalInfoBtn', function(){
            // Récupération des valeurs des champs sous forme de variables individuelles
            var nom_arabe = $('#nom_arabe').val();
            var prenom_arabe = $('#prenom_arabe').val();
            var date_naissance = $('#date_naissance').val();
            var nin = $('#nin').val();
            var nationnalite = $("#nationnalite").val();
            var prenom_pere = $('#prenom_pere').val();
            var tel_pere = $('#tel_pere').val();
            var nom_mere = $('#nom_mere').val();
            var prenom_mere = $('#prenom_mere').val();
            var tel_mere = $('#tel_mere').val();
            var has_handicap = $('#has_handicap').val();
            var type_handicap = $('#type_handicap').val();
            var groupe_sanguin = $('#groupe_sanguin').val();
            var adresse = $('#adresse_prospect').val();
            var niveau_scolaire = $('#niveau_scolaire').val();
            var diplome = $('#diplome').val();
            var etablissement_diplome = $('#etablissement_diplome').val();
            var indic_pere = $('#indicatif_pere').val();
            var indic_mere = $('#indicatif_mere').val();
            var commune = $('#commune').val();
            var annee_diplome = $("#annee_diplome").val();

            var pays = $('#pays').val();
            var wilaya = $('#wilaya').val();
            var code_zip = $('#code_zip').val();
            var lieu_naissance = $('#lieu_naissance').val();
            var secu = $("#secu").val();
            var specialite_obtenu = $('#specialite_diplome').val();

            var tuteur_legal = $('#tuteur_legal').val();
            var indicatif_tuteur = $('#indicatif_tuteur').val();
            var tel_tuteur = $('#tel_tuteur').val();
            var filiere = $('#filiere_prospect').val();
                        
            
            loadDataToUpdate(filiere,tuteur_legal,indicatif_tuteur,tel_tuteur,secu,annee_diplome,commune,wilaya,code_zip,pays,lieu_naissance,nom_arabe,prenom_arabe,date_naissance,nin,nationnalite,prenom_pere,tel_pere,nom_mere,prenom_mere,tel_mere,has_handicap,type_handicap,groupe_sanguin,adresse,niveau_scolaire,diplome,etablissement_diplome,indic_pere,indic_mere,specialite_obtenu)
                      
        });
  
        document.getElementById("saveDocumentBtn").addEventListener("click", function () {
            let btn = this; // Référence du bouton
            btn.disabled = true; // Désactiver le bouton
            let originalText = btn.innerHTML; // Sauvegarder le texte original

            // Afficher un spinner pendant le chargement
            btn.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Enregistrement...
            `;

            let name = document.getElementById("documentName").value;
            let type = document.getElementById("documentType").value;
            let fileInput = document.getElementById("documentFile");
            let file = fileInput.files[0];

            if (!name || !type || !file) {
                alertify.error("Veuillez remplir tous les champs (Type de document et Fichier)");
                btn.disabled = false;
                btn.innerHTML = originalText;
                return;
            }

            // Validation de la taille du fichier (client-side)
            const maxLimitKb = true;
            if (file.size > maxLimitKb * 1024) {
                alertify.error(`Le fichier est trop volumineux (${(file.size / 1024).toFixed(1)} KB). La limite est de ${maxLimitKb} KB.`);
                btn.disabled = false;
                btn.innerHTML = originalText;
                return;
            }

            let formData = new FormData();
            formData.append("name", name);
            formData.append("type", type);
            formData.append("file", file);
            formData.append("csrfmiddlewaretoken", "true");
            formData.append("id_prospect", id); 

            fetch("''", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alertify.success("Le document a été ajouté avec succès");
                    $('#addDocumentModal').modal('hide');
                    loadDocuments();
                    handleDocs();
                } else {
                    alertify.error(data.error || "Erreur lors de l'ajout du document");
                }
            })
            .catch(error => {
                console.error("Erreur AJAX:", error);
                alertify.error("Une erreur s'est produite !");
            })
            .finally(() => {
                // Réactiver le bouton dans tous les cas
                btn.disabled = false;
                btn.innerHTML = originalText;
            });
        });

        // --- Visualiseur de Document Premium ---
        $(document).on("click", ".view-doc", function () {
            currentFileUrl = $(this).data("url");
            const fileName = currentFileUrl.split('/').pop();
            
            // Reset UI
            $("#previewContent").html("").hide();
            $("#pdfPreviewContainer").hide();
            $("#pdfToolbar").attr('style', 'display: none !important');
            $("#pdfMetaInfo").text(fileName);
            $("#btnDownloadDoc").attr("href", currentFileUrl).attr("download", fileName);
            
            if (currentFileUrl.match(/\.(jpeg|jpg|png|gif|bmp|webp)$/i)) {
                // Rendu IMAGE
                $("#previewContent").show().html(`
                    <img src="${currentFileUrl}" class="img-fluid rounded-4 shadow-lg border" style="max-height: 70vh;">
                `);
                $("#pdfMetaInfo").text(fileName + " (Image)");
            } 
            else if (currentFileUrl.match(/\.pdf$/i)) {
                // Rendu PDF
                $("#pdfToolbar").attr('style', 'display: flex !important');
                $("#pdfPreviewContainer").show();
                $("#pdfPagesContainer").html(`
                    <div id="loadingOverlay" class="text-center p-5">
                        <div class="spinner-grow text-primary mb-3" role="status"></div>
                        <h6 class="fw-bold text-primary">Initialisation du moteur PDF...</h6>
                    </div>
                `);

                renderPdf(currentFileUrl);
            } else {
                $("#previewContent").show().html(`
                    <div class="p-5 text-center">
                        <i class="ri-file-unknow-line display-4 text-muted mb-3"></i>
                        <h5 class="text-muted">Aperçu non disponible</h5>
                        <a href="${currentFileUrl}" class="btn btn-primary rounded-pill mt-3" download>Télécharger pour consulter</a>
                    </div>
                `);
            }

            $("#previewDocumentModal").modal("show");
        });

        // Fonction de Rendu PDF Séquentiel
        async function renderPdf(url, scale = 1.5) {
            try {
                pdfjsLib.GlobalWorkerOptions.workerSrc = PDF_WORKER_URL;
                const loadingTask = pdfjsLib.getDocument({
                    url: url,
                    cMapUrl: 'https://cdn.jsdelivr.net/npm/pdfjs-dist@3.4.120/cmaps/',
                    cMapPacked: true,
                });
                
                currentPdf = await loadingTask.promise;
                $("#totalPageNum").text(currentPdf.numPages);
                $("#pdfMetaInfo").text(`Document PDF • ${currentPdf.numPages} pages`);
                $("#pdfPagesContainer").html("");

                for (let i = 1; i <= currentPdf.numPages; i++) {
                    const canvasId = `pdf-canvas-${i}`;
                    $("#pdfPagesContainer").append(`
                        <div class="pdf-page-card bg-white shadow rounded-3 mb-4 p-2 transition-all" style="max-width: 100%;">
                            <canvas id="${canvasId}" style="width: 100%; height: auto; display: block; border-radius: 4px;"></canvas>
                        </div>
                    `);

                    const page = await currentPdf.getPage(i);
                    const viewport = page.getViewport({ scale: scale });
                    const canvas = document.getElementById(canvasId);
                    const context = canvas.getContext('2d');
                    
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;

                    await page.render({
                        canvasContext: context,
                        viewport: viewport
                    }).promise;
                }
            } catch (err) {
                console.error("Erreur PDF:", err);
                $("#pdfPagesContainer").html(`
                    <div class="alert alert-danger m-4 rounded-4 shadow-sm border-0">
                        <i class="ri-error-warning-line me-2"></i> Erreur lors du chargement : ${err.message}
                    </div>
                `);
            }
        }

        // Contrôles de Zoom
        $("#btnZoomIn").on("click", function() {
            pdfScale += 0.25;
            if (pdfScale > 3) pdfScale = 3;
            updateZoomDisplay();
            renderPdf(currentFileUrl, pdfScale);
        });

        $("#btnZoomOut").on("click", function() {
            pdfScale -= 0.25;
            if (pdfScale < 0.5) pdfScale = 0.5;
            updateZoomDisplay();
            renderPdf(currentFileUrl, pdfScale);
        });

        function updateZoomDisplay() {
            $("#zoomLevel").text(Math.round(pdfScale * 100) + "%");
        }

        // Détection de la page active au scroll
        $("#pdfPreviewContainer").on("scroll", function() {
            const container = $(this);
            const cards = $(".pdf-page-card");
            let activePage = 1;

            cards.each(function(index) {
                const card = $(this);
                if (card.position().top < 200) {
                    activePage = index + 1;
                }
            });
            $("#currentPageNum").text(activePage);
        });
     
        handleDocs();

        // Fonction pour charger les documents manquants
        function loadMissingDocuments() {
            $.ajax({
                url: "''",
                dataType: "JSON",
                type: 'GET',
                data: {'id_prospect': id},
                success: function(data) {
                    var html = "";
                    
                    if (data.missing_docs && data.missing_docs.length > 0) {
                        $.each(data.missing_docs, function(index, doc) {
                            html += "<tr>";
                            html += "<td>" + doc.label + "</td>";
                            html += "<td class='text-center'>";
                            html += "<button class='btn btn-sm btn-primary add-missing-doc' data-doc-id='" + doc.id + "'>";
                            html += "<i class='ri-add-line me-1'></i>Ajouter";
                            html += "</button>";
                            html += "</td>";
                            html += "</tr>";
                        });
                    } else {
                        html += "<tr>";
                        html += "<td colspan='2' class='text-center text-success'>";
                        html += "<i class='ri-checkbox-circle-line fs-4 me-2'></i>";
                        html += "Tous les documents requis ont été fournis";
                        html += "</td>";
                        html += "</tr>";
                    }
                    
                    $('#missingDocumentsList').html(html);
                },
                error: function() {
                    $('#missingDocumentsList').html(
                        "<tr><td colspan='2' class='text-center text-danger'>Erreur lors du chargement des documents</td></tr>"
                    );
                }
            });
        }

        // Charger les documents manquants quand la modale s'ouvre
        $('#missingDocumentsModal').on('shown.bs.modal', function () {
            loadMissingDocuments();
        });

        // Rafraîchir la liste des documents manquants
        $(document).on('click', '#refreshMissingDocsBtn', function() {
            loadMissingDocuments();
        });

        // Gérer le clic sur le bouton d'ajout de document manquant
        $(document).on('click', '.add-missing-doc', function() {
            var docId = $(this).data('doc-id');
            // Charger les types de documents dans la modale d'ajout
            loadSelectDocuement();
            // Sélectionner automatiquement le document concerné
            $('#documentType').val(docId);
            // Fermer la modale des documents manquants
            $('#missingDocumentsModal').modal('hide');
            // Ouvrir la modale d'ajout de document
            $('#addDocumentModal').modal('show');
        });
        
        function showDerogationDetails(date_de_demande,statut,motif,date_de_traitement,observation){
            $('#derogation-date-demande').html(date_de_demande);
            $('#derogation-motif-demande').html(motif);
            $('#derogation-status').html(statut);
            $('#derogation-date-traitement').html(date_de_traitement);
            $('#derogation-commentaire-traitement').html(observation);
        }

        // Fonction pour vérifier l'état de la dérogation
        function checkDerogationStatus() {
            $.ajax({
                url: "''",
                dataType: "JSON",
                type: "GET",
                data: {'id_preinscrit': id},
                success: function(response) {

                     showDerogationDetails(
                        response.data.date_de_demande,
                        response.data.statut,
                        response.data.motif,
                        response.data.date_de_traitement,
                        response.data.observation
                    ); 

                    if (response.status === 'acceptee') {
                        document.getElementById('derogation_acceptee').hidden = false;
                        document.getElementById('derogation_refusee').hidden = true;
                        document.getElementById('derogation_attente').hidden = true;
                        document.getElementById('requestValidationBtn').disabled = false;
                        dergorationStatus = true;

                        
                    } else if (response.status === 'rejetee') {
                        document.getElementById('derogation_acceptee').hidden = true;
                        document.getElementById('derogation_refusee').hidden = false;
                        document.getElementById('derogation_attente').hidden = true;
                        document.getElementById('requestValidationBtn').disabled = false;


                    } else if(response.status === "en_attente"){
                        document.getElementById('derogation_attente').hidden = false;
                        document.getElementById('derogation_acceptee').hidden = true;
                        document.getElementById('derogation_refusee').hidden = true;
                        document.getElementById('requestValidationBtn').disabled = true;
                    }else{

                    }
                },
                error: function() {
                    // En cas d'erreur, cacher les deux notifications
                    document.getElementById('derogation_acceptee').hidden = true;
                    document.getElementById('derogation_refusee').hidden = true;
                    document.getElementById('derogation_attente').hidden = true;
                    document.getElementById('requestValidationBtn').disabled = false;

                }
            });
        }

        // Charger l'état de la dérogation au chargement de la page
        checkDerogationStatus();  

        $(document).on('click', '#requestValidationBtn', function(){
            $('#requestManagerValidationModal').modal('show');  
        });

         // Gérer la soumission de la demande de validation par un responsable
        $(document).on('click', '#submitValidationRequestBtn', function() {

            var btn = $(this); // référence du bouton
            btn.prop('disabled', true); // désactive le bouton

            // Optionnel : afficher un spinner pour indiquer le chargement
            var originalText = btn.html();
            btn.html(`
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Envoi en cours...
            `);

            var reason = $('#validationRequestReason').val();
            
            $.ajax({
                url : '''',
                dataType: 'JSON',
                type: 'POST',
                data : {
                    'id_preinscrit' : id,
                    'reason' : reason,
                    'csrfmiddlewaretoken': 'true',
                },
                success : function(response){
                    if (response.status === "success") {
                        alertify.success(response.message);
                        checkDerogationStatus();
                        $('#requestManagerValidationModal').modal('hide');
                        $('#validationRequestReason').val('');

                    }else{
                        alertify.error(response.message);
                    }
                },
                 complete: function() {
                    // Réactiver le bouton et restaurer son texte après la requête
                    btn.prop('disabled', false);
                    btn.html(originalText);
                }
            });      
        });

        // Fonction pour charger les données financières du pré-inscrit
        function loadFinancialData(){
            $.ajax({
                url : "''",
                dataType: "JSON",
                type: "GET",
                data : {'id_preinscrit' : id},
                success: function(data){
                    // Mise à jour des éléments avec les données financières
                    $('#montant-total').text(data.montant_total + ' DZD');
                    $('#montant-paye').text(data.montant_paye + ' DZD');
                    $('#solde').text(parseFloat(data.montant_total - data.montant_paye) + ' DZD');
                    
                    // Mise à jour des couleurs en fonction du solde
                    if (data.solde > 0) {
                        $('#solde').removeClass('text-success text-info').addClass('text-warning');
                    } else if (data.solde < 0) {
                        $('#solde').removeClass('text-success text-warning').addClass('text-info');
                    } else {
                        $('#solde').removeClass('text-info text-warning').addClass('text-success');
                    }
                },
                error: function(){
                    // En cas d'erreur, afficher des valeurs par défaut
                    $('#montant-total').text('0,00 DZD');
                    $('#montant-paye').text('0,00 DZD');
                    $('#solde').text('0,00 DZD');
                }
            });
        }

        function loadRemiderDetailsForUpdate(id_rendez_vous){
            $.ajax({
                url : "''",
                dataType: "JSON",
                type: "GET",
                data : {'id_rendez_vous' : id_rendez_vous},
                success: function(data){
                    $('#editDescriptionRemider').val(data[0].description);
                    $('#editDateReminder').val(data[0].date_rendez_vous);
                    $('#editTimeReminer').val(data[0].heure_rendez_vous);
                    $('#editObjectReminder').val(data[0].object);
                    $('#editTypeReminder').val(data[0].type);

                    $('#reminder-type').text(data[0].type_label)
                    $('#reminder-date-time').text(data[0].heure_rendez_vous)
                    $('#reminder-object').text(data[0].object)
                    $('#reminder-status').text(data[0].statut_label)
                    $('#reminder-description').text(data[0].description)


                    
                }
            });
        }

        $(document).on('click', '#editReminderBtn', function(){
            var id_reminder = $(this).data('id');
            loadRemiderDetailsForUpdate(id_reminder);
            $('#editReminderBtnSave').data('id', id_reminder);
            $('#editReminderModal').modal('show');
        });

        $(document).on('click','#editReminderBtnSave', function(){
            var editedDescription = $('#editDescriptionRemider').val();
            var editedType = $('#editTypeReminder').val();
            var editedDate = $('#editDateReminder').val();
            var editedTime = $('#editTimeReminer').val();
            var editedObject = $('#editObjectReminder').val();
            var id_rappel = $(this).data('id');
            $.ajax({
                url : "''",
                dataType : 'JSON',
                type: 'POST',
                data : {
                    'id_rappel' : id_rappel,
                    'type' : editedType,
                    'subject' : editedObject,
                    'date' : editedDate,
                    'time' : editedTime,
                    'description' : editedDescription,
                    'csrfmiddlewaretoken' : 'true'
                },

                success : function(response){
                    if(response.status == "success"){
                        alertify.success(response.message);
                        loadRappelRendezVous();
                        $('#editReminderModal').modal('hide');
                        
                    }else{
                        alertify.error(response.message);
                    }
                }
            })
        });

        $(document).on('click', '#detailsReminderBtn', function(){
            var id_reminder = $(this).data('id');
            loadRemiderDetailsForUpdate(id_reminder);
            $('#detailsReminderModal').modal('show');
        });

        $(document).on('click', '#validateReminderBtn', function(){
            var id_reminder = $(this).data('id');
            $('#confirmValidateReminderBtn').data('id', id_reminder);
            $('#validateReminderModal').modal('show');
        });

        $(document).on('click','#confirmValidateReminderBtn', function(){
            var id_reminder = $(this).data('id');
            var description = $('#observation_rappel').val();
            var statut_reminder = $('#validate_statut_reminder').val();

            $.ajax({
                url : "''",
                dataType : "JSON",
                type: 'POST',
                data : {
                    'id_reminder' : id_reminder,
                    'description' : description,
                    'statut_reminder' : statut_reminder,
                    'csrfmiddlewaretoken': 'true'
                },
                success : function(response){
                    if(response.status === "success"){
                        alertify.success("La validation du rappel a été effecuter avec succès");
                        loadRappelRendezVous();
                        $('#validateReminderModal').modal('hide');
                    }else{
                        alertify.error("Une erreur c'est produite lors du traitement de la requete !");
                    }
                }
            })
        });

        $(document).on('click', '#deleteReminderBtn', function(){
            var id_reminder = $(this).data('id');
            $('#ConfirmDeleteReminderBtn').data('id', id_reminder);
            $('#deleteReminderModal').modal('show');
        });

        $(document).on('click','#ConfirmDeleteReminderBtn', function(){
            var id_reminder = $(this).data('id');
            $.ajax({
                url :"''",
                dataType : "JSON",
                type: "GET",
                data : {
                    'id_reminder' :  id_reminder,
                },
                success : function(response){
                    if (response.status === "success"){
                        alertify.success("Suppression effectué avec succès");
                        loadRappelRendezVous();
                        $('#deleteReminderModal').modal('hide');
                    }else{  
                        alertify.error("Une erreur c'est produite lors du traitement de la requete !");
                    }
                }
            });
        });

        $(document).on('click', '#viewProfileBtn', function(){
            if (!has_completed_profile){
                $('#profil_incomplet_modal').modal('show');
            }else{
                $('#profileDetailsModal').modal('show');
            }
        });

        $(document).on('click', "#completerProfilBtn",function(){
            $("#profil_incomplet_modal").modal('hide');
            $('#additionalInfoModal').modal('show');
        }); 
       
        document.getElementById('tel_pere').addEventListener('input', function (e) {
            // 1️⃣ On récupère la valeur et on garde uniquement les chiffres
            let value = e.target.value.replace(/\D/g, '');

            // 2️⃣ Si le premier caractère est un 0, on le supprime
            if (value.startsWith('0')) {
                value = value.slice(1);
            }

            // 3️⃣ Reformater selon le schéma XXX-XX-XX-XX
            let formatted = '';
            if (value.length > 0) formatted += value.substring(0, 3);
            if (value.length >= 4) formatted += '-' + value.substring(3, 5);
            if (value.length >= 6) formatted += '-' + value.substring(5, 7);
            if (value.length >= 8) formatted += '-' + value.substring(7, 9);

            // 4️⃣ Réinjecter la valeur formatée dans le champ
            e.target.value = formatted;
        });

        document.getElementById('tel_mere').addEventListener('input', function (e) {
            // 1️⃣ On récupère la valeur et on garde uniquement les chiffres
            let value = e.target.value.replace(/\D/g, '');

            // 2️⃣ Si le premier caractère est un 0, on le supprime
            if (value.startsWith('0')) {
                value = value.slice(1);
            }

            // 3️⃣ Reformater selon le schéma XXX-XX-XX-XX
            let formatted = '';
            if (value.length > 0) formatted += value.substring(0, 3);
            if (value.length >= 4) formatted += '-' + value.substring(3, 5);
            if (value.length >= 6) formatted += '-' + value.substring(5, 7);
            if (value.length >= 8) formatted += '-' + value.substring(7, 9);

            // 4️⃣ Réinjecter la valeur formatée dans le champ
            e.target.value = formatted;
        });

        document.getElementById('tel_tuteur').addEventListener('input', function (e) {
            // 1️⃣ On récupère la valeur et on garde uniquement les chiffres
            let value = e.target.value.replace(/\D/g, '');

            // 2️⃣ Si le premier caractère est un 0, on le supprime
            if (value.startsWith('0')) {
                value = value.slice(1);
            }

            // 3️⃣ Reformater selon le schéma XXX-XX-XX-XX
            let formatted = '';
            if (value.length > 0) formatted += value.substring(0, 3);
            if (value.length >= 4) formatted += '-' + value.substring(3, 5);
            if (value.length >= 6) formatted += '-' + value.substring(5, 7);
            if (value.length >= 8) formatted += '-' + value.substring(7, 9);

            // 4️⃣ Réinjecter la valeur formatée dans le champ
            e.target.value = formatted;
        });

        // Annulation de la préinscription
        $(document).on('click', '#btnOpenCancelModal', function() {
            $('#modalAnnulerPreinscription').modal('show');
        });

        $(document).on('click', '#btnConfirmCancel', function() {
            const reason = $('#motif_annulation_text').val().trim();
            if (!reason) {
                alertify.error("Veuillez indiquer une raison pour l'annulation.");
                return;
            }

            const btn = $(this);
            btn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>Traitement...');

            $.ajax({
                url: '''',
                type: 'POST',
                data: {
                    'id_preinscrit': id,
                    'motif': reason,
                    'csrfmiddlewaretoken': 'true'
                },
                success: function(response) {
                    if (response.status === 'success') {
                        alertify.success(response.message);
                        setTimeout(function() {
                            window.location.href = "''";
                        }, 1500);
                    } else {
                        alertify.error(response.message);
                        btn.prop('disabled', false).html('<i class="ri-check-line me-1"></i>Confirmer l\'annulation');
                    }
                },
                error: function() {
                    alertify.error("Erreur lors de la communication avec le serveur.");
                    btn.prop('disabled', false).html('<i class="ri-check-line me-1"></i>Confirmer l\'annulation');
                }
            });
        });
    });


