import re

files = [
    'templates/tenant_folder/crm/preinscrits/details-preinscrit.html',
    'templates/tenant_folder/crm/preinscrits/details_preinscript_double.html'
]

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # The user wants fields to be mandatory (validation blocks submission) but not navigation.
    # We already disabled the blocking during tab navigation.
    # Now we need to add validation back on the final 'saveAdditionalInfoBtn' click.
    
    # Let's find:
    # $(document).on('click', '#saveAdditionalInfoBtn', function(){
    #             // if (!validateCurrentTab()) return;
    
    # We will replace it with a function that validates ALL tabs:
    
    new_validation = '''$(document).on('click', '#saveAdditionalInfoBtn', function(){
            var isValidGlobal = true;
            $('#additionalInfoModal .tab-pane').each(function() {
                var tabId = '#' + $(this).attr('id');
                if (!validateTab(tabId)) {
                    isValidGlobal = false;
                }
            });
            if (!isValidGlobal) {
                alertify.error("Veuillez remplir tous les champs obligatoires avant d'enregistrer.");
                return false;
            }
'''
    
    pattern = re.compile(r'\$\(document\)\.on\(\'click\',\s*\'#saveAdditionalInfoBtn\',\s*function\(\)\{\s*//\s*if\s*\(!validateCurrentTab\(\)\)\s*return;', re.DOTALL)
    
    # If already applied or pattern not found exactly like that, use a generic replace
    if not pattern.search(content):
        # Maybe the comment has no spaces or something
        pattern = re.compile(r'\$\(document\)\.on\(\'click\',\s*\'#saveAdditionalInfoBtn\',\s*function\(\)\{.*?(var formData = \{)', re.DOTALL)
        new_content = pattern.sub(new_validation + '\n            \\1', content)
    else:
        new_content = pattern.sub(new_validation, content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Added global validation on submission")
