import os
import re

IMPORT_STMT = "from institut_app.decorators import module_permission_required\n"

# Map of filepath -> [(function_name, module_code, permission_code)]
FILES_TO_MODIFY = {
    r"t_tresorerie/f_views/depenses.py": [
        ("ApiValidateDepense", "tre", "approuv"),
    ],
    r"t_tresorerie/f_views/preinscrit_paiements.py": [
        ("ApiConfirmInscription", "tre", "approuv"),
        ("ApiConfirmInscriptionDouble", "tre", "approuv"),
    ],
    r"t_tresorerie/f_views/facturation.py": [
        ("ApiValidateFacture", "tre", "approuv"),
    ],
    r"t_tresorerie/f_views/echeancier_special.py": [
        ("ApiValidateEcheancierSpecial", "tre", "approuv"),
        ("ApiApproveEcheancierSpecial", "tre", "approuv"),
    ],
    r"t_crm/views.py": [
        ("ApprouveVisiteurInscription", "crm", "approuv"),
        ("ApiConfirmDemandeInscription", "crm", "approuv"),
    ],
    r"t_crm/f_views/secondwishe.py": [
        ("ApiConfirmeSecondWish", "crm", "approuv"),
    ],
    r"t_crm/f_views/reminder.py": [
        ("ApiValidateRemider", "crm", "approuv"),
    ],
    r"t_crm/f_views/prinscrits.py": [
        ("ApiValidatePreinscrit", "crm", "approuv"),
    ],
    r"t_crm/f_views/prospects.py": [
        ("ApiValidateProspect", "crm", "approuv"),
        ("ApiValidateProspectDouble", "crm", "approuv"),
        ("ApiConfirmeDoubleDiplome", "crm", "approuv"),
    ],
    r"t_conseil/views.py": [
        ("ApiValidateDevis", "con", "approuv"),
        ("ApiValidateFacture", "con", "approuv"),
    ],
    r"t_conseil/f_views/groupes_conseil.py": [
        ("ApiConfirmParticipantForScolarite", "con", "approuv"),
        ("ApiCancelParticipantConfirmationForScolarite", "con", "approuv"),
    ],
    r"t_exam/f_views/commission.py": [
        ("validate_commission", "exa", "approuv"),
    ],
    r"t_exam/f_views/exam_plan.py": [
        ("validate_exam", "exa", "approuv"),
        ("validate_pv_exam", "exa", "approuv"),
    ],
    r"t_groupe/views.py": [
        ("validateGroupe", "scol", "approuv"),
    ],
    r"t_groupe/f_views/affectations.py": [
        ("ApiParticipantsConfirmes", "scol", "approuv"),
    ],
    r"t_timetable/views.py": [
        ("ApiValidateTimetable", "int", "approuv"),
    ],
    r"t_rh/views.py": [
        ("validerConge", "rh", "approuv"),
    ],
    r"t_stage/views.py": [
        ("validation_council", "rel", "approuv"),
    ],
}

def process_file(filepath, functions):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add import if missing
    if "from institut_app.decorators import module_permission_required" not in content:
        # Insert after other imports, typically after django imports
        if "from django." in content:
            # find last django import
            last_import = max(content.rfind("from django."), content.rfind("import "))
            # find end of that line
            end_of_line = content.find("\n", last_import)
            content = content[:end_of_line+1] + IMPORT_STMT + content[end_of_line+1:]
        else:
            content = IMPORT_STMT + content

    lines = content.split('\n')
    modified_lines = []
    
    for i, line in enumerate(lines):
        modified_lines.append(line)
        for func_name, mod_code, perm_code in functions:
            match = re.match(rf'^def {func_name}\(', line)
            if match:
                # check if decorator is already on the previous line
                prev_line = modified_lines[-2] if len(modified_lines) > 1 else ""
                decorator = f"@module_permission_required('{mod_code}', '{perm_code}')"
                
                # Check if it already has this specific decorator
                if decorator not in prev_line and decorator not in modified_lines[-3:-1]:
                    # Need to insert decorator right before the def
                    # We have to pop the 'def' line, append decorator, append 'def' line
                    def_line = modified_lines.pop()
                    modified_lines.append(decorator)
                    modified_lines.append(def_line)
                    print(f"Decorated {func_name} in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(modified_lines))

for fp, funcs in FILES_TO_MODIFY.items():
    process_file(fp, funcs)

print("Done applying decorators.")
