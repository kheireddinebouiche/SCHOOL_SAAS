import re

mapping = {
    'tresorerie': ['AttentesPaiements', 'SuivieEcheancier', 'PageSuiviPaiements', 'ListePenalite', 'ListeDesPaiements'],
    'remboursement': ['PageRemboursement', 'listeDesRembourssement', 'DetailsRembourssement'],
    'exec_edu': ['ListeDesFactures', 'ListeDesDevis', 'ListeDesClients'],
    'remises': ['ListeRemise'],
    'caisse': ['PageBrouillardCaisse', 'PageDepotBanque'],
    'banque': ['PageBrouillardBanque', 'PageSituationComptes', 'ImputationBancaire', 'PageRecouvrement'],
    'autres_paiements': ['PageAutrePaiements', 'PageNouveauAutrePaiement'],
    'depenses': ['PageDepenses', 'PageNouvelleDepense'],
    'fournisseurs': ['PageFournisseur', 'PageNouveauFournisseur', 'PageDetailsFournisseur'],
    'factures': ['PageFacturation', 'PageFacturesAvoir', 'DetailsFactureTresorerie'],
    'parametres': ['PageConfigPaiementSeuil', 'PageConfigPaiementFacturation', 'liste_types_depenses', 'PageProduits', 'PageCategoriesProduits', 'PageImputationComptable', 'PageConfPenalite', 'payment_type_list', 'PagePlanComptable', 'PagePlanComptableRecetteDepense'],
    'echeanciers': ['ListeModelEcheancier', 'CreeEcheancier', 'ListeEcheanciersConfigures', 'ListeEcheancierSpecial']
}

view_to_submenu = {}
for submenu, views in mapping.items():
    for v in views:
        view_to_submenu[v] = submenu

with open('t_tresorerie/urls.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'from django.urls import path' in line:
        new_lines.append(line)
        new_lines.append('from institut_app.decorators import submenu_access_required\n')
        continue
    
    modified = False
    for view_name, submenu_code in view_to_submenu.items():
        # Look for the exact view name passed as the second argument to path()
        # Pattern: space or comma, then optionally a module prefix, then view_name, then comma
        pattern = r'(,\s*(?:[a-zA-Z0-9_]+\.)?)(' + view_name + r')(\s*,)'
        if re.search(pattern, line) and 'submenu_access_required' not in line:
            replacement = r'\g<1>submenu_access_required("tre", "' + submenu_code + r'")(\g<2>)\g<3>'
            line = re.sub(pattern, replacement, line)
            modified = True
    new_lines.append(line)

with open('t_tresorerie/urls.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Protected t_tresorerie/urls.py")
