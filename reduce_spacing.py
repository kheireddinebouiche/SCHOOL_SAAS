import os
import re

directories = [
    'templates/tenant_folder/administration',
    'templates/tenant_folder/configuration',
    'templates/tenant_folder/users'
]

replacements = {
    'p-4': 'p-3',
    'mb-4': 'mb-3',
    'g-4': 'g-3',
    'p-lg-5': 'p-lg-4'
}

for root_dir in directories:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                for old, new in replacements.items():
                    # We use regex to replace class names safely, e.g., \bp-4\b
                    content = re.sub(rf'\b{old}\b', new, content)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'Updated spacing in {file_path}')
