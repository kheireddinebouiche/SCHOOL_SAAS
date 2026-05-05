# Synthèse du Projet : Compatibilité LMD pour SCHOOL_SAAS

Ce document regroupe l'audit, la stratégie et le plan d'action pour transformer la plateforme SaaS actuelle en un système compatible avec les exigences universitaires (Licence-Master-Doctorat).

---

## 1. État des Lieux (Audit)

Le système actuel est optimisé pour les **Écoles et Instituts de Formation**. Ses caractéristiques principales sont :
- **Multi-tenant** : Séparation stricte des données par établissement via `django-tenants`.
- **Structure Pédagogique** : Basée sur un triptyque `Formation` -> `Spécialité` -> `Module`.
- **Évaluations** : Calcul de moyennes par module et par semestre sans notion de compensation académique complexe.

### Limitations pour l'Université :
- Absence de hiérarchie administrative de haut niveau (**Facultés/Départements**).
- Absence de regroupement pédagogique par **Unités d'Enseignement (UE)**.
- Manque de gestion des **Crédits ECTS** et des volumes horaires détaillés (CM/TD/TP).
- Logique de délibération ne supportant pas la **compensation semi-annuelle ou annuelle**.

---

## 2. Décisions Stratégiques

### Bascule de Mode "One-Shot"
Le choix du type d'établissement (**École vs Université**) sera effectué **une seule fois à la création de l'instance (tenant)**. Cela garantit :
- Une interface utilisateur épurée et adaptée dès le départ.
- Des calculs de moyennes cohérents sans risque de corruption de données historique.
- Une structure de base de données stable.

---

## 3. Architecture Cible (LMD)

### Nouvelle Hiérarchie Administrative
1. **Faculté** (ex: Faculté des Sciences Exactes)
2. **Département** (ex: Département d'Informatique)
3. **Spécialité** (ex: Licence en Systèmes d'Information)

### Nouvelle Structure Pédagogique
- **Unité d'Enseignement (UE)** : Regroupe un ou plusieurs modules.
    - Type : Fondamentale, Méthodologique, Découverte, Transversale.
    - Propriétés : Crédits ECTS de l'UE, Coefficient.
- **Module (Matière)** :
    - Propriétés : Crédits ECTS, Volume Horaire (CM, TD, TP).

---

## 4. Moteur de Délibération

Le système de notation sera refondu pour supporter :
- **Moyenne UE** : Moyenne pondérée des modules de l'UE.
- **Acquisition d'UE** : Une UE est acquise si Moyenne UE >= 10.
- **Compensation** : Si le semestre est validé (Moyenne Semestrielle >= 10), toutes les UE du semestre sont considérées comme acquises.
- **Gestion des Dettes** : Un étudiant peut passer au niveau supérieur s'il a acquis un certain pourcentage de crédits, mais les modules non validés deviennent des "dettes".

---

## 5. Plan d'Action (Roadmap)

### Phase 1 : Configuration Global
- Mise à jour du modèle `Institut` et de l'interface SaaS Admin.
- Injection du mode de fonctionnement dans les vues via un context processor.

### Phase 2 : Modélisation LMD
- Implémentation des modèles `Faculte`, `Departement`, `UE`.
- Extension du modèle `Modules`.

### Phase 3 : Calculs et Délibération
- Développement de la logique de compensation.
- Création des Procès-Verbaux (PV) de délibération.

### Phase 4 : Interface et Rapports
- Refonte des tableaux de bord pédagogiques.
- Générateur de relevés de notes LMD.

---

## 6. Prochaines Étapes Immédiates
1. Modifier le modèle `Institut` dans `app/models.py`.
2. Mettre à jour le formulaire de création de tenant.
3. Initier la migration de la structure pédagogique.
