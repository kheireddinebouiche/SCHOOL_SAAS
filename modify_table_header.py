import sys
print("Démarrage du script de modification")
sys.stdout.flush()

# Read the file
try:
    with open('C:\\Users\\Bureau IT\\Documents\\SCHOOL_SAAS\\templates\\tenant_folder\\formateur\\affectation_modules.html', 'r', encoding='utf-8') as file:
        content = file.read()
    print("Fichier lu avec succès")
    sys.stdout.flush()
except Exception as e:
    print(f"Erreur lors de la lecture: {e}")
    sys.stdout.flush()
    exit(1)

# Vérifier si les chaînes existent
print(f"Contient 'width: 50px;': {'width: 50px;' in content}")
print(f"Contient 'selectAllCheckbox': {'selectAllCheckbox' in content}")
sys.stdout.flush()

# Remplacer la structure du tableau
old_header = '''                  <table class=\"table table-bordered dt-responsive nowrap table-striped align-middle\" style=\"width:100%\">
                    <thead class=\"bg-light\">
                      <tr>
                        <th class=\"border-0 rounded-start\" style=\"width: 50px;\">
                          <div class=\"form-check\">
                            <input class=\"form-check-input\" type=\"checkbox\" id=\"selectAllCheckbox\">
                          </div>
                        </th>
                        <th class=\"border-0\">Nom</th>
                        <th class=\"border-0\">Prénom</th>
                        <th class=\"border-0 rounded-end\">Email</th>
                      </tr>
                    </thead>'''

new_header = '''                  <table class=\"table table-bordered dt-responsive nowrap table-striped align-middle\" style=\"width:100%\">
                    <thead class=\"bg-light\">
                      <tr>
                        <th class=\"border-0 rounded-start\">Nom</th>
                        <th class=\"border-0\">Prénom</th>
                        <th class=\"border-0\">Email</th>
                        <th class=\"border-0 rounded-end text-center\">Actions</th>
                      </tr>
                    </thead>'''

if old_header in content:
    print("Chaîne trouvée, remplacement en cours")
    sys.stdout.flush()
    content = content.replace(old_header, new_header)
    
    # Écrire le fichier modifié
    with open('C:\\Users\\Bureau IT\\Documents\\SCHOOL_SAAS\\templates\\tenant_folder\\formateur\\affectation_modules.html', 'w', encoding='utf-8') as file:
        file.write(content)
    print("Remplacement effectué avec succès")
else:
    print("Chaîne non trouvée, tentative avec une version avec espaces différents")
    sys.stdout.flush()
    
    # Essayer avec une version qui gère différents types d'espaces
    import re
    # Trouver la section spécifique qui contient le tableau cible
    pattern = r'(<table class="table table-bordered dt-responsive nowrap table-striped align-middle" style="width:100%">\s*<thead class="bg-light">\s*<tr>\s*<th class="border-0 rounded-start" style="width: 50px;">.*?</tr>\s*</thead>)'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        print("Motif trouvé avec regex")
        sys.stdout.flush()
        old_part = match.group(1)
        
        # Créer la nouvelle version
        new_part = '''                  <table class="table table-bordered dt-responsive nowrap table-striped align-middle" style="width:100%">
                    <thead class="bg-light">
                      <tr>
                        <th class="border-0 rounded-start">Nom</th>
                        <th class="border-0">Prénom</th>
                        <th class="border-0">Email</th>
                        <th class="border-0 rounded-end text-center">Actions</th>
                      </tr>
                    </thead>'''
        
        content = content.replace(old_part, new_part)
        
        # Écrire le fichier modifié
        with open('C:\\Users\\Bureau IT\\Documents\\SCHOOL_SAAS\\templates\\tenant_folder\\formateur\\affectation_modules.html', 'w', encoding='utf-8') as file:
            file.write(content)
        print("Remplacement effectué avec regex")
    else:
        print("Aucun motif correspondant trouvé")
        sys.stdout.flush()