import os

FILES_TO_MODIFY = [
    r"t_tresorerie/f_views/depenses.py",
    r"t_tresorerie/f_views/preinscrit_paiements.py",
    r"t_tresorerie/f_views/facturation.py",
    r"t_tresorerie/f_views/echeancier_special.py",
    r"t_crm/views.py",
    r"t_crm/f_views/secondwishe.py",
    r"t_crm/f_views/reminder.py",
    r"t_crm/f_views/prinscrits.py",
    r"t_crm/f_views/prospects.py",
    r"t_conseil/views.py",
    r"t_conseil/f_views/groupes_conseil.py",
    r"t_exam/f_views/commission.py",
    r"t_exam/f_views/exam_plan.py",
    r"t_groupe/views.py",
    r"t_groupe/f_views/affectations.py",
    r"t_timetable/views.py",
    r"t_rh/views.py",
    r"t_stage/views.py",
]

IMPORT_STMT = "from institut_app.decorators import module_permission_required"

for filepath in FILES_TO_MODIFY:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    already_has_import = False
    
    for line in lines:
        if IMPORT_STMT in line:
            continue
        new_lines.append(line)
        
    # Now insert at the top
    # Check if there is already an import of module_permission_required (sometimes it's from institut_app.decorators import ... module_permission_required)
    
    # We'll just insert it at line index 1 (or 0)
    new_lines.insert(0, IMPORT_STMT + "\n")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
print("Imports fixed.")
