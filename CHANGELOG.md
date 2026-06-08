# 🗓️ Journal des Mises à Jour (Changelog)

## [Unreleased]
- **Ajout** : Fonctionnalité d'impression (génération de rapport) du taux d'utilisation de l'ERP avec possibilité de sélectionner spécifiquement un ou plusieurs instituts via une fenêtre modale.
- **Modification** : Refonte de l'affichage de la page `platform_usage_rate` pour utiliser des onglets (tabs) par tenant et ajout de la pagination DataTables.
- **Modification** : Le menu "Satisfaction" a été renommé en "Mesure de satisfaction" dans `menu.html`.
- **Modification** : Remplacement de la pagination serveur des tenants par une pagination locale (DataTables) des logs à l'intérieur de chaque onglet tenant sur la page `crm_user_logs`.
- **Modification** : Refonte de l'affichage de la page `crm_user_logs` pour utiliser des onglets (tabs) par tenant au lieu d'une liste verticale.
- **Modification** : Regroupement de "Stats CRM", "Logs" et "Taux d'utilisation" sous un seul menu déroulant "Statistiques" dans `menu.html` et `saas_menu.html`.
- **Ajout** : Nouvelle vue et page `platform_usage_rate` (Taux d'utilisation de l'ERP) calculant les actions/jour par utilisateur depuis la création du tenant.
- **Ajout** : Mise en place de filtres par institut, par utilisateur et par type d'action sur la page `crm_user_logs`.
- **Modification** : Le titre de la vue `crm_user_logs` a été changé de "Logs Utilisateurs CRM par Institut" à "Logs".
- **Correction** : Résolution de l'erreur `ModuleNotFoundError` en utilisant `app.models` au lieu de `school.models` pour `Institut`.
- **Modification** : Le lien de menu a été renommé en "Logs" (dans `menu.html` et `saas_menu.html`).
- **Modification** : La vue `crm_user_logs` récupère désormais tous les logs (sans limite de 100).
- **Ajout** : Lien vers `crm_user_logs` ajouté dans le menu `saas_menu.html`.
- **Ajout** : Nouvelle vue et page `crm_user_logs` dans `associe_app` pour afficher les logs utilisateurs (`UserActionLog`) CRM par tenant.

---

## [07/06/2026] - v1.2.x - Harmonisation de la configuration Facture

- **SaaS Admin / Notifications Globales** :
  - **Gestion des annonces** : Création d'une interface superadmin permettant de créer, lister, activer ou supprimer des annonces (`SystemAnnouncement`).
  - **Ciblage granulaire** : Possibilité de cibler l'ensemble des utilisateurs, un Tenant spécifique, ou un utilisateur précis au sein d'un Tenant.
  - **Temps Réel via WebSockets (Channels)** : Intégration au `NotificationConsumer` existant pour diffuser instantanément les annonces (`announcement_trigger`) sans rafraîchissement de page ni appels AJAX périodiques. Groupes de diffusions optimisés (`global_all_users`, `{schema_name}_all_users`).
  - **Relance d'annonce** : Ajout d'un bouton "Relancer" permettant de réinitialiser l'historique de lecture d'une annonce spécifique et de forcer sa réapparition en temps réel chez tous les utilisateurs ciblés.
  - **Suivi de lecture** : Affichage d'une modale pour les utilisateurs ciblés. Un système de validation ("J'ai lu cette annonce") enregistre la confirmation en base de données (`AnnouncementRead`) pour désactiver l'affichage.

- **SaaS Admin / Centre de Connaissance** :
  - Suppression de la mention de limitation de taille de fichier pour l'upload.
  - Ajout du support de lecture des vidéos (MP4) hébergées localement directement depuis le modal vidéo existant.

- **Trésorerie / Modèles d'échéancier** :
  - **Frais d'inscription** : Ajout de la possibilité d'activer/désactiver la configuration des frais d'inscription au niveau du modèle d'échéancier (`ModelEcheancier.has_frais_inscription`).
  - **Interface utilisateur** : Intégration de toggles "Activer la configuration des frais d'inscription" dans les formulaires de création et de modification des modèles d'échéancier (`gestion_echeancier.html`).
  - **Assistant d'échéancier** : Conditionnement de l'affichage et de l'obligation de saisie du montant des frais d'inscription et de l'entité associée dans le formulaire de création d'échéancier (`creer-un-echeancier.html`), selon la configuration du modèle choisi.

- **CRM / Double Diplomation** :
  - **Modification des Voeux** : Résolution du bug empêchant la modification des voeux (bouton "Mettre à jour") pour les prospects en double cursus, notamment ceux ayant été annulés ou modifiés sans changement de formation (récupération directe de `id_formation` via `#formation_voeux`).
  - **Changement de Cursus** : Correction d'une erreur 500 (`FicheVoeuxDouble.DoesNotExist`) survenant lors du passage d'un cursus double à un cursus standard, particulièrement pour les prospects annulés ayant des fiches de voeux déjà confirmées.
  - **Réinitialisation des Voeux** : Ajout d'un nouveau mécanisme (bouton et modale de confirmation) permettant de supprimer complètement les fiches de vœux d'un prospect (double et standard) et de réinitialiser son orientation.

- **Facturation (Conseil)** :
  - **Design & UI** : Harmonisation complète de la page `configure-facture.html` pour correspondre au design premium de `configure-devis.html`. Modification de la structure de la grille pour utiliser une barre latérale droite fixe (`.col-lg-4`) pour le récapitulatif, et une colonne principale (`.col-lg-8`) pour les informations générales, la liste des articles et les modalités. Adaptation du code JavaScript de génération du récapitulatif financier pour utiliser des éléments HTML `<div class="d-flex ...">` à la place de `<tr>`, afin de correspondre visuellement aux totaux du devis.
  - **Ligne d'ajout des articles** : Harmonisation de la ligne d'ajout (`tfoot`) avec les placeholders, les entêtes du tableau, la gestion des permissions (`disabled`) et le style Select2 (retrait du thème bootstrap-5 pour appliquer le style premium customisé).
  - **Conversion Devis en Facture** : Le prospect lié au devis devient automatiquement un client (avec le statut "convertit") lors de la conversion du devis en facture, s'il n'est pas déjà client.
  - **Liste des Devis** : Masquage de l'icône de modification (édition) pour les devis qui ne sont plus à l'état brouillon (déjà validés/envoyés/acceptés).
  - **Design & UI (Liste des Devis)** : Harmonisation complète du design de la page `liste_des_devis.html` avec celui de `liste_des_factures.html`. Ajout des filtres par statut et par dates (JS dynamique), badges de statuts subtils arrondis (`bg-xxx-subtle`), boutons d'actions circulaires (32x32) et compteurs de résultats (pagination dynamique).

## [05/06/2026] - v1.2.x - Permissions Menus Associe App

- **Associe App** :
  - **Satisfaction** : Ajout d'un nouveau menu "Satisfaction" affichant une page "FonctionnalitÃ© en attente de validation".
  - **Gestion des Permissions** : Ajout de conditions de permissions (`is_superuser` et `is_staff`) sur le menu horizontal `public_folder/menu.html` pour restreindre l'accÃ¨s. ParamÃ©trage et Administration sont rÃ©servÃ©s aux super-administrateurs, tandis que Dashboard, Stats CRM et Gestion BudgÃ©taire sont accessibles aux membres du staff.
  - **Gestion des Utilisateurs** : Ajout d'un mÃ©canisme (checkbox) pour activer ou dÃ©sactiver le statut super-utilisateur lors de l'ajout ou de l'Ã©dition d'un utilisateur dans le panel d'administration (`associe_app`).

