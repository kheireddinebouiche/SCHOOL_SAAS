import re

files = [
    'templates/tenant_folder/crm/preinscrits/details-preinscrit.html',
    'templates/tenant_folder/crm/preinscrits/details_preinscript_double.html'
]

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace isTabValidationEnabled with requiredFields
    content = re.sub(
        r'const isTabValidationEnabled = {{ config\.crm_tab_validation_enabled\|yesno:"true,false" }};',
        'const isTabValidationEnabled = true;\n        const requiredFields = {{ required_fields_json|safe }};\n',
        content
    )

    # 2. Update validateTab function
    new_validate_tab = '''function validateTab(tabId) {
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

                if (requiredFields[id] === true) {
                    if (!value || value === "" || value === "0") {
                        isValid = false;
                        field.addClass('is-invalid');
                        if (field.hasClass('select2-hidden-accessible')) {
                            field.next('.select2-container').find('.select2-selection').addClass('border-danger');
                        }
                    }
                }
            });

            if (tabId === '#medical') {
                var hasHandicap = $('#has_handicap').val();
                if (hasHandicap === "True" && !$('#type_handicap').val()) {
                    // Force type handicap validation if has_handicap is true
                    if (requiredFields['has_handicap'] === true || requiredFields['type_handicap'] === true) {
                        isValid = false;
                        $('#type_handicap').addClass('is-invalid');
                    }
                }
            }

            return isValid;
        }'''
        
    content = re.sub(
        r'function validateTab\(tabId\) \{.*?return isValid;\n        \}',
        new_validate_tab,
        content,
        flags=re.DOTALL
    )

    # 3. Add JS snippet to append '*' to labels of required fields
    add_asterisks_script = '''
        // Add asterisk to required fields
        for (const [key, value] of Object.entries(requiredFields)) {
            if (value === true) {
                var label = $('label[for="' + key + '"]');
                if (label.length > 0 && label.find('.text-danger').length === 0) {
                    label.append(' <span class="text-danger">*</span>');
                }
            }
        }
    '''

    # Inject add_asterisks_script inside document.ready
    idx = content.find("const isTabValidationEnabled = true;")
    if idx != -1:
        # Find next line after 'const requiredFields = ...'
        idx2 = content.find("\n", content.find("const requiredFields =", idx))
        content = content[:idx2] + add_asterisks_script + content[idx2:]

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done modifying templates")
