import re

file_path = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\saas_admin_app\saas_tenant_data_explorer.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the literal '\n' which causes Uncaught SyntaxError
content = content.replace("\\n        $('#cancelSelection').on('click', function() {", "\n        $('#cancelSelection').on('click', function() {")
content = content.replace("\\n", "\n") # just in case there are other loose \n

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed literal '\\n' that caused Uncaught SyntaxError.")
