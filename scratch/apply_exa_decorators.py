import os
import re
import glob

TARGET_FILES = glob.glob('t_exam/views.py') + glob.glob('t_exam/f_views/*.py')

def determine_permission(func_name):
    lower_name = func_name.lower()
    if any(x in lower_name for x in ['delete', 'remove', 'supprimer']):
        return 'delete'
    if any(x in lower_name for x in ['update', 'edit', 'config', 'modifier']):
        return 'change'
    if any(x in lower_name for x in ['add', 'new', 'create', 'generate', 'save', 'plane', 'nouveau', 'load']):
        return 'add'
    if any(x in lower_name for x in ['valid', 'approuv', 'soumettre', 'confirm', 'deliberate']):
        return 'approuv'
    return 'view'

def add_decorator(match):
    func_def = match.group(0)
    func_name_match = re.search(r'def\s+([a-zA-Z0-9_]+)\(', func_def)
    if func_name_match:
        func_name = func_name_match.group(1)
        perm = determine_permission(func_name)
        decorator = f"@module_permission_required('exa', '{perm}')\n"
        print(f"Added {perm} to {func_name}")
        return decorator + func_def
    return func_def

for file_path in TARGET_FILES:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'def ' not in content:
        continue

    # Clean existing module_permission_required to overwrite with new heuristic
    content = re.sub(r'@module_permission_required\([^\)]+\)\n', '', content)

    content = re.sub(r'def\s+[a-zA-Z0-9_]+\(\s*request[^)]*\):', add_decorator, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done re-applying decorators to exa module.")
