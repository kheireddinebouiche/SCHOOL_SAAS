import os
import re
import glob

# Search for views.py and anything in f_views/ and views/
TARGET_FILES = glob.glob('t_tresorerie/views.py') + glob.glob('t_tresorerie/f_views/*.py') + glob.glob('t_tresorerie/views/*.py')

def determine_permission(func_name):
    lower_name = func_name.lower()
    if any(x in lower_name for x in ['delete', 'remove', 'supprimer', 'cancel', 'archive']):
        return 'delete'
    if any(x in lower_name for x in ['update', 'edit', 'config', 'modifier', 'toggle']):
        return 'change'
    if any(x in lower_name for x in ['add', 'new', 'create', 'generate', 'save', 'store', 'apply']):
        return 'add'
    if any(x in lower_name for x in ['valid', 'approuv', 'soumettre', 'confirm', 'deliberate', 'imput']):
        return 'approuv'
    return 'view'

def add_decorator(match):
    func_def = match.group(0)
    func_name_match = re.search(r'def\s+([a-zA-Z0-9_]+)\(', func_def)
    if func_name_match:
        func_name = func_name_match.group(1)
        perm = determine_permission(func_name)
        decorator = f"@module_permission_required('tre', '{perm}')\n"
        print(f"Added {perm} to {func_name}")
        return decorator + func_def
    return func_def

for file_path in TARGET_FILES:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if it's an empty file or doesn't have functions
    if 'def ' not in content:
        continue

    # Ensure imports are present
    if 'module_permission_required' not in content:
        content = "from institut_app.decorators import module_permission_required\n" + content

    # Clean existing module_permission_required just in case
    content = re.sub(r'@module_permission_required\([^\)]+\)\n', '', content)

    # We only want to decorate functions that take 'request' as an argument (or first arg usually)
    content = re.sub(r'def\s+[a-zA-Z0-9_]+\(\s*request[^)]*\):', add_decorator, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done applying decorators to tre module.")
