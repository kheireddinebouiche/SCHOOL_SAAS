import os
import re

FILES_ALL_VIEWS = [
    r'institut_app/f_views/permissions.py',
    r'institut_app/f_views/users.py',
    r'institut_app/f_views/config.py',
]

FILE_SPECIFIC_VIEWS = r'institut_app/views.py'

VIEWS_TO_DECORATE = [
    'UsersListePage', 'ApiListeUsers', 'ApiGetDetailsProfile', 'ApiCreateProfile',
    'ApiDeactivateUser', 'ApiActivateUser', 'ListGroupePage', 'ApilistGroupe',
    'NewCustomGroupe', 'ApiGetGroupFrom', 'ApiGetNewUserForm', 'PageUpdateUserDetails',
    'ApiSaveUser', 'ApiCheckUsernameDisponibility', 'ApiGetUpdateGroupForm', 'ApiSaveGroup',
    'ApiGetUserDetails', 'ApiGetGroupeDetails', 'ApiDeleteGroup', 'active_sessions_view',
    'terminate_session_api'
]

# We are intentionally EXCLUDING anything related to "entreprise" to keep it accessible

def decorate_file(file_path, decorate_all=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to add imports if missing
    imports = []
    if 'user_passes_test' not in content:
        imports.append("from django.contrib.auth.decorators import user_passes_test")
    
    if imports:
        content = "\n".join(imports) + "\n" + content

    def add_decorator(match):
        func_def = match.group(0)
        func_name_match = re.search(r'def\s+([a-zA-Z0-9_]+)\(', func_def)
        if func_name_match:
            func_name = func_name_match.group(1)
            
            # If we decorate all, or if it's in the specific list
            if decorate_all or func_name in VIEWS_TO_DECORATE:
                # Make sure it's not already decorated with user_passes_test
                # Actually, some might be decorated, but we don't want to duplicate.
                # Let's just add it. The regex replaces `def func(...)`, so we just put it before `def`
                decorator = "@user_passes_test(lambda u: u.is_superuser)\n"
                print(f"Secured {func_name} in {file_path}")
                return decorator + func_def
        return func_def

    # Remove any existing `@user_passes_test(lambda u: u.is_superuser)` just to avoid duplicates if we run twice
    content = re.sub(r'@user_passes_test\(lambda u: u\.is_superuser\)\n', '', content)

    # Match def declarations
    content = re.sub(r'def\s+[a-zA-Z0-9_]+\(\s*request[^)]*\):', add_decorator, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for fp in FILES_ALL_VIEWS:
    decorate_file(fp, decorate_all=True)

decorate_file(FILE_SPECIFIC_VIEWS, decorate_all=False)

print("Done applying superuser decorators.")
