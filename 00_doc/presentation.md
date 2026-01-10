# Présentation Générale - SCHOOL_SAAS

**Date de mise à jour :** 10 Janvier 2026
**Superviseur Technique :** Saldae Systems AI

---

## 1. Introduction

**SCHOOL_SAAS** est un ERP (Enterprise Resource Planning) de gestion scolaire complet, conçu en mode SaaS (Software as a Service) et Multi-Tenant. Il ne s'agit pas d'une simple application de gestion d'étudiants, mais d'un système intégré capable de piloter l'ensemble des processus administratifs, pédagogiques et financiers d'un réseau d'établissements (Agences, Écoles Supérieures, Centres de Formation).

Il se distingue par une gestion rigoureuse des processus critiques (Sécurité des notes d'examen, Traçabilité financière fiscale) et une flexibilité académique (Double diplomation, Systèmes LMD ou Classique).

## 2. Architecture Technique

*   **Backend :** Python / Django (Architecture Modulaire).
*   **Base de Données :** PostgreSQL (Schéma `pg_insim_model` / `alger` analysé).
*   **Architecture Multi-Tenant :** Isolation logique des données par le modèle `Entreprise` (institut_app).
*   **Sécurité :** RBAC (Role-Based Access Control) granulaire au niveau du couple Utilisateur/Module (`UserModuleRole`).

## 3. Modules Fonctionnels

Le système est découpé en domaines fonctionnels autonomes mais interconnectés :

### 🏛️ Core Administratif (`institut_app`)
Le cœur du système. Il gère l'identité légale de l'établissement.
*   **Multi-Société :** Chaque tenant possède son propre RC, NIF, Logo et configuration documentaire.
*   **Configuration :** Gestion centralisée des comptes bancaires, salles de classe et paramètres globaux.
*   **Sécurité Avancée :** Un utilisateur peut être "Administrateur" sur le module Pédagogie mais simple "Visiteur" sur le module RH.

### 🎓 Offre Pédagogique (`t_formations`)
Modélise la structure académique de l'école.
*   **Hiérarchie :** Formation → Spécialité (avec gestion de versions) → Modules.
*   **Internationalisation :** Prise en charge native de la **Double Diplomation** avec des partenaires étrangers.
*   **Programmes :** Définition flexible des programmes par semestre, avec coefficients et crédits.

### 👥 CRM & Cycle de Vie Étudiant (`t_crm`, `t_etudiants`)
Un flux continu de la prospection à la diplomation.
1.  **Prospect :** Captation, suivi (appels/relances) et qualification.
2.  **Admission :** Gestion des fiches de vœux et validation par commission.
3.  **Inscription :** Conversion en Étudiant avec lien persistant vers la fiche d'état civil (Prospect).
4.  **Scolarité :** Suivi des présences et historique académique.

### 📅 Planification & Logistique (`t_timetable`, `t_groupe`)
*   **Groupes :** Gestion des cohortes par promotion et rentrée (Octobre/Mars).
*   **Emplois du Temps :** Moteur flexible basé sur des modèles de créneaux hebdomadaires (JSON), avec gestion des conflits Salles/Formateurs.
*   **Collaboratif :** Système de verrouillage d'édition (`EditionLock`) pour éviter les conflits lors de la conception des plannings.

### 📝 Évaluation & Examens (`t_exam`)
Zone critique sécurisée.
*   **Flexibilité :** Modèles de bulletins configurables (`ModelBuilltins`) pour s'adapter à différents systèmes (Formation Pro vs Universitaire).
*   **Intégrité :** Verrouillage strict des PV (`PvExamen`). Une fois validé, une note ne peut plus être modifiée techniquement.
*   **Délibération :** Automatisation des décisions de jury (Admis, Rattrapage, Ajourné).

### 💰 Trésorerie & Finance (`t_tresorerie`)
Gestion comptable et fiscale intégrée.
*   **Recettes :** Échéanciers de paiement personnalisables, gestion des dettes et recouvrement.
*   **Séquençage Fiscal :** Génération automatique de numéros de pièces uniques et traçables (ex: `N°00123/ST/ALGER/...`) garantissant la conformité fiscale.
*   **Dépenses :** Suivi des achats et rapprochement bancaire.

## 4. Points Forts Techniques

1.  **Intégrité des Données :** Utilisation intensive de contraintes relationnelles et de validations au niveau des modèles (`save()`, `clean()`) pour empêcher la corruption de données métier (Notes, Paiements).
2.  **Traçabilité :** Module `UserActionLog` (vu dans `t_crm`) permettant d'auditer les actions sensibles.
3.  **Extensibilité :** L'usage de champs JSON dans les modules de planification permet de faire évoluer les structures horaires sans migration de base de données lourde.

---
*Document généré automatiquement suite à l'audit technique du 10/01/2026.*
