import os
import re

apps = [
    'institut_app', 't_rh', 't_formations', 't_etudiants', 't_tresorerie', 't_exam', 't_remise', 't_crm', 't_conseil', 't_communication', 't_timetable'
]

replacements = {
    'label': 'Sans label',
    'designation': 'Sans désignation',
    'bank_code': 'Sans code',
    'titre': 'Sans titre',
    'nom': 'Sans nom',
    'code': 'Sans code',
    'value': 'Sans valeur'
}

for app in apps:
    models_file = os.path.join(app, 'models.py')
    if not os.path.exists(models_file): continue
    
    with open(models_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    for field, default_str in replacements.items():
        pattern = r'return self\.' + field + r'\s*$'
        replacement = f'return str(self.{field}) if getattr(self, \"{field}\", None) else \"{default_str}\"'
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
    if content != original:
        with open(models_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed __str__ methods in {models_file}')
