import os
import re

FILES_ALL_VIEWS = [
    r'institut_app/f_views/permissions.py',
    r'institut_app/f_views/users.py',
    r'institut_app/f_views/config.py',
    r'institut_app/views.py'
]

def swap_decorator(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add import if missing
    if 'superuser_required' not in content:
        content = "from institut_app.decorators import superuser_required\n" + content

    # Replace decorator
    content = re.sub(r'@user_passes_test\(lambda u: u\.is_superuser\)', '@superuser_required', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for fp in FILES_ALL_VIEWS:
    swap_decorator(fp)

print("Done swapping to superuser_required.")
