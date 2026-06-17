import re

files = [
    'templates/tenant_folder/crm/preinscrits/details-preinscrit.html',
    'templates/tenant_folder/crm/preinscrits/details_preinscript_double.html'
]

new_validation = '''$(document).on('click', '#saveAdditionalInfoBtn', function(){
            var isValidGlobal = true;
            $('#additionalInfoModal .tab-pane').each(function() {
                var tabId = '#' + $(this).attr('id');
                if (!validateTab(tabId)) {
                    isValidGlobal = false;
                }
            });
            
            if (!isValidGlobal) {
                var missingFields = [];
                $('#additionalInfoModal .is-invalid').each(function() {
                    var id = $(this).attr('id');
                    var labelText = $('label[for="' + id + '"]').text().replace('*', '').trim();
                    if (labelText) {
                        missingFields.push(labelText);
                    } else {
                        if (id === 'type_handicap') missingFields.push("Type d'handicap");
                        else missingFields.push(id);
                    }
                });
                
                // Remove duplicates
                missingFields = [...new Set(missingFields)];
                
                var errorHtml = '<strong>Veuillez remplir les champs obligatoires suivants :</strong><ul class="mb-0 mt-2">';
                missingFields.forEach(function(f) { errorHtml += '<li>' + f + '</li>'; });
                errorHtml += '</ul>';
                
                if ($('#validationErrors').length === 0) {
                    $('#additionalInfoModal .modal-body').prepend('<div id="validationErrors" class="alert alert-danger mb-4"></div>');
                }
                $('#validationErrors').html(errorHtml).removeClass('d-none');
                
                // Scroll to top
                $('#additionalInfoModal').animate({ scrollTop: 0 }, 'fast');
                
                return false;
            } else {
                if ($('#validationErrors').length > 0) {
                    $('#validationErrors').addClass('d-none');
                }
            }
'''

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # The previous logic was:
    #             if (!isValidGlobal) {
    #                 alertify.error("Veuillez remplir tous les champs obligatoires avant d'enregistrer.");
    #                 return false;
    #             }
    
    # Let's replace the whole $(document).on('click', '#saveAdditionalInfoBtn' function up to `var formData`
    
    pattern = re.compile(r'\$\(document\)\.on\(\'click\',\s*\'#saveAdditionalInfoBtn\',\s*function\(\)\{.*?(var formData = \{)', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(new_validation + '\n            \\1', content)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)

print("Updated global validation to show missing fields")
