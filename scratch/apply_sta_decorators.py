import os
import re

VIEWS_FILE = r't_stage/views.py'

# 1. Clean imports
with open(VIEWS_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove 'role_required' from imports
content = re.sub(r'from institut_app\.decorators import ajax_required, module_permission_required, role_required',
                 r'from institut_app.decorators import ajax_required, module_permission_required', content)

# Remove all existing @role_required(...) decorators
content = re.sub(r'@role_required\([^\)]+\)\n', '', content)

# Remove all existing @module_permission_required(...) decorators so we can rewrite them cleanly
content = re.sub(r'@module_permission_required\([^\)]+\)\n', '', content)

# Define the mapping of functions to their new required permissions
permission_map = {
    'stage_dashboard': ('sta', 'view'),
    'list_stages': ('sta', 'view'),
    'focus_group_detail': ('sta', 'view'),
    'ajax_get_students_by_group': ('sta', 'view'),
    'list_focus_groups': ('sta', 'view'),
    'council_detail': ('sta', 'view'),
    'print_sessions': ('sta', 'view'),
    
    'progressive_presentation_form': ('sta', 'add'),
    'launch_stage': ('sta', 'add'),
    'create_focus_group': ('sta', 'add'),
    'add_seance': ('sta', 'add'),
    
    'edit_stage': ('sta', 'change'),
    
    'delete_presentation': ('sta', 'delete'),
    
    'validation_council': ('sta', 'approuv'),
    'quick_decision': ('sta', 'approuv'),
}

# Apply the new decorators
def add_decorator(match):
    func_def = match.group(0)
    func_name_match = re.search(r'def\s+([a-zA-Z0-9_]+)\(', func_def)
    if func_name_match:
        func_name = func_name_match.group(1)
        if func_name in permission_map:
            module, perm = permission_map[func_name]
            decorator = f"@module_permission_required('{module}', '{perm}')\n"
            print(f"Added @module_permission_required('{module}', '{perm}') to {func_name}")
            return decorator + func_def
    return func_def

# The regex matches "def func_name("
content = re.sub(r'def\s+[a-zA-Z0-9_]+\(', add_decorator, content)

with open(VIEWS_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done applying decorators to sta module.")
