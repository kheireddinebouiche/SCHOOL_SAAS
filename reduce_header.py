import os
import re

directories = [
    'templates/tenant_folder/administration',
    'templates/tenant_folder/users',
    'templates/tenant_folder/configuration'
]

for root_dir in directories:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Replace 'p-3' or 'p-4' with 'p-3 py-2' for the page header. 
                # Let's search for 'd-sm-flex align-items-center justify-content-between' 
                # which is typical for the header card.
                
                content = re.sub(r'(class="[^"]*card[^"]*)\bp-4\b([^"]*d-sm-flex align-items-center justify-content-between)', r'\1p-3 py-2\2', content)
                content = re.sub(r'(class="[^"]*card[^"]*)\bp-3\b([^"]*d-sm-flex align-items-center justify-content-between)', r'\1p-3 py-2\2', content)
                
                content = content.replace('p-3 py-2 py-2', 'p-3 py-2')
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'Updated header in {file_path}')
