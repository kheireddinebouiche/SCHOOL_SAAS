import os
import re

TRH_VIEWS = r't_rh/views.py'
TRESOURCE_VIEWS = r't_ressource_humaine/views.py'

# ----------------- t_rh/views.py -----------------
with open(TRH_VIEWS, 'r', encoding='utf-8') as f:
    content_trh = f.read()

# Make sure imports are present
if 'module_permission_required' not in content_trh:
    content_trh = "from institut_app.decorators import module_permission_required\n" + content_trh

# Clean existing @module_permission_required (except validerConge which is correct but we'll overwrite it anyway)
content_trh = re.sub(r'@module_permission_required\([^\)]+\)\n', '', content_trh)

trh_perm_map = {
    'dashboardRH': 'view',
    'listeEmployes': 'view',
    'detailsEmploye': 'view',
    'listeServices': 'view',
    'ApiListeServices': 'view',
    'ApiGetService': 'view',
    'listeTypeContrat': 'view',
    'ApiListeTypeContrat': 'view',
    'ApiGetTypeContrat': 'view',
    'ClausesTypeContrat': 'view',
    'ApiGetClauseStandardOfType': 'view',
    'ListeCategorieContrat': 'view',
    'ApiListCategorie': 'view',
    'detailsCategorie': 'view',
    'ApiGetCategorieContratDetails': 'view',
    'ApiGetCategorieContrat': 'view',
    'ApiGetDefaultValueForContrat': 'view',
    'ApiGetListeTypeContratByCategorie': 'view',
    'ApiGetRubriquesOfType': 'view',
    'ApiGetListContratForEmploye': 'view',
    'ApiGetDetailsOfContract': 'view',
    'listeArticlesContrat': 'view',
    'detailsArticleContrat': 'view',
    'ApiListePostes': 'view',
    'ListeDesPostes': 'view',
    'ApiGetPostDetails': 'view',
    'ApiGetListPostTaches': 'view',
    'ApiGetEntite': 'view',
    'listeDesContrats': 'view',
    'imprimerContrat': 'view',
    'imprimerAttestation': 'view',
    'imprimerBadge': 'view',
    'listePresences': 'view',
    'fichesMensuelles': 'view',
    'listeConges': 'view',
    'listeFichesPaie': 'view',
    'detailFichePaie': 'view',
    'hubConfigRH': 'view',
    'assistantPaie': 'view',
    
    'nouveauEmploye': 'add',
    'nouveauService': 'add',
    'ApiAddService': 'add',
    'ApiAddTypeContrat': 'add',
    'ApiAddNewClause': 'add',
    'ApiAddCategorieContrat': 'add',
    'NouveauArticleContrat': 'add',
    'ApiAddPoste': 'add',
    'nouveauContrat': 'add',
    'ApiCreateContrat': 'add',
    'ApiMarkPresence': 'add',
    'demandeConge': 'add',
    
    'updateEmploye': 'change',
    'ApiUpdateService': 'change',
    'ApiUpdateTypeContrat': 'change',
    'ApiUpdateClause': 'change',
    'ApiUpdateCategorieGroupe': 'change',
    'ApiUpdateCategorie': 'change',
    'modifierArticleContrat': 'change',
    'UpdatePoste': 'change',
    'configFiscalite': 'change',
    'configRH': 'change',
    
    'ApiDeleteService': 'delete',
    'ApiDeleteTypeContrat': 'delete',
    'ApiDeleteClause': 'delete',
    'ApiDeleteCategorie': 'delete',
    'supprimerArticleContrat': 'delete',
    
    'validerConge': 'approuv',
}

def add_decorator_trh(match):
    func_def = match.group(0)
    func_name_match = re.search(r'def\s+([a-zA-Z0-9_]+)\(', func_def)
    if func_name_match:
        func_name = func_name_match.group(1)
        if func_name in trh_perm_map:
            perm = trh_perm_map[func_name]
            decorator = f"@module_permission_required('rh', '{perm}')\n"
            return decorator + func_def
    return func_def

content_trh = re.sub(r'def\s+[a-zA-Z0-9_]+\(', add_decorator_trh, content_trh)

with open(TRH_VIEWS, 'w', encoding='utf-8') as f:
    f.write(content_trh)
print("Updated t_rh/views.py")

# ----------------- t_ressource_humaine/views.py -----------------
with open(TRESOURCE_VIEWS, 'r', encoding='utf-8') as f:
    content_tress = f.read()

imports_to_add = []
if 'method_decorator' not in content_tress:
    imports_to_add.append("from django.utils.decorators import method_decorator")
if 'module_permission_required' not in content_tress:
    imports_to_add.append("from institut_app.decorators import module_permission_required")

if imports_to_add:
    content_tress = "\n".join(imports_to_add) + "\n" + content_tress

# Clean existing decorators just in case
content_tress = re.sub(r'@module_permission_required\([^\)]+\)\n', '', content_tress)
content_tress = re.sub(r'@method_decorator\(module_permission_required\([^\)]+\),\s*name=[\'"]dispatch[\'"]\)\n', '', content_tress)

tress_fbv_map = {
    'fiches_mensuelles': 'view',
    'select_entreprise_paie': 'view',
    'export_rubriques': 'view',
    
    'generer_paie': 'add',
    'init_conventional_primes': 'add',
    'import_rubriques': 'add',
    
    'modifier_paie': 'change',
    'config_paie': 'change',
    'manage_rubriques_contrat': 'change',
    
    'supprimer_paie': 'delete',
}

tress_cbv_map = {
    'ContratListView': 'view',
    'ContratDetailView': 'view',
    'FichePaieListView': 'view',
    'FichePaieDetailView': 'view',
    'RubriqueListView': 'view',
    
    'ContratCreateView': 'add',
    'RubriqueCreateView': 'add',
    
    'ContratUpdateView': 'change',
    'RubriqueUpdateView': 'change',
    
    'RubriqueDeleteView': 'delete',
}

def add_decorator_tress_fbv(match):
    func_def = match.group(0)
    func_name_match = re.search(r'def\s+([a-zA-Z0-9_]+)\(', func_def)
    if func_name_match:
        func_name = func_name_match.group(1)
        if func_name in tress_fbv_map:
            perm = tress_fbv_map[func_name]
            decorator = f"@module_permission_required('rh', '{perm}')\n"
            return decorator + func_def
    return func_def

def add_decorator_tress_cbv(match):
    cls_def = match.group(0)
    cls_name_match = re.search(r'class\s+([a-zA-Z0-9_]+)\(', cls_def)
    if cls_name_match:
        cls_name = cls_name_match.group(1)
        if cls_name in tress_cbv_map:
            perm = tress_cbv_map[cls_name]
            decorator = f"@method_decorator(module_permission_required('rh', '{perm}'), name='dispatch')\n"
            return decorator + cls_def
    return cls_def

content_tress = re.sub(r'def\s+[a-zA-Z0-9_]+\(', add_decorator_tress_fbv, content_tress)
content_tress = re.sub(r'class\s+[a-zA-Z0-9_]+\(', add_decorator_tress_cbv, content_tress)

with open(TRESOURCE_VIEWS, 'w', encoding='utf-8') as f:
    f.write(content_tress)
print("Updated t_ressource_humaine/views.py")

