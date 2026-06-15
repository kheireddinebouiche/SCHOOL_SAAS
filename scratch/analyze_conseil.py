import re, os, glob

report = []

def analyze_file(filepath):
    try:
        content = open(filepath, 'r', encoding='utf-8').read()
        lines = content.split('\n')
        
        # Check for unhandled objects.get
        get_calls = []
        for i, line in enumerate(lines):
            if 'objects.get(' in line and 'try:' not in lines[i-1] and 'try:' not in lines[i-2] and 'try:' not in line:
                get_calls.append(f"Line {i+1}: {line.strip()}")
        
        if get_calls:
            report.append(f"\n### Unhandled objects.get in {filepath}:\n" + "\n".join(get_calls))

        # Check for views with save() or delete() without @transaction.atomic
        # This is a bit naive but gives an idea
        if 't_conseil' in filepath and 'views' in filepath:
            views_missing_atomic = []
            in_view = False
            view_name = ""
            has_atomic = False
            has_db_write = False
            
            for i, line in enumerate(lines):
                if line.startswith('def '):
                    if in_view and has_db_write and not has_atomic:
                        views_missing_atomic.append(view_name)
                    
                    in_view = True
                    view_name = line.split('(')[0].replace('def ', '')
                    has_atomic = False
                    has_db_write = False
                    
                    # check decorators above
                    for j in range(1, 5):
                        if i-j >= 0 and '@transaction.atomic' in lines[i-j]:
                            has_atomic = True
                            
                elif in_view:
                    if line.startswith('class '):
                        in_view = False
                    elif '.save(' in line or '.delete(' in line or '.create(' in line or '.update(' in line:
                        has_db_write = True
                        
            if in_view and has_db_write and not has_atomic:
                views_missing_atomic.append(view_name)
                
            if views_missing_atomic:
                report.append(f"\n### Functions missing @transaction.atomic in {filepath}:\n" + "\n".join(views_missing_atomic))

    except Exception as e:
        report.append(f"Error reading {filepath}: {e}")

analyze_file('t_conseil/views.py')
for f in glob.glob('t_conseil/f_views/*.py'):
    analyze_file(f)

with open('scratch/conseil_report.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(report))
