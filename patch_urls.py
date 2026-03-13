import os
import re

NAMES = [
    'configuration_index', 'configuration_budget', 'configuration_structure',
    'tenant_data_list', 'get_tenant_categories', 'purge_tenant_categories',
    'crm_statistics', 'get_crm_stats_api',
    'global_payment_type_list', 'global_payment_type_create', 'global_payment_type_edit', 'global_payment_type_delete', 'sync_payment_types',
    'global_payment_category_list', 'global_payment_category_create', 'global_payment_category_edit', 'global_payment_category_delete', 'export_payment_categories', 'import_payment_categories',
    'global_depenses_category_list', 'global_depenses_category_create', 'global_depenses_category_edit', 'global_depenses_category_delete', 'export_depenses_categories', 'import_depenses_categories',
    'postes_budgetaires_list', 'postes_budgetaire_create', 'postes_budgetaire_edit', 'postes_budgetaire_delete',
    'budget_campaign_list', 'budget_campaign_create', 'budget_campaign_instituts', 'budget_campaign_activate', 'budget_campaign_delete', 'budget_campaign_review',
    'extension_requests_list', 'review_extension', 'sync_categories_view'
]

targets = [
    r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\associe_app\views.py',
    r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\public_folder\menu.html'
]
template_dir = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\associe_app'
if os.path.exists(template_dir):
    for f in os.listdir(template_dir):
        if f.endswith('.html'):
            targets.append(os.path.join(template_dir, f))

changed_files = 0
for filepath in targets:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    modified = content
    for name in NAMES:
        # replace templates
        modified = re.sub(rf"\{{%\s*url\s+['\"](?!associe_app:){name}['\"]", f"{{% url 'associe_app:{name}'", modified)
        
        # replace in views: redirect('name' ...)
        modified = re.sub(rf"redirect\(['\"](?!associe_app:){name}['\"]", f"redirect('associe_app:{name}'", modified)
        
        # replace in views: reverse('name' ...)
        modified = re.sub(rf"reverse\(['\"](?!associe_app:){name}['\"]", f"reverse('associe_app:{name}'", modified)

    if modified != content:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(modified)
        changed_files += 1

print(f"Patched {changed_files} files.")
