# Processus Ressources Humaines (RH) - SCHOOL_SAAS

**Module :** `t_rh`
**Version :** 1.0
**Dernière mise à jour :** 10 Janvier 2026

---

## 1. Vue d'Ensemble
Le module RH n'est pas un simple annuaire. Il gère le cycle de vie contractuel et financier des collaborateurs (Enseignants, Administratifs). Il est étroitement lié au module **Authentification**, car chaque employé est potentiellement un utilisateur du système.

## 2. Création d'un Collaborateur

### Étape 1 : Fiche Identité (`Employees`)
*   Saisie des données civiles (Nom, Prénom, Date de naissance).
*   **Civilite :** Monsieur, Madame...
*   **Poste :** Affectation à une fonction.

### Étape 2 : Création du Compte Utilisateur (Facultatif)
Un bouton d'action permet de transformer un `Employee` en `User` Django.
*   Génération automatique du `username` (souvent basé sur nom.prenom).
*   Attribution du mot de passe initial.
*   Lien One-to-One : `Employees.user <-> User`.

## 3. Workflow Contractuel

### Étape 1 : Définition du Contrat (`Contrats`)
Chaque contrat est lié à un employé.
*   **Types de Contrat :** CDI, CDD, Vacation (pour les formateurs vacataires).
*   **Paramètres Financiers :**
    *   `salaire_brut` : Base de rémunération (Mensuel ou Horaire).
    *   `volume_horaire` : Pour les vacataires.

### Étape 2 : Modélisation et Génération PDF
Le système utilise un moteur de template pour générer les documents légaux.
*   **Modèles (`ModeleContrat`) :** L'admin définit des squelettes de texte avec des variables dynamiques (`{{nom}}`, `{{salaire}}`).
*   **Génération :** Au clic, le système fusionne les données de l'employé avec le modèle et génère un PDF prêt à signer via `WeasyPrint`.

## 4. Gestion de la Paie
*En cours d'analyse plus fine sur la partie calcul automatique*.
Le système permet de saisir des **Éléments de Paie** (Primes exceptionnelles, Retenues sur salaire).
*   Chaque mois, l'admin peut valider la paie.
*   Le système génère une **fiche de paie** (bulletin) imprimable.

## 5. Gestion des Congés
*   Les employés soumettent des demandes de congé.
*   Workflow de validation (Maner RH).
*   Impact direct sur le pointage mensuel.

---
*Ce processus assure la gestion administrative du personnel, qu'il soit permanent ou vacataire.*
