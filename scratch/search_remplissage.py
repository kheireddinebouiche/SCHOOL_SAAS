with open('templates/tenant_folder/exams/remplissage_notes.html', 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f, 1):
        if 'student' in line or 'etudiant' in line or 'matricule' in line:
            stripped = line.strip()
            if len(stripped) > 0:
                print(f'{i}: {stripped[:120]}')
