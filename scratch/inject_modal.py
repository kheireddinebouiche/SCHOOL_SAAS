import os

src = 'c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/templates/tenant_folder/formateur/liste_des_formateur.html'
dst = 'c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/templates/t_ressource_humaine/contrat_list.html'

with open(src, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    modal_html = ''.join(lines[476:596])
    
with open(dst, 'r', encoding='utf-8') as f:
    content = f.read()

if 'id="newFormateurModal"' not in content:
    # Add JS script for AJAX form submission
    js_script = """
<script>
$(document).ready(function() {
    $('#saveFormateurBtn').on('click', function(e) {
        e.preventDefault();
        var formData = $('#createFormateurForm').serialize();
        $.ajax({
            url: "{% url 't_formations:create_formateur' %}",
            type: "POST",
            data: formData + '&csrfmiddlewaretoken={{ csrf_token }}',
            success: function(response) {
                if(response.status === 'success') {
                    $('#newFormateurModal').modal('hide');
                    alertify.success('Formateur créé avec succès');
                    
                    // Option 1: Reload page to reflect new formateur
                    setTimeout(function() { location.reload(); }, 1000);
                } else {
                    alertify.error(response.message || 'Erreur lors de la création');
                }
            },
            error: function() {
                alertify.error('Une erreur réseau est survenue');
            }
        });
    });
});
</script>
"""
    new_content = content.replace('<!-- Modern AJAX Modal Interface -->', modal_html + '\n' + js_script + '\n<!-- Modern AJAX Modal Interface -->')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Modal added")
