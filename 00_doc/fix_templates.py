import os
import re

# ==============================================================================
# SCRIPT DE CORRECTION AUTOMATIQUE DES TEMPLATES (Archive)
# Date de création : 10/01/2026
# Usage : python 00_doc/fix_templates.py
# ==============================================================================

# Configuration
# Le script calcule le chemin absolu du dossier templates par rapport à son propre emplacement
# (Supposé être dans SCHOOL_SAAS/00_doc/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Liste des Remplacements (Regex, Remplacement)
# Ces patterns sont ceux utilisés lors de la correction massive du 10/01/2026.
REPLACEMENTS = [
    # Orthographe Mots-Clés
    (r"([Ss])éssion", r"\1ession"),
    (r"([Pp])lannification", r"\1lanification"),
    (r"([Hh])orraire", r"\1oraire"),
    (r"([Cc])oéfficiant", r"\1oefficient"),
    (r"([Ss])uppréssion", r"\1uppression"),
    (r"([Aa])cceuil", r"\1ccueil"),
    (r"Ressource Humaines", "Ressources Humaines"),
    
    # Grammaire / Conjugaison
    (r"\bà été\b", "a été"),
    (r"\bon été\b", "ont été"),
    (r"\bmis à jours\b", "mis à jour"),
    
    # Corrections Grammaire Alertify spécifiques (Messages Succès)
    (r"valider avec succès", "validée avec succès"), 
    (r"enregistrer avec succès", "enregistré avec succès"),
    (r"supprimer avec succès", "supprimé avec succès"),
    (r"effectuer avec succès", "effectuée avec succès"),
]

def fix_templates():
    print(f"Demarrage de la CORRECTION AUTOMATIQUE sur : {TEMPLATE_DIR}")
    
    if not os.path.exists(TEMPLATE_DIR):
        print(f"ERREUR CRITIQUE : Le dossier {TEMPLATE_DIR} n'existe pas.")
        return

    fixed_files = 0
    total_fixes = 0

    for root, dirs, files in os.walk(TEMPLATE_DIR):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    file_fixes = 0
                    
                    for pattern, replacement in REPLACEMENTS:
                        new_content, count = re.subn(pattern, replacement, content)
                        if count > 0:
                            content = new_content
                            file_fixes += count
                    
                    if file_fixes > 0:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Corrigé: {file} ({file_fixes} correction(s))")
                        fixed_files += 1
                        total_fixes += file_fixes
                        
                except Exception as e:
                    print(f"Erreur traitement {file}: {e}")

    print("-" * 50)
    print(f"Terminé. {total_fixes} corrections appliquées dans {fixed_files} fichiers.")

if __name__ == "__main__":
    fix_templates()
