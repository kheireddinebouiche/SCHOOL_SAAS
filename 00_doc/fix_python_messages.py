import os
import re

# Configuration
PROJECT_DIR = r"c:/Users/mbenk/Documents/model_project/SCHOOL_SAAS"

# Remplacements ciblés sur les messages (Strings dans Python)
# On inclut les variantes de conjugaison horribles trouvées
REPLACEMENTS = [
    # Verbe 'Avoir' vs 'à'
    (r"\bà été crée\b", "a été créé"),
    (r"\bà été créée\b", "a été créée"),
    (r"\bà été effectuer\b", "a été effectuée"),
    (r"\bà été effectué\b", "a été effectué"),
    (r"\bà été enregistrer\b", "a été enregistré"),
    (r"\bà été enregistré\b", "a été enregistré"),
    (r"\bà été supprimer\b", "a été supprimé"),
    (r"\bà été supprimée\b", "a été supprimée"),
    (r"\bà été ajouter\b", "a été ajouté"),
    (r"\bà été ajoutée\b", "a été ajoutée"),
    (r"\bà été affecter\b", "a été affecté"),
    (r"\bà été planifier\b", "a été planifié"),
    (r"\bà été valider\b", "a été validée"), # Souvent fém. (demande, note)
    
    # Pluriels et Accords
    (r"\bon été mis à jours\b", "ont été mises à jour"), # Souvent "les données" ou "les infos"
    (r"\bont été mis à jours\b", "ont été mises à jour"),
    (r"\bon été modifier\b", "ont été modifiées"),
    
    # Orthographe pure
    (r"([Ss])uppréssion", r"\1uppression"),
    (r"([Cc])oéfficiant", r"\1oefficient"),
    (r"([Hh])orraire", r"\1oraire"),
    (r"([Ss])éssion", r"\1ession"),
    (r"Accueil", "Accueil"), # Risqué dans le code ? Seulement si string. Grep a montré usage dans choices.
]

def fix_python_files():
    print(f"Demarrage de la CORRECTION PYTHON sur {PROJECT_DIR}...")
    fixed_count = 0
    
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Ignorer venv et .git
        if 'venv' in root or '.git' in root or '__pycache__' in root:
            continue
            
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    file_fixes = 0
                    
                    for pattern, replacement in REPLACEMENTS:
                        # On remplace globalement dans le fichier
                        new_content, count = re.subn(pattern, replacement, content)
                        if count > 0:
                            content = new_content
                            file_fixes += count
                    
                    if file_fixes > 0:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Corrigé: {file} ({file_fixes} fautes)")
                        fixed_count += 1
                        
                except Exception as e:
                    print(f"Erreur traitement {file}: {e}")

    print(f"Terminé. {fixed_count} fichiers Python corrigés.")

if __name__ == "__main__":
    fix_python_files()
