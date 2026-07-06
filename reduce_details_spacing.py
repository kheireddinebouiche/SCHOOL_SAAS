import os
import re

directories = [
    'templates/tenant_folder/conseil/prospect',
]

for root_dir in directories:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith('details_prospect') and filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Reduce page title header size
                content = re.sub(r'(class="[^"]*card[^"]*)\bp-4\b([^"]*d-sm-flex align-items-center justify-content-between)', r'\1p-3 py-2\2', content)
                content = re.sub(r'(class="[^"]*card[^"]*)\bp-3\b([^"]*d-sm-flex align-items-center justify-content-between)', r'\1p-3 py-2\2', content)
                content = content.replace('p-3 py-2 py-2', 'p-3 py-2')
                
                content = content.replace('p-3 bg-white rounded-4 shadow-sm', 'p-3 py-2 bg-white rounded-4 shadow-sm')
                content = content.replace('p-4 bg-white rounded-4 shadow-sm', 'p-3 py-2 bg-white rounded-4 shadow-sm')
                
                # Reduce paddings and margins globally in the file
                content = re.sub(r'\bp-4\b', 'p-3', content)
                content = re.sub(r'\bmb-4\b', 'mb-3', content)
                content = re.sub(r'\bg-4\b', 'g-3', content)
                
                # Specifically for icon backgrounds
                content = content.replace('rounded-3 p-3 me-3', 'rounded-3 p-2 me-3')
                
                content = re.sub(r'class="card shadow-sm border-0 rounded-4 p-3"', 'class="card shadow-sm border-0 rounded-4 p-3 py-2"', content)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'Updated spacing in {file_path}')
