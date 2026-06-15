import os
import re

ETUDIANTS_FILE = r'C:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_etudiants\urls.py'
GROUPE_FILE = r'C:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_groupe\urls.py'

def process_file(file_path, mappings):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    
    # Check if import is present
    if 'submenu_access_required' not in content:
        # Add import after the first few lines
        import_added = False
        for line in lines:
            if not import_added and line.startswith('app_name='):
                new_lines.append('from institut_app.decorators import submenu_access_required')
                import_added = True
            new_lines.append(line)
        lines = new_lines
        new_lines = []

    pattern = r'^(.*?path\([\'"].*?[\'"]\s*,\s*)([a-zA-Z0-9_\.]+(?:\.as_view\(\))?)(.*)$'

    for line in lines:
        if 'path(' in line and 'submenu_access_required' not in line:
            # Determine submenu code
            submenu_code = None
            for key, val in mappings.items():
                if key in line:
                    submenu_code = val
                    break
            
            if submenu_code:
                # Need to handle the .as_view() case as well
                match = re.search(pattern, line)
                if match:
                    new_line = f'{match.group(1)}submenu_access_required("sco", "{submenu_code}")({match.group(2)}){match.group(3)}'
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    print(f"Updated {file_path}")

mappings_etudiants = {
    'liste-des-etudiants': 'etudiants',
    'ApiListeDesEtudiants': 'etudiants',
    'ApiSaveStudentDatas': 'etudiants',
    'ApiSaveStudentNote': 'etudiants',
    'ApiUpdateStudentNote': 'etudiants',
    'ApiAccomplirNote': 'etudiants',
    'ApiSaveStudentRappel': 'etudiants',
    'ApiUpdateReminder': 'etudiants',
    'ApiGetStudentFinancialsData': 'etudiants',
    
    'registres-cours': 'presences',
    'ApiSaveRegistreGroupe': 'presences',
    'details-registre': 'presences',
    'liste_registres': 'presences',
    'details-liste-presence': 'presences',
    'ApiLoadDatas': 'presences',
    'ApiAjouterHistoriqueAbsence': 'presences',
    'ApiGetHistoriqueEtudiant': 'presences',
    'ApiUpdateAbsenceReason': 'presences',
    'presences-des-etudiants': 'presences',
    'etat-presences': 'presences',
    
    'contrat/modele': 'contrats',
    'ApiCreateModeleContrat': 'contrats',
    'ApiGetModeleContratByFormation': 'contrats',
    
    'transfert': 'transferts',
    'request-transfer': 'transferts',
    'get-specialites-promos': 'transferts',
    'update-transfer-status': 'transferts',
    'execute-transfer': 'transferts',
    'get-groups-for-transfer': 'transferts',
    'delete_transfer_request': 'transferts',
}

mappings_groupe = {
    'nouveau-groupe': 'groupes',
    'liste-des-groupes': 'groupes',
    'details-groupe': 'groupes',
    'mise-à-jour': 'groupes',
    'supprimer-groupe': 'groupes',
    'brouilon': 'groupes',
    'valider-groupe': 'groupes',
    'closeGroupe': 'groupes',
    'api-close-inscription': 'groupes',
    'api-open-inscription': 'groupes',
    'toggle-admissible-stage': 'groupes',
    'ApiGetGroupeList': 'groupes',
    'ApiUpdateGroupeCode': 'groupes',
    'ApiSelectSpecialite': 'groupes',
    'ApiGetFormation': 'groupes',
    'ApiListePromo': 'groupes',
    'ApiCreateGroupe': 'groupes',
    'ApiDeleteGroupe': 'groupes',
    'api-generate-payment': 'groupes',
    'bulk-print': 'groupes',
    
    'affectation-en-attente': 'affectations',
    'ApiLoadAttenteAffectation': 'affectations',
    'ApiListePromosEnAttente': 'affectations',
    'autre-affectation': 'affectations',
    'participants-confirmes': 'affectations',
    'affecter-participant-groupe': 'affectations',
    'ApiSpecialiteByPromo': 'affectations',
    'affectation-au-groupe': 'affectations',
    'ApiListeStudentNotAffected': 'affectations',
    'ApiGroupeListeForAffectation': 'affectations',
    'ApiGetSpecialiteDatas': 'affectations',
    'ApiGetBrouillonGroupes': 'affectations',
    'ApiAffectStudentToGroupe': 'affectations',
    'ApiCancelStudentAffectation': 'affectations',
    
    'profile-etudiant': 'etudiants',
    'ApiUpdate_etudiant': 'etudiants',
    'ApiUpdateStudentPassword': 'etudiants',
    'ApiUpdateStudentPhoto': 'etudiants',
    'students/': 'etudiants',
}

process_file(ETUDIANTS_FILE, mappings_etudiants)
process_file(GROUPE_FILE, mappings_groupe)
