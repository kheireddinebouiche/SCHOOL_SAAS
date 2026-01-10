# Processus Examens & Délibérations - SCHOOL_SAAS

**Module :** `t_exam`
**Version :** 1.0
**Dernière mise à jour :** 10 Janvier 2026

---

## 1. Vue d'Ensemble
Ce module gère à la fois la **logistique** (qui passe l'examen quand ?) et le **pédagogique** (calcul des notes, jury et décisions de passage).

## 2. Cycle de Vie d'une Session d'Examen

### 2. Planification d'une Session
**Acteurs :** Directeur des Études, Admin.

1.  **Création de la Session :**
    *   Définition d'un code unique (ex: `S1_2023`).
    *   Dates de début et de fin (Validation requise).
    *   **Configuration des Groupes :** Association des groupes d'étudiants à la session.
        *   Sélection du Groupe.
        *   Choix du **Semestre** (1, 2, 3, 4).
        *   Dates spécifiques pour le groupe (Début/Fin).

2.  **Ajout de Modules (Si hors programme standard) :**
    *   Nom du module, Code Module.
    *   **Coefficient** et **Volume Horaire**.
    *   *Note : Ces infos surchargeant potentiellement le programme par défaut.*

3.  **Planification des Examens (Calendrier) :**
    *   Pour chaque module, on définit une "Ligne de Planification" :
        *   **Type d'examen :** Ordinaire, Rachat de crédit, Rattrapage.
        *   **Mode :** Examen sur table, Travail à remettre, En ligne.
        *   **Logistique :** Date, Heure Début/Fin, Salle.
    *   Génération automatique des **Feuilles d'Émargement**.

### Phase 2 : Notation & PV (`PvExamen`)
Une fois l'examen passé :
1.  Les notes sont saisies dans le système via les PV numériques.
2.  Le système supporte des structures de notes complexes :
    *   **NoteBloc :** Groupe de types de notes (ex: CC + EMD).
    *   **ExamTypeNote :** Type précis (ex: TP, Oral, Écrit).
    *   **ExamSousNote :** Sous-division fine.

### Phase 3 : Délibération & Commission (`deliberation.py`, `commission.py`)
C'est le calcul final.
1.  **Tableau de Délibération :** Le système agrège toutes les notes par étudiant et par module.
2.  **Calcul de la Moyenne :** Application des coefficients des modules.
3.  **Décision du Jury :**
    *   *Admis*
    *   *Ajourné* (Avec liste des modules à repasser)
    *   *Rachat* (Passage conditionnel)

### Phase 4 : Clôture & Automatisation
Action puissante du système lors de la clôture d'une commission (`close_commission`) :
*   Si des étudiants sont **Ajournés**, le système peut **automatiquement générer la Session de Rattrapage**.
*   Il pré-crée les planifications pour les modules échoués uniquement.

---
*Ce processus automatise la transition critique entre l'échec à une session et l'inscription au rattrapage.*
