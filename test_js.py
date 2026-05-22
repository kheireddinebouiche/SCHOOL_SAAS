import re
import subprocess

with open(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\saas_admin_app\saas_tenant_data_explorer.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'{% block extra_js %}(.*?){% endblock extra_js %}', text, re.DOTALL)
if match:
    js = match.group(1)
    # just strip out the html script tags
    js = js.replace('<script>', '').replace('</script>', '')
    # replace django tags with a JS string to avoid syntax errors
    js = re.sub(r'{%.*?%}', '"DJANGO"', js)
    js = re.sub(r'{{.*?}}', '"DJANGO"', js)
    
    with open('test_script.js', 'w', encoding='utf-8') as out:
        out.write(js)
    
    result = subprocess.run(['node', '-c', 'test_script.js'], capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
else:
    print('Block not found')
