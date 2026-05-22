import sys

file_path = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\saas_admin_app\saas_tenant_data_explorer.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace main structure
old_structure = '''    <!-- Main Content Area -->
    <div class="row" style="margin-top: 2rem;">
        <div class="col-12">
            <div class="d-flex justify-content-center mb-4">
                <ul class="nav nav-pills nav-pills-custom shadow-sm" role="tablist">'''

new_structure = '''    <!-- Main Content Area -->
    <div class="row" style="margin-top: 2rem;">
        <!-- Sidebar -->
        <div class="col-lg-3 mb-4">
            <div class="glass-sidebar p-3 position-sticky" style="top: 20px; background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(15px); border-radius: 20px; border: 1px solid rgba(255,255,255,0.4); box-shadow: 0 10px 40px rgba(0,0,0,0.03);">
                <h5 class="mb-3 px-3 fw-bold text-primary"><i class="ri-table-line me-2"></i>Entités</h5>
                <ul class="nav flex-column nav-pills nav-pills-custom-sidebar gap-2" role="tablist">'''
content = content.replace(old_structure, new_structure)

# Update the end of the ul and the start of tab-content
old_end_ul = '''                </ul>
            </div>

            <div class="tab-content">'''

new_end_ul = '''                </ul>
            </div>
        </div>

        <!-- Content Area -->
        <div class="col-lg-9">
            <div class="tab-content">'''
content = content.replace(old_end_ul, new_end_ul)

# Add custom CSS for nav-pills-custom-sidebar
css_to_add = '''
    .nav-pills-custom-sidebar .nav-link {
        border-radius: 12px;
        padding: 0.75rem 1.25rem;
        font-weight: 600;
        color: #475569;
        transition: all 0.3s ease;
        border: 1px solid transparent;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .nav-pills-custom-sidebar .nav-link:hover {
        background: rgba(255,255,255,0.5);
        color: #4361ee;
    }
    .nav-pills-custom-sidebar .nav-link.active {
        background: #4361ee !important;
        color: #fff !important;
        box-shadow: 0 4px 15px rgba(67, 97, 238, 0.25);
    }
'''
if "nav-pills-custom-sidebar" not in content:
    content = content.replace("</style>", css_to_add + "</style>")

# Let's also add icons to the nav items to make them look good.
# Replacing nav items one by one
nav_items_replacements = [
    ("Prospects", "<i class='ri-user-follow-line'></i> Prospects"),
    ("Vœux", "<i class='ri-file-list-3-line'></i> Vœux"),
    ("Doubles", "<i class='ri-file-copy-2-line'></i> Doubles"),
    ("Formations", "<i class='ri-book-open-line'></i> Formations"),
    ("Spécialités", "<i class='ri-medal-line'></i> Spécialités"),
    ("Montants Dus", "<i class='ri-money-dollar-circle-line'></i> Montants Dus"),
    ("Paiements", "<i class='ri-bank-card-line'></i> Paiements"),
    ("Opérations Bancaires", "<i class='ri-bank-line'></i> Opérations Bancaires"),
    ("Demandes Remboursement", "<i class='ri-refund-2-line'></i> Demandes Remboursement"),
    ("Remboursements", "<i class='ri-exchange-dollar-line'></i> Remboursements"),
    ("Autres Produits", "<i class='ri-shopping-bag-3-line'></i> Autres Produits"),
]

for old, new in nav_items_replacements:
    # Be careful not to replace things inside tab contents, only in the nav-links
    # Since they are surrounded by whitespace and newlines, we can do a targeted replace
    # Actually, let's just replace them inside the ul block by finding the block first.
    pass

# A safer way to inject icons:
import re
def inject_icons(match):
    text = match.group(0)
    for old, new in nav_items_replacements:
        if f">{old}<" in text.replace('\\n', '').replace(' ', ''): # this is tricky
            pass
    return text

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patch 1 applied: Sidebar Layout created')
