# Processus Finance & Trésorerie - SCHOOL_SAAS

**Module :** `t_tresorerie`
**Version :** 1.0
**Dernière mise à jour :** 10 Janvier 2026

---

## 1. Vue d'Ensemble
Ce module est le "banquier" du système. Il valide financièrement toutes les opérations initiées par le CRM (Inscriptions) ou la Pédagogie (Rattrapages payants).

## 2. Le Modèle de Revenus

### Échéanciers (`EcheancierPaiement`)
*   Chaque Formation a un échéancier par défaut attaché à une Promo.
*   **Tranches :** Le coût total est divisé en tranches datées (ex: 1er versement à l'inscription, Solde en Janvier).
*   **Flexibilité :** Le système permet des **Échéanciers Spéciaux** dérogatoires pour s'adapter aux difficultés financières d'un étudiant spécifique.

## 3. Workflow d'Encaissement

### Étape 1 : La Demande (`ClientPaiementsRequest`)
C'est l'ordre de payer.
*   Créée automatiquement par le CRM (Inscription) ou manuellement.
*   Statut : `En attente`, `Partiel`, `Terminé`.

### Étape 2 : Le Paiement (`ApiStorePaiement`)
L'opérateur de caisse saisit le versement.
*   **Montant perçu :** Peut être partiel.
*   **Conséquence :**
    *   Si `Montant Restant = 0` -> La demande passe à `Terminé`.
    *   Cela débloque le statut de l'étudiant dans le CRM (`Instance` -> `Inscrit`).

## 4. Gestion des Remboursements
Workflow strict pour éviter les fraudes :
1.  **Demande (`ApiSetRembourssement`) :** L'étudiant demande un remboursement (ex: Désistement).
2.  **Validation Administrative :** Un responsable doit approuver la demande (`ApiAccepteRembourssement`).
3.  **Exécution :** Le montant est déduit de la caisse (`ApiSetRembourssement`).

## 5. Gestion des Dépenses & Achats
Contrairement aux recettes automatisées, les dépenses suivent un circuit de validation manuel.

### Étape 1 : Saisie de la Dépense (`DepenseTransaction`)
*   Le gestionnaire saisit une dépense (ex: Achat fournitures, Facture électricité).
*   Catégorisation (ex: Fonctionnement, Investissement).
*   Pièce jointe : Scan de la facture fournisseur obligatoirement uploadé.

### Étape 2 : Workflow de Validation
Pour éviter les abus de caisse :
1.  **Statut `En attente` :** La dépense est saisie mais pas décaissée.
2.  **Validation Directeur :** Un utilisateur avec droit `validate_depense` approuve.
3.  **Statut `Validé/Payé` :** La somme est déduite du solde de caisse/banque sélectionné.

### Étape 3 : Suivi Fournisseurs
Le système permet de créer des comptes "Tiers" pour les fournisseurs récurrents et de suivre l'historique des achats par fournisseur.

---
*Ce processus garantit la traçabilité de chaque dinar et conditionne l'accès aux services pédagogiques.*
