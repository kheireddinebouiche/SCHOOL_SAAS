import re

file_path = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\saas_admin_app\urls.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
import_pattern = r"saas_export_prospects_view, saas_force_user_password_change_view\s*\)"
if "saas_reset_tresorerie_view" not in content:
    content = re.sub(
        import_pattern,
        "saas_export_prospects_view, saas_force_user_password_change_view,\n    saas_reset_tresorerie_view\n)",
        content
    )

# Add URL
url_pattern = r"path\('api/tenant/<int:tenant_id>/delete-specialite/', api_tenant_delete_specialite_view, name='api_tenant_delete_specialite'\),"
new_url = "path('api/tenant/<int:tenant_id>/reset-tresorerie/', saas_reset_tresorerie_view, name='saas_reset_tresorerie_action'),\n    " + url_pattern

if "reset-tresorerie" not in content:
    content = re.sub(url_pattern, new_url, content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added saas_reset_tresorerie_view to urls.py")
else:
    print("URL already exists.")
