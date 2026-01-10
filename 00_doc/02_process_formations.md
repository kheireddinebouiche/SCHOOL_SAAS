# Processus Offre Pédagogique - SCHOOL_SAAS

**Module :** `t_formations`
**Version :** 1.0
**Dernière mise à jour :** 10 Janvier 2026

---

## 1. Vue d'Ensemble
Ce module est le catalogue produits de l'école. Il définit ce qui est enseigné, combien ça coûte, et comment c'est structuré dans le temps.

**Particularité SaaS :** L'offre est centralisée par le "Master Tenant" et propagée vers les agences. Une agence ne crée pas ses propres diplômes (sauf exception), elle les reçoit.

## 2. Modèle de Données Académiques

### Hiérarchie Standard
1.  **Formation (`Formation`)**
    *   Objet racine (ex: Master Général).
    *   Définit le **Partenaire** (Diplôme national ou Étranger).
    *   *Exemple :* MBDS (Partenaire: Université Nice Sophia Antipolis).

2.  **Spécialité (`Specialites`)**
    *   C'est le produit vendable.
    *   Détails : Prix standard, Prix double diplomation (souvent plus cher).
    *   **Versioning :** Champ `version` et `etat` ('last'/'updated') pour gérer les évolutions de programme sans casser l'historique des anciens étudiants.

3.  **Module (`Modules`)**
    *   L'unité atomique d'enseignement.
    *   Attributs : Coefficient, Durée (Heures), Note éliminatoire (`n_elimate`).

4.  **Programme (`ProgrammeFormation`)**
    *   La "recette" qui assemble les Modules dans des Semestres pour une Spécialité donnée.
    *   *Exemple :* Le module "Comptabilité" est enseigné au Semestre 1 de la spécialité "Finance" mais au Semestre 2 de la spécialité "Management".

## 3. Workflow de Synchronisation (Master -> Tenants)

Le système utilise un mécanisme de **Push Sync** déclenché manuellement par l'administrateur Master.

### Algorithme `ApiSyncUpdateFormation`
1.  L'admin modifie une Formation ou ses Modules sur le Master.
2.  Il clique sur "Synchroniser".
3.  Le système itère sur **tous les Tenants** (sauf 'public').
4.  Pour chaque Tenant :
    *   Change le contexte PostgreSQL (`schema_context`).
    *   **Upsert** (Update or Create) la Formation.
    *   **Upsert** les Spécialités associées.
    *   **Upsert** les Modules.
5.  *Résultat :* Toutes les écoles du réseau ont instantanément le programme à jour.

## 4. Gestion des Promos (Rentrées)

L'objet `Promos` définit les périodes temporelles d'accueil (Cohortes).
*   **Sessions :** Octobre (Rentrée classique) ou Mars (Rentrée décalée).
*   **Cycle de vie :**
    *   Une promo a une date de début et de fin.
    *   Elle porte les règles financières de la période : `prix_rachat_credit`, `penalite_retard`.

---
*Ce processus garantit l'uniformité académique sur tout le réseau d'écoles.*
