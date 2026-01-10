# Processus Core & Administration - SCHOOL_SAAS

**Module :** `institut_app`
**Version :** 2.0 (Détaillée)
**Dernière mise à jour :** 10 Janvier 2026

---

## 1. Vue d'Ensemble & Dashboards
Le module Core orchestre l'expérience utilisateur dès la connexion. Il route l'utilisateur vers le tableau de bord approprié selon son rôle principal.

### Tableaux de Bord (Logique de Routing)
*   **CRM Dashboard (`crm_dashboard`) :**
    *   **KPIs :** Taux de conversion (Prospect -> Étudiant), Convertis par Canal (Instagram, Web...), Rappels en attente.
    *   **Visualisation :** Graphique d'évolution des prospects sur 7 jours.
*   **Pédagogie Dashboard (`pedago_dashboard`) :**
    *   **KPIs :** Groupes actifs, Taux d'occupation salles.
    *   **Gantt :** Visualisation temps réel de l'occupation des salles (`Gantt Chart` basé sur `TimetableEntry`).
*   **Finance Dashboard :** Vue macro des échéances échues et des encaissements du jour.

## 2. Processus : Initialisation & Identité Tenant

### Création (SuperAdmin)
La vue `NewEntreprise` initialise une nouvelle entité juridique.
*   **Contrôles :** Unicité du RC et NIF.
*   **Configuration API :** La méthode `ApiUpdateEntreprise` permet la mise à jour asynchrone des métadonnées (Site web, Téléphone, Adresses) sans rechargement de page.

## 3. Sécurité & Gestion des Utilisateurs

### Authentification Renforcée
1.  **Contrôle de Session Unique :**
    *   À chaque login (`login_view`), une clé de session est stockée dans `UserSession`.
    *   Si un utilisateur tente de se reconnecter ailleurs, le système détecte le conflit et peut bloquer l'accès (`ShowBlockedConnexion`).
2.  **Activation/Désactivation :**
    *   Les APIs `ApiActivateUser` / `ApiDeactivateUser` permettent un blocage immédiat d'un compte sans le supprimer (archivage logique).

### Workflow RBAC (Role-Based Access Control)
Le système ne se contente pas des groupes Django. Il calcule les **Permissions Effectives**.

**Algorithme d'accès (`GetMyProfile`) :**
1.  Récupération de l'utilisateur connecté.
2.  Interrogation de la table de liaison `UserModuleRole`.
3.  Pour chaque module assigné :
    *   Récupération du Rôle (ex: "Manager").
    *   Extraction des `RolePermission` associées.
    *   *Résultat :* Une liste JSON de capacités (ex: `['crm.add_prospect', 'crm.view_prospect']`) injectée dans le contexte du template.

## 4. Structures Critiques & API

### Gestion des Salles (Immobilier)
*   Utilisé par le diagramme de Gantt pédagogique.
*   Données critiques : Capacité (pour alerte surcharge), Type (TP/Cours/Amphi).

### APIs Internes (JSON)
Le frontend communique massivement avec le backend via des endpoints dédiés :
*   `ApiListeUsers` : Liste légère pour les Select2.
*   `ApiGetDetailsProfile` : Récupération asynchrone des données RH.
*   `ApiFinanceKPIs` : Calcul temps réel des dettes et échéances pour le widget header.

---
*Ce document détaille la logique implémentée dans `views.py` et `models.py`.*
