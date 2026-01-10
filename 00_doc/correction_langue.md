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
**Statut Global :** 🟢 **Partiellement Corrigé (Script 10/01/2026)**
Les fautes de conjugaison lourdes ("à été effectuer") ont été corrigées automatiquement.

### Reste à faire (Manuel) :
*   **URLs :** Le terme `plannification` dans `urls.py` doit être corrigé avec précaution (impact Frontend).
*   **Contexte fin :** Vérifier les accords pluriels complexes non gérés par regex.

### Corrections Appliquées (10/01/2026) :
*   `à été [verbe]` -> `a été [verbe]` (créé, supprimé, effectué...)
*   `suppréssion` -> `suppression`
*   `Acceuil` -> `Accueil` (Models choices)
*   `coéfficiant` -> `coefficient`

### 🔴 Urgence "Visible Utilisateur" (Ce qui restait avant correction auto, à vérifier)

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
| `t_crm/models.py` | 228 | `('acc','Acceuil')` | `('acc','Accueil')` (Choix DB) |
| `t_etudiants/views.py` | 129 | `on été enregistrer avec suucès` | `ont été enregistrées avec succès` |
| `t_crm/f_views/prospects.py` | 283 | `à été effectuer` | `a été effectuée` |

#### Module : Examens (`t_exam`)
| Fichier | Ligne Approx | Contexte | Correction |
| :--- | :---: | :--- | :--- |
| `views.py` | 86 | `session à été supprimée` | `session a été supprimée` |
| `views.py` | 120 | `Suppréssion effectuer` | `Suppression effectuée` |
| `views.py` | 285 | `à été planifier` | `a été planifié` |
| `urls.py` | 27, 121 | `plannification-examens` | `planification-examens` (URL visible!) |
| `commission.py` | 53 | `La commision à été crée` | `La commission a été créée` |

#### Module : Ressources Humaines (`t_rh`)
| Fichier | Ligne Approx | Contexte | Correction |
| :--- | :---: | :--- | :--- |
| `views.py` | 318 | `catégorie à été crée` | `catégorie a été créée` |
| `views.py` | 465 | `à été ajouter avec suucès` | `a été ajouté avec succès` |

#### Module : Timetable & Tresorerie
| Fichier | Ligne Approx | Contexte | Correction |
| :--- | :---: | :--- | :--- |
| `t_timetable/views.py` | 77 | `L'emploie du temps à été crée` | `L'emploi du temps a été créé` |
| `t_tresorerie/views.py` | 596 | `suppréssion a été effectuer` | `suppression a été effectuée` |

---
*Dernière mise à jour : 10/01/2026*
