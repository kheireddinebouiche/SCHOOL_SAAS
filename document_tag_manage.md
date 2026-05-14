# Plan d'implémentation : Système de Tags pour l'Éditeur de Documents

Ce plan détaille la mise en place d'un système intelligent pour détecter, répertorier et injecter automatiquement des variables (tags) dans les templates de documents.

## Objectifs
- **Détection Automatique :** Identifier tous les tags `{{ variable }}` présents dans un template.
- **Registre Centralisé :** Définir une liste de tags disponibles par catégorie (Étudiant, Finance, Institution).
- **Préparation des Données :** Créer un mécanisme pour remplir ces tags avec les données réelles de la base de données.

---

## 1. Architecture du Système de Tags

### A. Registre des Tags (`pdf_editor/tags.py`) [NOUVEAU]
Création d'un fichier centralisant la définition des tags disponibles.

```python
TAG_REGISTRY = {
    'etudiant': {
        'student_name': 'Nom complet de l\'étudiant',
        'student_id': 'Matricule',
        'student_group': 'Groupe actuel',
        'student_formation': 'Formation suivie',
    },
    'finance': {
        'total_amount': 'Montant total du contrat',
        'paid_amount': 'Montant déjà payé',
        'remaining_amount': 'Reste à payer',
        'invoice_number': 'Numéro de facture',
    },
    'institution': {
        'school_name': 'Nom de l\'établissement',
        'school_logo': 'Logo de l\'école',
        'school_address': 'Adresse de l\'école',
    }
}
```

### B. Moteur de Détection (`pdf_editor/utils.py`)
Ajout d'une fonction pour extraire les tags d'un contenu HTML/TinyMCE.

```python
import re

def extract_tags(content):
    """Extrait tous les tags de type {{ variable }} du contenu"""
    return list(set(re.findall(r'\{\{\s*([\w\.]+)\s*\}\}', content)))
```

---

## 2. Intégration dans le Workflow

### A. Interface de l'Éditeur (TinyMCE)
- Ajouter un bouton "Insérer un Tag" dans la barre d'outils.
- Afficher une liste déroulante classée par catégories (Étudiant, Finance, etc.).

### B. Préparation du Contexte (Backend)
Modifier la logique de génération pour mapper les tags détectés aux champs des modèles Django.

```python
def prepare_document_context(template_type, object_id):
    """Prépare le dictionnaire de données pour le rendu"""
    context = {}
    if template_type == 'invoice':
        payment = Paiements.objects.get(id=object_id)
        context.update({
            'paid_amount': payment.montant_paye,
            'student_name': str(payment.etudiant),
            # ...
        })
    return context
```

---

## 3. Liste des Tags à Préparer (Initialement)

| Catégorie | Tag | Source (Modèle) |
| :--- | :--- | :--- |
| **Étudiant** | `{{ student_full_name }}` | `Etudiant.relation.nom/prenom` |
| **Étudiant** | `{{ student_birth_date }}` | `Etudiant.relation.date_naissance` |
| **Formation** | `{{ course_label }}` | `Formation.label` |
| **Finance** | `{{ amount_letters }}` | Conversion du montant en lettres |
| **Système** | `{{ current_date }}` | `timezone.now()` |

---

## 4. Avantages
- **Utilisation simple :** L'utilisateur n'a plus besoin de deviner le nom des variables.
- **Validation :** Le système peut avertir si un tag utilisé n'existe pas dans le registre.
- **Extensibilité :** Facile d'ajouter de nouveaux tags sans modifier la logique de rendu.

---

> [!IMPORTANT]
> Ce plan prévoit que chaque `template_type` (Facture, Contrat, etc.) ait accès à un sous-ensemble spécifique du registre de tags pour éviter les erreurs de contexte.

## Étapes de Validation
- [ ] Création du fichier `tags.py` avec les définitions.
- [ ] Test de la fonction d'extraction sur des templates existants.
- [ ] Intégration visuelle dans le sélecteur de variables de l'éditeur.
