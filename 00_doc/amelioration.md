# Pistes d'Amélioration & Refactorisation

Ce document propose des axes d'amélioration pour la maintenabilité, la performance et la clarté du code `SCHOOL_SAAS`.

## 1. Architecture des Modules
*   **Fusion/Nettoyage `t_commercial` vs `t_conseil` :**
    *   **Constat :** Le module `t_commercial` est présent mais vide (`models.py` contient des pass). Le module `t_conseil` semble contenir la logique B2B (Devis, Clients Entreprise).
    *   **Proposition :** Supprimer `t_commercial` et officialiser `t_conseil` comme module de Gestion Commerciale/Formation Continue.

*   **Module `t_stage` Embryonnaire :**
    *   **Constat :** Contient un modèle unique `Stagiaire`.
    *   **Proposition :** Si pas d'évolution prévue, intégrer ce modèle dans `t_etudiants` ou le développer complètement (Suivi de stage, maitre de stage, rapport).

## 2. Conventions de Nommage (Code Style)
*   **Modèles Django (Singulier vs Pluriel) :**
    *   **Standard Django :** Les noms de classes doivent être au singulier (ex: `Employee`, `Role`).
    *   **Actuel :** `Employees`, `Roles`, `Contrats` (Pluriel).
    *   **Proposition :** Renommer les modèles au singulier lors d'un futur refactor majeur (risqué sans couverture de tests).

*   **Variables Obscures :**
    *   `t_formations.models`: `n_elimate` -> `note_eliminatoire`
    *   `t_rh.models`: Clarifier `ArticlesContratStandard` vs `ArticleContratSpecial`.

## 3. Sécurité & Bonnes Pratiques
*   **Gestion des Secrets :** S'assurer que `DEBUG=True` n'est jamais actif en production.
*   **URLs Hardcodées :** Remplacer les chaînes de redirection login hardcodées (source du bug `insitut`) par des constantes ou `reverse_lazy`.

## 4. Frontend & UX
*   **Internationalisation (i18n) :**
    *   Le projet mélange traduction manuelle et textes en dur.
    *   **Proposition :** Utiliser systématiquement `{% trans "Texte" %}` et les fichiers `.po` de Django pour faciliter le support futur de l'arabe ou de l'anglais.

*   **Feedback Utilisateur :**
    *   Les `alertify` sont bien utilisés mais contiennent beaucoup de fautes de grammaire générées manuellement. Créer une classe utilitaire JS pour uniformiser les messages (ex: `Notify.success('create', 'Visiteur')` qui génère "Visiteur créé avec succès" sans faute).

---
*Dernière mise à jour : 10/01/2026*