- **SaaS Admin** :
  - **Gestion du Changelog** : Correction d'une erreur 403 (CSRF) lors de la suppression d'une mise Ã  jour dans le panel SaaS Admin. Le jeton CSRF Ã©tait mal formatÃ© dans la requÃªte AJAX (`templates/saas_admin_app/saas_changelog.html`).

---

## [04/06/2026] - v1.2.0 - Refonte de l'IRG (ConformitÃƒÂ© LÃƒÂ©gale AlgÃƒÂ©rienne)

- **Ressources Humaines (FiscalitÃƒÂ© & Paie)** :
  - **Prise en charge des Primes / Rubriques dans la Paie EmployÃƒÂ©s** :
    - IntÃƒÂ©gration du calcul des rubriques/primes dynamiques (gains et retenues) dans la gÃƒÂ©nÃƒÂ©ration de la paie en masse via `assistantPaie`. La mÃƒÂ©thode synchronise automatiquement le contrat `t_rh.models.Contrats` avec le contrat `t_ressource_humaine.models.Contrat` pour rÃƒÂ©cupÃƒÂ©rer et appliquer la bonne configuration des rubriques et leurs valeurs par dÃƒÂ©faut ou personnalisÃƒÂ©es.
    - Persistance correcte des lignes de paie (`LignePaie`) associÃƒÂ©es ÃƒÂ  chaque bulletin lors de la validation en masse, en ÃƒÂ©vitant les doublons (suppression prÃƒÂ©alable des anciennes lignes de paie pour la mÃƒÂªme fiche).
    - AmÃƒÂ©lioration de la vue de dÃƒÂ©tail du bulletin de paie de l'employÃƒÂ© (`fiche_paie_detail.html`) pour boucler sur `fiche.lignes_paie.all` (au lieu de la relation incorrecte `fiche.lignes.all`) et utiliser le libellÃƒÂ© correct (`ligne.rubrique.libelle` au lieu de `ligne.rubrique.nom`).
    - Affichage des lignes de primes exceptionnelles, de l'indemnitÃƒÂ© de panier, de l'indemnitÃƒÂ© de transport et des retenues pour absences directement sous forme de lignes du tableau pour les employÃƒÂ©s.
    - Ajout des conditions pour charger le nom et l'identifiant de l'employÃƒÂ© ou du formateur de maniÃƒÂ¨re dynamique dans `fiche_paie_print.html` et `_fiche_paie_detail.html` afin d'ÃƒÂ©viter tout plantage `AttributeError` ou omission.
  - **Filtres & Gestion de l'Historique de Paie** : Modernisation de l'historique des fiches de paie (`liste_fiches_paie.html`). Ajout de filtres de recherche avancÃƒÂ©s par employÃƒÂ©, entitÃƒÂ© lÃƒÂ©gale, mois, annÃƒÂ©e et statut de validation (ValidÃƒÂ© ou Brouillon). Les filtres s'appliquent en temps rÃƒÂ©el (via l'ÃƒÂ©vÃƒÂ©nement `onchange` sur tous les sÃƒÂ©lecteurs) et mettent ÃƒÂ  jour l'historique du navigateur (`window.history.pushState`) pour des filtres persistants sans rechargement de page.
  - **Correction du chargement des rubriques** : RÃƒÂ©solution d'une erreur 404 dans `details_employe.html` lors de l'ouverture du modal de gestion des rubriques/primes pour un employÃƒÂ©. Remplacement du chemin d'accÃƒÂ¨s AJAX codÃƒÂ© en dur par la balise Django dynamique `{% url %}` ciblant l'URL correcte sous le namespace `t_ressource_humaine`.
  - **Validation & Suppression Individuelle/En Masse** : IntÃƒÂ©gration de checkboxes de sÃƒÂ©lection et d'une barre d'actions groupÃƒÂ©es permettant de valider ou d'annuler la validation de plusieurs bulletins de paie simultanÃƒÂ©ment. Ajout d'un bouton de suppression sÃƒÂ©curisÃƒÂ© par SweetAlert2, accessible uniquement pour les bulletins de paie ÃƒÂ  l'ÃƒÂ©tat de brouillon (non validÃƒÂ©s).
  - **PrÃƒÂ©-visualisation et Confirmation de Paie (Masse Salariale)** : Ajout d'une ÃƒÂ©tape de prÃƒÂ©-visualisation/confirmation avant le scellement dÃƒÂ©finitif de la paie. Les pages d'assistant de paie (salariÃƒÂ©s et formateurs) calculent dÃƒÂ©sormais les totaux gÃƒÂ©nÃƒÂ©raux (nombre de personnes, masse salariale brute globale, total cotisations SS, total retenues IRG et total Net ÃƒÂ  payer) et les prÃƒÂ©sentent dans une fenÃƒÂªtre de confirmation SweetAlert2 ergonomique et claire.
  - **Correction de l'assistant de paie** : RÃƒÂ©solution d'un plantage `AttributeError` lors de la validation globale de la paie dans `t_rh/views.py::assistantPaie` oÃƒÂ¹ le champ inexistant `date_debut` du modÃƒÂ¨le `Contrats` a ÃƒÂ©tÃƒÂ© remplacÃƒÂ© par le champ correct `date_embauche`.
  - **Moteur de calcul IRG** : Refonte totale de `calculer_irg` dans `t_ressource_humaine/logic.py` pour implÃƒÂ©menter la mÃƒÂ©thode officielle algÃƒÂ©rienne (LF 2022 / LF 2026) :
    - Arrondi systÃƒÂ©matique du salaire imposable ÃƒÂ  la dizaine de DA infÃƒÂ©rieure avant le calcul du barÃƒÂ¨me.
    - Application du premier abattement proportionnel de 40% sur l'IRG brut (limitÃƒÂ© au minimum de 1 000 DA et maximum de 1 500 DA par mois).
    - Formule de lissage pour le **Cas GÃƒÂ©nÃƒÂ©ral** (de 30 000 DA ÃƒÂ  35 000 DA) : $\text{IRG} = \text{IRG1} \times \frac{137}{51} - \frac{27925}{8}$.
    - Formule de lissage pour le **Cas Particulier** (RetraitÃƒÂ©s & HandicapÃƒÂ©s, de 30 000 DA ÃƒÂ  42 500 DA) : $\text{IRG} = \text{IRG1} \times \frac{93}{61} - \frac{81213}{41}$.
    - Arrondi fiscal systÃƒÂ©matique au dÃƒÂ©cime (dizaine de centimes).
  - **Correction du calcul CDI/CDD** : RÃƒÂ©solution du bug appliquant incorrectement le taux flat de 10% des vacataires ÃƒÂ  tous les enseignants (mÃƒÂªme sous CDD/CDI) ; dÃƒÂ©sormais, seuls les contrats de type `VACATION` sont soumis ÃƒÂ  ce taux flat.
  - **Base de donnÃƒÂ©es / ModÃƒÂ¨les** : Ajout du champ `is_particular_irg` dans les modÃƒÂ¨les `Employees` et `Formateurs`. IntÃƒÂ©gration automatique dans les formulaires et les modals de crÃƒÂ©ation et modification (modals d'ajout/ÃƒÂ©dition dans `liste_des_formateur.html` et formulaire `NouveauEmploye`).
  - **Prise en charge Formateurs** : Adaptation de `PaieEngine.calculer_paie` pour rÃƒÂ©soudre et transmettre le drapeau `is_particular_irg` ÃƒÂ  partir du contrat de l'enseignant (CDI/CDD) et du formateur reliÃƒÂ©, appliquant ainsi correctement le barÃƒÂ¨me de lissage particulier (retraitÃƒÂ©s/handicapÃƒÂ©s) dans le calcul et la gÃƒÂ©nÃƒÂ©ration finale des fiches de paie.
  - **Migrations de Base de DonnÃƒÂ©es** : GÃƒÂ©nÃƒÂ©ration et application de la migration `0013_formateurs_is_particular_irg.py` pour ajouter le champ dans le schÃƒÂ©ma et migration sur tous les schÃƒÂ©mas locataires (multi-tenant isolation).
  - **Interface & Simulation ModernisÃƒÂ©e (Design Premium)** : 
    - IntÃƒÂ©gration de la description dÃƒÂ©taillÃƒÂ©e du barÃƒÂ¨me, des abattements et des formules de lissage (cas gÃƒÂ©nÃƒÂ©ral et cas particulier) dans l'interface de configuration fiscale `templates/tenant_folder/rh/paie/config_fiscalite.html`.
    - Ajout d'un **Simulateur IRG InstantanÃƒÂ©** interactif en Javascript, permettant de calculer en temps rÃƒÂ©el l'IRG pour n'importe quel montant imposable saisi, pour le cas gÃƒÂ©nÃƒÂ©ral et le cas particulier.
    - Refonte visuelle complÃƒÂ¨te sous forme de cartes en verre dÃƒÂ©poli (Glassmorphism) avec des dÃƒÂ©gradÃƒÂ©s fins, des ombres fluides et une disposition responsive.
    - AmÃƒÂ©lioration de l'ergonomie des formulaires avec des focus adoucis (`soft-glow`), des tooltips informatifs et des styles de boutons raffinÃƒÂ©s.
    - Ajout d'une micro-animation de pulsation (`pulse-update` par transform scale) sur les cartes de rÃƒÂ©sultats du simulateur (Vert/Ãƒâ€°meraude pour le Cas GÃƒÂ©nÃƒÂ©ral, Bleu/Info pour le Cas Particulier) dÃƒÂ©clenchÃƒÂ©e ÃƒÂ  chaque frappe de clavier.
  - **Validation des tests** : Ajout de nouveaux tests unitaires pour valider les calculs exacts d'IRG pour les cas gÃƒÂ©nÃƒÂ©raux et particuliers (ex: 30 900 DA & 30 930 DA imposable) et ajustement des assertions de test ÃƒÂ  l'abattement de 40% (ex: 45 500 DA imposable).

---

## [04/06/2026] - v1.1.0 - Refonte de StabilitÃƒÂ© (Executive Education & RH)

- **Global / Core** :
  - Correction d'une erreur fatale au dÃƒÂ©marrage du serveur (NameError) dans `school/settings.py` causÃƒÂ©e par `DEBUG = F`.
- **Ressources Humaines (Paie, PrÃƒÂ©sences & Formateurs)** :
  - **Assistant de Paie Formateurs** : CrÃƒÂ©ation d'une page dÃƒÂ©diÃƒÂ©e "Assistant de Paie - Formateurs" permettant de gÃƒÂ©nÃƒÂ©rer en masse les fiches de paie basÃƒÂ©es sur les fiches mensuelles validÃƒÂ©es.
  - **Historique DÃƒÂ©diÃƒÂ© & Redesign** : SÃƒÂ©paration de l'historique des fiches de paie pour les formateurs avec un tout nouveau design premium (Glassmorphism, animations au survol, dÃƒÂ©gradÃƒÂ©s de couleurs).
  - **Taux IRG Vacataires** : Ajout d'une configuration globale (dans les ParamÃƒÂ¨tres RH) pour appliquer le taux IRG forfaitaire (sans abattement) spÃƒÂ©cifique aux formateurs vacataires (par dÃƒÂ©faut 10%). Ce paramÃƒÂ¨tre est pris en charge par le moteur de paie de faÃƒÂ§on automatique.
  - **Correction du systÃƒÂ¨me de paie formateur** : Correction de l'erreur d'attribut `types_contrat` vers `eligible_types` dans `generer_paie`.
  - **Liaison Paie-Formateur** : Ajout d'un bouton "GÃƒÂ©nÃƒÂ©rer Paie" dynamique sur les fiches mensuelles des formateurs.
  - **Validation des Fiches Mensuelles** : CrÃƒÂ©ation du modÃƒÂ¨le `ValidationFicheMensuelleFormateur` avec bouton AJAX SweetAlert2 pour verrouiller et approuver une fiche mensuelle de formateur (affichage d'un badge "ValidÃƒÂ©e").
  - Restructuration du menu principal "Ressources Humaines" pour sÃƒÂ©parer clairement "Espace EmployÃƒÂ©s" et "Espace Formateurs" (et les garder ouverts au bon endroit).
  - Modification du formulaire d'ajout d'employÃƒÂ© pour rendre tous les champs non obligatoires.
  - RÃƒÂ©solution d'un bug empÃƒÂªchant l'affichage des nouveaux employÃƒÂ©s dans les vues de prÃƒÂ©sences et dans l'assistant de paie en autorisant les ÃƒÂ©tats (etat) non dÃƒÂ©finis ou vides.
  - RÃƒÂ©solution d'un bug bloquant l'ajout d'un nouvel employÃƒÂ© dÃƒÂ» ÃƒÂ  la validation silencieuse de champs manquants dans le formulaire (exclusion de `solde_conge`, `solde_conge_annee_prec`, `is_teacher`, etc.).
  - RÃƒÂ©solution d'un bug similaire empÃƒÂªchant la crÃƒÂ©ation d'un nouveau contrat pour un formateur (exclusion des champs non rendus comme `prime_transport`, `prime_panier`, `employee` du `ContratForm`).
  - RÃƒÂ©solution de l'erreur `KeyError` dans le calcul des paies.
- **CRM / Prospects** :
  - Ajout de la fonctionnalitÃƒÂ© d'importation en masse de prospects particuliers via fichier Excel (`.xlsx`).
  - Ajout d'une fonctionnalitÃƒÂ© pour tÃƒÂ©lÃƒÂ©charger le modÃƒÂ¨le d'import. Les prospects importÃƒÂ©s ont le statut "pas de vÃ…â€œux formulÃƒÂ©s pour le moment".
- **SaaS Admin** :
  - Correction d'une erreur de syntaxe (`SyntaxError`) dans `urls.py` causÃƒÂ©e par des caractÃƒÂ¨res `\n` mal formatÃƒÂ©s empÃƒÂªchant l'accÃƒÂ¨s au portail.
  - Correction d'une erreur `NameError` due au dÃƒÂ©corateur `@saas_superuser_required` non dÃƒÂ©fini dans `views.py` (remplacÃƒÂ© par `@user_passes_test(superadmin_only)`).
  - Correction de la localisation des noms de mois en anglais dans les fiches mensuelles de prÃƒÂ©sence.
  - CrÃƒÂ©ation des pages "Empty States" Premium pour les tableaux vides (CongÃƒÂ©s, PrÃƒÂ©sences, Fiches Mensuelles, EmployÃƒÂ©s).
- **Executive Education (`t_conseil`)** :
  - SÃƒÂ©curisation complÃƒÂ¨te des API contre les plantages silencieux (`Erreur 500`) : Ajout de la gestion `DoesNotExist` pour plus de 30 requÃƒÂªtes `.get()`.
  - Fixation d'une faille `KeyError` lors de l'accÃƒÂ¨s aux donnÃƒÂ©es JSON non fournies dans l'API de gestion des groupes.

### Ã¢Å“Â¨ AmÃƒÂ©liorations (Optimisations)
- **Base de donnÃƒÂ©es (`@transaction.atomic`)** :
  - Application du verrouillage transactionnel sur toutes les fonctions critiques de crÃƒÂ©ation (`Devis`, `Factures`, `Clients`, `Groupes`) de l'Executive Education, garantissant qu'aucune donnÃƒÂ©e fantÃƒÂ´me ne soit gÃƒÂ©nÃƒÂ©rÃƒÂ©e en cas d'erreur de rÃƒÂ©seau.
- **Ressources Humaines** :
  - Refonte de la suppression d'employÃƒÂ©s avec un effacement en cascade strict des contrats, piÃƒÂ¨ces jointes et absences (`models.CASCADE`).
  - Restructuration visuelle de la configuration HUB en onglets modernes.

---
*(Ajoutez les prochaines entrÃƒÂ©es ci-dessus)*
-   A j o u t   d e   l a   m o d i f i c a t i o n   e t   s u p p r e s s i o n   d e s   c o n t r a t s   ( i n t e r f a c e   L i s t e   d e s   c o n t r a t s )   d a n s   r h .  
 -   R e f o n t e   d e   l a   m o d i f i c a t i o n   d e s   c o n t r a t s   :   c r Ã© a t i o n   d ' u n e   p a g e   c o m p l Ã¨ t e   d Ã© d i Ã© e   ( u p d a t e _ c o n t r a t . h t m l )   b a s Ã© e   s u r   l ' a s s i s t a n t   d e   c r Ã© a t i o n   a v e c   p r Ã© - r e m p l i s s a g e   d e s   r u b r i q u e s .  
 -   C o r r e c t i o n   d u   p r Ã© - r e m p l i s s a g e   d e s   d o n n Ã© e s   s u r   l a   p a g e   d e   m o d i f i c a t i o n   d u   c o n t r a t   ( p r o b l Ã¨ m e   d e   s Ã© r i a l i s a t i o n   J S O N   d e s   d o n n Ã© e s   P y t h o n ) .  
 -   M e n u   l a t Ã© r a l   :   a j o u t   d e   l a   r o u t e   ' u p d a t e C o n t r a t P a g e '   p o u r   m a i n t e n i r   l e   m e n u   ' G e s t i o n   d e s   C o n t r a t s '   a c t i f   l o r s   d e   l a   m o d i f i c a t i o n   d ' u n   c o n t r a t .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n   m Ã© c a n i s m e   d e   p r Ã© v i s u a l i s a t i o n   ( m o d a l )   p o u r   c h a q u e   l i g n e   d e   f i c h e   d e   p a i e .  
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d e   l a   f e n Ãª t r e   m o d a l e   d e   p r Ã© v i s u a l i s a t i o n   d a n s   l ' a s s i s t a n t   d e   p a i e   ( d Ã© p l a c e m e n t   e n   d e h o r s   d u   c o n t e n e u r   d u   t a b l e a u   p o u r   Ã© v i t e r   l e s   c o n f l i t s   C S S ) .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   a n i m a t i o n   d ' a l e r t e   s u r   l e   b o u t o n   d e   r e c h e r c h e   l o r s q u e   l e   m o i s   o u   l ' a n n Ã© e   e s t   m o d i f i Ã©   a f i n   d ' i n c i t e r   l ' u t i l i s a t e u r   Ã    a c t u a l i s e r   l e s   d o n n Ã© e s .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   s e c t i o n   d e   s y n t h Ã¨ s e   g l o b a l e   a f f i c h a n t   l e   t o t a l   d e s   p a i e m e n t s   n e t s ,   l e   t o t a l   d e s   p r i m e s   e t   l e   t o t a l   d e   l a   f i s c a l i t Ã©   ( S S   +   I R G ) .  
 -   M o t e u r   d e   p a i e   :   a j o u t   d ' u n   n o u v e a u   m o d e   d e   c a l c u l   p o u r   l e s   r u b r i q u e s   e t   p r i m e s   ( ' J O U R S '   :   P a r   j o u r   t r a v a i l l Ã© )   p e r m e t t a n t   d e   m u l t i p l i e r   l e   m o n t a n t   s a i s i   p a r   l e   n o m b r e   d e   j o u r s   d e   p r Ã© s e n c e   d e   l ' e m p l o y Ã© .  
 -   C o r r e c t i o n   d u   m e n u   l a t Ã© r a l   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   o Ã¹   l e   s o u s - m e n u   d e s   f i c h e s   d e   p a i e   f o r m a t e u r s   s ' a f f i c h a i t   c o m m e   a c t i f   ( e n   s u r b r i l l a n c e )   l o r s q u ' o n   s e   t r o u v a i t   s u r   l ' a s s i s t a n t   d e   p a i e   d e s   e m p l o y Ã© s   ( p r o b l Ã¨ m e   d e   m a t c h i n g   d e   c h a Ã® n e   d e   c a r a c t Ã¨ r e s ) .  
 -   I n t e r f a c e   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   ( s c r o l l   h o r i z o n t a l   i n d Ã© s i r a b l e )   s u r   l a   p a g e   d ' h i s t o r i q u e   d e s   f i c h e s   d e   p a i e   d e s   f o r m a t e u r s ,   c a u s Ã©   p a r   u n   Ã© l Ã© m e n t   d Ã© c o r a t i f   q u i   d Ã© p a s s a i t   d e   l ' Ã© c r a n .  
 -   A s s i s t a n t   d e   p a i e   :   e x c l u s i o n   a u t o m a t i q u e   d e s   e m p l o y Ã© s   d o n t   l a   f i c h e   d e   p a i e   a   d Ã© j Ã    Ã© t Ã©   g Ã© n Ã© r Ã© e   p o u r   l e   m o i s   e n   c o u r s   a f i n   d ' Ã© v i t e r   l e s   d o u b l o n s   ( i l s   r Ã© a p p a r a Ã® t r o n t   s i   l e u r   f i c h e   e s t   a n n u l Ã© e ) .  
 -   A s s i s t a n t   d e   p a i e   :   a f f i c h a g e   d ' u n e   v u e   d e   s y n t h Ã¨ s e   ' P a i e   c l Ã´ t u r Ã© e   p o u r   c e   m o i s '   l o r s q u e   t o u t e s   l e s   f i c h e s   d e   p a i e   o n t   d Ã© j Ã    Ã© t Ã©   g Ã© n Ã© r Ã© e s   p o u r   l e   m o i s   s Ã© l e c t i o n n Ã© ,   r e m p l a Ã§ a n t   l e   m e s s a g e   d ' e r r e u r   ' A u c u n e   d o n n Ã© e   d i s p o n i b l e ' .  
 -   C o r r e c t i o n   d e   l ' i n t e r f a c e   :   l ' i c Ã´ n e   d u   m e n u   ' A s s i s t a n t   d e   P a i e '   n e   s ' a f f i c h a i t   p a s   e n   r a i s o n   d ' u n e   c l a s s e   d ' i c Ã´ n e   i n e x i s t a n t e   d a n s   l a   b i b l i o t h Ã¨ q u e   u t i l i s Ã© e .   R e m p l a c Ã© e   p a r   u n e   i c Ã´ n e   f o n c t i o n n e l l e   Ã© q u i v a l e n t e .  
 
- IntÃƒÂ©gration Paie-Finance : crÃƒÂ©ation d'un nouvel espace dans ComptabilitÃƒÂ©/Finance pour lister les ÃƒÂ©tats de paie et lancer les dÃƒÂ©penses associÃƒÂ©es de maniÃƒÂ¨re globale.

- Gestion des permissions : ajout de la vÃƒÂ©rification de permission spÃƒÂ©cifique (sous-menu paie_salaires) sur les vues de la paie dans ComptabilitÃƒÂ©/Finance, assurant le mÃƒÂªme niveau de sÃƒÂ©curitÃƒÂ© que les autres vues.

- Ajout d'un bouton de validation globale du mois dans /rh/paie/fiches/ avec envoi de notification au personnel configurÃ© dans les paramÃ¨tres gÃ©nÃ©raux.

-   A j o u t   d e   l a   m o d i f i c a t i o n   e t   s u p p r e s s i o n   d e s   c o n t r a t s   ( i n t e r f a c e   L i s t e   d e s   c o n t r a t s )   d a n s   r h .  
 -   R e f o n t e   d e   l a   m o d i f i c a t i o n   d e s   c o n t r a t s   :   c r Ã© a t i o n   d ' u n e   p a g e   c o m p l Ã¨ t e   d Ã© d i Ã© e   ( u p d a t e _ c o n t r a t . h t m l )   b a s Ã© e   s u r   l ' a s s i s t a n t   d e   c r Ã© a t i o n   a v e c   p r Ã© - r e m p l i s s a g e   d e s   r u b r i q u e s .  
 -   C o r r e c t i o n   d u   p r Ã© - r e m p l i s s a g e   d e s   d o n n Ã© e s   s u r   l a   p a g e   d e   m o d i f i c a t i o n   d u   c o n t r a t   ( p r o b l Ã¨ m e   d e   s Ã© r i a l i s a t i o n   J S O N   d e s   d o n n Ã© e s   P y t h o n ) .  
 -   M e n u   l a t Ã© r a l   :   a j o u t   d e   l a   r o u t e   ' u p d a t e C o n t r a t P a g e '   p o u r   m a i n t e n i r   l e   m e n u   ' G e s t i o n   d e s   C o n t r a t s '   a c t i f   l o r s   d e   l a   m o d i f i c a t i o n   d ' u n   c o n t r a t .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n   m Ã© c a n i s m e   d e   p r Ã© v i s u a l i s a t i o n   ( m o d a l )   p o u r   c h a q u e   l i g n e   d e   f i c h e   d e   p a i e .  
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d e   l a   f e n Ãª t r e   m o d a l e   d e   p r Ã© v i s u a l i s a t i o n   d a n s   l ' a s s i s t a n t   d e   p a i e   ( d Ã© p l a c e m e n t   e n   d e h o r s   d u   c o n t e n e u r   d u   t a b l e a u   p o u r   Ã© v i t e r   l e s   c o n f l i t s   C S S ) .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   a n i m a t i o n   d ' a l e r t e   s u r   l e   b o u t o n   d e   r e c h e r c h e   l o r s q u e   l e   m o i s   o u   l ' a n n Ã© e   e s t   m o d i f i Ã©   a f i n   d ' i n c i t e r   l ' u t i l i s a t e u r   Ã    a c t u a l i s e r   l e s   d o n n Ã© e s .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   s e c t i o n   d e   s y n t h Ã¨ s e   g l o b a l e   a f f i c h a n t   l e   t o t a l   d e s   p a i e m e n t s   n e t s ,   l e   t o t a l   d e s   p r i m e s   e t   l e   t o t a l   d e   l a   f i s c a l i t Ã©   ( S S   +   I R G ) .  
 -   M o t e u r   d e   p a i e   :   a j o u t   d ' u n   n o u v e a u   m o d e   d e   c a l c u l   p o u r   l e s   r u b r i q u e s   e t   p r i m e s   ( ' J O U R S '   :   P a r   j o u r   t r a v a i l l Ã© )   p e r m e t t a n t   d e   m u l t i p l i e r   l e   m o n t a n t   s a i s i   p a r   l e   n o m b r e   d e   j o u r s   d e   p r Ã© s e n c e   d e   l ' e m p l o y Ã© .  
 -   C o r r e c t i o n   d u   m e n u   l a t Ã© r a l   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   o Ã¹   l e   s o u s - m e n u   d e s   f i c h e s   d e   p a i e   f o r m a t e u r s   s ' a f f i c h a i t   c o m m e   a c t i f   ( e n   s u r b r i l l a n c e )   l o r s q u ' o n   s e   t r o u v a i t   s u r   l ' a s s i s t a n t   d e   p a i e   d e s   e m p l o y Ã© s   ( p r o b l ÃƒÂ¨ m e   d e   m a t c h i n g   d e   c h a ÃƒÂ® n e   d e   c a r a c t ÃƒÂ¨ r e s ) .  
 -   I n t e r f a c e   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   ( s c r o l l   h o r i z o n t a l   i n d ÃƒÂ© s i r a b l e )   s u r   l a   p a g e   d ' h i s t o r i q u e   d e s   f i c h e s   d e   p a i e   d e s   f o r m a t e u r s ,   c a u s ÃƒÂ©   p a r   u n   ÃƒÂ© l ÃƒÂ© m e n t   d ÃƒÂ© c o r a t i f   q u i   d ÃƒÂ© p a s s a i t   d e   l ' ÃƒÂ© c r a n .  
 -   A s s i s t a n t   d e   p a i e   :   e x c l u s i o n   a u t o m a t i q u e   d e s   e m p l o y ÃƒÂ© s   d o n t   l a   f i c h e   d e   p a i e   a   d ÃƒÂ© j ÃƒÂ    ÃƒÂ© t ÃƒÂ©   g ÃƒÂ© n ÃƒÂ© r ÃƒÂ© e   p o u r   l e   m o i s   e n   c o u r s   a f i n   d ' ÃƒÂ© v i t e r   l e s   d o u b l o n s   ( i l s   r ÃƒÂ© a p p a r a ÃƒÂ® t r o n t   s i   l e u r   f i c h e   e s t   a n n u l ÃƒÂ© e ) .  
 -   A s s i s t a n t   d e   p a i e   :   a f f i c h a g e   d ' u n e   v u e   d e   s y n t h ÃƒÂ¨ s e   ' P a i e   c l ÃƒÂ´ t u r ÃƒÂ© e   p o u r   c e   m o i s '   l o r s q u e   t o u t e s   l e s   f i c h e s   d e   p a i e   o n t   d ÃƒÂ© j ÃƒÂ    ÃƒÂ© t ÃƒÂ©   g ÃƒÂ© n ÃƒÂ© r ÃƒÂ© e s   p o u r   l e   m o i s   s ÃƒÂ© l e c t i o n n ÃƒÂ© ,   r e m p l a ÃƒÂ§ a n t   l e   m e s s a g e   d ' e r r e u r   ' A u c u n e   d o n n ÃƒÂ© e   d i s p o n i b l e ' .  
 -   C o r r e c t i o n   d e   l ' i n t e r f a c e   :   l ' i c ÃƒÂ´ n e   d u   m e n u   ' A s s i s t a n t   d e   P a i e '   n e   s ' a f f i c h a i t   p a s   e n   r a i s o n   d ' u n e   c l a s s e   d ' i c ÃƒÂ´ n e   i n e x i s t a n t e   d a n s   l a   b i b l i o t h ÃƒÂ¨ q u e   u t i l i s ÃƒÂ© e .   R e m p l a c ÃƒÂ© e   p a r   u n e   i c ÃƒÂ´ n e   f o n c t i o n n e l l e   ÃƒÂ© q u i v a l e n t e .  
 
- IntÃ©gration Paie-Finance : crÃ©ation d'un nouvel espace dans ComptabilitÃ©/Finance pour lister les Ã©tats de paie et lancer les dÃ©penses associÃ©es de maniÃ¨re globale.

- Gestion des permissions : ajout de la vÃ©rification de permission spÃ©cifique (sous-menu paie_salaires) sur les vues de la paie dans ComptabilitÃ©/Finance, assurant le mÃªme niveau de sÃ©curitÃ© que les autres vues.

- Ajout d'un bouton de validation globale du mois dans /rh/paie/fiches/ avec envoi de notification au personnel configurÃ© dans les paramÃ¨tres gÃ©nÃ©raux.

- RÃ©organisation de l'ordre des groupes dans l'onglet Gestion des modules (ParamÃ¨tres gÃ©nÃ©raux) pour suivre un workflow plus logique : CRM -> Inscriptions -> TrÃ©sorerie -> ScolaritÃ© -> Communication.

- Correction de la fenÃªtre modale de paiement dans /comptabilite/tresorerie/paies/liste/ qui ne s'ouvrait pas ou Ã©tait bloquÃ©e (dÃ©placement du code HTML de la modale en dehors de la balise 	able-responsive pour corriger les problÃ¨mes de z-index et d'overflow de Bootstrap).

- Ajout d'un champ 'Date de paiement effective' dans la modale de paiement de la paie (/comptabilite/tresorerie/paies/liste/) afin de permettre Ã  l'utilisateur de spÃ©cifier la date rÃ©elle du rÃ¨glement (met Ã  jour la dÃ©pense et les fiches de paie).

- CrÃ©ation automatique d'une entrÃ©e OperationsBancaire lors du lancement de la dÃ©pense de paie (mode 'vir') pour que la dÃ©pense remonte dans le module d'Imputation Bancaire.

- TrÃ©sorerie : Regroupement des lignes par compte comptable associÃ© dans la liste des imputations comptables des spÃ©cialitÃ©s (/comptabilite/tresorerie/imputation-comptable/specialite/liste/). Ajout d'une fonctionnalitÃ© d'accordÃ©on (fermÃ© par dÃ©faut) pour masquer/afficher les spÃ©cialitÃ©s liÃ©es Ã  chaque compte.
-   S é p a r a t i o n   d u   ' T o t a l   P r o p o s é '   e n   ' R e c e t t e s   P r o p o s é e s '   e t   ' D é p e n s e s   P r o p o s é e s '   d a n s   l a   v u e    u d g e t _ c a m p a i g n _ r e v i e w   e t   s o n   t e m p l a t e   a s s o c i é .  
 -   C o r r e c t i o n   d u   c a l c u l   d e   l a   p r o g r e s s i o n   e t   d e   l ' é c a r t   r e s t a n t   d a n s   l a   v u e    u d g e t _ c a m p a i g n _ r e v i e w   :   l e   c a l c u l   e s t   d é s o r m a i s   b a s é   u n i q u e m e n t   s u r   l e s   d é p e n s e s   p r o p o s é e s   a u   l i e u   d e   l a   s o m m e   d e s   r e c e t t e s   e t   d é p e n s e s .  
 -   A j o u t   d ' u n e   m e n t i o n   e x p l i c a t i v e   s o u s   l a   b a r r e   d e   p r o g r e s s i o n   d a n s   l a   v u e    u d g e t _ c a m p a i g n _ r e v i e w   p o u r   p r é c i s e r   q u e   l e   c a l c u l   e s t   b a s é   s u r   l e s   d é p e n s e s .  
 -   A j o u t   d ' u n   t i t r e   d y n a m i q u e   ( ' D e m a n d e   d e   r a l l o n g e   -   { n o m _ c a m p a g n e } ' )   p o u r   l a   p a g e   d e   d e m a n d e   d e   r a l l o n g e   b u d g é t a i r e   (  e q u e s t _ e x t e n s i o n ) .  
 -   D a n s   l a   l i s t e   d e s   c a m p a g n e s   b u d g é t a i r e s   (  u d g e t _ c a m p a i g n _ l i s t . h t m l ) ,   r e m p l a c e m e n t   d u   b o u t o n   ' C o n f i g u r e r   l e s   o b j e c t i f s '   p a r   ' C o n s u l t e r   l e s   d é t a i l s '   ( a v e c   u n e   i c ô n e   d ' Si l )   l o r s q u e   l a   c a m p a g n e   e s t   a c t i v e .  
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d e s   d é t a i l s   d e   l a   d e m a n d e   d e   r a l l o n g e   (  e v i e w _ e x t e n s i o n )   :   a f f i c h a g e   d u   n o m   d e   l ' e n t r e p r i s e   v i a   u n e   m a p   d e   c l é s   e n   c h a î n e s   d e   c a r a c t è r e s   e t   a j o u t   d u   m o n t a n t   t o t a l   d e m a n d é   d a n s   l a   s e c t i o n   ' D é t a i l s   d e   l a   d e m a n d e ' .  
 -   M o d e r n i s a t i o n   c o m p l è t e   d u   d e s i g n   d e   l a   p a g e   d ' e x a m e n   d e s   r a l l o n g e s   (  e v i e w _ e x t e n s i o n . h t m l )   :   s t y l e   p r e m i u m   a v e c   g l a s s m o r p h i s m   a m é l i o r é ,   n o u v e l l e s   p a l e t t e s   d e   c o u l e u r s ,   e f f e t s   d e   s u r v o l ,   b a d g e s   m o d e r n i s é s   e t   i n t é g r a t i o n   d e   n o m b r e u s e s   i c ô n e s .  
 
- DÃ©placement de la rubrique 'Gestion des Ã‰chÃ©anciers' sous la rubrique 'ParamÃ¨tres Financiers' dans le menu de navigation (menu.html).

- Trésorerie : Ajout de la configuration des références de paiements dans le brouillard de banque (brouillard_banque.html) avec une interface modale calquée sur le fonctionnement du brouillard de caisse.

- Trésorerie : Correction d'un problème empêchant la modification de la référence de paiement dans le brouillard de banque (ajout des champs item_id et model_type dans l'API json).

- Correction de l'affichage du montant total demandé dans la page de révision des rallonges budgétaires (associe_app).

- Trésorerie : Retrait des décorateurs de permission (@module_permission_required) sur les actions de suppression et modification des échéanciers configurés (ApiDeleteEcheancier, ApiBulkDeleteEcheanciers, ApiUpdateEcheancier).

- Trésorerie : Restauration des décorateurs de permission (@module_permission_required) sur les actions de suppression et modification des échéanciers configurés suite à une erreur (ApiDeleteEcheancier, ApiBulkDeleteEcheanciers, ApiUpdateEcheancier).


### [Fixed] - 2026-06-06
- **Trésorerie** : Correction du bug où l'application d'une remise ne mettait pas à jour les montants des échéances dans la base de données (DuePaiements) si l'inscription était déjà confirmée. Modifié ApiApplyRemiseToPaiement dans 	_tresorerie/f_views/preinscrit_paiements.py pour recalculer et mettre à jour montant_due et montant_restant des tranches.
- **UI** : Deplacement du sous-menu Paie & Salaires juste en dessous du sous-menu Depenses dans le menu principal Comptabilite/Finance (menu.html).
- **UI** : Remplacement du menu deroulant d'actions par des boutons d'icones dans la liste des fournisseurs (liste_des_fournisseurs.html). Correction egalement des colonnes du filtre de recherche.
- **Backend** : Modification de l'assistant de paie (assistantPaie) pour prendre en compte et filtrer par entite_legal. Le dropdown 'entreprise' a ete ajoute a l'interface (assistant_paie.html).
- **Finance** : Mise à jour de la liste des paies (liste_paie_finance) pour grouper et afficher l'entité (entreprise) associée à chaque fiche de paie. L'opération de paiement (lancer_depense_paie) a également été ajustée pour créer des dépenses distinctes par entité.
- **Finance** : Ajout d'une balise titre (title) sur la page des listes de paie Finance (liste_paie_finance.html). Ajout d'un formulaire de filtres complets (mois, annee, entreprise, statut de paiement) dans l'interface et gestion de ces filtres depuis la vue (views_paie.py).
- **Finance / Interface** : Déplacement du formulaire des filtres de la liste des paies (liste_paie_finance.html) juste au-dessus du tableau des données, pour une meilleure clarté visuelle et ergonomie.
- **RH / Finance** : Vérification complète du traitement de la paie par entité. La notification envoyée par ApiValiderPaieMois inclut désormais le nom de l'entité si celle-ci a été spécifiée lors de la validation.
- **Trésorerie / Banque** : Ajout d'un tableau de bord affichant la situation de l'imputation bancaire (total opérations, rapprochées, en attente) et la situation de recouvrement des chèques/virements sur la page du brouillard de banque. Ajout de raccourcis rapides vers les pages concernées.
- **RH / Formateurs** : Modernisation de l'interface des contrats (intégration de DataTables pour la recherche/pagination, déplacement du filtre d'entité, ajout d'actions rapides inline pour un workflow plus fluide).
- **RH / Formateurs** : Harmonisation du design de la modal de création/édition de contrat pour un aspect plus premium (espacement, fonds teintés, bords arrondis, et icônes).
- **RH / Formateurs** : Correction du design et de l'alignement des filtres DataTables (Affichage et Recherche) dans la liste des contrats.
- **RH / Formateurs** : Refonte totale de la disposition des filtres pour la liste des contrats. Les filtres (Entité, Recherche, Pagination) sont désormais placés dans une carte dédiée au-dessus du tableau (Filter Section), harmonisée avec la vue fiches-mensuelles.
-   H a r m o n i s a t i o n   d e s   i c ô n e s   d e   l ' E s p a c e   e m p l o y é   a v e c   l ' E s p a c e   f o r m a t e u r   ( u t i l i s a t i o n   d e   B o x i c o n s   a u   l i e u   d e   R e m i x   I c o n s   d a n s   l e   m e n u   R H ) .  
 -   S u p p r e s s i o n   d e s   c e r c l e s   d e   c o u l e u r   a u t o u r   d e s   i c ô n e s   d e s   s o u s - m e n u s   d e   l ' E s p a c e   e m p l o y é   p o u r   c o r r e s p o n d r e   a u   s t y l e   s i m p l e   d e   l ' E s p a c e   f o r m a t e u r .  
 -   A j o u t   d e s   d é c o r a t e u r s   d e   p e r m i s s i o n s   m a n q u a n t s   ( @ m o d u l e _ p e r m i s s i o n _ r e q u i r e d   e t   @ r o l e _ r e q u i r e d )   s u r   l e s   v u e s   b u d g e t _ c a m p a i g n _ d i s p a t c h ,   r e q u e s t _ e x t e n s i o n   e t   b u d g e t _ c a m p a i g n _ r e a l i z a t i o n .  
 -   S u p p r e s s i o n   d e   l ' o n g l e t   F o r m a t i o n s   d a n s   l a   p a g e   / c o n s e i l / l i s t e - d e s - t h e m a t i q u e s /  
 -   A j o u t   d ' u n e   m o d a l e   p o u r   c o n f i g u r e r   e t   a j o u t e r   r a p i d e m e n t   d e s   p a r t i c i p a n t s   d e p u i s   l a   v u e   d e   c r é a t i o n   d ' u n   n o u v e a u   g r o u p e   c o n s e i l .  
 -   M o d e r n i s a t i o n   d u   d e s i g n   d e   l a   m o d a l e   d ' a j o u t   r a p i d e   d ' u n   p a r t i c i p a n t   ( l a b e l s   f l o t t a n t s ,   d é g r a d é s ,   i c ô n e s ,   g l a s s m o r p h i s m ) .  
 -   S u p p r e s s i o n   d e s   d é g r a d é s   d a n s   l a   m o d a l e   d ' a j o u t   r a p i d e   d e   p a r t i c i p a n t   p o u r   l ' h a r m o n i s e r   a v e c   l e   d e s i g n   g l o b a l   d u   p r o j e t   ( u t i l i s a t i o n   d e s   c l a s s e s   b g - p r i m a r y   e t   t e x t - p r i m a r y   s t a n d a r d ) .  
 -   A j o u t   d e s   d é c o r a t e u r s   @ m o d u l e _ p e r m i s s i o n _ r e q u i r e d   m a n q u a n t s   s u r   l ' e n s e m b l e   d e s   v u e s   e t   A P I s   d u   m o d u l e   C o n s e i l   ( t _ c o n s e i l )   p o u r   s é c u r i s e r   l ' a c c è s   a u x   p a g e s   e t   a u x   a c t i o n s .  
 -   A j o u t   d e   l a   s u p p r e s s i o n   e n   c a s c a d e   d e s   f a c t u r e s   d e   c o n s e i l   ( m ê m e   c e l l e s   v a l i d é e s ) ,   e n   s u p p r i m a n t   l e s   p a i e m e n t s ,   l e t t r a g e s   b a n c a i r e s   e t   r e m b o u r s e m e n t s   l i é s ,   t o u t   e n   p r é s e r v a n t   l e   d e v i s   s o u r c e .  
 -   R é i n i t i a l i s a t i o n   d e   l ' é t a t   d u   c l i e n t   d a n s   l e   p i p e l i n e   ( r e t o u r   à   ' d e v i s _ e n v o y e '   o u   ' n e g o c i a t i o n ' )   l o r s   d e   l a   s u p p r e s s i o n   d ' u n e   f a c t u r e   d e   c o n s e i l .  
 -   S u p p r e s s i o n   d e   l a   c o n f i g u r a t i o n   d e s   d r o i t s   d e   t i m b r e   d a n s   l e   m o d u l e   C o n s e i l .   L a   g e s t i o n   e t   l e   c a l c u l   d e s   d r o i t s   d e   t i m b r e   s ' e f f e c t u e n t   d é s o r m a i s   d e   m a n i è r e   c e n t r a l i s é e   v i a   l e s   p a r a m è t r e s   f i n a n c i e r s   d e   l a   T r é s o r e r i e .  
 -   I s o l a t i o n   d e   l a   c o n f i g u r a t i o n   d e s   T a x e s   &   F i s c a l i t é   d a n s   l e   m o d u l e   C o n s e i l   :   l a   s é l e c t i o n   d e   l ' e n t r e p r i s e   n ' i m p a c t e   p l u s   q u e   l e s   o n g l e t s   D o c u m e n t s ,   O f f r e s   R e m i s e s   e t   M e n t i o n s   L é g a l e s .   L a   T V A   e s t   g é r é e   d e   m a n i è r e   g l o b a l e .  
 -   A m é l i o r a t i o n   d e   l ' e x p é r i e n c e   u t i l i s a t e u r   d a n s   l a   c r é a t i o n   d e   d e v i s   ( c o n s e i l / n o u v e a u - d e v i s / )   :   l e   c h a m p   d e   s é l e c t i o n   d u   c l i e n t   e s t   d é s o r m a i s   f i l t r a b l e   v i a   S e l e c t 2 .  
 -   C o r r e c t i o n   d e   l ' e n c o d a g e   d e s   m e s s a g e s   ( A l e r t i f y   e t   D j a n g o   M e s s a g e s )   d a n s   l ' e n s e m b l e   d u   m o d u l e   C o n s e i l .  
 -   L e   c h a m p   d e   s é l e c t i o n   d e   l a   t h é m a t i q u e   d a n s   l a   c o n f i g u r a t i o n   d ' u n   d e v i s   e s t   d é s o r m a i s   f i l t r a b l e   v i a   S e l e c t 2 .  
 -   B l o c a g e   d e   l ' a c c è s   a u x   d é t a i l s   d ' u n   d e v i s   t a n t   q u ' i l   n ' e s t   p a s   v a l i d é   ( b o u t o n   d é s a c t i v é   d a n s   l a   l i s t e   e t   r e d i r e c t i o n   s e r v e u r   s é c u r i s é e ) .  
 -   A u t o - r e m p l i s s a g e   d e s   c o n d i t i o n s   c o m m e r c i a l e s   :   l o r s   d e   l a   c r é a t i o n   d ' u n   d e v i s   o u   d ' u n e   f a c t u r e ,   l e s   c o n d i t i o n s   c o m m e r c i a l e s   p a r   d é f a u t   d é f i n i e s   d a n s   l a   c o n f i g u r a t i o n   g l o b a l e   s ' a p p l i q u e n t   d é s o r m a i s   a u t o m a t i q u e m e n t .  
 -   M o d e r n i s a t i o n   d u   d e s i g n   d e s   l i g n e s   d e   d e v i s   ( i c ô n e s ,   b a d g e s ,   b o u t o n s   a r r o n d i s )   d a n s   l e   f o r m u l a i r e   d e   c o n f i g u r a t i o n .  
 -   L e   c h a m p   d e   s é l e c t i o n   d u   c l i e n t / p r o s p e c t   d a n s   l a   c r é a t i o n   d ' u n e   n o u v e l l e   f a c t u r e   e s t   d é s o r m a i s   f i l t r a b l e   v i a   S e l e c t 2 .  
 -   B l o c a g e   d e   l ' a c c è s   a u x   d é t a i l s   d ' u n e   f a c t u r e   t a n t   q u ' e l l e   n ' e s t   p a s   v a l i d é e   ( b o u t o n   d é s a c t i v é   d a n s   l a   l i s t e   e t   r e d i r e c t i o n   s e r v e u r   s é c u r i s é e ,   c o m m e   p o u r   l e s   d e v i s ) .  
 -   B l o c a g e   d e   l ' a c c è s   à   l a   g é n é r a t i o n   d u   P D F   p o u r   l e s   f a c t u r e s   n o n   v a l i d é e s   ( b o u t o n   d é s a c t i v é   e t   r o u t e   s é c u r i s é e ) .  
 -   A j u s t e m e n t   d u   d e s i g n   d e   l a   c o n f i g u r a t i o n   d e   f a c t u r e   :   r e p o s i t i o n n e m e n t   p r o p r e   d u   b a d g e   d e   s t a t u t   ( B r o u i l l o n )   d a n s   l e   c o i n   s u p é r i e u r   d r o i t   e t   r é o r g a n i s a t i o n   d u   c h a m p   ' M o d e   d e   p a i e m e n t   a t t e n d u '   a u - d e s s u s   d e s   c o n d i t i o n s .  
 -   R e p o s i t i o n n e m e n t   d u   b a d g e   d e   s t a t u t   ( B r o u i l l o n )   :   d é p l a c é   à   c ô t é   d u   t i t r e   p r i n c i p a l   p o u r   é v i t e r   t o u t   c h e v a u c h e m e n t   a v e c   l e   c o n t e n u   d u   d o c u m e n t .  
 -   I n t é g r a t i o n   d e   S e l e c t 2   d a n s   l a   c o n f i g u r a t i o n   d e s   f a c t u r e s   ( c o n s e i l / c o n f i g u r e - f a c t u r e . h t m l )   p o u r   r e n d r e   l a   s é l e c t i o n   d e   l a   t h é m a t i q u e   f i l t r a b l e   a v e c   b a r r e   d e   r e c h e r c h e   i n t é g r é e .  
 -   C o r r e c t i o n   d u   d e s i g n   d u   c h a m p   T h é m a t i q u e   ( S e l e c t 2 )   p o u r   q u ' i l   a d o p t e   l e   m ê m e   s t y l e   v i s u e l   q u e   l e s   a u t r e s   i n p u t s   ( f o r m - c o n t r o l - c u s t o m ) .  
 -   H a r m o n i s a t i o n   d u   d e s i g n   d e s   l i g n e s   d e   f a c t u r a t i o n   p o u r   c o r r e s p o n d r e   e x a c t e m e n t   à   c e l u i   d e s   d e v i s   ( a j o u t   d ' a v a t a r s   p o u r   l e s   d é s i g n a t i o n s ,   s t y l e   d e s   b a d g e s   p o u r   q u a n t i t é s / r e m i s e s ,   e t   b o u t o n s   d ' a c t i o n s   a r r o n d i s ) .  
 -   A j u s t e m e n t   C S S   d e   S e l e c t 2   ( T h é m a t i q u e )   :   f o r ç a g e   d e   l a   l a r g e u r   à   1 0 0 % ,   a j o u t   d u   m a r g i n - b o t t o m   m a n q u a n t   e t   a l i g n e m e n t   f l e x   p o u r   m a t c h e r   p a r f a i t e m e n t   l e s   d i m e n s i o n s   d e s   a u t r e s   c h a m p s   d u   f o r m u l a i r e .  
 -   C o r r e c t i o n   d u   d é b o r d e m e n t   d e   t e x t e   d a n s   l e   c h a m p   T h é m a t i q u e   S e l e c t 2   l o r s   d e   l a   s é l e c t i o n   :   r e m p l a c e m e n t   d u   d i s p l a y :   f l e x   p a r   u n   p o s i t i o n n e m e n t   a b s o l u   p o u r   l e   b o u t o n   d e   s u p p r e s s i o n   ( x )   e t   l a   f l è c h e ,   a v e c   u n   t e x t - o v e r f l o w   ( p o i n t s   d e   s u s p e n s i o n )   p o u r   l e s   t e x t e s   t r o p   l o n g s .  
 -   N o u v e l l e   c o r r e c t i o n   S e l e c t 2   :   R e t o u r   à   l a   m é t h o d e   n a t i v e   d e   S e l e c t 2   ( v i a   l i n e - h e i g h t )   s a n s   f o r c e r   l e   f l e x   o u   l e   p o s i t i o n n e m e n t   a b s o l u ,   c e   q u i   r è g l e   d é f i n i t i v e m e n t   l e   b u g   v i s u e l   d u   b o u t o n   d e   s u p p r e s s i o n   ' x '   e t   l e   c h e v a u c h e m e n t   d u   t e x t e .  
 -   A j o u t   d ' u n   e s p a c e m e n t   ( m a r g i n - b o t t o m )   e n t r e   l e   c h a m p   S e l e c t 2   d e   T h é m a t i q u e   e t   l e   c h a m p   D é s i g n a t i o n .  
 -   R e f o n t e   t o t a l e   d e   l a   z o n e   d ' a j o u t   d e   l i g n e   d e   f a c t u r a t i o n   :   i n t é g r a t i o n   d i r e c t e   d a n s   l e   t a b l e a u   e n   < t f o o t > ,   r e m p l a c e m e n t   d e s   d i v   p a r   u n   F l e x b o x   g a p - 2   p o u r   u n   e s p a c e m e n t   i n f a i l l i b l e   e t   a l i g n e m e n t   p a r f a i t   a v e c   l e   d e s i g n   d e s   d e v i s .  
 -   C o r r e c t i o n   d u   c e n t r a g e   v e r t i c a l   d u   t e x t e   d a n s   S e l e c t 2   :   s u p p r e s s i o n   d e s   m a r g e s   e t   p a d d i n g s   p a r   d é f a u t   q u i   d é c a l a i e n t   l e   t e x t e   v e r s   l e   b a s   a v e c   l a   h a u t e u r   d é f i n i e .  
 -   H a r m o n i s a t i o n   d e   l a   t a i l l e   d u   c h a m p   S e l e c t 2   ( T h é m a t i q u e )   p o u r   c o r r e s p o n d r e   e x a c t e m e n t   à   l a   h a u t e u r   e t   l a   t a i l l e   d e   p o l i c e   ( 1 2 p x )   d e s   c h a m p s   D é s i g n a t i o n   e t   D e s c r i p t i o n .  
 -   R e f o n t e   g l o b a l e   d e   l a   p a g e   C o n f i g u r a t i o n   F a c t u r e   p o u r   a d o p t e r   l e   d e s i g n   P r e m i u m   ( h a r m o n i s é   a v e c   l e   d e v i s )   :   s u p p r e s s i o n   d u   C S S   f a i t   m a i s o n   e t   a d o p t i o n   d e   c a r d - p r e m i u m ,   t a b l e - p r e m i u m ,   e t   d u   C S S   S e l e c t 2   o f f i c i e l   q u i   c o r r i g e   d é f i n i t i v e m e n t   l e   b u g   d e   l a   c r o i x .  
 