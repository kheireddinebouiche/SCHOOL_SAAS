# Bugs Techniques Identifiés

Ce document recense les erreurs techniques critiques impactant le bon fonctionnement de l'application ou l'intégrité des donnés (hors orthographe pure).

## 🚨 CRITIQUE : Authentification & Redirections
Ce bug impacte la redirection des utilisateurs non connectés, provoquant potentiellement des erreurs 404 ou 500 lors de l'accès aux pages protégées.

| Module | Fichier | Ligne (approx) | Contexte Erroné | Correction | Impact |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `t_groupe` | `views.py` | 10 | `login_url="insitut_app:login"` | `login_url="institut_app:login"` | Redirection login invalide (Typo 'insitut') |
| Potentiel | *Multiple* | - | `@login_required(login_url='insitut...')` | Vérifier globalement | Redirection login invalide |

## ⚠️ IMPORTANT : Modélisation de Données (DB Fields)
Ces erreurs sont dans les définitions de modèles (noms de champs). Une correction nécessite une migration de base de données. Attention aux impacts sur le code existant utilisant ces champs.

| Module | Fichier | Modèle | Champ (Actuel) | Problème | Suggestion (Post-Migration) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `t_formations` | `models.py` | `Specialite` (prob.) | `est_valider` | Grammaire dans nom champ (Verbe) | `est_valide` (Adjectif) |
| `t_formations` | `models.py` | `Matiere` (prob.) | `n_elimate` | Nom obscur / Typos supposée | `note_eliminatoire` |

## 🐛 BUGS FONCTIONNELS
| Module | Fichier | Description | Piste de Résolution |
| :--- | :--- | :--- | :--- |
| `t_commercial` | *Whole Module* | Module vide/coquille installé dans `INSTALLED_APPS` mais inactif. Crée confusion avec `t_conseil`. | Supprimer ou implémenter. |

---
*Dernière mise à jour : 10/01/2026*
