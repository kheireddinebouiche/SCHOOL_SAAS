# Corrections Linguistiques (Orthographe & Traduction)

Ce document centralise toutes les corrections de langue à appliquer sur l'ensemble du projet `SCHOOL_SAAS` (Backend & Frontend).

## 1. TEMPLATES HTML (Frontend)
**Statut Global :** 🟢 **Partiellement Corrigé (Script)**
Cependant, des interventions manuelles restent nécessaires pour les termes non francisés.

### Reste à faire (Manuel) :
*   **Traductions Manquantes (Anglais -> Français) :**
    *   `Profile` -> `Profil` (Headers, Menus)
    *   `Logout` -> `Déconnexion`
    *   `Submit` -> `Valider`
    *   `Cancel` -> `Annuler`
    *   `Delete` -> `Supprimer`
    *   `Edit` -> `Modifier`
    *   Placeholder : "Your Elite author...", "New messages" -> À supprimer.

### Historique des Corrections Automatiques (10/01/2026) :
*   `Séssion` -> `Session`
*   `Plannification` -> `Planification`
*   `Coéfficiant` -> `Coefficient`
*   `Horraire` -> `Horaire`
*   `à été` -> `a été` (et variantes grammaticales dans les `alertify`)

---

## 2. BACKEND PYTHON (Messages & Labels)
Ces corrections concernent les fichiers `views.py` (messages `messages.success/error`) et `models.py` (`verbose_name`, `help_text`).

### 🔴 Urgence "Visible Utilisateur"

#### Module : Core (`institut_app`)
| Fichier | Ligne Approx | Contexte | Correction |
| :--- | :---: | :--- | :--- |
| `models.py` | 17 | `Chargé(e) clientèle` | `Chargé(e) de clientèle` |
| `models.py` | 86 | `Abreviation a afficher` | `Abréviation à afficher` |
| `models.py` | 284 | `Roles Utilisteur-Module` | `Rôles Utilisateur-Module` |
| `views.py` | 466 | `Aucun profile trouvé` | `Aucun profil trouvé` |
| `views.py` | 486 | `profile de l'utilisateur` | `profil de l'utilisateur` |
| `views.py` | 506 | `Désactiver avec succès` | `Désactivé avec succès` |
| `views.py` | 572 | `à été ajouter` | `a été ajouté` |

#### Module : Pédagogie (`t_formations`)
| Fichier | Ligne Approx | Contexte | Correction |
| :--- | :---: | :--- | :--- |
| `models.py` | 41 | `Formation étrangere` | `Formation étrangère` |
| `views.py` | 77 | `spécailité` | `spécialité` |
| `views.py` | 101 | `ont été modifier` | `ont été modifiées` |
| `views.py` | 425 | `spécialitée ont été mis à jours` | `spécialité ont été mises à jour` |
| `views.py` | 428 | `c'est produite` | `s'est produite` |
| `views.py` | 534 | `à été affecté` | `a été affecté` |

#### Module : CRM & Étudiants (`t_crm`, `t_etudiants`)
| Fichier | Ligne Approx | Contexte | Correction |
| :--- | :---: | :--- | :--- |
| `t_crm/views.py` | 126 | `sauvegarder ave succès` | `sauvegardées avec succès` |
| `t_crm/views.py` | 282 | `incription à été confirmer` | `inscription a été confirmée` |
| `t_crm/views.py` | 301 | `Action non autorisé` | `Action non autorisée` |
| `t_etudiants/views.py` | 64 | `La note est enregistrer` | `La note est enregistrée` |
| `t_etudiants/views.py` | 129 | `on été enregistrer avec suucès` | `ont été enregistrées avec succès` |

#### Module : Examens (`t_exam`)
| Fichier | Ligne Approx | Contexte | Correction |
| :--- | :---: | :--- | :--- |
| `views.py` | 273 | `déja planifier` | `déjà planifié` |
| `commission.py` | 53 | `La commision à été crée` | `La commission a été créée` |
| `commission.py` | 113 | `a été valider` | `a été validée` |

#### Module : Finance (`t_tresorerie`)
| Fichier | Ligne Approx | Contexte | Correction |
| :--- | :---: | :--- | :--- |
| `views.py` | 128 | `suppréssion a été effectuer` | `La suppression a été effectuée` |
| `views.py` | 783 | `remboursement à été enregistrer` | `remboursement a été enregistrée` |

---
*Dernière mise à jour : 10/01/2026*
