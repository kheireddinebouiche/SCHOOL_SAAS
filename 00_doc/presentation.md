# Présentation Générale - SCHOOL_SAAS

**Version :** 2.0 (Post-Audit Complet)
**Date de mise à jour :** 10 Janvier 2026
**Superviseur Technique :** Saldae Systems AI

---

## 1. Vision du Produit
**SCHOOL_SAAS** est un ERP (Enterprise Resource Planning) de gestion scolaire de nouvelle génération, conçu en mode **SaaS Multi-Tenant**. Il permet à un réseau d'établissements (Écoles Supérieures, Instituts de Formation, Lycées Privés) de centraliser l'intégralité de leurs opérations sur une plateforme unique, sécurisée et modulaire.

Sa force réside dans sa **double compétence** :
1.  **Académique Rigoureuse :** Respect strict des normes LMD, gestion des diplômes d'État et des doubles diplomations internationales.
2.  **Gestion d'Entreprise :** Outils financiers, comptables et RH dignes d'un ERP PME classique.

---

## 2. Architecture Technique
La solidité du système repose sur une stack éprouvée et robuste :

*   **Backend :** Python 3.x / Django 4.x (Framework Web de haut niveau).
*   **Base de Données :** PostgreSQL (Robuste, transactionnel). Le schéma actuel est `pg_insim_model` (base de développement).
*   **Architecture Multi-Tenant :** Isolation logique des données. Chaque requête est filtrée par l'entité `Entreprise` de l'utilisateur connecté.
*   **Frontend :** Django Templates + Bootstrap 5 + JavaScript (jQuery/Vanilla, AlertifyJS pour les notifications). Interface 100% "Server-Side Rendered" pour la performance SEO et la sécurité.
*   **Sécurité :** RBAC (Role-Based Access Control) fin. Les permissions sont définies par **Module** et par **Utilisateur** (ex: Admin sur la Pédagogie, mais Lecteur sur la Trésorerie).

---

## 3. Cartographie des Modules Fonctionnels

### 🏛️ Core & Administration (`institut_app`)
Le socle du système qui gère l'identité des établissements.
*   **Multi-Société :** Chaque tenant possède son propre RC, NIF, Logo, configuration documentaire et comptes bancaires.
*   **Configuration Globale :** Salles, Types de documents, Paramètres système.
*   **Sécurité unifiée :** Gestion centralisée des employés/utilisateurs ayant accès au Back-Office.

### 🎓 Offre Pédagogique & Scolarité (`t_formations`, `t_etudiants`)
Le cœur du métier académique.
*   **Structure LMD :** Gestion hiérarchique : Formation > Spécialité (Versioning) > Semestre > Module > Matière.
*   **Double Diplomation :** Gestion native des partenariats internationaux avec synchronisation des programmes.
*   **Cursus :** Gestion différenciée des parcours "Standard" (Diplômant) et "Spécial" (Certifiant/Carte).
*   **Documents Académiques :** Génération automatique de certificats de scolarité, relevés de notes, attestations.

### 👥 CRM & Admission (`t_crm`)
Un pipeline de vente dédié à l'enseignement.
*   **Entonnoir de Conversion :** `Acceuil` (Visiteur) -> `Conseil` (Orientation) -> `Préinscrit` -> `Étudiant`.
*   **Suivi Commercial :** Historique des interactions (appels, RDV), qualification des leads, statistiques de conversion.
*   **Workflow d'Innovation :** Les données de l'état civil sont saisies une seule fois au stade prospect et suivent l'étudiant toute sa vie.

### 📅 Planification & Logistique (`t_timetable`, `t_groupe`)
L'orchestration du temps et de l'espace.
*   **Cohortes :** Gestion des groupes d'étudiants par promotion et rentrée (Octobre/Février).
*   **Emplois du Temps Dynmaiques :** Moteur flexible basé sur des créneaux horaires configurables (JSON). Détection de conflits Salles/Profs.
*   **Verrouillage :** Système `EditionLock` pour collaborer en sécurité sur les plannings.

### 📝 Examens & Délibérations (`t_exam`)
Zone de haute sécurité pour garantir la valeur du diplôme.
*   **Planification des Examens :** Gestion des surveillants, des salles d'examen et des convocations.
*   **Anonymat & Saisie :** Processus sécurisé de saisie des notes.
*   **Commissions de Délibération :** Algorithmes automatiques pour le calcul des moyennes, crédits ECTS, et décisions de jury (Admis, Ajourné, Rattrapage).
*   **Bulletins :** Modèles configurables (`ModelBuilltins`) pour s'adapter à toutes les chartes graphiques.

### 💰 Finance & Trésorerie (`t_tresorerie`)
Une comptabilité auxiliaire intégrée et stricte.
*   **Recettes Scolaires :** Échéanciers de paiement personnalisables par étudiant. Suivi des impayés et relances.
*   **Caisse & Banques :** Gestion multi-comptes, rapprochement bancaire, journal de caisse.
*   **Dépenses :** Workflow de validation des achats (Demande -> Bon de commande -> Facture -> Paiement).
*   **Conformité Fiscale :** Génération de numéros de pièces séquentiels inaltérables.

### 👔 Ressources Humaines & Paie (`t_rh`)
Gestion complète du capital humain.
*   **Dossier Employé :** Centralisation des infos, contrats, et documents RH.
*   **Contrats Dynamiques :** Génération de contrats de travail PDF basés sur des modèles (CDI, CDD, Vacation).
*   **Gestion de la Paie :** Calcul des salaires basé sur des "Éléments de paie" configurables (Primes, Retenues).
*   **Pointage & Congés :** Gestion des absences et des droits à congé.

### 💼 B2B & Formation Continue (`t_conseil`)
*Module remplaçant l'ancien `t_commercial`.*
*   **Clients Entreprises :** Gestion des conventions de formation avec des partenaires B2B.
*   **Devis & Facturation Pro :** Workflow commercial complet pour la vente de formation continue.

---

## 4. Fonctionnalités Avancées & Transverses
*   **Génération de Documents (PDF) :** Utilisation de `WeasyPrint` (supposé) pour des documents PDF haute-fidélité (Contrats, Relevés, Factures).
*   **Notifications Temps Réel :** Système d'alerte interne (Header) pour les tâches urgentes (Jury à valider, Paiement en retard).
*   **Tableaux de Bord :** Chaque module dispose de son propre Dashboard avec KPI spécifiques.
*   **Audit Log :** Traçabilité complète des actions critiques (qui a modifié cette note ? qui a supprimé ce paiement ?).

---

## 5. État des Lieux (Janvier 2026)
*   **Modules Matures (Production Ready) :** Pédagogie, Examens, RH, Trésorerie, Core.
*   **Modules en Consolidation :** CRM (Modèle solide, interface à polir), Timetable (Logique complexe validée).
*   **Modules Embryonnaires/Vides :**
    *   `t_commercial` (Coquille vide, fonctions migrées vers `t_conseil`).
    *   `t_remise` (Fonctionnel mais basique).
    *   `t_stage` (Seulement le modèle de données, pas de logique métier).

---
*Ce document sert de référence unique pour la présentation fonctionnelle et technique du projet SCHOOL_SAAS.*
