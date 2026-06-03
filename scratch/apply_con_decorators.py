import os
import re

IMPORT_STMT = "from institut_app.decorators import module_permission_required\n"

VIEWS_MAPPING = {
    "ConseilDashboard": "view",
    "PipelineConseil": "view",
    "ListeGroupesConseil": "view",
    "PaiementsConseilListe": "view",
    "ListeDesDevis": "view",
    "ListeDesFactures": "view",
    "ListeDesAvoirs": "view",
    "ListeDesClients": "view",
    "ListeThematique": "view",
    "ListeDAS": "view",
    "DetailsProspectConseil": "view",
    "DetailsClient": "view",
    "DetailsDevis": "view",
    "DetailsFacture": "view",
    "DetailsGroupeConseil": "view",
    "ApiLoadProspect": "view",
    "ApiListeClients": "view",
    "ApiLoadProspectDevis": "view",
    "ApiLoadProspectFactures": "view",
    "ApiLoadProspectFinancials": "view",
    "ApiGetClientDevis": "view",
    "ApiGetDevisDetails": "view",
    "ApiLoadThematique": "view",
    "ApiLoadThematiqueDetails": "view",
    "ApiLoadArchivedThematique": "view",
    "ApiGetOpportunite": "view",
    "ApiGetDegreeFormations": "view",
    "ApiLoadDegreeFormationsList": "view",
    "ApiGetSpecialiteDetails": "view",
    "ApiGetGroups": "view",
    "ApiLoadProspectParticipants": "view",
    "ApiLoadBankAccounts": "view",
    "ExportPipelineCsv": "view",
    "SessionAttendancePDF": "view",
    
    "AddNewDevis": "add",
    "AddNewFacture": "add",
    "NouveauGroupeConseil": "add",
    "ConfigurationConseil": "add",
    "ApiSaveThematique": "add",
    "ApiCreateProspect": "add",
    "ApiQuickCreateProspect": "add",
    "ApiSaveLigneDevis": "add",
    "ApiSaveDevisItems": "add",
    "ApiSaveFactureItems": "add",
    "ApiCreateOpportunite": "add",
    "ApiAddPaiement": "add",
    "ApiCreateAvoir": "add",
    "ApiSaveDAS": "add",
    "ApiSaveParticipants": "add",
    "ApiEnrollToGroup": "add",
    "ApiSaveParticipant": "add",
    "ApiSaveEtsDetails": "add",
    "ApiSaveBankAccount": "add",
    "ApiCreateGroupFromParticipants": "add",
    "ApiSaveConseilGroupe": "add",
    "ApiAddPlanningSession": "add",
    "make_prospect_client": "change",

    "configure_devis": "change",
    "configure_facture": "change",
    "ApiActivateThematique": "change",
    "ApiUpdateThematique": "change",
    "ApiTransformeToClient": "change",
    "ApiStartTransformationDevisToFacture": "change",
    "ApiUpdatePipelineStage": "change",
    "ApiToggleFavorite": "change",
    "ApiConvertProspectToDevis": "change",
    "ApiUpdateOpportunite": "change",
    "ApiUpdateGroupeSettings": "change",
    "ApiRevertDevisToDraft": "change",
    "ApiRevertFactureToDraft": "change",
    "ApiCloturerGroupeConseil": "change",

    "ArchiveThematique": "delete",
    "ApiArchiveThematique": "delete",
    "ApiDeleteFinalThematique": "delete",
    "ApiDeleteOpportunite": "delete",
    "ApiDeleteDevis": "delete",
    "ApiDeleteFacture": "delete",
    "ApiDeleteDAS": "delete",
    "ApiDeleteParticipant": "delete",
    "ApiDeleteBankAccount": "delete",
    "ApiDeleteGroupeConseil": "delete",
    "ApiDeletePlanningSession": "delete"
}

FILES = [
    r"t_conseil/views.py",
    r"t_conseil/f_views/groupes_conseil.py",
    r"t_conseil/f_views/prospects.py",
]

for filepath in FILES:
    if not os.path.exists(filepath):
        print(f"Not found: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Check import
    has_import = any("module_permission_required" in line for line in lines)
    if not has_import:
        lines.insert(0, IMPORT_STMT)
        
    modified_lines = []
    
    for i, line in enumerate(lines):
        modified_lines.append(line)
        match = re.match(r'^def ([A-Za-z0-9_]+)\(', line)
        if match:
            func_name = match.group(1)
            if func_name in VIEWS_MAPPING:
                perm = VIEWS_MAPPING[func_name]
                decorator = f"@module_permission_required('con', '{perm}')"
                
                prev_line = modified_lines[-2] if len(modified_lines) > 1 else ""
                prev_prev = modified_lines[-3] if len(modified_lines) > 2 else ""
                
                # check if this specific decorator is already there
                # Or if any @module_permission_required is there (like 'approuv' which we did earlier)
                if decorator not in prev_line and decorator not in prev_prev:
                    if "@module_permission_required" not in prev_line and "@module_permission_required" not in prev_prev:
                        def_line = modified_lines.pop()
                        modified_lines.append(decorator + "\n")
                        modified_lines.append(def_line)
                        print(f"Added {decorator} to {func_name} in {filepath}")
                    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(''.join(modified_lines))

print("Done applying decorators to con module.")
