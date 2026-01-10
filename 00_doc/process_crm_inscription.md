# Processus CRM & Inscription - SCHOOL_SAAS

**Modules :** `t_crm`, `t_etudiants`
**Version :** 1.0
**Dernière mise à jour :** 10 Janvier 2026

---

## 1. Vue d'Ensemble
Le CRM est le point d'entrée de tous les futurs étudiants. Il gère le "Pipeline d'Admission" qui transforme un inconnu (Visiteur) en client payant (Étudiant).

**Concept Clé :** L'entité `Prospets` (sic) est persistante. Un étudiant reste un prospect techniquement, seul son `statut` change.

## 2. Tunnel d'Admission (Workflow)

### Étape 1 : Saisie Visiteur (`VisiteurForm`)
*   **Source :** Accueil physique, Téléphone ou Site Web.
*   **Données :** État civil complet.
*   **Action :** Si le visiteur exprime un choix clair, une `DemandeInscription` est créée immédiatement avec :
    *   Formation / Spécialité.
    *   Session (Octobre/Mars).
    *   Promotion cible.

### Étape 2 : Commission Pédagogique
*   L'administration consulte la liste des demandes (`ListeDemandeInscription`).
*   **Validation (`ApiConfirmDemandeInscription`) :**
    *   L'administration clique sur "Accepter".
    *   L'état de la demande passe à `accepte`.
    *   Le statut du visiteur passe à `instance` (En attente de paiement).

### Étape 3 : Instance de Paiement (Le Verrou)
C'est l'étape critique qui lie le Pédagogique au Financier.
*   Automatiquement à l'acceptation, le système génère une **Demande de Paiement (`ClientPaiementsRequest`)**.
*   **Montant calculé :** Frais d'inscription + Assurance + (Éventuellement) 1ère tranche.
*   **Blocage :** Tant que cette demande n'est pas soldée dans le module **Trésorerie**, l'étudiant n'est pas considéré comme "Inscrit" (statut `convertit`).

## 3. Gestion de la Double Diplomation

Le système gère nativement les parcours hybrides via `FicheVoeuxDouble`.
*   Un étudiant peut avoir une inscription principale (ex: Master Local) et une "option" Double Diplôme.
*   Ces vœux suivent un circuit de validation parallèle.

## 4. Suivi Relationnel (CRM)

Même après inscription, le module `t_etudiants` permet de maintenir la relation :
*   **Notes de suivi (`NotesProcpects`) :** Commentaires libres sur le dossier étudiant (ex: "Problème de dossier manquant").
*   **Rappels (`RendezVous`) :** Système de tâches planifiées pour relancer l'étudiant (ex: "Rappel paiement tranche 2").

---
*Ce processus assure qu'aucun étudiant n'entre en scolarité sans être passé par la case finance.*
