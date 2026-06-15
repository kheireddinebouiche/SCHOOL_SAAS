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
                if 'from django.contrib import messages' not in content:
                    lines.insert(i+2, 'from django.contrib import messages')
                break
                
    new_lines = []
    
    in_view = False
    is_api = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if entering a view
        m_def = re.match(r'^def\s+(\w+)\s*\(', line)
        if m_def:
            func_name = m_def.group(1)
            in_view = True
            is_api = func_name.startswith('Api')
            
            # Simple heuristic for @transaction.atomic
            # We look ahead to see if it modifies DB
            has_db_write = False
            look_ahead = i
            while look_ahead < len(lines) and (lines[look_ahead].startswith(' ') or lines[look_ahead].startswith('\t') or lines[look_ahead] == '' or look_ahead == i):
                fl = lines[look_ahead]
                if '.save(' in fl or '.delete(' in fl or '.create(' in fl or '.update(' in fl:
                    has_db_write = True
                look_ahead += 1
            
            if has_db_write and '@transaction.atomic' not in content[max(0, i-200):min(len(content), i+200)]: 
                # Very basic check: just insert above def if it's an API
                if is_api:
                    new_lines.append('@transaction.atomic')
                    
        # Check for objects.get assignment
        match = re.match(r'^(\s*)(\w+(?:\.\w+)?)\s*=\s*(\w+)\.objects\.get\((.*?)\)\s*(#.*)?$', line)
        if match and 'try:' not in new_lines[-1] and 'try:' not in new_lines[-2] and 'get_or_create' not in line:
            indent, var, model, args, comment = match.groups()
            comment = comment or ''
            new_lines.append(f"{indent}try:")
            new_lines.append(f"{indent}    {var} = {model}.objects.get({args}) {comment}".strip('\r'))
            new_lines.append(f"{indent}except {model}.DoesNotExist:")
            if is_api:
                new_lines.append(f"{indent}    return JsonResponse({{'status': 'error', 'message': '{model} introuvable.'}})")
            else:
                new_lines.append(f"{indent}    messages.error(request, '{model} introuvable.')")
                new_lines.append(f"{indent}    return redirect(request.META.get('HTTP_REFERER', '/'))")
        else:
            new_lines.append(line)
        i += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

patch_file('t_conseil/views.py')
for f in glob.glob('t_conseil/f_views/*.py'):
    patch_file(f)

print("Patching completed.")
