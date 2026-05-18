import glob
for path in glob.glob('templates/tenant_folder/exams/*.html'):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            if any(term in line.lower() for term in ['nom', 'prenom', 'etudiant', 'student']) and 'matricule' not in line.lower():
                # check if it's in a td or loop
                if '<td>' in line.lower() or '{{' in line.lower() or 'for' in line.lower():
                    stripped = line.strip()
                    if len(stripped) > 0 and len(stripped) < 150:
                        print(f'{path}:{i}: {stripped}')
