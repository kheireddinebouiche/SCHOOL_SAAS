import re

files = [
    r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\menu.html',
    r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\public_folder\menu.html'
]

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix the corrupted single quote from my previous buggy regex.
        # Find any `url_name in ' ... "` and replace the `"` with `'` before `%}`
        content = re.sub(r'(in\s+\'[^\']*)\"\s*%\}', r"\1' %}", content)
        
        content = re.sub(r'(==\s+\'[^\']*)\"\s*%\}', r"\1' %}", content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed {file_path}')
    except Exception as e:
        print(f'Error: {e}')
