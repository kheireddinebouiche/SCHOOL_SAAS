import re, glob
import os

def patch_file(filepath):
    content = open(filepath, 'r', encoding='utf-8').read()
    lines = content.split('\n')
    
    # 1. Add missing transaction imports
    if 'from django.db import transaction' not in content:
        # insert after first import
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                lines.insert(i+1, 'from django.db import transaction')
                break
                
    # 2. Add @transaction.atomic to functions starting with Api
    in_view = False
    view_name = ""
    has_atomic = False
    has_db_write = False
    new_lines = []
    
    # Helper to check if a function needs atomic
    def needs_atomic(func_lines):
        has_write = False
        has_atomic_dec = False
        for fl in func_lines:
            if '@transaction.atomic' in fl:
                has_atomic_dec = True
            if '.save(' in fl or '.delete(' in fl or '.create(' in fl or '.update(' in fl:
                has_write = True
        return has_write and not has_atomic_dec
        
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for objects.get assignment
        match = re.match(r'^(\s*)(\w+(?:\.\w+)?)\s*=\s*(\w+)\.objects\.get\((.*?)\)\s*(#.*)?$', line)
        if match and 'try:' not in new_lines[-1] and 'try:' not in new_lines[-2] and 'get_or_create' not in line:
            indent, var, model, args, comment = match.groups()
            comment = comment or ''
            new_lines.append(f"{indent}try:")
            new_lines.append(f"{indent}    {var} = {model}.objects.get({args}) {comment}".strip('\r'))
            new_lines.append(f"{indent}except {model}.DoesNotExist:")
            new_lines.append(f"{indent}    return JsonResponse({{'status': 'error', 'message': '{model} introuvable.'}})")
        else:
            new_lines.append(line)
        i += 1
        
    # Phase 2: Add atomic
    content2 = '\n'.join(new_lines)
    
    # Split by decorators and defs
    final_lines = []
    lines2 = content2.split('\n')
    j = 0
    while j < len(lines2):
        line = lines2[j]
        if line.startswith('def Api'):
            # Look ahead to see if it writes
            look_ahead = j
            func_lines = []
            while look_ahead < len(lines2) and (lines2[look_ahead].startswith(' ') or lines2[look_ahead].startswith('\t') or lines2[look_ahead] == '' or look_ahead == j):
                func_lines.append(lines2[look_ahead])
                look_ahead += 1
                
            if needs_atomic(func_lines):
                # Need to insert @transaction.atomic right above the def
                # Wait, what if there are other decorators? (e.g. @login_required)
                # It's usually fine to put it right above def
                final_lines.append('@transaction.atomic')
                
        final_lines.append(line)
        j += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(final_lines))

patch_file('t_conseil/views.py')
for f in glob.glob('t_conseil/f_views/*.py'):
    patch_file(f)

print("Patching completed.")
