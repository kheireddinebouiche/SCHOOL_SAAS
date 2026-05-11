# Plan de Chiffrement Structurel des Montants (Base de Données)

Ce plan détaille l'approche technique pour sécuriser les données financières par un chiffrement au repos (Encryption at Rest) au niveau des colonnes de la base de données.

## Objectif Principal
Sécuriser les montants monétaires en les rendant illisibles dans la base de données sans la clé de déchiffrement. Cette solution est purement structurelle et ne dépend d'aucune préférence utilisateur ou bouton d'interface.

---

## 1. Stratégie de Chiffrement (Field-Level Encryption)

Nous recommandons l'utilisation d'un chiffrement symétrique (AES-256) pour les champs sensibles.

### Champs cibles prioritaires
- **Demandes de paiement :** `ClientPaiementsRequest.amount`
- **Échéances :** `DuePaiements.montant_due`, `DuePaiements.montant_restant`
- **Paiements effectifs :** `Paiements.montant_paye`
- **Remboursements :** `Rembourssements.allowed_amount`

---

## 2. Mise en Œuvre Technique

### A. Remplacement des types de champs
Les colonnes `DecimalField` actuelles seront converties en champs chiffrés (ex: via une bibliothèque comme `django-fernet-fields` ou `django-cryptography`).

### B. Gestion des Clés
- **Clé de chiffrement :** Stockée en tant que variable d'environnement système.
- **Sécurité :** La base de données ne contient que le "cipher-text" (texte chiffré). Sans la clé présente sur le serveur applicatif, les données sont inexploitables.

---

## 3. Impact sur les Opérations Financières

### Calculs et Agrégations
Le chiffrement empêche l'utilisation directe des fonctions SQL comme `SUM()` ou `AVG()` sur les colonnes chiffrées.
- **Solution :** Les calculs de totaux et de balances seront effectués au niveau de la couche applicative (Python) après déchiffrement automatique par le modèle Django.

### Performance
Un léger surcoût CPU est à prévoir lors de la lecture/écriture pour les opérations de (dé)chiffrement, mais celui-ci reste négligeable pour le volume de transactions standard d'un SaaS scolaire.

---

## 4. Plan de Migration des Données

1. **Sauvegarde :** Export complet de la base de données.
2. **Migration :** Script de conversion pour chiffrer les montants existants vers le nouveau format.
3. **Vérification :** Test de cohérence sur les balances après chiffrement.

---

> [!IMPORTANT]
> Cette approche garantit qu'en cas de fuite de la base de données, aucune information financière réelle n'est exposée.

## Étapes de Validation
- [ ] Choix de la bibliothèque de chiffrement Django.
- [ ] Script de migration des données monétaires existantes.
- [ ] Test des calculs de balance élève avec données chiffrées.
