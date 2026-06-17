import re

filename = 'templates/tenant_folder/configuration/general_settings.html'
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

profiles = {
    'national': 'crm_required_fields_national',
    'etranger': 'crm_required_fields_etranger',
    'double': 'crm_required_fields_double'
}

for profile_key, config_key in profiles.items():
    # Find <div class="row g-3"> right after the tab-pane
    search_str = f'<div class="tab-pane fade'
    idx = content.find(search_str, content.find(f'id="pills-{profile_key}"') - 50)
    
    if idx != -1:
        idx2 = content.find('<div class="row g-3">', idx)
        if idx2 != -1:
            toggle_html = f'''
                                                        <div class="d-flex justify-content-end mb-3 border-bottom pb-2">
                                                            <div class="form-check form-switch">
                                                                <input class="form-check-input select-all-toggle" type="checkbox" id="selectAll_{profile_key}" data-target="{profile_key}" data-config="{config_key}">
                                                                <label class="form-check-label small fw-bold text-primary" for="selectAll_{profile_key}">Activer toutes les validations</label>
                                                            </div>
                                                        </div>
'''
            # ensure we don't insert twice
            if 'selectAll_' + profile_key not in content:
                content = content[:idx2] + toggle_html + content[idx2:]

# Now inject the javascript
js_code = '''
    <script>
    $(document).ready(function() {
        $('.select-all-toggle').on('change', function() {
            var isChecked = this.checked;
            var target = $(this).data('target');
            var configKey = $(this).data('config');
            
            // Update visually without triggering individual onchange
            $('#pills-' + target + ' input[type="checkbox"]').not(this).prop('checked', isChecked);
            
            var fullConfig = {};
            $('#pills-' + target + ' input[type="checkbox"]').not(this).each(function() {
                var fieldId = $(this).attr('id').replace('req_' + target + '_', '');
                fullConfig[fieldId] = isChecked;
            });
            
            $.ajax({
                url: "{% url 'institut_app:ApiUpdateGlobalSettings' %}",
                type: "POST",
                data: {
                    'setting_name': configKey,
                    'setting_value': JSON.stringify(fullConfig),
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                success: function(response) {
                    if (response.status === 'success') {
                        alertify.success('Tous les champs ont été ' + (isChecked ? 'sélectionnés' : 'désélectionnés') + ' avec succès.');
                    } else {
                        alertify.error(response.message);
                    }
                },
                error: function() {
                    alertify.error("Une erreur s'est produite lors de la mise à jour.");
                }
            });
        });
    });
    </script>
'''

if 'select-all-toggle' not in content[content.rfind('</body>'):]:
    idx3 = content.rfind('{% endblock js %}')
    if idx3 != -1:
        content = content[:idx3] + js_code + content[idx3:]

with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)

print("Toggle buttons added")
