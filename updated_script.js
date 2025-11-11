<script>
    $(document).ready(function(){
        // Add edit functionality
        $(document).on('click', '.edit-item-btn', function() {
            const id = $(this).data('id');
            // In a real application, you would fetch the type data and populate the form
            $('#typeId').val(id);
            $('#typeName').val('Type ' + id);
            $('#typeDescription').val('Description pour le type ' + id);
            
            // Update radio buttons based on status (in a real app this would come from the data)
            $('#statusActive').prop('checked', true); // Default
            $('#statusInactive').prop('checked', false);
            
            $('#typeCategory').val('');
            $('#addTypeModalLabel').html('<i class="ri-edit-box-line me-2"></i>Modifier le Type de Dépense');
            $('#saveTypeBtn').html('<i class="ri-refresh-line me-1"></i>Mettre à jour');
            bootstrap.Modal.getOrCreateInstance(document.getElementById('addTypeModal')).show();
        });

        // Add delete functionality
        $(document).on('click', '.remove-item-btn', function() {
            const id = $(this).data('id');
            // Store the ID for deletion
            $('#confirmDeleteBtn').data('id', id);
            bootstrap.Modal.getOrCreateInstance(document.getElementById('deleteModal')).show();
        });

        // Confirm deletion
        $('#confirmDeleteBtn').click(function() {
            const id = $(this).data('id');
            // In a real application, you would make an AJAX call to delete the type
            console.log('Deleting type with ID: ' + id);
            // Close the modal and show a success message
            bootstrap.Modal.getOrCreateInstance(document.getElementById('deleteModal')).hide();
            showNotification('Type de dépense supprimé avec succès', 'success');
        });

        // Save type functionality
        $('#saveTypeBtn').click(function() {
            // In a real application, you would gather form data and make an AJAX call
            const id = $('#typeId').val();
            const name = $('#typeName').val();
            const status = $('input[name="statusRadio"]:checked').val();
            const category = $('#typeCategory').val();

            // Close the modal and show a success message
            bootstrap.Modal.getOrCreateInstance(document.getElementById('addTypeModal')).hide();
            if(id) {
                showNotification('Type de dépense "' + name + '" mis à jour avec succès', 'success');
            } else {
                showNotification('Type de dépense "' + name + '" ajouté avec succès', 'success');
            }

            // Reset form
            $('#typeForm')[0].reset();
            $('#statusActive').prop('checked', true); // Default to active
            $('#typeCategory').val('');
            $('#addTypeModalLabel').html('<i class="ri-add-line me-2"></i>Créer un nouveau type de dépense');
            $('#saveTypeBtn').html('<i class="ri-save-3-line me-1"></i>Enregistrer');
        });

        // Function to show notification
        function showNotification(message, type) {
            // For now, just show a simple alert
            alert(message);
        }

        // Clear form when modal is closed
        $('#addTypeModal').on('hidden.bs.modal', function() {
            $('#typeForm')[0].reset();
            $('#typeId').val('');
            $('#statusActive').prop('checked', true); // Default to active
            $('#typeCategory').val('');
            $('#addTypeModalLabel').html('<i class="ri-add-line me-2"></i>Créer un nouveau type de dépense');
            $('#saveTypeBtn').html('<i class="ri-save-3-line me-1"></i>Enregistrer');
        });

        // Initialize statistics
        $('#totalTypes').text(3);
        $('#activeTypes').text(2);
        $('#inactiveTypes').text(1);
        $('#totalMontantTypes').text('0 DA');
    });
</script>