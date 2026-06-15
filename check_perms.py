import ast
import glob
import os

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
    except Exception as e:
        return []
    
    missing = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check if it's a view (takes request as first arg)
            if node.args.args and node.args.args[0].arg == 'request':
                has_perm = False
                for dec in node.decorator_list:
                    if isinstance(dec, ast.Call) and hasattr(dec.func, 'id') and dec.func.id == 'module_permission_required':
                        has_perm = True
                    elif isinstance(dec, ast.Name) and dec.id == 'module_permission_required':
                        has_perm = True
                if not has_perm:
                    missing.append(node.name)
    return missing

files = glob.glob('c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/t_conseil/**/*.py', recursive=True)
for f in files:
    m = check_file(f)
    if m:
        print(f"{f}: {m}")
