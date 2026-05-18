with open('templates/tenant_folder/formations/groupe/details_du_groupe.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if 'student' in line.lower() and ('phone' in line.lower() or 'indic' in line.lower() or 'tel' in line.lower()):
            print(f'Line {i}: {line.strip()}')
