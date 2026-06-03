import re

def process_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = {
        'dashboard': (r'<div class="col-12">\s*<div class="submenu-item bg-light bg-opacity-50 rounded-2 mb-1">\s*<a href="{% url \'institut_app:FinanceDashboard\' %}"', r'</a>\s*</div>\s*(?=<a href="#sidebarTresorerie")'),
        'tresorerie': (r'<a href="#sidebarTresorerie"', 'tresorerie'),
        'exec_edu': (r'<a href="#sidebarFinanceConseil"', 'exec_edu'),
        'remboursement': (r'<a href="#sidebarRemboursement"', 'remboursement'),
        'remises': (r'<a href="#sidebarRemises"', 'remises'),
        'caisse': (r'<a href="#sidebarCaisse"', 'caisse'),
        'banque': (r'<a href="#sidebarBanque"', 'banque'),
        'autres_paiements': (r'<a href="#sidebarProduit"', 'autres_paiements'),
        'depenses': (r'<a href="#sidebarDepenses"', 'depenses'),
        'fournisseurs': (r'<a href="#sidebarFournisseurs"', 'fournisseurs'),
        'factures': (r'<a href="#sidebarFactures"', 'factures'),
        'parametres': (r'<a href="#sidbareParam"', 'parametres'),
        'echeanciers': (r'<a href="#sidebarEcheanciers"', 'echeanciers'),
    }

    # Instead of parsing nested divs, let's inject {% if %} directly inside the template.
    # Actually, it's safer to just inject it before the col-12 and after it.
    
    # We will just write a simple state machine to parse the file line by line
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    out_lines = []
    in_finance = False
    
    # Mapping sidebar ID to submenu code
    sidebars = {
        '#sidebarTresorerie': 'tresorerie',
        '#sidebarFinanceConseil': 'exec_edu',
        '#sidebarRemboursement': 'remboursement',
        '#sidebarRemises': 'remises',
        '#sidebarCaisse': 'caisse',
        '#sidebarBanque': 'banque',
        '#sidebarProduit': 'autres_paiements',
        '#sidebarDepenses': 'depenses',
        '#sidebarFournisseurs': 'fournisseurs',
        '#sidebarFactures': 'factures',
        '#sidbareParam': 'parametres',
        '#sidebarEcheanciers': 'echeanciers',
    }

    div_depth = 0
    current_submenu = None
    target_depth = 0

    for i, line in enumerate(lines):
        # Detect start of Finance menu
        if 'id="sidebarFinance"' in line:
            in_finance = True
            
        if not in_finance:
            out_lines.append(line)
            continue
            
        # If we are in finance, we look for Dashboard specifically
        if '<div class="submenu-item bg-light bg-opacity-50 rounded-2 mb-1">' in line and 'institut_app:FinanceDashboard' in lines[i+1]:
            out_lines.append(f"                                        {{% has_submenu_access request.user 'tre' 'dashboard' as can_view_dashboard %}}\n")
            out_lines.append(f"                                        {{% if can_view_dashboard %}}\n")
            out_lines.append(line)
            current_submenu = 'dashboard'
            target_depth = div_depth
            div_depth += line.count('<div') - line.count('</div')
            continue

        # Let's detect col-12 mt-2
        if '<div class="col-12 mt-2">' in line or '<div class="col-12 mt-2 mb-2">' in line:
            # Check next line for sidebar id
            next_line = lines[i+1]
            found = None
            for sb, code in sidebars.items():
                if f'href="{sb}"' in next_line:
                    found = code
                    break
            
            if found:
                out_lines.append(f"                                    {{% has_submenu_access request.user 'tre' '{found}' as can_view_{found} %}}\n")
                out_lines.append(f"                                    {{% if can_view_{found} %}}\n")
                out_lines.append(line)
                current_submenu = found
                target_depth = div_depth
                div_depth += line.count('<div') - line.count('</div')
                continue

        if current_submenu:
            div_depth += line.count('<div') - line.count('</div')
            out_lines.append(line)
            if div_depth == target_depth: # We closed the col-12 div
                out_lines.append(f"                                    {{% endif %}}\n")
                current_submenu = None
            continue
            
        out_lines.append(line)
        
        # Stop condition
        if '<!-- Fin Menu Finance -->' in line or ('id="sidebarRH"' in line):
            # Not exact, but we only need to parse inside finance.
            pass

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)

process_html(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\menu.html')
print("Done updating menu.html")
