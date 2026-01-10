# Processus Planification & Scolarité - SCHOOL_SAAS

**Modules :** `t_timetable`, `t_groupe`
**Version :** 1.0
**Dernière mise à jour :** 10 Janvier 2026

---

## 1. Vue d'Ensemble
Ces modules gèrent le "Quoi, Quand, Où, Qui".
Le système est conçu pour empêcher les conflits logistiques (Double réservation de salle ou de prof) avant même qu'ils n'arrivent.

## 2. Gestion des Groupes (Cohortes)

Le `Groupe` est l'entité pivot.
*   **Cycle de Vie :**
    1.  **Brouillon :** Création administrative. Suppression possible.
    2.  **Ouvert aux Inscriptions :** Les étudiants peuvent y être affectés.
    3.  **Actif / En Cours :** La scolarité a commencé.
    4.  **Clôturé :** Archivage.

## 3. Moteur d'Emplois du Temps (`Timetable`)

### Workflow de Conception
1.  **Initialisation :** Création d'un planning vierge pour un Groupe/Semestre.
2.  **Configuration des Créneaux (`ModelCrenau`) :** Définition de la grille horaire type (ex: 08:30 - 10:00, 10:15 - 11:45).
3.  **Placement des Cours (Drag & Drop logique) :**
    *   L'utilisateur place un Module sur un Créneau.
    *   **Vérificateurs de Conflits (Backend) :**
        *   `checkFormateurDispo` : Le prof est-il déjà pris ailleurs ?
        *   `checkSalleDispo` : La salle est-elle libre ?
        *   `checkAssignedSameHoraire` : Le groupe a-t-il déjà cours ?

### Validation & Génération Automatique
C'est le point fort du système.
Une fois le planning validé (`ApiValidateTimetable`) :
1.  Il devient figé (Lecture seule) pour les étudiants et profs.
2.  **Génération des Registres (`ApiGenerateRegistre`) :**
    *   Le système projette ce planning sur toute la durée du semestre.
    *   Il crée physiquement les entrées `RegistrePresence` pour chaque séance prévue.
    *   *Avantage :* Les feuilles de présence sont prêtes à l'avance pour la saisie des absences.

## 4. Gestion des Disponibilités
Les formateurs ont des contraintes (`dispo` JSONField dans `Formateurs`).
Le moteur de planning respecte ces contraintes lors de l'affectation.

---
*Ce processus garantit une logistique sans conflit et automatise la création des feuilles d'appel.*
