# 📝 Journal des Mises à Jour (Changelog)

Ce fichier recense toutes les modifications, corrections de bugs et nouvelles fonctionnalités apportées au projet `SCHOOL_SAAS` par l'assistant Antigravity. Ce journal peut être utilisé pour alimenter la vue "Nouveautés" des superutilisateurs.

---

## [04/06/2026] - v1.1.0 - Refonte de Stabilité (Executive Education & RH)

### 🐛 Corrections de Bugs (Bugfixes)
- **Ressources Humaines (Paie & Présences)** :
  - Modification du formulaire d'ajout d'employé pour rendre tous les champs non obligatoires.
  - Résolution d'un bug empêchant l'affichage des nouveaux employés dans les vues de présences et dans l'assistant de paie en autorisant les états (etat) non définis ou vides.
  - Résolution d'un bug bloquant l'ajout d'un nouvel employé dû à la validation silencieuse de champs manquants dans le formulaire (exclusion de `solde_conge`, `solde_conge_annee_prec`, `is_teacher`, etc.).
  - Résolution de l'erreur `KeyError` dans le calcul des paies.
- **SaaS Admin** :
  - Correction d'une erreur de syntaxe (`SyntaxError`) dans `urls.py` causée par des caractères `\n` mal formatés empêchant l'accès au portail.
  - Correction d'une erreur `NameError` due au décorateur `@saas_superuser_required` non défini dans `views.py` (remplacé par `@user_passes_test(superadmin_only)`).
  - Correction de la localisation des noms de mois en anglais dans les fiches mensuelles de présence.
  - Création des pages "Empty States" Premium pour les tableaux vides (Congés, Présences, Fiches Mensuelles, Employés).
- **Executive Education (`t_conseil`)** :
  - Sécurisation complète des API contre les plantages silencieux (`Erreur 500`) : Ajout de la gestion `DoesNotExist` pour plus de 30 requêtes `.get()`.
  - Fixation d'une faille `KeyError` lors de l'accès aux données JSON non fournies dans l'API de gestion des groupes.

### ✨ Améliorations (Optimisations)
- **Base de données (`@transaction.atomic`)** :
  - Application du verrouillage transactionnel sur toutes les fonctions critiques de création (`Devis`, `Factures`, `Clients`, `Groupes`) de l'Executive Education, garantissant qu'aucune donnée fantôme ne soit générée en cas d'erreur de réseau.
- **Ressources Humaines** :
  - Refonte de la suppression d'employés avec un effacement en cascade strict des contrats, pièces jointes et absences (`models.CASCADE`).
  - Restructuration visuelle de la configuration HUB en onglets modernes.

---
*(Ajoutez les prochaines entrées ci-dessus)*
