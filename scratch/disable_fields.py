import re

fields = [
    'nom_arabe', 'prenom_arabe', 'date_naissance', 'lieu_naissance', 'nin', 'secu', 'groupe_sanguin', 'nationnalite',
    'prenom_pere', 'tel_pere', 'indicatif_pere', 'nom_mere', 'prenom_mere', 'tel_mere', 'indicatif_mere', 'tuteur_legal', 'tel_tuteur', 'indicatif_tuteur',
    'has_handicap', 'type_handicap',
    'adresse_prospect', 'commune', 'wilaya', 'pays', 'code_zip',
    'niveau_scolaire', 'filiere_prospect', 'diplome', 'specialite_diplome', 'etablissement_diplome', 'annee_diplome'
]

files = [
    'templates/tenant_folder/crm/preinscrits/details-preinscrit.html',
    'templates/tenant_folder/crm/preinscrits/details_preinscript_double.html'
]

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    for field in fields:
        # Regex to match input/select tags with id="field" inside the modal (we can just match the id since IDs should be unique)
        # We need to insert {% if config.crm_field_locks.field %}disabled{% endif %} before the closing >
        # Be careful not to add it twice
        
        # We'll find <input ... id="field" ... > or <select ... id="field" ... >
        # and replace > with {% if config.crm_field_locks.field %}disabled{% endif %}>
        
        pattern = re.compile(r'(<(input|select)[^>]+id="' + field + r'"[^>]*?)(/?>)')
        
        def replacer(match):
            tag_content = match.group(1)
            end = match.group(3)
            
            # check if it already has disabled or the template tag
            if 'config.crm_field_locks.' + field in tag_content:
                return match.group(0)
                
            return f'{tag_content} {{% if config.crm_field_locks.{field} %}}disabled{{% endif %}}{end}'
            
        content = pattern.sub(replacer, content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated templates.')
