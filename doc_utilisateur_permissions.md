# Documentation Utilisateur : Module Interface Utilisateur (Administration)

Le module **Utilisateur & Permissions** est accessible depuis le menu principal, sous la section **Configuration**. Il permet aux administrateurs (et utilisateurs disposant des droits nécessaires) de gérer les comptes utilisateurs, leurs rôles, leurs accès, ainsi que de surveiller l'activité sur l'application.

> [!NOTE]
> Seuls les utilisateurs avec des droits d'administration (Superuser ou des rôles spécifiques) peuvent accéder et modifier ces éléments.

## Accès au Module
1. Dans le menu latéral de gauche de l'application, descendez jusqu'à la section de fin.
2. Cliquez sur l'onglet **Configuration** pour le dérouler.
3. Cliquez ensuite sur la section **Utilisateur & Permissions** (marquée par une icône en forme d'engrenage / de réglages) pour afficher les différentes options du module.

---

## Guide d'Utilisation : Étape par Étape

### A. Comment créer un nouvel utilisateur ?
L'ajout d'un collaborateur lui permet d'avoir accès à la plateforme avec ses propres identifiants.

1. Allez dans `Configuration` > `Utilisateur & Permissions` > `Gestion des utilisateurs`.
2. Cliquez sur le bouton d'ajout (généralement "+ Nouvel utilisateur" ou une icône similaire).
3. Remplissez le formulaire avec les informations du collaborateur :
   *   **Nom et Prénom**
   *   **Adresse Email** (qui servira d'identifiant de connexion)
   *   **Mot de passe** provisoire (que l'utilisateur pourra changer plus tard)
4. Assurez-vous que l'option **"Actif"** est cochée pour que l'utilisateur puisse se connecter immédiatement.
5. Cliquez sur **Enregistrer** (ou Valider).  
   > L'utilisateur est désormais créé mais n'a pas encore de permissions spécifiques. Il faut lui attribuer un rôle.

### B. Comment créer un nouveau rôle commercial ou pédagogique ?
Un rôle définit ce que l'utilisateur aura le droit de voir ou de modifier.

1. Allez dans `Configuration` > `Utilisateur & Permissions` > `Rôles`.
2. Cliquez sur **Ajouter un Rôle**.
3. Saisissez un **Nom de rôle** explicite (ex: *Responsable Scolarité*, *Commercial Junior*).
4. La page affiche ensuite une matrice ou une liste de permissions classées par modules (Scolarité, CRM, Finance, etc.).
5. Cochez les cases correspondant aux droits que vous souhaitez accorder (ex : `Voir les prospects`, `Modifier un paiement`, `Ajouter une note`).
6. Validez la création du rôle en cliquant sur **Sauvegarder**.

### C. Comment affecter des accès (rôles) à un utilisateur ?
Une fois le compte créé (Étape A) et le rôle défini (Étape B), il faut les lier.

1. Naviguez vers `Configuration` > `Utilisateur & Permissions` > `Attribution des rôles`.
2. Repérez l'utilisateur concerné dans la liste et cliquez sur son nom ou sur le bouton "Modifier ses rôles".
3. Une fenêtre ou une liste de rôles apparaît. Saisissez ou cochez le rôle créé précédemment (ex: *Responsable Scolarité*).
4. Cliquez sur **Enregistrer**. L'utilisateur a maintenant les droits correspondants. Il devra peut-être se reconnecter pour voir les changements s'appliquer au niveau de son menu.

### D. Comment bloquer l'accès d'un ancien employé ?
Si un collaborateur quitte l'entreprise, il est crucial de révoquer son accès.

1. Rendez-vous dans `Configuration` > `Utilisateur & Permissions` > `Gestion des utilisateurs`.
2. Recherchez le nom de l'employé dans la barre de recherche.
3. Cliquez sur l'icône de modification (crayon) ou d'état de ce compte.
4. Décochez la case **"Actif"** (ou "Compte activé").
5. Enregistrez. L'employé ne pourra plus se connecter avec ses identifiants. Ses données (actions passées) sont conservées dans le système.
6. **(Optionnel mais recommandé) :** Allez dans `Sessions actives` et si l'utilisateur est listé, fermez sa session en cours pour le déconnecter immédiatement.

---

## Description Détaillée des Écrans

### 1. Gestion des Utilisateurs
Cette page centralise tous les comptes de votre plateforme.
*   **Liste et Recherche :** Vous pouvez filtrer les comptes par statut ou chercher par nom.
*   **Actions :** Création, modification (nom, email, réinitialisation de mot de passe) ou désactivation.

### 2. Modules
Les modules correspondent aux grandes sections de l'application (CRM, Scolarité, RH...).
*   **Paramétrage :** Permet une vue d'ensemble sur l'activation/désactivation de certaines briques fonctionnelles.

### 3. Rôles
Un rôle est un groupe de permissions (ex: *Directeur*, *Pédagogie*).
*   **Droits granulaires :** Vous contrôlez finement qui peut *Ajouter*, *Observer*, *Modifier* ou *Supprimer* des éléments.

### 4. Attribution des Rôles
Le panneau permettant de lier comptes et rôles. Un utilisateur peut cumuler plusieurs rôles (ex: *Pédagogie* ET *RH*).

### 5. Journal d'Actions
L'historique (Logs) permettant de tracer toutes les opérations.
*   **Audit de sécurité :** Découvrez qui a validé une facture, supprimé un profil ou modifié la configuration, et à quelle heure précise.

### 6. Sessions Actives
Suivi en temps réel des connexions.
*   **Sécurité immédiate :** Visualisez les IP et adressez les fermetures de sessions forcées en un simple clic.

---

> [!TIP]
> **Règle d'or de sécurité :** N'utilisez les droits de "Super Administrateur" que pour les interventions techniques. Pour l'usage quotidien, créez un rôle "Directeur" qui possède tous les accès fonctionnels mais ne peut pas altérer la structure profonde du logiciel.
