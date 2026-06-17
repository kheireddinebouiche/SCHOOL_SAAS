# Ã°Å¸â€”â€œÃ¯Â¸ï¿½ Journal des Mises ÃƒÂ  Jour (Changelog)

## [Unreleased]
- **Configuration:** Ajout de paramètres de validation des champs requis CRM en fonction du profil (crm_required_fields_national, crm_required_fields_etranger, crm_required_fields_double).
- **CRM:** Validation dynamique côté client et ajout automatique d'astérisques rouges pour les champs requis selon le contexte du partenaire.
- **Configuration:** Remplacement de la validation globale des onglets CRM par des verrous individuels (JSONField crm_field_locks) pour chaque champ de la fiche pré-inscrit.
- **CRM:** Ajout de l'attribut disabled de manière dynamique sur les champs du profil pré-inscrit selon la configuration.
- **Nouveauté (Trésorerie)** : Séparation de l'affichage des chèques et des virements dans le module "Recouvrement des paiements" (`/comptabilite/tresorerie/recouvrement/`) via l'ajout de deux onglets distincts.
- **Nouveauté (Trésorerie)** : Séparation de l'affichage des chèques et des virements dans le module "Suivi des chèques et virements émis" (`/comptabilite/tresorerie/caisse/suivi-cheques-emis/`) avec la création de deux onglets distincts pour un meilleur filtrage.
- **Nouveauté (Trésorerie)** : Adaptation des statuts pour les virements émis. Les virements ont désormais leurs propres statuts ("En attente" et "Virement effectué") distincts de ceux des chèques ("Émis", "En attente de signature", "Remis", "Décaissé").
- **Nouveauté (Formateurs)** : Création de la vue `ChargeHoraireFormateur` pour calculer et afficher le détail des charges horaires (hebdomadaire, mensuelle, semestrielle) des formateurs par groupe et par jour. Réactivation du lien dans le menu.
- **Correction (UI/Menu)** : Commentaire du lien vers `ChargeHoraireFormateur` dans `menu.html` pour corriger l'erreur `NoReverseMatch` suite à la désactivation de cette vue non définie.
- **Correction (Migrations)** : Fusion des migrations conflictuelles (merge) pour l'application `t_formations` (`0013_formateurs_is_particular_irg` et `0015_alter_planscadre_type_plan`).
- **Correction (Formations)** : Commentaire de la route `formateurs/charge-horaire/` qui appelait la vue non dǸfinie `ChargeHoraireFormateur` et provoquait une erreur au lancement du serveur.
- **FonctionnalitÃ© (Conseil/Devis)** : L'impression des devis (depuis la page des dÃ©tails) utilise dÃ©sormais le modÃ¨le `dolibare` de l'application `pdf_editor` pour gÃ©nÃ©rer le PDF avec les bonnes variables au lieu de l'impression basique du navigateur.
- **SÃ©curitÃ© (Conseil)** : Ajout de la permission manquante (`@module_permission_required`) sur la vue `ApiCreateRendezVousPipeline`.
- **Modification UI (Conseil/Prospects)** : Remplacement du menu dÃ©roulant d'actions par des icÃ´nes d'action alignÃ©es (consulter, modifier, supprimer) dans la liste des prospects en instance (`/conseil/prospects-en-instance/`).
- **Configuration** : DÃ©placement de la variable `DEBUG` de `settings.py` vers les variables d'environnement (`.env`).
- **NouveautÃ© (Conseil)** : CrÃ©ation d'un tableau de bord global et agrÃ©gÃ© pour Executive Education (`/conseil/dashboard/`) affichant les KPIs consolidÃ©s pour le CRM (prospects, pipeline), les Ventes (devis, factures, chiffre d'affaires) et la Formation (groupes, participants), incluant un graphique de rÃ©partition du pipeline.
- **FonctionnalitÃ© (Conseil/Groupes)** : Ajout d'une fonctionnalitÃ© de suivi des sÃ©ances dans l'onglet Planning (`/conseil/groupes/details-groupe/<id>/`), permettant de marquer une sÃ©ance comme tenue et de renseigner un compte-rendu des Ã©lÃ©ments abordÃ©s avec un indicateur d'Ã©tat (En attente / Tenue).
- **Alerte (Conseil/Groupes)** : Lors de la crÃ©ation d'un nouveau groupe, la sÃ©lection d'un client affiche dÃ©sormais une notification (alerte visuelle et message Alertify) si celui-ci possÃ¨de dÃ©jÃ  un groupe en cours.
- **AmÃ©lioration (Conseil/Groupes)** : Dans la page de dÃ©tails d'un groupe (`/conseil/groupes/details-groupe/<id>/`), le panneau latÃ©ral affiche dÃ©sormais la facture associÃ©e au devis si elle existe, en la mettant en Ã©vidence (avec le devis liÃ© relÃ©guÃ© au second plan), permettant un accÃ¨s rapide Ã  la facturation.
- **AmÃ©lioration (Conseil/Groupes)** : Dans l'assistant de crÃ©ation de groupe (Ã‰tape 2), si le client possÃ¨de des factures, le systÃ¨me affiche dÃ©sormais les factures avec leurs devis liÃ©s en prioritÃ©, ainsi que les devis non facturÃ©s. Sinon, il n'affiche que les devis.
- **Modification (Conseil/Groupes)** : Harmonisation du design de la fenÃªtre modale d'ajout rapide de participant (remplacement des `form-floating` par un style plus propre avec `input-group` et icÃ´nes, en accord avec le thÃ¨me premium "glass-card").
- **Correction (Conseil/Groupes)** : Le formulaire d'ajout rapide de participant dans l'assistant de crÃ©ation de groupe associe dÃ©sormais correctement le nouveau participant au devis sÃ©lectionnÃ©, ce qui lui permet d'apparaÃ®tre immÃ©diatement dans la liste.
- **Refonte UI (Conseil/Clients)** : Transformation de la page "DÃ©tails du Client" (`/conseil/details-client/<id>/`) en un vÃ©ritable "Tableau de Bord Client" premium :
  - CrÃ©ation d'une banniÃ¨re de profil dÃ©gradÃ©e avec l'avatar du client en chevauchement.
  - Remplacement des cartes KPI par un widget "Bilan Financier" ultra-compact et esthÃ©tique.
  - Suppression du "Workflow Stepper" (pipeline CRM) qui n'Ã©tait plus pertinent pour un client confirmÃ©.
  - Refonte de la navigation par onglets (style "underline" minimaliste).
  - DÃ©placement de la liste des opportunitÃ©s vers un nouvel onglet dÃ©diÃ© "Dossiers & OpportunitÃ©s".
- **Modification (Conseil/Ventes)** : Remplacement de l'alerte de confirmation (alertify) par une fenÃªtre modale personnalisÃ©e (thÃ¨me "glass-card") lors du clic sur le bouton "Rendre en brouillon" dans les dÃ©tails d'un devis.
- **Modification (Conseil/Ventes)** : Harmonisation du design de la fenÃªtre modale "Conversion en Facture" sur la page des dÃ©tails d'un devis (`/conseil/details-devis/<id>/`) avec le thÃ¨me "glass-card" (coins arrondis, icÃ´nes amÃ©liorÃ©es et typographie modernisÃ©e).
- **Modification (Conseil/Pipeline)** : Ajout d'une fenÃªtre de confirmation (alertify) avertissant l'utilisateur qu'un devis brouillon sera gÃ©nÃ©rÃ© automatiquement lorsqu'il dÃ©place (glisser-dÃ©poser) une opportunitÃ© vers la colonne "NÃ©gociation". En cas de confirmation, le devis est crÃ©Ã© et la page est actualisÃ©e.
- **Correction (Conseil/Pipeline)** : Lors de la conversion en devis, la carte est dÃ©sormais correctement positionnÃ©e dans la colonne "NÃ©gociation" au lieu de "Devis envoyÃ©" (le devis Ã©tant crÃ©Ã© en brouillon). Le texte de la modale a Ã©tÃ© mis Ã  jour en consÃ©quence.
- **Modification (Conseil/Ventes)** : RÃ©duction de la taille des Ã©lÃ©ments (padding, boutons d'action et polices) dans les tableaux des listes de devis, factures et avoirs (`/conseil/liste-des-devis/`, `/conseil/liste-des-factures/`) pour un affichage plus compact et optimisÃ©.
- **Modification (Conseil/Pipeline)** : Harmonisation du design de la fenÃªtre modale "Convertir en devis" avec le thÃ¨me de la page `/conseil/pipeline/` (style "glass-card", coins arrondis, icÃ´nes amÃ©liorÃ©es et espacement optimisÃ©).
- **Correction (Conseil/CRM)** : Correction de l'affichage "undefined" pour l'Ã©tat des prospects dans la liste (`/conseil/prospects-en-instance/`) en ajoutant des valeurs par dÃ©faut pour les labels d'Ã©tat ("En attente" et "ConfirmÃ©").
- **Ajout (Conseil/CRM)** : Affichage de la liste des opportunitÃ©s liÃ©es sur la page des dÃ©tails du client (`/conseil/details-client/<slug>/`). L'historique des opportunitÃ©s a Ã©tÃ© intÃ©grÃ© sous l'onglet "RÃ©sumÃ©" pour un suivi centralisÃ©.
- **Ajout (Conseil/CRM)** : Affichage de la liste des opportunitÃ©s liÃ©es sur la page des dÃ©tails du prospect (`/conseil/details-prospect/<slug>/`). Les opportunitÃ©s sont prÃ©sentÃ©es sous forme de cartes premium avec leur statut, budget, probabilitÃ© et le commercial associÃ©.
- **Modification (Conseil/CRM)** : Modernisation de l'affichage de la liste des prospects en instance (`/conseil/prospects-en-instance/`) via l'amÃ©lioration du rendu JavaScript (ajout d'avatars avec initiales, badges arrondis, typographie affinÃ©e et effets de survol interactifs sur les lignes et boutons d'action).
- **Modification (Examens)** : Modernisation de l'affichage des cartes de groupes de sessions d'examens (`examens/deliberation/builltins/session/`) avec un design premium (icÃ´nes amÃ©liorÃ©es, statistiques internes sur fond clair, boutons arrondis et effets de survol dynamiques).
- **Correction (Examens/Logs)** : RÃ©solution de l'erreur `DoesNotExist` (500) lors de la suppression en cascade d'une session d'examen, causÃ©e par l'accÃ¨s Ã  des objets liÃ©s inexistants lors de la journalisation de suppression (`log_exam_action_delete`).
- **Modification (Conseil)** : Modernisation des lignes du tableau de la page "Mapping DAS" (`/conseil/das/`) avec des effets de survol dynamiques (Ã©lÃ©vation, ombrage, fond translucide) pour accentuer l'effet "glass-card".
- **Modification (Conseil)** : Harmonisation du design de la fenÃªtre de crÃ©ation (modale DAS) avec le thÃ¨me "glass-card" de la page.
- **Ajout (Stages)** : MÃƒÂ©canisme de suppression des sÃƒÂ©ances de Focus Group (historique des sÃƒÂ©ances) via une fenÃƒÂªtre modale de confirmation.
- **Ajout (Stages)** : MÃƒÂ©canisme d'affectation de stages existants ÃƒÂ  un Focus Group directement depuis la vue de dÃƒÂ©tail du Focus Group (`stage/focus-group/<id>/`) via une fenÃƒÂªtre modale.
- **Ajout (Stages)** : MÃƒÂ©canisme de suppression des stages directement depuis la liste des stages (`stage/list/`) avec confirmation par fenÃƒÂªtre modale et journalisation.
- **SÃƒÂ©curitÃƒÂ© & Audit (Stages)** : Ajout de la journalisation complÃƒÂ¨te (via `UserActionLog`) pour toutes les actions de mutation effectuÃƒÂ©es dans le module des Stages (t_stage). Cela inclut les actions sur les stages (crÃƒÂ©ation, modification, suppression), les prÃƒÂ©sentations progressives (ajout, suppression), les focus groups (crÃƒÂ©ation, ajout/suppression de sÃƒÂ©ances, affectation de stages), les conseils de validation, les dÃƒÂ©cisions, et les notes d'examen final.
- **SÃƒÂ©curitÃƒÂ© & Audit (Executive Education)** : Ajout de la journalisation complÃƒÂ¨te (via `UserActionLog`) pour toutes les actions de mutation effectuÃƒÂ©es dans le module Executive Education (t_conseil). Cela inclut les actions sur les prospects, les opportunitÃƒÂ©s, les devis (crÃƒÂ©ation, validation, acceptation/rejet), les factures (crÃƒÂ©ation, validation, annulation, suppression), les groupes, les paiements, les thÃƒÂ©matiques, et les informations liÃƒÂ©es (participants, DAS, infos bancaires).
- **SÃƒÂ©curitÃƒÂ© & Audit** : Ajout de la journalisation complÃƒÂ¨te (logs d'accÃƒÂ¨s et de modification via `UserActionLog`) pour toutes les actions effectuÃƒÂ©es dans le menu Configuration (gestion des utilisateurs, rÃƒÂ´les, modules, sessions actives, ÃƒÂ©dition des documents PDF, informations de l'entreprise et paramÃƒÂ¨tres gÃƒÂ©nÃƒÂ©raux).
- **Ajout** : FonctionnalitÃƒÂ© d'impression (gÃƒÂ©nÃƒÂ©ration de rapport) du taux d'utilisation de l'ERP avec possibilitÃƒÂ© de sÃƒÂ©lectionner spÃƒÂ©cifiquement un ou plusieurs instituts via une fenÃƒÂªtre modale.
- **Modification** : Refonte de l'affichage de la page `platform_usage_rate` pour utiliser des onglets (tabs) par tenant et ajout de la pagination DataTables.
- **Modification** : Le menu "Satisfaction" a ÃƒÂ©tÃƒÂ© renommÃƒÂ© en "Mesure de satisfaction" dans `menu.html`.
- **Modification** : Remplacement de la pagination serveur des tenants par une pagination locale (DataTables) des logs ÃƒÂ  l'intÃƒÂ©rieur de chaque onglet tenant sur la page `crm_user_logs`.
- **Modification** : Refonte de l'affichage de la page `crm_user_logs` pour utiliser des onglets (tabs) par tenant au lieu d'une liste verticale.
- **Modification** : Regroupement de "Stats CRM", "Logs" et "Taux d'utilisation" sous un seul menu dÃƒÂ©roulant "Statistiques" dans `menu.html` et `saas_menu.html`.
- **Ajout** : Nouvelle vue et page `platform_usage_rate` (Taux d'utilisation de l'ERP) calculant les actions/jour par utilisateur depuis la crÃƒÂ©ation du tenant.
- **Ajout** : Mise en place de filtres par institut, par utilisateur et par type d'action sur la page `crm_user_logs`.
- **Modification** : Le titre de la vue `crm_user_logs` a ÃƒÂ©tÃƒÂ© changÃƒÂ© de "Logs Utilisateurs CRM par Institut" ÃƒÂ  "Logs".
- **Correction** : RÃƒÂ©solution de l'erreur `ModuleNotFoundError` en utilisant `app.models` au lieu de `school.models` pour `Institut`.
- **Modification** : Le lien de menu a ÃƒÂ©tÃƒÂ© renommÃƒÂ© en "Logs" (dans `menu.html` et `saas_menu.html`).
- **Modification** : La vue `crm_user_logs` rÃƒÂ©cupÃƒÂ¨re dÃƒÂ©sormais tous les logs (sans limite de 100).
- **Ajout** : Lien vers `crm_user_logs` ajoutÃƒÂ© dans le menu `saas_menu.html`.
- **Ajout** : Nouvelle vue et page `crm_user_logs` dans `associe_app` pour afficher les logs utilisateurs (`UserActionLog`) CRM par tenant.

---

## [07/06/2026] - v1.2.x - Harmonisation de la configuration Facture

- **SaaS Admin / Notifications Globales** :
  - **Gestion des annonces** : CrÃƒÂ©ation d'une interface superadmin permettant de crÃƒÂ©er, lister, activer ou supprimer des annonces (`SystemAnnouncement`).
  - **Ciblage granulaire** : PossibilitÃƒÂ© de cibler l'ensemble des utilisateurs, un Tenant spÃƒÂ©cifique, ou un utilisateur prÃƒÂ©cis au sein d'un Tenant.
  - **Temps RÃƒÂ©el via WebSockets (Channels)** : IntÃƒÂ©gration au `NotificationConsumer` existant pour diffuser instantanÃƒÂ©ment les annonces (`announcement_trigger`) sans rafraÃƒÂ®chissement de page ni appels AJAX pÃƒÂ©riodiques. Groupes de diffusions optimisÃƒÂ©s (`global_all_users`, `{schema_name}_all_users`).
  - **Relance d'annonce** : Ajout d'un bouton "Relancer" permettant de rÃƒÂ©initialiser l'historique de lecture d'une annonce spÃƒÂ©cifique et de forcer sa rÃƒÂ©apparition en temps rÃƒÂ©el chez tous les utilisateurs ciblÃƒÂ©s.
  - **Suivi de lecture** : Affichage d'une modale pour les utilisateurs ciblÃƒÂ©s. Un systÃƒÂ¨me de validation ("J'ai lu cette annonce") enregistre la confirmation en base de donnÃƒÂ©es (`AnnouncementRead`) pour dÃƒÂ©sactiver l'affichage.

- **SaaS Admin / Centre de Connaissance** :
  - Suppression de la mention de limitation de taille de fichier pour l'upload.
  - Ajout du support de lecture des vidÃƒÂ©os (MP4) hÃƒÂ©bergÃƒÂ©es localement directement depuis le modal vidÃƒÂ©o existant.

- **TrÃƒÂ©sorerie / ModÃƒÂ¨les d'ÃƒÂ©chÃƒÂ©ancier** :
  - **Frais d'inscription** : Ajout de la possibilitÃƒÂ© d'activer/dÃƒÂ©sactiver la configuration des frais d'inscription au niveau du modÃƒÂ¨le d'ÃƒÂ©chÃƒÂ©ancier (`ModelEcheancier.has_frais_inscription`).
  - **Interface utilisateur** : IntÃƒÂ©gration de toggles "Activer la configuration des frais d'inscription" dans les formulaires de crÃƒÂ©ation et de modification des modÃƒÂ¨les d'ÃƒÂ©chÃƒÂ©ancier (`gestion_echeancier.html`).
  - **Assistant d'ÃƒÂ©chÃƒÂ©ancier** : Conditionnement de l'affichage et de l'obligation de saisie du montant des frais d'inscription et de l'entitÃƒÂ© associÃƒÂ©e dans le formulaire de crÃƒÂ©ation d'ÃƒÂ©chÃƒÂ©ancier (`creer-un-echeancier.html`), selon la configuration du modÃƒÂ¨le choisi.

- **CRM / Double Diplomation** :
  - **Modification des Voeux** : RÃƒÂ©solution du bug empÃƒÂªchant la modification des voeux (bouton "Mettre ÃƒÂ  jour") pour les prospects en double cursus, notamment ceux ayant ÃƒÂ©tÃƒÂ© annulÃƒÂ©s ou modifiÃƒÂ©s sans changement de formation (rÃƒÂ©cupÃƒÂ©ration directe de `id_formation` via `#formation_voeux`).
  - **Changement de Cursus** : Correction d'une erreur 500 (`FicheVoeuxDouble.DoesNotExist`) survenant lors du passage d'un cursus double ÃƒÂ  un cursus standard, particuliÃƒÂ¨rement pour les prospects annulÃƒÂ©s ayant des fiches de voeux dÃƒÂ©jÃƒÂ  confirmÃƒÂ©es.
  - **RÃƒÂ©initialisation des Voeux** : Ajout d'un nouveau mÃƒÂ©canisme (bouton et modale de confirmation) permettant de supprimer complÃƒÂ¨tement les fiches de vÃ…â€œux d'un prospect (double et standard) et de rÃƒÂ©initialiser son orientation.

- **Facturation (Conseil)** :
  - **Design & UI** : Harmonisation complÃƒÂ¨te de la page `configure-facture.html` pour correspondre au design premium de `configure-devis.html`. Modification de la structure de la grille pour utiliser une barre latÃƒÂ©rale droite fixe (`.col-lg-4`) pour le rÃƒÂ©capitulatif, et une colonne principale (`.col-lg-8`) pour les informations gÃƒÂ©nÃƒÂ©rales, la liste des articles et les modalitÃƒÂ©s. Adaptation du code JavaScript de gÃƒÂ©nÃƒÂ©ration du rÃƒÂ©capitulatif financier pour utiliser des ÃƒÂ©lÃƒÂ©ments HTML `<div class="d-flex ...">` ÃƒÂ  la place de `<tr>`, afin de correspondre visuellement aux totaux du devis.
  - **Ligne d'ajout des articles** : Harmonisation de la ligne d'ajout (`tfoot`) avec les placeholders, les entÃƒÂªtes du tableau, la gestion des permissions (`disabled`) et le style Select2 (retrait du thÃƒÂ¨me bootstrap-5 pour appliquer le style premium customisÃƒÂ©).
  - **Conversion Devis en Facture** : Le prospect liÃƒÂ© au devis devient automatiquement un client (avec le statut "convertit") lors de la conversion du devis en facture, s'il n'est pas dÃƒÂ©jÃƒÂ  client.
  - **Liste des Devis** : Masquage de l'icÃƒÂ´ne de modification (ÃƒÂ©dition) pour les devis qui ne sont plus ÃƒÂ  l'ÃƒÂ©tat brouillon (dÃƒÂ©jÃƒÂ  validÃƒÂ©s/envoyÃƒÂ©s/acceptÃƒÂ©s).
  - **Design & UI (Liste des Devis)** : Harmonisation complÃƒÂ¨te du design de la page `liste_des_devis.html` avec celui de `liste_des_factures.html`. Ajout des filtres par statut et par dates (JS dynamique), badges de statuts subtils arrondis (`bg-xxx-subtle`), boutons d'actions circulaires (32x32) et compteurs de rÃƒÂ©sultats (pagination dynamique).

## [05/06/2026] - v1.2.x - Permissions Menus Associe App

- **Associe App** :
  - **Satisfaction** : Ajout d'un nouveau menu "Satisfaction" affichant une page "FonctionnalitÃƒÆ’Ã‚Â© en attente de validation".
  - **Gestion des Permissions** : Ajout de conditions de permissions (`is_superuser` et `is_staff`) sur le menu horizontal `public_folder/menu.html` pour restreindre l'accÃƒÆ’Ã‚Â¨s. ParamÃƒÆ’Ã‚Â©trage et Administration sont rÃƒÆ’Ã‚Â©servÃƒÆ’Ã‚Â©s aux super-administrateurs, tandis que Dashboard, Stats CRM et Gestion BudgÃƒÆ’Ã‚Â©taire sont accessibles aux membres du staff.
  - **Gestion des Utilisateurs** : Ajout d'un mÃƒÆ’Ã‚Â©canisme (checkbox) pour activer ou dÃƒÆ’Ã‚Â©sactiver le statut super-utilisateur lors de l'ajout ou de l'ÃƒÆ’Ã‚Â©dition d'un utilisateur dans le panel d'administration (`associe_app`).

- **SaaS Admin** :
  - **Gestion du Changelog** : Correction d'une erreur 403 (CSRF) lors de la suppression d'une mise ÃƒÆ’Ã‚Â  jour dans le panel SaaS Admin. Le jeton CSRF ÃƒÆ’Ã‚Â©tait mal formatÃƒÆ’Ã‚Â© dans la requÃƒÆ’Ã‚Âªte AJAX (`templates/saas_admin_app/saas_changelog.html`).

---

## [04/06/2026] - v1.2.0 - Refonte de l'IRG (ConformitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© LÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©gale AlgÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rienne)

- **Ressources Humaines (FiscalitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© & Paie)** :
  - **Prise en charge des Primes / Rubriques dans la Paie EmployÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s** :
    - IntÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©gration du calcul des rubriques/primes dynamiques (gains et retenues) dans la gÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ration de la paie en masse via `assistantPaie`. La mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©thode synchronise automatiquement le contrat `t_rh.models.Contrats` avec le contrat `t_ressource_humaine.models.Contrat` pour rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cupÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rer et appliquer la bonne configuration des rubriques et leurs valeurs par dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©faut ou personnalisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es.
    - Persistance correcte des lignes de paie (`LignePaie`) associÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  chaque bulletin lors de la validation en masse, en ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©vitant les doublons (suppression prÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©alable des anciennes lignes de paie pour la mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªme fiche).
    - AmÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©lioration de la vue de dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tail du bulletin de paie de l'employÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© (`fiche_paie_detail.html`) pour boucler sur `fiche.lignes_paie.all` (au lieu de la relation incorrecte `fiche.lignes.all`) et utiliser le libellÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© correct (`ligne.rubrique.libelle` au lieu de `ligne.rubrique.nom`).
    - Affichage des lignes de primes exceptionnelles, de l'indemnitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© de panier, de l'indemnitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© de transport et des retenues pour absences directement sous forme de lignes du tableau pour les employÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s.
    - Ajout des conditions pour charger le nom et l'identifiant de l'employÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© ou du formateur de maniÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨re dynamique dans `fiche_paie_print.html` et `_fiche_paie_detail.html` afin d'ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©viter tout plantage `AttributeError` ou omission.
  - **Filtres & Gestion de l'Historique de Paie** : Modernisation de l'historique des fiches de paie (`liste_fiches_paie.html`). Ajout de filtres de recherche avancÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s par employÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©, entitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© lÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©gale, mois, annÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e et statut de validation (ValidÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© ou Brouillon). Les filtres s'appliquent en temps rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©el (via l'ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©vÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nement `onchange` sur tous les sÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©lecteurs) et mettent ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  jour l'historique du navigateur (`window.history.pushState`) pour des filtres persistants sans rechargement de page.
  - **Correction du chargement des rubriques** : RÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©solution d'une erreur 404 dans `details_employe.html` lors de l'ouverture du modal de gestion des rubriques/primes pour un employÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©. Remplacement du chemin d'accÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s AJAX codÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© en dur par la balise Django dynamique `{% url %}` ciblant l'URL correcte sous le namespace `t_ressource_humaine`.
  - **Validation & Suppression Individuelle/En Masse** : IntÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©gration de checkboxes de sÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©lection et d'une barre d'actions groupÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es permettant de valider ou d'annuler la validation de plusieurs bulletins de paie simultanÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ment. Ajout d'un bouton de suppression sÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©curisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© par SweetAlert2, accessible uniquement pour les bulletins de paie ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  l'ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tat de brouillon (non validÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s).
  - **PrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©-visualisation et Confirmation de Paie (Masse Salariale)** : Ajout d'une ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tape de prÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©-visualisation/confirmation avant le scellement dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©finitif de la paie. Les pages d'assistant de paie (salariÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s et formateurs) calculent dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sormais les totaux gÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©raux (nombre de personnes, masse salariale brute globale, total cotisations SS, total retenues IRG et total Net ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  payer) et les prÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sentent dans une fenÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªtre de confirmation SweetAlert2 ergonomique et claire.
  - **Correction de l'assistant de paie** : RÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©solution d'un plantage `AttributeError` lors de la validation globale de la paie dans `t_rh/views.py::assistantPaie` oÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¹ le champ inexistant `date_debut` du modÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨le `Contrats` a ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© remplacÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© par le champ correct `date_embauche`.
  - **Moteur de calcul IRG** : Refonte totale de `calculer_irg` dans `t_ressource_humaine/logic.py` pour implÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©menter la mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©thode officielle algÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rienne (LF 2022 / LF 2026) :
    - Arrondi systÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©matique du salaire imposable ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  la dizaine de DA infÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rieure avant le calcul du barÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨me.
    - Application du premier abattement proportionnel de 40% sur l'IRG brut (limitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© au minimum de 1 000 DA et maximum de 1 500 DA par mois).
    - Formule de lissage pour le **Cas GÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ral** (de 30 000 DA ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  35 000 DA) : $\text{IRG} = \text{IRG1} \times \frac{137}{51} - \frac{27925}{8}$.
    - Formule de lissage pour le **Cas Particulier** (RetraitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s & HandicapÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s, de 30 000 DA ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  42 500 DA) : $\text{IRG} = \text{IRG1} \times \frac{93}{61} - \frac{81213}{41}$.
    - Arrondi fiscal systÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©matique au dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cime (dizaine de centimes).
  - **Correction du calcul CDI/CDD** : RÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©solution du bug appliquant incorrectement le taux flat de 10% des vacataires ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  tous les enseignants (mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªme sous CDD/CDI) ; dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sormais, seuls les contrats de type `VACATION` sont soumis ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  ce taux flat.
  - **Base de donnÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es / ModÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨les** : Ajout du champ `is_particular_irg` dans les modÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨les `Employees` et `Formateurs`. IntÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©gration automatique dans les formulaires et les modals de crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation et modification (modals d'ajout/ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©dition dans `liste_des_formateur.html` et formulaire `NouveauEmploye`).
  - **Prise en charge Formateurs** : Adaptation de `PaieEngine.calculer_paie` pour rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©soudre et transmettre le drapeau `is_particular_irg` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  partir du contrat de l'enseignant (CDI/CDD) et du formateur reliÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©, appliquant ainsi correctement le barÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨me de lissage particulier (retraitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s/handicapÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s) dans le calcul et la gÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ration finale des fiches de paie.
  - **Migrations de Base de DonnÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es** : GÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ration et application de la migration `0013_formateurs_is_particular_irg.py` pour ajouter le champ dans le schÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ma et migration sur tous les schÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©mas locataires (multi-tenant isolation).
  - **Interface & Simulation ModernisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e (Design Premium)** : 
    - IntÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©gration de la description dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©taillÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e du barÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨me, des abattements et des formules de lissage (cas gÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ral et cas particulier) dans l'interface de configuration fiscale `templates/tenant_folder/rh/paie/config_fiscalite.html`.
    - Ajout d'un **Simulateur IRG InstantanÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©** interactif en Javascript, permettant de calculer en temps rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©el l'IRG pour n'importe quel montant imposable saisi, pour le cas gÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ral et le cas particulier.
    - Refonte visuelle complÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨te sous forme de cartes en verre dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©poli (Glassmorphism) avec des dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©gradÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s fins, des ombres fluides et une disposition responsive.
    - AmÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©lioration de l'ergonomie des formulaires avec des focus adoucis (`soft-glow`), des tooltips informatifs et des styles de boutons raffinÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s.
    - Ajout d'une micro-animation de pulsation (`pulse-update` par transform scale) sur les cartes de rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sultats du simulateur (Vert/ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â°meraude pour le Cas GÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ral, Bleu/Info pour le Cas Particulier) dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©clenchÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  chaque frappe de clavier.
  - **Validation des tests** : Ajout de nouveaux tests unitaires pour valider les calculs exacts d'IRG pour les cas gÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©raux et particuliers (ex: 30 900 DA & 30 930 DA imposable) et ajustement des assertions de test ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  l'abattement de 40% (ex: 45 500 DA imposable).

---

## [04/06/2026] - v1.1.0 - Refonte de StabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© (Executive Education & RH)

- **Global / Core** :
  - Correction d'une erreur fatale au dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©marrage du serveur (NameError) dans `school/settings.py` causÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e par `DEBUG = F`.
- **Ressources Humaines (Paie, PrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sences & Formateurs)** :
  - **Assistant de Paie Formateurs** : CrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation d'une page dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©diÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e "Assistant de Paie - Formateurs" permettant de gÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rer en masse les fiches de paie basÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es sur les fiches mensuelles validÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es.
  - **Historique DÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©diÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© & Redesign** : SÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©paration de l'historique des fiches de paie pour les formateurs avec un tout nouveau design premium (Glassmorphism, animations au survol, dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©gradÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s de couleurs).
  - **Taux IRG Vacataires** : Ajout d'une configuration globale (dans les ParamÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨tres RH) pour appliquer le taux IRG forfaitaire (sans abattement) spÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cifique aux formateurs vacataires (par dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©faut 10%). Ce paramÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨tre est pris en charge par le moteur de paie de faÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§on automatique.
  - **Correction du systÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨me de paie formateur** : Correction de l'erreur d'attribut `types_contrat` vers `eligible_types` dans `generer_paie`.
  - **Liaison Paie-Formateur** : Ajout d'un bouton "GÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rer Paie" dynamique sur les fiches mensuelles des formateurs.
  - **Validation des Fiches Mensuelles** : CrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation du modÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨le `ValidationFicheMensuelleFormateur` avec bouton AJAX SweetAlert2 pour verrouiller et approuver une fiche mensuelle de formateur (affichage d'un badge "ValidÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e").
  - Restructuration du menu principal "Ressources Humaines" pour sÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©parer clairement "Espace EmployÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s" et "Espace Formateurs" (et les garder ouverts au bon endroit).
  - Modification du formulaire d'ajout d'employÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© pour rendre tous les champs non obligatoires.
  - RÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©solution d'un bug empÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªchant l'affichage des nouveaux employÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s dans les vues de prÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sences et dans l'assistant de paie en autorisant les ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tats (etat) non dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©finis ou vides.
  - RÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©solution d'un bug bloquant l'ajout d'un nouvel employÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â» ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  la validation silencieuse de champs manquants dans le formulaire (exclusion de `solde_conge`, `solde_conge_annee_prec`, `is_teacher`, etc.).
  - RÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©solution d'un bug similaire empÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªchant la crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation d'un nouveau contrat pour un formateur (exclusion des champs non rendus comme `prime_transport`, `prime_panier`, `employee` du `ContratForm`).
  - RÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©solution de l'erreur `KeyError` dans le calcul des paies.
- **CRM / Prospects** :
  - Ajout de la fonctionnalitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© d'importation en masse de prospects particuliers via fichier Excel (`.xlsx`).
  - Ajout d'une fonctionnalitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© pour tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©lÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©charger le modÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨le d'import. Les prospects importÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s ont le statut "pas de vÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œux formulÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s pour le moment".
- **SaaS Admin** :
  - Correction d'une erreur de syntaxe (`SyntaxError`) dans `urls.py` causÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e par des caractÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨res `\n` mal formatÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s empÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªchant l'accÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s au portail.
  - Correction d'une erreur `NameError` due au dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©corateur `@saas_superuser_required` non dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©fini dans `views.py` (remplacÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© par `@user_passes_test(superadmin_only)`).
  - Correction de la localisation des noms de mois en anglais dans les fiches mensuelles de prÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sence.
  - CrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation des pages "Empty States" Premium pour les tableaux vides (CongÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s, PrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sences, Fiches Mensuelles, EmployÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s).
- **Executive Education (`t_conseil`)** :
  - SÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©curisation complÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨te des API contre les plantages silencieux (`Erreur 500`) : Ajout de la gestion `DoesNotExist` pour plus de 30 requÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªtes `.get()`.
  - Fixation d'une faille `KeyError` lors de l'accÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s aux donnÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es JSON non fournies dans l'API de gestion des groupes.

### ÃƒÆ’Ã‚Â¢Ãƒâ€¦Ã¢â‚¬Å“Ãƒâ€šÃ‚Â¨ AmÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©liorations (Optimisations)
- **Base de donnÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es (`@transaction.atomic`)** :
  - Application du verrouillage transactionnel sur toutes les fonctions critiques de crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation (`Devis`, `Factures`, `Clients`, `Groupes`) de l'Executive Education, garantissant qu'aucune donnÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e fantÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´me ne soit gÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e en cas d'erreur de rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©seau.
- **Ressources Humaines** :
  - Refonte de la suppression d'employÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s avec un effacement en cascade strict des contrats, piÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ces jointes et absences (`models.CASCADE`).
  - Restructuration visuelle de la configuration HUB en onglets modernes.

---
*(Ajoutez les prochaines entrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es ci-dessus)*
-   A j o u t   d e   l a   m o d i f i c a t i o n   e t   s u p p r e s s i o n   d e s   c o n t r a t s   ( i n t e r f a c e   L i s t e   d e s   c o n t r a t s )   d a n s   r h . 
 
 -   R e f o n t e   d e   l a   m o d i f i c a t i o n   d e s   c o n t r a t s   :   c r ÃƒÆ’Ã‚Â© a t i o n   d ' u n e   p a g e   c o m p l ÃƒÆ’Ã‚Â¨ t e   d ÃƒÆ’Ã‚Â© d i ÃƒÆ’Ã‚Â© e   ( u p d a t e _ c o n t r a t . h t m l )   b a s ÃƒÆ’Ã‚Â© e   s u r   l ' a s s i s t a n t   d e   c r ÃƒÆ’Ã‚Â© a t i o n   a v e c   p r ÃƒÆ’Ã‚Â© - r e m p l i s s a g e   d e s   r u b r i q u e s . 
 
 -   C o r r e c t i o n   d u   p r ÃƒÆ’Ã‚Â© - r e m p l i s s a g e   d e s   d o n n ÃƒÆ’Ã‚Â© e s   s u r   l a   p a g e   d e   m o d i f i c a t i o n   d u   c o n t r a t   ( p r o b l ÃƒÆ’Ã‚Â¨ m e   d e   s ÃƒÆ’Ã‚Â© r i a l i s a t i o n   J S O N   d e s   d o n n ÃƒÆ’Ã‚Â© e s   P y t h o n ) . 
 
 -   M e n u   l a t ÃƒÆ’Ã‚Â© r a l   :   a j o u t   d e   l a   r o u t e   ' u p d a t e C o n t r a t P a g e '   p o u r   m a i n t e n i r   l e   m e n u   ' G e s t i o n   d e s   C o n t r a t s '   a c t i f   l o r s   d e   l a   m o d i f i c a t i o n   d ' u n   c o n t r a t . 
 
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n   m ÃƒÆ’Ã‚Â© c a n i s m e   d e   p r ÃƒÆ’Ã‚Â© v i s u a l i s a t i o n   ( m o d a l )   p o u r   c h a q u e   l i g n e   d e   f i c h e   d e   p a i e . 
 
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d e   l a   f e n ÃƒÆ’Ã‚Âª t r e   m o d a l e   d e   p r ÃƒÆ’Ã‚Â© v i s u a l i s a t i o n   d a n s   l ' a s s i s t a n t   d e   p a i e   ( d ÃƒÆ’Ã‚Â© p l a c e m e n t   e n   d e h o r s   d u   c o n t e n e u r   d u   t a b l e a u   p o u r   ÃƒÆ’Ã‚Â© v i t e r   l e s   c o n f l i t s   C S S ) . 
 
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   a n i m a t i o n   d ' a l e r t e   s u r   l e   b o u t o n   d e   r e c h e r c h e   l o r s q u e   l e   m o i s   o u   l ' a n n ÃƒÆ’Ã‚Â© e   e s t   m o d i f i ÃƒÆ’Ã‚Â©   a f i n   d ' i n c i t e r   l ' u t i l i s a t e u r   ÃƒÆ’Ã‚Â    a c t u a l i s e r   l e s   d o n n ÃƒÆ’Ã‚Â© e s . 
 
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   s e c t i o n   d e   s y n t h ÃƒÆ’Ã‚Â¨ s e   g l o b a l e   a f f i c h a n t   l e   t o t a l   d e s   p a i e m e n t s   n e t s ,   l e   t o t a l   d e s   p r i m e s   e t   l e   t o t a l   d e   l a   f i s c a l i t ÃƒÆ’Ã‚Â©   ( S S   +   I R G ) . 
 
 -   M o t e u r   d e   p a i e   :   a j o u t   d ' u n   n o u v e a u   m o d e   d e   c a l c u l   p o u r   l e s   r u b r i q u e s   e t   p r i m e s   ( ' J O U R S '   :   P a r   j o u r   t r a v a i l l ÃƒÆ’Ã‚Â© )   p e r m e t t a n t   d e   m u l t i p l i e r   l e   m o n t a n t   s a i s i   p a r   l e   n o m b r e   d e   j o u r s   d e   p r ÃƒÆ’Ã‚Â© s e n c e   d e   l ' e m p l o y ÃƒÆ’Ã‚Â© . 
 
 -   C o r r e c t i o n   d u   m e n u   l a t ÃƒÆ’Ã‚Â© r a l   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   o ÃƒÆ’Ã‚Â¹   l e   s o u s - m e n u   d e s   f i c h e s   d e   p a i e   f o r m a t e u r s   s ' a f f i c h a i t   c o m m e   a c t i f   ( e n   s u r b r i l l a n c e )   l o r s q u ' o n   s e   t r o u v a i t   s u r   l ' a s s i s t a n t   d e   p a i e   d e s   e m p l o y ÃƒÆ’Ã‚Â© s   ( p r o b l ÃƒÆ’Ã‚Â¨ m e   d e   m a t c h i n g   d e   c h a ÃƒÆ’Ã‚Â® n e   d e   c a r a c t ÃƒÆ’Ã‚Â¨ r e s ) . 
 
 -   I n t e r f a c e   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   ( s c r o l l   h o r i z o n t a l   i n d ÃƒÆ’Ã‚Â© s i r a b l e )   s u r   l a   p a g e   d ' h i s t o r i q u e   d e s   f i c h e s   d e   p a i e   d e s   f o r m a t e u r s ,   c a u s ÃƒÆ’Ã‚Â©   p a r   u n   ÃƒÆ’Ã‚Â© l ÃƒÆ’Ã‚Â© m e n t   d ÃƒÆ’Ã‚Â© c o r a t i f   q u i   d ÃƒÆ’Ã‚Â© p a s s a i t   d e   l ' ÃƒÆ’Ã‚Â© c r a n . 
 
 -   A s s i s t a n t   d e   p a i e   :   e x c l u s i o n   a u t o m a t i q u e   d e s   e m p l o y ÃƒÆ’Ã‚Â© s   d o n t   l a   f i c h e   d e   p a i e   a   d ÃƒÆ’Ã‚Â© j ÃƒÆ’Ã‚Â    ÃƒÆ’Ã‚Â© t ÃƒÆ’Ã‚Â©   g ÃƒÆ’Ã‚Â© n ÃƒÆ’Ã‚Â© r ÃƒÆ’Ã‚Â© e   p o u r   l e   m o i s   e n   c o u r s   a f i n   d ' ÃƒÆ’Ã‚Â© v i t e r   l e s   d o u b l o n s   ( i l s   r ÃƒÆ’Ã‚Â© a p p a r a ÃƒÆ’Ã‚Â® t r o n t   s i   l e u r   f i c h e   e s t   a n n u l ÃƒÆ’Ã‚Â© e ) . 
 
 -   A s s i s t a n t   d e   p a i e   :   a f f i c h a g e   d ' u n e   v u e   d e   s y n t h ÃƒÆ’Ã‚Â¨ s e   ' P a i e   c l ÃƒÆ’Ã‚Â´ t u r ÃƒÆ’Ã‚Â© e   p o u r   c e   m o i s '   l o r s q u e   t o u t e s   l e s   f i c h e s   d e   p a i e   o n t   d ÃƒÆ’Ã‚Â© j ÃƒÆ’Ã‚Â    ÃƒÆ’Ã‚Â© t ÃƒÆ’Ã‚Â©   g ÃƒÆ’Ã‚Â© n ÃƒÆ’Ã‚Â© r ÃƒÆ’Ã‚Â© e s   p o u r   l e   m o i s   s ÃƒÆ’Ã‚Â© l e c t i o n n ÃƒÆ’Ã‚Â© ,   r e m p l a ÃƒÆ’Ã‚Â§ a n t   l e   m e s s a g e   d ' e r r e u r   ' A u c u n e   d o n n ÃƒÆ’Ã‚Â© e   d i s p o n i b l e ' . 
 
 -   C o r r e c t i o n   d e   l ' i n t e r f a c e   :   l ' i c ÃƒÆ’Ã‚Â´ n e   d u   m e n u   ' A s s i s t a n t   d e   P a i e '   n e   s ' a f f i c h a i t   p a s   e n   r a i s o n   d ' u n e   c l a s s e   d ' i c ÃƒÆ’Ã‚Â´ n e   i n e x i s t a n t e   d a n s   l a   b i b l i o t h ÃƒÆ’Ã‚Â¨ q u e   u t i l i s ÃƒÆ’Ã‚Â© e .   R e m p l a c ÃƒÆ’Ã‚Â© e   p a r   u n e   i c ÃƒÆ’Ã‚Â´ n e   f o n c t i o n n e l l e   ÃƒÆ’Ã‚Â© q u i v a l e n t e . 
 
 
- IntÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©gration Paie-Finance : crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation d'un nouvel espace dans ComptabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©/Finance pour lister les ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tats de paie et lancer les dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©penses associÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es de maniÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨re globale.

- Gestion des permissions : ajout de la vÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rification de permission spÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cifique (sous-menu paie_salaires) sur les vues de la paie dans ComptabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©/Finance, assurant le mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªme niveau de sÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©curitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© que les autres vues.

- Ajout d'un bouton de validation globale du mois dans /rh/paie/fiches/ avec envoi de notification au personnel configurÃƒÆ’Ã‚Â© dans les paramÃƒÆ’Ã‚Â¨tres gÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©raux.

-   A j o u t   d e   l a   m o d i f i c a t i o n   e t   s u p p r e s s i o n   d e s   c o n t r a t s   ( i n t e r f a c e   L i s t e   d e s   c o n t r a t s )   d a n s   r h .  
 -   R e f o n t e   d e   l a   m o d i f i c a t i o n   d e s   c o n t r a t s   :   c r ÃƒÆ’Ã‚Â© a t i o n   d ' u n e   p a g e   c o m p l ÃƒÆ’Ã‚Â¨ t e   d ÃƒÆ’Ã‚Â© d i ÃƒÆ’Ã‚Â© e   ( u p d a t e _ c o n t r a t . h t m l )   b a s ÃƒÆ’Ã‚Â© e   s u r   l ' a s s i s t a n t   d e   c r ÃƒÆ’Ã‚Â© a t i o n   a v e c   p r ÃƒÆ’Ã‚Â© - r e m p l i s s a g e   d e s   r u b r i q u e s .  
 -   C o r r e c t i o n   d u   p r ÃƒÆ’Ã‚Â© - r e m p l i s s a g e   d e s   d o n n ÃƒÆ’Ã‚Â© e s   s u r   l a   p a g e   d e   m o d i f i c a t i o n   d u   c o n t r a t   ( p r o b l ÃƒÆ’Ã‚Â¨ m e   d e   s ÃƒÆ’Ã‚Â© r i a l i s a t i o n   J S O N   d e s   d o n n ÃƒÆ’Ã‚Â© e s   P y t h o n ) .  
 -   M e n u   l a t ÃƒÆ’Ã‚Â© r a l   :   a j o u t   d e   l a   r o u t e   ' u p d a t e C o n t r a t P a g e '   p o u r   m a i n t e n i r   l e   m e n u   ' G e s t i o n   d e s   C o n t r a t s '   a c t i f   l o r s   d e   l a   m o d i f i c a t i o n   d ' u n   c o n t r a t .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n   m ÃƒÆ’Ã‚Â© c a n i s m e   d e   p r ÃƒÆ’Ã‚Â© v i s u a l i s a t i o n   ( m o d a l )   p o u r   c h a q u e   l i g n e   d e   f i c h e   d e   p a i e .  
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d e   l a   f e n ÃƒÆ’Ã‚Âª t r e   m o d a l e   d e   p r ÃƒÆ’Ã‚Â© v i s u a l i s a t i o n   d a n s   l ' a s s i s t a n t   d e   p a i e   ( d ÃƒÆ’Ã‚Â© p l a c e m e n t   e n   d e h o r s   d u   c o n t e n e u r   d u   t a b l e a u   p o u r   ÃƒÆ’Ã‚Â© v i t e r   l e s   c o n f l i t s   C S S ) .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   a n i m a t i o n   d ' a l e r t e   s u r   l e   b o u t o n   d e   r e c h e r c h e   l o r s q u e   l e   m o i s   o u   l ' a n n ÃƒÆ’Ã‚Â© e   e s t   m o d i f i ÃƒÆ’Ã‚Â©   a f i n   d ' i n c i t e r   l ' u t i l i s a t e u r   ÃƒÆ’Ã‚Â    a c t u a l i s e r   l e s   d o n n ÃƒÆ’Ã‚Â© e s .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   s e c t i o n   d e   s y n t h ÃƒÆ’Ã‚Â¨ s e   g l o b a l e   a f f i c h a n t   l e   t o t a l   d e s   p a i e m e n t s   n e t s ,   l e   t o t a l   d e s   p r i m e s   e t   l e   t o t a l   d e   l a   f i s c a l i t ÃƒÆ’Ã‚Â©   ( S S   +   I R G ) .  
 -   M o t e u r   d e   p a i e   :   a j o u t   d ' u n   n o u v e a u   m o d e   d e   c a l c u l   p o u r   l e s   r u b r i q u e s   e t   p r i m e s   ( ' J O U R S '   :   P a r   j o u r   t r a v a i l l ÃƒÆ’Ã‚Â© )   p e r m e t t a n t   d e   m u l t i p l i e r   l e   m o n t a n t   s a i s i   p a r   l e   n o m b r e   d e   j o u r s   d e   p r ÃƒÆ’Ã‚Â© s e n c e   d e   l ' e m p l o y ÃƒÆ’Ã‚Â© .  
 -   C o r r e c t i o n   d u   m e n u   l a t ÃƒÆ’Ã‚Â© r a l   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   o ÃƒÆ’Ã‚Â¹   l e   s o u s - m e n u   d e s   f i c h e s   d e   p a i e   f o r m a t e u r s   s ' a f f i c h a i t   c o m m e   a c t i f   ( e n   s u r b r i l l a n c e )   l o r s q u ' o n   s e   t r o u v a i t   s u r   l ' a s s i s t a n t   d e   p a i e   d e s   e m p l o y ÃƒÆ’Ã‚Â© s   ( p r o b l ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ m e   d e   m a t c h i n g   d e   c h a ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â® n e   d e   c a r a c t ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ r e s ) .  
 -   I n t e r f a c e   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   ( s c r o l l   h o r i z o n t a l   i n d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s i r a b l e )   s u r   l a   p a g e   d ' h i s t o r i q u e   d e s   f i c h e s   d e   p a i e   d e s   f o r m a t e u r s ,   c a u s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   p a r   u n   ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© l ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© m e n t   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© c o r a t i f   q u i   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© p a s s a i t   d e   l ' ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© c r a n .  
 -   A s s i s t a n t   d e   p a i e   :   e x c l u s i o n   a u t o m a t i q u e   d e s   e m p l o y ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s   d o n t   l a   f i c h e   d e   p a i e   a   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© j ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â    ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© t ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   g ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© n ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e   p o u r   l e   m o i s   e n   c o u r s   a f i n   d ' ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© v i t e r   l e s   d o u b l o n s   ( i l s   r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© a p p a r a ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â® t r o n t   s i   l e u r   f i c h e   e s t   a n n u l ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e ) .  
 -   A s s i s t a n t   d e   p a i e   :   a f f i c h a g e   d ' u n e   v u e   d e   s y n t h ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ s e   ' P a i e   c l ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´ t u r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e   p o u r   c e   m o i s '   l o r s q u e   t o u t e s   l e s   f i c h e s   d e   p a i e   o n t   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© j ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â    ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© t ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   g ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© n ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e s   p o u r   l e   m o i s   s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© l e c t i o n n ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© ,   r e m p l a ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ a n t   l e   m e s s a g e   d ' e r r e u r   ' A u c u n e   d o n n ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e   d i s p o n i b l e ' .  
 -   C o r r e c t i o n   d e   l ' i n t e r f a c e   :   l ' i c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´ n e   d u   m e n u   ' A s s i s t a n t   d e   P a i e '   n e   s ' a f f i c h a i t   p a s   e n   r a i s o n   d ' u n e   c l a s s e   d ' i c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´ n e   i n e x i s t a n t e   d a n s   l a   b i b l i o t h ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ q u e   u t i l i s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e .   R e m p l a c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e   p a r   u n e   i c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´ n e   f o n c t i o n n e l l e   ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© q u i v a l e n t e .  
 
- IntÃƒÆ’Ã‚Â©gration Paie-Finance : crÃƒÆ’Ã‚Â©ation d'un nouvel espace dans ComptabilitÃƒÆ’Ã‚Â©/Finance pour lister les ÃƒÆ’Ã‚Â©tats de paie et lancer les dÃƒÆ’Ã‚Â©penses associÃƒÆ’Ã‚Â©es de maniÃƒÆ’Ã‚Â¨re globale.

- Gestion des permissions : ajout de la vÃƒÆ’Ã‚Â©rification de permission spÃƒÆ’Ã‚Â©cifique (sous-menu paie_salaires) sur les vues de la paie dans ComptabilitÃƒÆ’Ã‚Â©/Finance, assurant le mÃƒÆ’Ã‚Âªme niveau de sÃƒÆ’Ã‚Â©curitÃƒÆ’Ã‚Â© que les autres vues.

- Ajout d'un bouton de validation globale du mois dans /rh/paie/fiches/ avec envoi de notification au personnel configurÃƒÆ’Ã‚Â© dans les paramÃƒÆ’Ã‚Â¨tres gÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©raux.

- RÃƒÆ’Ã‚Â©organisation de l'ordre des groupes dans l'onglet Gestion des modules (ParamÃƒÆ’Ã‚Â¨tres gÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©raux) pour suivre un workflow plus logique : CRM -> Inscriptions -> TrÃƒÆ’Ã‚Â©sorerie -> ScolaritÃƒÆ’Ã‚Â© -> Communication.

- Correction de la fenÃƒÆ’Ã‚Âªtre modale de paiement dans /comptabilite/tresorerie/paies/liste/ qui ne s'ouvrait pas ou ÃƒÆ’Ã‚Â©tait bloquÃƒÆ’Ã‚Â©e (dÃƒÆ’Ã‚Â©placement du code HTML de la modale en dehors de la balise 	able-responsive pour corriger les problÃƒÆ’Ã‚Â¨mes de z-index et d'overflow de Bootstrap).

- Ajout d'un champ 'Date de paiement effective' dans la modale de paiement de la paie (/comptabilite/tresorerie/paies/liste/) afin de permettre ÃƒÆ’Ã‚Â  l'utilisateur de spÃƒÆ’Ã‚Â©cifier la date rÃƒÆ’Ã‚Â©elle du rÃƒÆ’Ã‚Â¨glement (met ÃƒÆ’Ã‚Â  jour la dÃƒÆ’Ã‚Â©pense et les fiches de paie).

- CrÃƒÆ’Ã‚Â©ation automatique d'une entrÃƒÆ’Ã‚Â©e OperationsBancaire lors du lancement de la dÃƒÆ’Ã‚Â©pense de paie (mode 'vir') pour que la dÃƒÆ’Ã‚Â©pense remonte dans le module d'Imputation Bancaire.

- TrÃƒÆ’Ã‚Â©sorerie : Regroupement des lignes par compte comptable associÃƒÆ’Ã‚Â© dans la liste des imputations comptables des spÃƒÆ’Ã‚Â©cialitÃƒÆ’Ã‚Â©s (/comptabilite/tresorerie/imputation-comptable/specialite/liste/). Ajout d'une fonctionnalitÃƒÆ’Ã‚Â© d'accordÃƒÆ’Ã‚Â©on (fermÃƒÆ’Ã‚Â© par dÃƒÆ’Ã‚Â©faut) pour masquer/afficher les spÃƒÆ’Ã‚Â©cialitÃƒÆ’Ã‚Â©s liÃƒÆ’Ã‚Â©es ÃƒÆ’Ã‚Â  chaque compte.
-   S ÃƒÂ© p a r a t i o n   d u   ' T o t a l   P r o p o s ÃƒÂ© '   e n   ' R e c e t t e s   P r o p o s ÃƒÂ© e s '   e t   ' D ÃƒÂ© p e n s e s   P r o p o s ÃƒÂ© e s '   d a n s   l a   v u e    u d g e t _ c a m p a i g n _ r e v i e w   e t   s o n   t e m p l a t e   a s s o c i ÃƒÂ© . 
 
 -   C o r r e c t i o n   d u   c a l c u l   d e   l a   p r o g r e s s i o n   e t   d e   l ' ÃƒÂ© c a r t   r e s t a n t   d a n s   l a   v u e    u d g e t _ c a m p a i g n _ r e v i e w   :   l e   c a l c u l   e s t   d ÃƒÂ© s o r m a i s   b a s ÃƒÂ©   u n i q u e m e n t   s u r   l e s   d ÃƒÂ© p e n s e s   p r o p o s ÃƒÂ© e s   a u   l i e u   d e   l a   s o m m e   d e s   r e c e t t e s   e t   d ÃƒÂ© p e n s e s . 
 
 -   A j o u t   d ' u n e   m e n t i o n   e x p l i c a t i v e   s o u s   l a   b a r r e   d e   p r o g r e s s i o n   d a n s   l a   v u e    u d g e t _ c a m p a i g n _ r e v i e w   p o u r   p r ÃƒÂ© c i s e r   q u e   l e   c a l c u l   e s t   b a s ÃƒÂ©   s u r   l e s   d ÃƒÂ© p e n s e s . 
 
 -   A j o u t   d ' u n   t i t r e   d y n a m i q u e   ( ' D e m a n d e   d e   r a l l o n g e   -   { n o m _ c a m p a g n e } ' )   p o u r   l a   p a g e   d e   d e m a n d e   d e   r a l l o n g e   b u d g ÃƒÂ© t a i r e   ( 
 e q u e s t _ e x t e n s i o n ) . 
 
 -   D a n s   l a   l i s t e   d e s   c a m p a g n e s   b u d g ÃƒÂ© t a i r e s   (  u d g e t _ c a m p a i g n _ l i s t . h t m l ) ,   r e m p l a c e m e n t   d u   b o u t o n   ' C o n f i g u r e r   l e s   o b j e c t i f s '   p a r   ' C o n s u l t e r   l e s   d ÃƒÂ© t a i l s '   ( a v e c   u n e   i c ÃƒÂ´ n e   d ' Si l )   l o r s q u e   l a   c a m p a g n e   e s t   a c t i v e . 
 
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d e s   d ÃƒÂ© t a i l s   d e   l a   d e m a n d e   d e   r a l l o n g e   ( 
 e v i e w _ e x t e n s i o n )   :   a f f i c h a g e   d u   n o m   d e   l ' e n t r e p r i s e   v i a   u n e   m a p   d e   c l ÃƒÂ© s   e n   c h a ÃƒÂ® n e s   d e   c a r a c t ÃƒÂ¨ r e s   e t   a j o u t   d u   m o n t a n t   t o t a l   d e m a n d ÃƒÂ©   d a n s   l a   s e c t i o n   ' D ÃƒÂ© t a i l s   d e   l a   d e m a n d e ' . 
 
 -   M o d e r n i s a t i o n   c o m p l ÃƒÂ¨ t e   d u   d e s i g n   d e   l a   p a g e   d ' e x a m e n   d e s   r a l l o n g e s   ( 
 e v i e w _ e x t e n s i o n . h t m l )   :   s t y l e   p r e m i u m   a v e c   g l a s s m o r p h i s m   a m ÃƒÂ© l i o r ÃƒÂ© ,   n o u v e l l e s   p a l e t t e s   d e   c o u l e u r s ,   e f f e t s   d e   s u r v o l ,   b a d g e s   m o d e r n i s ÃƒÂ© s   e t   i n t ÃƒÂ© g r a t i o n   d e   n o m b r e u s e s   i c ÃƒÂ´ n e s . 
 
 
- DÃƒÆ’Ã‚Â©placement de la rubrique 'Gestion des ÃƒÆ’Ã¢â‚¬Â°chÃƒÆ’Ã‚Â©anciers' sous la rubrique 'ParamÃƒÆ’Ã‚Â¨tres Financiers' dans le menu de navigation (menu.html).

- TrÃƒÂ©sorerie : Ajout de la configuration des rÃƒÂ©fÃƒÂ©rences de paiements dans le brouillard de banque (brouillard_banque.html) avec une interface modale calquÃƒÂ©e sur le fonctionnement du brouillard de caisse.

- TrÃƒÂ©sorerie : Correction d'un problÃƒÂ¨me empÃƒÂªchant la modification de la rÃƒÂ©fÃƒÂ©rence de paiement dans le brouillard de banque (ajout des champs item_id et model_type dans l'API json).

- Correction de l'affichage du montant total demandÃƒÂ© dans la page de rÃƒÂ©vision des rallonges budgÃƒÂ©taires (associe_app).

- TrÃƒÂ©sorerie : Retrait des dÃƒÂ©corateurs de permission (@module_permission_required) sur les actions de suppression et modification des ÃƒÂ©chÃƒÂ©anciers configurÃƒÂ©s (ApiDeleteEcheancier, ApiBulkDeleteEcheanciers, ApiUpdateEcheancier).

- TrÃƒÂ©sorerie : Restauration des dÃƒÂ©corateurs de permission (@module_permission_required) sur les actions de suppression et modification des ÃƒÂ©chÃƒÂ©anciers configurÃƒÂ©s suite ÃƒÂ  une erreur (ApiDeleteEcheancier, ApiBulkDeleteEcheanciers, ApiUpdateEcheancier).


### [Fixed] - 2026-06-06
- **TrÃƒÂ©sorerie** : Correction du bug oÃƒÂ¹ l'application d'une remise ne mettait pas ÃƒÂ  jour les montants des ÃƒÂ©chÃƒÂ©ances dans la base de donnÃƒÂ©es (DuePaiements) si l'inscription ÃƒÂ©tait dÃƒÂ©jÃƒÂ  confirmÃƒÂ©e. ModifiÃƒÂ© ApiApplyRemiseToPaiement dans 	_tresorerie/f_views/preinscrit_paiements.py pour recalculer et mettre ÃƒÂ  jour montant_due et montant_restant des tranches.
- **UI** : Deplacement du sous-menu Paie & Salaires juste en dessous du sous-menu Depenses dans le menu principal Comptabilite/Finance (menu.html).
- **UI** : Remplacement du menu deroulant d'actions par des boutons d'icones dans la liste des fournisseurs (liste_des_fournisseurs.html). Correction egalement des colonnes du filtre de recherche.
- **Backend** : Modification de l'assistant de paie (assistantPaie) pour prendre en compte et filtrer par entite_legal. Le dropdown 'entreprise' a ete ajoute a l'interface (assistant_paie.html).
- **Finance** : Mise ÃƒÂ  jour de la liste des paies (liste_paie_finance) pour grouper et afficher l'entitÃƒÂ© (entreprise) associÃƒÂ©e ÃƒÂ  chaque fiche de paie. L'opÃƒÂ©ration de paiement (lancer_depense_paie) a ÃƒÂ©galement ÃƒÂ©tÃƒÂ© ajustÃƒÂ©e pour crÃƒÂ©er des dÃƒÂ©penses distinctes par entitÃƒÂ©.
- **Finance** : Ajout d'une balise titre (title) sur la page des listes de paie Finance (liste_paie_finance.html). Ajout d'un formulaire de filtres complets (mois, annee, entreprise, statut de paiement) dans l'interface et gestion de ces filtres depuis la vue (views_paie.py).
- **Finance / Interface** : DÃƒÂ©placement du formulaire des filtres de la liste des paies (liste_paie_finance.html) juste au-dessus du tableau des donnÃƒÂ©es, pour une meilleure clartÃƒÂ© visuelle et ergonomie.
- **RH / Finance** : VÃƒÂ©rification complÃƒÂ¨te du traitement de la paie par entitÃƒÂ©. La notification envoyÃƒÂ©e par ApiValiderPaieMois inclut dÃƒÂ©sormais le nom de l'entitÃƒÂ© si celle-ci a ÃƒÂ©tÃƒÂ© spÃƒÂ©cifiÃƒÂ©e lors de la validation.
- **TrÃƒÂ©sorerie / Banque** : Ajout d'un tableau de bord affichant la situation de l'imputation bancaire (total opÃƒÂ©rations, rapprochÃƒÂ©es, en attente) et la situation de recouvrement des chÃƒÂ¨ques/virements sur la page du brouillard de banque. Ajout de raccourcis rapides vers les pages concernÃƒÂ©es.
- **RH / Formateurs** : Modernisation de l'interface des contrats (intÃƒÂ©gration de DataTables pour la recherche/pagination, dÃƒÂ©placement du filtre d'entitÃƒÂ©, ajout d'actions rapides inline pour un workflow plus fluide).
- **RH / Formateurs** : Harmonisation du design de la modal de crÃƒÂ©ation/ÃƒÂ©dition de contrat pour un aspect plus premium (espacement, fonds teintÃƒÂ©s, bords arrondis, et icÃƒÂ´nes).
- **RH / Formateurs** : Correction du design et de l'alignement des filtres DataTables (Affichage et Recherche) dans la liste des contrats.
- **RH / Formateurs** : Refonte totale de la disposition des filtres pour la liste des contrats. Les filtres (EntitÃƒÂ©, Recherche, Pagination) sont dÃƒÂ©sormais placÃƒÂ©s dans une carte dÃƒÂ©diÃƒÂ©e au-dessus du tableau (Filter Section), harmonisÃƒÂ©e avec la vue fiches-mensuelles.
-   H a r m o n i s a t i o n   d e s   i c ÃƒÂ´ n e s   d e   l ' E s p a c e   e m p l o y ÃƒÂ©   a v e c   l ' E s p a c e   f o r m a t e u r   ( u t i l i s a t i o n   d e   B o x i c o n s   a u   l i e u   d e   R e m i x   I c o n s   d a n s   l e   m e n u   R H ) . 
 
 -   S u p p r e s s i o n   d e s   c e r c l e s   d e   c o u l e u r   a u t o u r   d e s   i c ÃƒÂ´ n e s   d e s   s o u s - m e n u s   d e   l ' E s p a c e   e m p l o y ÃƒÂ©   p o u r   c o r r e s p o n d r e   a u   s t y l e   s i m p l e   d e   l ' E s p a c e   f o r m a t e u r . 
 
 -   A j o u t   d e s   d ÃƒÂ© c o r a t e u r s   d e   p e r m i s s i o n s   m a n q u a n t s   ( @ m o d u l e _ p e r m i s s i o n _ r e q u i r e d   e t   @ r o l e _ r e q u i r e d )   s u r   l e s   v u e s   b u d g e t _ c a m p a i g n _ d i s p a t c h ,   r e q u e s t _ e x t e n s i o n   e t   b u d g e t _ c a m p a i g n _ r e a l i z a t i o n . 
 
 -   S u p p r e s s i o n   d e   l ' o n g l e t   F o r m a t i o n s   d a n s   l a   p a g e   / c o n s e i l / l i s t e - d e s - t h e m a t i q u e s / 
 
 -   A j o u t   d ' u n e   m o d a l e   p o u r   c o n f i g u r e r   e t   a j o u t e r   r a p i d e m e n t   d e s   p a r t i c i p a n t s   d e p u i s   l a   v u e   d e   c r ÃƒÂ© a t i o n   d ' u n   n o u v e a u   g r o u p e   c o n s e i l . 
 
 -   M o d e r n i s a t i o n   d u   d e s i g n   d e   l a   m o d a l e   d ' a j o u t   r a p i d e   d ' u n   p a r t i c i p a n t   ( l a b e l s   f l o t t a n t s ,   d ÃƒÂ© g r a d ÃƒÂ© s ,   i c ÃƒÂ´ n e s ,   g l a s s m o r p h i s m ) . 
 
 -   S u p p r e s s i o n   d e s   d ÃƒÂ© g r a d ÃƒÂ© s   d a n s   l a   m o d a l e   d ' a j o u t   r a p i d e   d e   p a r t i c i p a n t   p o u r   l ' h a r m o n i s e r   a v e c   l e   d e s i g n   g l o b a l   d u   p r o j e t   ( u t i l i s a t i o n   d e s   c l a s s e s   b g - p r i m a r y   e t   t e x t - p r i m a r y   s t a n d a r d ) . 
 
 -   A j o u t   d e s   d ÃƒÂ© c o r a t e u r s   @ m o d u l e _ p e r m i s s i o n _ r e q u i r e d   m a n q u a n t s   s u r   l ' e n s e m b l e   d e s   v u e s   e t   A P I s   d u   m o d u l e   C o n s e i l   ( t _ c o n s e i l )   p o u r   s ÃƒÂ© c u r i s e r   l ' a c c ÃƒÂ¨ s   a u x   p a g e s   e t   a u x   a c t i o n s . 
 
 -   A j o u t   d e   l a   s u p p r e s s i o n   e n   c a s c a d e   d e s   f a c t u r e s   d e   c o n s e i l   ( m ÃƒÂª m e   c e l l e s   v a l i d ÃƒÂ© e s ) ,   e n   s u p p r i m a n t   l e s   p a i e m e n t s ,   l e t t r a g e s   b a n c a i r e s   e t   r e m b o u r s e m e n t s   l i ÃƒÂ© s ,   t o u t   e n   p r ÃƒÂ© s e r v a n t   l e   d e v i s   s o u r c e . 
 
 -   R ÃƒÂ© i n i t i a l i s a t i o n   d e   l ' ÃƒÂ© t a t   d u   c l i e n t   d a n s   l e   p i p e l i n e   ( r e t o u r   ÃƒÂ    ' d e v i s _ e n v o y e '   o u   ' n e g o c i a t i o n ' )   l o r s   d e   l a   s u p p r e s s i o n   d ' u n e   f a c t u r e   d e   c o n s e i l . 
 
 -   S u p p r e s s i o n   d e   l a   c o n f i g u r a t i o n   d e s   d r o i t s   d e   t i m b r e   d a n s   l e   m o d u l e   C o n s e i l .   L a   g e s t i o n   e t   l e   c a l c u l   d e s   d r o i t s   d e   t i m b r e   s ' e f f e c t u e n t   d ÃƒÂ© s o r m a i s   d e   m a n i ÃƒÂ¨ r e   c e n t r a l i s ÃƒÂ© e   v i a   l e s   p a r a m ÃƒÂ¨ t r e s   f i n a n c i e r s   d e   l a   T r ÃƒÂ© s o r e r i e . 
 
 -   I s o l a t i o n   d e   l a   c o n f i g u r a t i o n   d e s   T a x e s   &   F i s c a l i t ÃƒÂ©   d a n s   l e   m o d u l e   C o n s e i l   :   l a   s ÃƒÂ© l e c t i o n   d e   l ' e n t r e p r i s e   n ' i m p a c t e   p l u s   q u e   l e s   o n g l e t s   D o c u m e n t s ,   O f f r e s   R e m i s e s   e t   M e n t i o n s   L ÃƒÂ© g a l e s .   L a   T V A   e s t   g ÃƒÂ© r ÃƒÂ© e   d e   m a n i ÃƒÂ¨ r e   g l o b a l e . 
 
 -   A m ÃƒÂ© l i o r a t i o n   d e   l ' e x p ÃƒÂ© r i e n c e   u t i l i s a t e u r   d a n s   l a   c r ÃƒÂ© a t i o n   d e   d e v i s   ( c o n s e i l / n o u v e a u - d e v i s / )   :   l e   c h a m p   d e   s ÃƒÂ© l e c t i o n   d u   c l i e n t   e s t   d ÃƒÂ© s o r m a i s   f i l t r a b l e   v i a   S e l e c t 2 . 
 
 -   C o r r e c t i o n   d e   l ' e n c o d a g e   d e s   m e s s a g e s   ( A l e r t i f y   e t   D j a n g o   M e s s a g e s )   d a n s   l ' e n s e m b l e   d u   m o d u l e   C o n s e i l . 
 
 -   L e   c h a m p   d e   s ÃƒÂ© l e c t i o n   d e   l a   t h ÃƒÂ© m a t i q u e   d a n s   l a   c o n f i g u r a t i o n   d ' u n   d e v i s   e s t   d ÃƒÂ© s o r m a i s   f i l t r a b l e   v i a   S e l e c t 2 . 
 
 -   B l o c a g e   d e   l ' a c c ÃƒÂ¨ s   a u x   d ÃƒÂ© t a i l s   d ' u n   d e v i s   t a n t   q u ' i l   n ' e s t   p a s   v a l i d ÃƒÂ©   ( b o u t o n   d ÃƒÂ© s a c t i v ÃƒÂ©   d a n s   l a   l i s t e   e t   r e d i r e c t i o n   s e r v e u r   s ÃƒÂ© c u r i s ÃƒÂ© e ) . 
 
 -   A u t o - r e m p l i s s a g e   d e s   c o n d i t i o n s   c o m m e r c i a l e s   :   l o r s   d e   l a   c r ÃƒÂ© a t i o n   d ' u n   d e v i s   o u   d ' u n e   f a c t u r e ,   l e s   c o n d i t i o n s   c o m m e r c i a l e s   p a r   d ÃƒÂ© f a u t   d ÃƒÂ© f i n i e s   d a n s   l a   c o n f i g u r a t i o n   g l o b a l e   s ' a p p l i q u e n t   d ÃƒÂ© s o r m a i s   a u t o m a t i q u e m e n t . 
 
 -   M o d e r n i s a t i o n   d u   d e s i g n   d e s   l i g n e s   d e   d e v i s   ( i c ÃƒÂ´ n e s ,   b a d g e s ,   b o u t o n s   a r r o n d i s )   d a n s   l e   f o r m u l a i r e   d e   c o n f i g u r a t i o n . 
 
 -   L e   c h a m p   d e   s ÃƒÂ© l e c t i o n   d u   c l i e n t / p r o s p e c t   d a n s   l a   c r ÃƒÂ© a t i o n   d ' u n e   n o u v e l l e   f a c t u r e   e s t   d ÃƒÂ© s o r m a i s   f i l t r a b l e   v i a   S e l e c t 2 . 
 
 -   B l o c a g e   d e   l ' a c c ÃƒÂ¨ s   a u x   d ÃƒÂ© t a i l s   d ' u n e   f a c t u r e   t a n t   q u ' e l l e   n ' e s t   p a s   v a l i d ÃƒÂ© e   ( b o u t o n   d ÃƒÂ© s a c t i v ÃƒÂ©   d a n s   l a   l i s t e   e t   r e d i r e c t i o n   s e r v e u r   s ÃƒÂ© c u r i s ÃƒÂ© e ,   c o m m e   p o u r   l e s   d e v i s ) . 
 
 -   B l o c a g e   d e   l ' a c c ÃƒÂ¨ s   ÃƒÂ    l a   g ÃƒÂ© n ÃƒÂ© r a t i o n   d u   P D F   p o u r   l e s   f a c t u r e s   n o n   v a l i d ÃƒÂ© e s   ( b o u t o n   d ÃƒÂ© s a c t i v ÃƒÂ©   e t   r o u t e   s ÃƒÂ© c u r i s ÃƒÂ© e ) . 
 
 -   A j u s t e m e n t   d u   d e s i g n   d e   l a   c o n f i g u r a t i o n   d e   f a c t u r e   :   r e p o s i t i o n n e m e n t   p r o p r e   d u   b a d g e   d e   s t a t u t   ( B r o u i l l o n )   d a n s   l e   c o i n   s u p ÃƒÂ© r i e u r   d r o i t   e t   r ÃƒÂ© o r g a n i s a t i o n   d u   c h a m p   ' M o d e   d e   p a i e m e n t   a t t e n d u '   a u - d e s s u s   d e s   c o n d i t i o n s . 
 
 -   R e p o s i t i o n n e m e n t   d u   b a d g e   d e   s t a t u t   ( B r o u i l l o n )   :   d ÃƒÂ© p l a c ÃƒÂ©   ÃƒÂ    c ÃƒÂ´ t ÃƒÂ©   d u   t i t r e   p r i n c i p a l   p o u r   ÃƒÂ© v i t e r   t o u t   c h e v a u c h e m e n t   a v e c   l e   c o n t e n u   d u   d o c u m e n t . 
 
 -   I n t ÃƒÂ© g r a t i o n   d e   S e l e c t 2   d a n s   l a   c o n f i g u r a t i o n   d e s   f a c t u r e s   ( c o n s e i l / c o n f i g u r e - f a c t u r e . h t m l )   p o u r   r e n d r e   l a   s ÃƒÂ© l e c t i o n   d e   l a   t h ÃƒÂ© m a t i q u e   f i l t r a b l e   a v e c   b a r r e   d e   r e c h e r c h e   i n t ÃƒÂ© g r ÃƒÂ© e . 
 
 -   C o r r e c t i o n   d u   d e s i g n   d u   c h a m p   T h ÃƒÂ© m a t i q u e   ( S e l e c t 2 )   p o u r   q u ' i l   a d o p t e   l e   m ÃƒÂª m e   s t y l e   v i s u e l   q u e   l e s   a u t r e s   i n p u t s   ( f o r m - c o n t r o l - c u s t o m ) . 
 
 -   H a r m o n i s a t i o n   d u   d e s i g n   d e s   l i g n e s   d e   f a c t u r a t i o n   p o u r   c o r r e s p o n d r e   e x a c t e m e n t   ÃƒÂ    c e l u i   d e s   d e v i s   ( a j o u t   d ' a v a t a r s   p o u r   l e s   d ÃƒÂ© s i g n a t i o n s ,   s t y l e   d e s   b a d g e s   p o u r   q u a n t i t ÃƒÂ© s / r e m i s e s ,   e t   b o u t o n s   d ' a c t i o n s   a r r o n d i s ) . 
 
 -   A j u s t e m e n t   C S S   d e   S e l e c t 2   ( T h ÃƒÂ© m a t i q u e )   :   f o r ÃƒÂ§ a g e   d e   l a   l a r g e u r   ÃƒÂ    1 0 0 % ,   a j o u t   d u   m a r g i n - b o t t o m   m a n q u a n t   e t   a l i g n e m e n t   f l e x   p o u r   m a t c h e r   p a r f a i t e m e n t   l e s   d i m e n s i o n s   d e s   a u t r e s   c h a m p s   d u   f o r m u l a i r e . 
 
 -   C o r r e c t i o n   d u   d ÃƒÂ© b o r d e m e n t   d e   t e x t e   d a n s   l e   c h a m p   T h ÃƒÂ© m a t i q u e   S e l e c t 2   l o r s   d e   l a   s ÃƒÂ© l e c t i o n   :   r e m p l a c e m e n t   d u   d i s p l a y :   f l e x   p a r   u n   p o s i t i o n n e m e n t   a b s o l u   p o u r   l e   b o u t o n   d e   s u p p r e s s i o n   ( x )   e t   l a   f l ÃƒÂ¨ c h e ,   a v e c   u n   t e x t - o v e r f l o w   ( p o i n t s   d e   s u s p e n s i o n )   p o u r   l e s   t e x t e s   t r o p   l o n g s . 
 
 -   N o u v e l l e   c o r r e c t i o n   S e l e c t 2   :   R e t o u r   ÃƒÂ    l a   m ÃƒÂ© t h o d e   n a t i v e   d e   S e l e c t 2   ( v i a   l i n e - h e i g h t )   s a n s   f o r c e r   l e   f l e x   o u   l e   p o s i t i o n n e m e n t   a b s o l u ,   c e   q u i   r ÃƒÂ¨ g l e   d ÃƒÂ© f i n i t i v e m e n t   l e   b u g   v i s u e l   d u   b o u t o n   d e   s u p p r e s s i o n   ' x '   e t   l e   c h e v a u c h e m e n t   d u   t e x t e . 
 
 -   A j o u t   d ' u n   e s p a c e m e n t   ( m a r g i n - b o t t o m )   e n t r e   l e   c h a m p   S e l e c t 2   d e   T h ÃƒÂ© m a t i q u e   e t   l e   c h a m p   D ÃƒÂ© s i g n a t i o n . 
 
 -   R e f o n t e   t o t a l e   d e   l a   z o n e   d ' a j o u t   d e   l i g n e   d e   f a c t u r a t i o n   :   i n t ÃƒÂ© g r a t i o n   d i r e c t e   d a n s   l e   t a b l e a u   e n   < t f o o t > ,   r e m p l a c e m e n t   d e s   d i v   p a r   u n   F l e x b o x   g a p - 2   p o u r   u n   e s p a c e m e n t   i n f a i l l i b l e   e t   a l i g n e m e n t   p a r f a i t   a v e c   l e   d e s i g n   d e s   d e v i s . 
 
 -   C o r r e c t i o n   d u   c e n t r a g e   v e r t i c a l   d u   t e x t e   d a n s   S e l e c t 2   :   s u p p r e s s i o n   d e s   m a r g e s   e t   p a d d i n g s   p a r   d ÃƒÂ© f a u t   q u i   d ÃƒÂ© c a l a i e n t   l e   t e x t e   v e r s   l e   b a s   a v e c   l a   h a u t e u r   d ÃƒÂ© f i n i e . 
 
 -   H a r m o n i s a t i o n   d e   l a   t a i l l e   d u   c h a m p   S e l e c t 2   ( T h ÃƒÂ© m a t i q u e )   p o u r   c o r r e s p o n d r e   e x a c t e m e n t   ÃƒÂ    l a   h a u t e u r   e t   l a   t a i l l e   d e   p o l i c e   ( 1 2 p x )   d e s   c h a m p s   D ÃƒÂ© s i g n a t i o n   e t   D e s c r i p t i o n . 
 
 -   R e f o n t e   g l o b a l e   d e   l a   p a g e   C o n f i g u r a t i o n   F a c t u r e   p o u r   a d o p t e r   l e   d e s i g n   P r e m i u m   ( h a r m o n i s ÃƒÂ©   a v e c   l e   d e v i s )   :   s u p p r e s s i o n   d u   C S S   f a i t   m a i s o n   e t   a d o p t i o n   d e   c a r d - p r e m i u m ,   t a b l e - p r e m i u m ,   e t   d u   C S S   S e l e c t 2   o f f i c i e l   q u i   c o r r i g e   d ÃƒÂ© f i n i t i v e m e n t   l e   b u g   d e   l a   c r o i x . 
 
 
- **Refonte Workflow Conseil de Validation** : Modification du modÃ¨le ConseilValidation (ajout de statut 'ouvert'/'cloture'). Refonte de la page stage/council/ avec blocage de l'affichage des stages et des dÃ©cisions rapides si aucun conseil n'est actif. ImplÃ©mentation du design Premium (Glassmorphism) pour cette interface.

- **Design** : Harmonisation des interfaces d'Examens Finaux (Liste des groupes, Saisie des notes, Bulletins) avec le design Premium (Glassmorphism, bords arrondis) utilisÃ© sur la page Conseil de Validation.

- **Design** : Alignement de la CSS des tableaux et badges de council.html, list_groupes.html, saisie_notes.html, et bulletins.html avec la charte graphique de list_stages.html (Premium Look & Feel).

- **Bugfix** : Correction de l'erreur AttributeError ('str' object has no attribute 'strftime') lors de la crÃ©ation d'un Conseil de Validation. Le modÃ¨le gÃ¨re dÃ©sormais les dates transmises sous forme de chaÃ®ne de caractÃ¨res lors de l'enregistrement.

- **Conseil de Validation** : Modification de la vue et du template pour enregistrer et afficher les dÃ©cisions dÃ©jÃ  prises pour les stages lors d'un conseil (avec update_or_create pour Ã©viter les doublons).

- **Conseil de Validation** : Ajout de la sÃ©lection des stages et groupes focus Ã©valuÃ©s lors de la crÃ©ation d'un conseil. Mise Ã  jour du modÃ¨le ConseilValidation (ManyToMany) et ajout des Select2 dans la modale.

- **Conseil de Validation** : Modification de la modale de crÃ©ation pour rendre la sÃ©lection des stages et groupes focus mutuellement exclusive via des boutons radio et du JavaScript.

- **Design** : Harmonisation de l'affichage des tableaux dans council.html avec le style premium de list_stages.html (avatars, barre de progression arrondie, espacements et boutons d'action).

- **Design (Refonte Totale)** : Remplacement des tableaux de la page Conseil par un espace de travail Kanban interactif. IntÃ©gration d'un panneau latÃ©ral (Offcanvas) pour la saisie des dÃ©cisions afin de ne pas perdre le contexte visuel du board Kanban.
- 
 
 M i s e 
 
 a 
 
 j o u r 
 
 d e 
 
 l a 
 
 v u e 
 
 P r i n t F a c t u r e C o n s e i l 
 
 e t 
 
 d u 
 
 t e m p l a t e 
 
 d o l i b a r e _ f a c t u r e 
 
 p o u r 
 
 i n c l u r e 
 
 l e 
 
 d r o i t 
 
 d e 
 
 t i m b r e 
 
 e t 
 
 l e 
 
 m o d e 
 
 d e 
 
 p a i e m e n t . 
 
 - Ajout de la possibilité de définir un compte bancaire par défaut dans la configuration de conseil, et affichage de ses coordonnées (Nom et IBAN) sur la facture dolibare.

 # #   [ 2 0 2 6 - 0 6 - 1 0 ]   A j o u t   d e   l a   f l e x i b i l i t e   D e v i s / F a c t u r e   p o u r   l a   c r e a t i o n   d e   G r o u p e s   ( E x e c u t i v e   E d u c a t i o n ) 
 -   M o d e l e   G r o u p e C o n s e i l   :   C l e   e t r a n g e r e   d e v i s   r e n d u e   o p t i o n n e l l e   e t   a j o u t   d e   f a c t u r e . 
 -   V u e s   A p i G e t C l i e n t D e v i s ,   A p i G e t D e v i s D e t a i l s   e t   A p i S a v e C o n s e i l G r o u p e   m i s e s   a   j o u r   p o u r   s u p p o r t e r   l e s   I D s   p r e f i x e s . 
 -   T e m p l a t e   n o u v e a u _ g r o u p e _ c o n s e i l . h t m l   a j u s t e   p o u r   e n v o y e r   l e s   b o n s   i d e n t i f i a n t s . 
 -   A p i S a v e P a r t i c i p a n t   e t   g e n e r a t i o n   d e s   f e u i l l e s   d ' e m a r g e m e n t   P D F   a d a p t e e s . 
 
 
 -   A j o u t   d ' u n e   v a l i d a t i o n   f r o n t e n d   p o u r   s ' a s s u r e r   q u e   l a   d a t e   d e   d e b u t   d u   g r o u p e   n ' e s t   p a s   s u p e r i e u r e   a   l a   d a t e   d e   f i n   l o r s   d e   s a   c r e a t i o n . 
 
 
 -   A j o u t   d e   l ' o p t i o n   ' P a s s e r   p o u r   l e   m o m e n t '   a   l ' e t a p e   d e   s e l e c t i o n   d e s   p a r t i c i p a n t s   l o r s   d e   l a   c r e a t i o n   d ' u n   g r o u p e ,   p e r m e t t a n t   d e   c o n f i g u r e r   l e s   p a r t i c i p a n t s   p l u s   t a r d . 
 
 
 -   C o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   d a n s   l e   m e n u   o u   l a   s e c t i o n   ' C o m p t a b i l i t e / F i n a n c e   \ >   F a c t u r e s   e m i s e s '   d e v e n a i t   a c t i v e   p a r   e r r e u r   l o r s   d e   l a   c o n s u l t a t i o n   d ' u n e   f a c t u r e   d u   m o d u l e   C o n s e i l .   ( R e n o m m a g e   d e   l ' u r l   d e   t r e s o r e r i e   p o u r   e v i t e r   l e s   c o r r e s p o n d a n c e s   p a r t i e l l e s ) . 
 
 
 -   R e n o m m a g e   f i n a l   d e   l a   v u e   d e   f a c t u r a t i o n   t r e s o r e r i e   e n   T r e s o r e r i e V i e w F a c t u r e   p o u r   e v i t e r   t o u t   c h e v a u c h e m e n t   d e   s o u s - c h a i n e   a v e c   D e t a i l s F a c t u r e . 
 
 
 -   C o r r e c t i o n   d ' u n   p r o b l e m e   o u   l e   p r i x   u n i t a i r e   n ' e t a i t   p a s   e n r e g i s t r e   l o r s   d e   l a   c r e a t i o n   d e s   l i g n e s   d e   f a c t u r e .   U n   s c r i p t   a   e g a l e m e n t   e t e   l a n c e   p o u r   r e c a l c u l e r   e t   m e t t r e   a   j o u r   l e   p r i x   u n i t a i r e   d e s   f a c t u r e s   e x i s t a n t e s . 
 
 
- Ajout de la gestion des Consultants pour le module Executive Education (Conseil). CRUD complet et intÃ©gration au Wizard de crÃ©ation de groupes conseil.

- Deplacement du menu Consultants sous Groupes et Sessions et harmonisation du header de la page.

- Correction du comportement de la modale de modification/suppression des consultants (dÃ©placement des divs hors de la balise table pour Ã©viter les bugs Bootstrap de backdrop).

- IntÃ©gration de Select2 dans la phase 4 du Wizard de crÃ©ation de groupes conseil pour rendre la sÃ©lection des intervenants filtrable (recherchable).

- Correction de l'erreur NoReverseMatch sur la page des dÃ©tails du groupe lorsque le groupe est rattachÃ© uniquement Ã  une facture (sans devis).

- Ajout de la possibilitÃ© de crÃ©er un groupe conseil Ã  partir d'un devis Ã  l'Ã©tat 'envoyÃ©' (en plus de l'Ã©tat 'acceptÃ©').

- Ajout d'un avertissement lors de la conversion d'un devis en facture pour rappeler Ã  l'utilisateur si les informations lÃ©gales de l'entreprise (RC, NIF, NIS, NÂ° ART) sont manquantes.

- Harmonisation du design de la fenÃªtre modale de saisie d'un paiement sur la page des dÃ©tails de la facture (look premium et alignement avec le reste de l'UI).

- Ajout d'un CSS personnalisÃ© (@page { margin: 0.5cm; }) pour les modÃ¨les de factures et devis gÃ©nÃ©rÃ©s par l'Ã©diteur de documents.


### 2026-06-10
- **TrÃ©sorerie/Configuration**: Ajout de la configuration du format de numÃ©rotation des quittances (prÃ©fixe et suffixe) au niveau des entitÃ©s (Entreprise). Le modÃ¨le Paiements formatte dÃ©sormais automatiquement le numÃ©ro selon cette configuration de l'entitÃ©.
- **TrÃ©sorerie/Configuration**: DÃ©placement de la configuration de la numÃ©rotation des quittances vers la page de configuration de paiement/facturation (config_paiement_facturation.html). Ajout de la vue ApiUpdateQuittanceFormat.
- **TrÃ©sorerie/Configuration**: Modification du systÃ¨me de configuration de numÃ©rotation des quittances pour utiliser un format complet avec tag {seq}. Ajout de la longueur configurable de sÃ©quence.
- **UI/UX TrÃ©sorerie**: Refonte complÃ¨te du design de la page de configuration de paiement/facturation en utilisant une navigation par onglets verticaux (Premium Look & Feel).
- Normalisation des icÃ´nes dans menu.html (public et tenant) : utilisation exclusive de boxicons (x-*) et suppression des couleurs (	ext-*) sur les icÃ´nes.

- Nettoyage supplmentaire : suppression des couleurs de fond (g-*) appliques aux conteneurs d'icnes (.submenu-icon) dans les menus, en particulier dans la section RH / Espace Employ.

- Correction : Ajout de rgles CSS spcifiques dans menu.html pour forcer les icnes (.bx) et les arrire-plans .submenu-icon  prendre une couleur neutre (gris #6a7187 et #f3f6f9) afin d'craser le bleu par dfaut du thme.

- Correction (Bug) : Rparation de l'erreur de syntaxe de template Django caus par la modification prcdente (les apostrophes de fin pour les conditions url_name in avaient t accidentellement remplaces par des guillemets).

 
 - **TrÃ©sorerie/DÃ©penses** : Transformation du systÃ¨me d'enregistrement des dÃ©penses pour supporter un format multi-lignes. Ajout d'une gestion dynamique des taux de TVA par article (0%, 9%, 19%) et calcul automatique du Droit de Timbre (1% du TTC, min 5 DA, max 2500 DA) pour les paiements en espÃ¨ces. Refonte complÃ¨te de la page de crÃ©ation (
ouvelle_depense.html) et des vues de l'API.
- **TrÃ©sorerie/DÃ©penses** : Suppression du champ 'CatÃ©gorie' global de la dÃ©pense. Les catÃ©gories sont dÃ©sormais affectÃ©es uniquement au niveau de chaque ligne d'article.
- **TrÃ©sorerie/DÃ©penses** : Correction de l'erreur 500 sur ApiListeDepenses due Ã  la rÃ©fÃ©rence rÃ©siduelle Ã  \category__name\ aprÃ¨s la suppression du champ.
- **TrÃ©sorerie/DÃ©penses** : Ã‰largissement du formulaire de crÃ©ation de dÃ©pense pour utiliser toute la largeur de l'Ã©cran (\col-12\).
- **TrÃ©sorerie/DÃ©penses** : Ajout de la fonctionnalitÃ© de filtrage (recherche) sur le champ CatÃ©gorie pour chaque ligne de dÃ©pense grÃ¢ce Ã  Select2.
- **TrÃ©sorerie/DÃ©penses** : Ajout du champ \
eference_document\ pour permettre de saisir la rÃ©fÃ©rence du document d'achat (ex: NÂ° Facture, BL) en plus de la piÃ¨ce justificative. Le champ a Ã©tÃ© intÃ©grÃ© dans la crÃ©ation, modification et affichage des dÃ©tails.
- **TrÃ©sorerie/DÃ©penses** : Suppression temporaire de la section \Paiement & DÃ©tails\ du formulaire de crÃ©ation de dÃ©pense, car la gestion des paiements sera traitÃ©e sÃ©parÃ©ment dans une Ã©tape ultÃ©rieure.
- **TrÃ©sorerie/DÃ©penses** : Remplacement de la fenÃªtre modale par une page complÃ¨te (\/comptabilite/tresorerie/depenses/details/\) pour la consultation des dÃ©tails d'une dÃ©pense. Ajout de l'affichage dÃ©taillÃ© de toutes les lignes associÃ©es Ã  la dÃ©pense dans cette nouvelle vue.
- **TrÃ©sorerie/DÃ©penses** : Harmonisation de l'interface de la page \details_depense.html\ pour qu'elle corresponde exactement au design moderne et Ã©purÃ© de \
ouvelle_depense.html\ (carte pleine largeur, en-tÃªte premium, rÃ©sumÃ© financier clair).
- **Menu de Navigation** : Mise Ã  jour du fichier \menu.html\ pour s'assurer que le sous-menu \DÃ©penses\ et le lien \Liste des dÃ©penses\ restent visuellement actifs lors de la consultation de la nouvelle page de dÃ©tails d'une dÃ©pense (\PageDetailDepense\).
- **Fournisseurs** : Harmonisation du design de la page \liste_des_fournisseurs.html\ (en-tÃªte, section KPI, boutons d'action et filtres) pour qu'elle corresponde au style \glass-card\ haut de gamme de la page \ttentes_de_paiements.html\.
- **Fournisseurs** : Harmonisation du design de la page \details_fournisseur.html\ avec la page de dÃ©tails client (style glass-card, banniÃ¨re de profil, KPIs financiers, navigation par onglets).
- **Fournisseurs / DÃ©penses** : Ajout de la rÃ©cupÃ©ration et de l'affichage de l'historique des dÃ©penses liÃ©es au fournisseur dans la page de dÃ©tails (\PageDetailsFournisseur\), incluant le calcul dynamique des KPIs (Total AchetÃ©, Total PayÃ©, Reste Ã  Payer).
- **TrÃ©sorerie** : DÃ©couplage complet de la logique de Remboursements par rapport aux DÃ©penses. Ajout du lien \
emboursement\ dans \OperationsBancaire\. Mise Ã  jour des journaux de caisse (Brouillards EspÃ¨ce et Banque) et de l'imputation bancaire pour traiter nativement les remboursements.
- **TrÃ©sorerie** : DÃ©sactivation et masquage du bouton de demande de remboursement dans les pages de dÃ©tails de demande de paiement (standard et double).
- **TrÃ©sorerie** : Remplacement de l'affectation automatique LIFO par une ventilation manuelle (input modifiable) dans le modal de confirmation de remboursement (details_rembourssement.html).
- **TrÃ©sorerie** : Ã‰largissement de la fenÃªtre modale de confirmation de remboursement (modal-lg vers modal-xl) pour un meilleur affichage de la ventilation manuelle.
- **TrÃ©sorerie** : Nettoyage du template details_rembourssement.html (retrait de la sÃ©lection de la 'CatÃ©gorie de dÃ©pense' et remplacement des mentions 'DÃ©clencher la dÃ©pense' par 'Traiter le remboursement') suite au dÃ©couplage des remboursements et des dÃ©penses.
- **TrÃ©sorerie** : Ajout du champ category au modÃ¨le Rembourssements et restauration de la sÃ©lection du Compte / CatÃ©gorie dans la modale de remboursement, permettant un regroupement analytique des sorties sans crÃ©er de dÃ©pense.
- **TrÃ©sorerie** : Correction d'une erreur fatale (\TypeError: __str__ returned non-string\) sur la page d'exploration de donnÃ©es causÃ©e par les mÃ©thodes \__str__\ des modÃ¨les \Rembourssements\, \SeuilPaiements\ et \PromoRembourssement\ qui retournaient des objets (ForeignKeys) ou des Decimal au lieu de chaÃ®nes de caractÃ¨res.
- **Global** : Correction d'autres erreurs fatales \TypeError\ similaires causÃ©es par la mÃ©thode \__str__\ dans d'autres modÃ¨les de trÃ©sorerie (ex: \ClientPaiementsRequest\, \clientPaiementsRequestLine\, \EcheancierPaiementLine\, \EcheancierPaiementSpecialLine\).
- **Global** : Automatisation de la correction de TOUS les modÃ¨les Django du projet pour qu'aucune mÃ©thode \__str__\ ne retourne un objet ou \None\ lorsqu'elle est appelÃ©e sur un enregistrement vide (notamment avec les champs \get_..._display()\, \label\, \designation\, \
om\, etc.). L'explorateur de donnÃ©es est dÃ©sormais parfaitement stable.
- **TrÃ©sorerie / Remboursements** : Correction du ciblage de la fenÃªtre modale \
efundModal\ lors d'une demande de remboursement pour qu'elle se ferme correctement et que le tableau se rafraÃ®chisse automatiquement via \loadRemboursementsData()\.
- **TrÃ©sorerie / Liste des Remboursements** : DÃ©sactivation de la possibilitÃ© d'effectuer un remboursement tant que celui-ci n'a pas Ã©tÃ© traitÃ© (ApprouvÃ©) dans la section principale des remboursements.
- **TrÃ©sorerie / Liste des Remboursements** : Masquage du bouton 'DÃ©tails' pour les remboursements dont le statut est 'En cours de traitement'.
- **TrÃ©sorerie / Liste des Remboursements** : Ajout du badge 'En attente de traitement' dans la colonne Action lorsque le remboursement est Ã  l'Ã©tat 'enc'.
- **Tableau de Bord / Configuration (SaaS Admin)** : Correction d'une erreur \FieldError: Cannot resolve keyword 'category' into field\ sur la page de configuration, survenue suite Ã  la restructuration des dÃ©penses. Les calculs budgÃ©taires parcourent dÃ©sormais les catÃ©gories associÃ©es aux lignes de chaque dÃ©pense (\DepenseLigne\) plutÃ´t qu'Ã  la dÃ©pense globale.
- **Tableau de Bord Budget** : IntÃ©gration des remboursements (traitÃ©s et catÃ©gorisÃ©s) dans le calcul du suivi de rÃ©alisation budgÃ©taire. Les remboursements partiels ou intÃ©graux apparaissent dÃ©sormais automatiquement en tant que *DÃ©pense* sous leur poste budgÃ©taire correspondant, reflÃ©tant ainsi la sortie d'argent rÃ©elle dans le budget.
- **Tableau de Bord Budget** : Ajustement du calcul du budget : Les remboursements sont dÃ©sormais dÃ©duits directement des recettes (paiements initiaux) au lieu d'Ãªtre comptabilisÃ©s comme dÃ©penses. Cela permet d'afficher la recette nette rÃ©elle sans fausser le solde global par un double comptage.
- **Tableau de Bord Budget** : RÃ©intÃ©gration des remboursements dans la section DÃ©penses du budget. Ainsi, le montant est dÃ©duit de la recette (pour afficher la recette nette) ET apparaÃ®t en tant que dÃ©pense sous la catÃ©gorie choisie, rÃ©pondant Ã  la demande d'affichage spÃ©cifique de l'utilisateur.
- **ComptabilitÃ© / DÃ©penses** : Correction d'une erreur \TypeError: unexpected keyword arguments 'category_id'\ lors de la crÃ©ation d'une nouvelle dÃ©pense, due Ã  un reliquat de l'ancienne structure oÃ¹ la catÃ©gorie Ã©tait liÃ©e Ã  la dÃ©pense globale au lieu de ses lignes.
-   A c t u a l i s a t i o n   d e   l a   p a g e   a p r è s   g é n é r a t i o n   d ' u n e   f a c t u r e   d a n s   l e s   d é t a i l s   d e   p a i e m e n t   ( s t a n d a r d   e t   d o u b l e ) 
 
 -   A j o u t   d e s   r e m b o u r s e m e n t s   e n   e s p è c e s   d a n s   l e   b r o u i l l a r d   d e   c a i s s e 
 
 -   C o r r e c t i o n   d ' u n e   e r r e u r   5 0 0   ( T y p e E r r o r )   l o r s   d u   t r i   c h r o n o l o g i q u e   d e s   m o u v e m e n t s   d e   c a i s s e 
 
 -   F o r m a t a g e   d e   l a   d a t e   d e   r e m b o u r s e m e n t   p o u r   n ' a f f i c h e r   q u e   l a   d a t e   s a n s   l ' h e u r e   d a n s   l e   J S O N 
 
 -   C o r r e c t i o n   d e   l ' e s p a c e m e n t   p o u r   l e   m o d e   d e   p a i e m e n t   e t   l e   s t a t u t   ( D é p e n s e   d é c l e n c h é e )   d a n s   l a   l i s t e   d e s   r e m b o u r s e m e n t s 
 
 -   C o r r e c t i o n   d e s   p r o b l è m e s   d ' e n c o d a g e   s u r   l e   m o d è l e   R e m b o u r s e m e n t s   ( E s p è c e ,   C h è q u e ,   e t c . ) 
 
 -   I m p l é m e n t a t i o n   d e   l a   p r o c é d u r e   l é g a l e   d e   c o n t r e - p a s s a t i o n   ( g é n é r a t i o n   d e   q u i t t a n c e   n é g a t i v e   a u   l i e u   d e   s u p p r e s s i o n )   l o r s   d e   l ' a n n u l a t i o n   d ' u n   c h è q u e   o u   v i r e m e n t   n o n   e n c a i s s é 
 
 -   C o r r e c t i o n   d e   l ' e n c o d a g e   d u   m o d e   d e   p a i e m e n t   e t   d u   c o n t e x t e   p o u r   l e   m o d è l e   P a i e m e n t s 
 
 -   C o r r e c t i o n   d e   l a   f e r m e t u r e   d e   l a   m o d a l e   d e   d e m a n d e   d e   r e m b o u r s e m e n t   ( B o o t s t r a p   5 )   e t   r a f r a î c h i s s e m e n t   d e   l a   l i s t e 
 
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d u   m o n t a n t   a b s o l u   d a n s   l e s   b r o u i l l a r d s   d e   c a i s s e   e t   b a n q u e   p o u r   é v i t e r   l ' a p p a r i t i o n   d u   s i g n e   + - 
 
 -   P r i s e   e n   c o m p t e   d e   l ' a n n u l a t i o n   d ' u n   c h è q u e   n o n   e n c a i s s é   d a n s   l ' i m p u t a t i o n   b a n c a i r e   ( m a s q u a g e   d e   l ' o p é r a t i o n   d ' e n t r é e   e t   n o n   c r é a t i o n   d ' u n e   s o r t i e ) 
 
 -   C o r r e c t i o n   d e   l ' e r r e u r   l o a d R e m b o u r s e m e n t s D a t a   i s   n o t   d e f i n e d   d a n s   l i s t e - d e s - r e m b o u r s s e m e n t . h t m l   e n   r e n d a n t   l a   f o n c t i o n   g l o b a l e . 
 
 -   R a j o u t   d u   m o d e   d e   p a i e m e n t   d a n s   l a   l i s t e   d e s   p a i e m e n t s   d e   l a   f e n ê t r e   d e   v e n t i l a t i o n   d e   r e m b o u r s e m e n t   ( d e t a i l s _ r e m b o u r s s e m e n t . h t m l ) . 
 
 -   T r i   c h r o n o l o g i q u e   i n v e r s é   ( d u   p l u s   r é c e n t   a u   p l u s   a n c i e n )   d e s   o p é r a t i o n s   d e   c a i s s e   ( e t   b a n q u e )   p o u r   c h a q u e   j o u r n é e   a f f i c h é e   d a n s   l e   b r o u i l l a r d . 
 
 -   C o r r e c t i o n   d e   l ' o r d r e   d ' a f f i c h a g e   d a n s   l e   b r o u i l l a r d   :   U t i l i s a t i o n   d u   t i m e s t a m p   ( c r e a t e d _ a t )   p o u r   t r i e r   v é r i t a b l e m e n t   l e s   o p é r a t i o n s   d e   m a n i è r e   c h r o n o l o g i q u e   a v a n t   d e   l e s   i n v e r s e r . 
 
 -   C o r r e c t i o n   d e s   s t a t i s t i q u e s   d u   b r o u i l l a r d   b a n q u e   :   e x c l u s i o n   d e s   p a i e m e n t s   r e m b o u r s é s   ( p a i e m e n t _ _ i s _ r e f u n d = T r u e )   p o u r   r e f l é t e r   c o r r e c t e m e n t   l e   n o m b r e   r é e l   d ' i m p u t a t i o n s   b a n c a i r e s   e n   a t t e n t e . 
 
 -   F e n ê t r e   m o d a l e   d e   r e m b o u r s e m e n t   :   E x c l u s i o n   d e s   p a i e m e n t s   c o r r e s p o n d a n t   a u x   f r a i s   d ' i n s c r i p t i o n   p o u r   é v i t e r   t o u t e   a l l o c a t i o n   a c c i d e n t e l l e   s u r   c e s   m o n t a n t s . 
 
 -   I m p u t a t i o n   B a n c a i r e   :   I n t é g r a t i o n   d e s   o p é r a t i o n s   b a n c a i r e s   d e   t y p e   r e m b o u r s e m e n t   ( s o r t i e s )   d a n s   l a   p a g e   d ' i m p u t a t i o n .   C e s   o p é r a t i o n s   é t a i e n t   a u p a r a v a n t   m a s q u é e s ,   c e   q u i   c r é a i t   u n e   i n c o h é r e n c e   e n t r e   l e s   s t a t i s t i q u e s   d u   b r o u i l l a r d   e t   l a   l i s t e   d e s   o p é r a t i o n s   à   i m p u t e r . 
 
 -   L i s t e   d e s   r e m b o u r s e m e n t s   :   A f f i c h a g e   e x c l u s i f   d e s   m o n t a n t s   e n c a i s s é s   ( e s p è c e s   o u   c h è q u e s / v i r e m e n t s   m a r q u é s   c o m m e   r é g l é s )   d a n s   l e   c a l c u l   d u   t o t a l   p a y é   p o u r   c h a q u e   l i g n e ,   y   c o m p r i s   d a n s   l a   m o d a l e   d e   d e m a n d e   d e   r e m b o u r s e m e n t . 
 
 -   L i s t e   d e s   r e m b o u r s e m e n t s   :   A f f i c h a g e   d u   m o n t a n t   ' E n   a t t e n t e   d ' e n c a i s s e m e n t '   ( c h è q u e s   o u   v i r e m e n t s   n o n   e n c o r e   v a l i d é s )   e n   d e s s o u s   d u   t o t a l   e n c a i s s é ,   à   l a   f o i s   d a n s   l e   t a b l e a u   p r i n c i p a l   e t   d a n s   l a   f e n ê t r e   m o d a l e   d e   r e c h e r c h e . 
 
 -   D é t a i l s   d u   r e m b o u r s e m e n t   &   M o d a l e   d é t a i l s   ( L i s t e )   :   D a n s   l ' o n g l e t   É c h é a n c i e r ,   l a   c o l o n n e   ' M o n t a n t   P a y é '   a   é t é   r e n o m m é e   ' M o n t a n t   E n c a i s s é '   p o u r   n ' a f f i c h e r   q u e   l e s   p a i e m e n t s   v a l i d é s ,   e t   u n e   n o u v e l l e   c o l o n n e   ' E n   A t t e n t e '   a   é t é   a j o u t é e   p o u r   l e s   p a i e m e n t s   n o n   e n c o r e   v a l i d é s . 
 
 -   L i s t e   &   D é t a i l s   d e s   r e m b o u r s e m e n t s   :   M i s e   à   j o u r   d e s   m o d a l e s   d e   ' D e m a n d e   d e   r e m b o u r s e m e n t '   e t   ' T r a i t e m e n t   d e   r e m b o u r s e m e n t '   p o u r   q u ' e l l e s   n ' a f f i c h e n t   e t   n ' a u t o r i s e n t   l e   r e m b o u r s e m e n t   q u e   s u r   l a   b a s e   d u   ' M o n t a n t   e n c a i s s é '   ( e x c l u a n t   l e s   c h è q u e s / v i r e m e n t s   e n   a t t e n t e ) . 
 
 -   M o d a l   d e   D é t a i l s   ( R e m b o u r s e m e n t )   :   L ' o n g l e t   É c h é a n c i e r   a   é t é   s u p p r i m é   e t   s o n   c o n t e n u   a   é t é   i n t é g r é   d i r e c t e m e n t   d a n s   l ' o n g l e t   ' R é s u m é   &   D e m a n d e '   a v e c   u n e   p r é s e n t a t i o n   m o d e r n i s é e . 
 
 -   M o d a l   d e   D é t a i l s   ( R e m b o u r s e m e n t )   :   M o d e r n i s a t i o n   d e   l ' a f f i c h a g e   d e s   s e c t i o n s   ' I n f o r m a t i o n s   É t u d i a n t '   e t   ' D é t a i l s   R e m b o u r s e m e n t '   ( r e m p l a c e m e n t   d e s   c h a m p s   f o r m u l a i r e s   p a r   u n   d e s i g n   s o u s   f o r m e   d e   c a r t e s   é l é g a n t e s ) . 
 
 -   G e s t i o n   d e s   R e m b o u r s e m e n t s   :   P o s s i b i l i t é   d e   t r a i t e r   e t   a c c e p t e r   u n e   d e m a n d e   d e   r e m b o u r s e m e n t   ( c o m m e   u n e   s i m p l e   c o n f i r m a t i o n   d ' a n n u l a t i o n )   m ê m e   s i   l e   m o n t a n t   p a y é   e s t   d e   0   D A   ( p a r   e x e m p l e   s i   s e u l s   l e s   f r a i s   d ' i n s c r i p t i o n   o n t   é t é   r é g l é s ) .   L e   b o u t o n   r e s t e   a c t i f   e t   l e s   c h a m p s   d e   p a i e m e n t   s o n t   m a s q u é s   l o r s   d e   l ' a c c e p t a t i o n . 
 
 -   D é t a i l s   d u   R e m b o u r s e m e n t   ( P a g e   d é d i é e )   :   A j o u t   d e   l a   p o s s i b i l i t é   d e   v a l i d e r   l ' a n n u l a t i o n   ( c o n f i r m a t i o n   d e   r e m b o u r s e m e n t   à   0   D A )   s a n s   o b l i g e r   l ' u t i l i s a t e u r   à   s é l e c t i o n n e r   u n e   e n t i t é ,   u n   c o m p t e   o u   à   f a i r e   u n e   r é p a r t i t i o n   f i n a n c i è r e . 
 
 -   D é t a i l s   d u   R e m b o u r s e m e n t   ( P a g e   d é d i é e )   :   E x c l u s i o n   t o t a l e   d e s   p a i e m e n t s   l i é s   a u x   f r a i s   d ' i n s c r i p t i o n   ( h i s t o r i q u e ,   c a l c u l   d u   t o t a l ,   e t   t a b l e a u   d e   r é p a r t i t i o n )   d e p u i s   l e   b a c k e n d   ( v i e w s ) . 
 
 -   L i s t e   d e s   R e m b o u r s e m e n t s   ( M o d a l e   d e   T r a i t e m e n t )   :   C o r r e c t i o n   d u   c a l c u l   d u   ' M o n t a n t   d é j à   p a y é '   p o u r   e x c l u r e   s y s t é m a t i q u e m e n t   l e s   f r a i s   d ' i n s c r i p t i o n   ( p a r   c o n t e x t e ,   b o o l é e n   e t   l i b e l l é ) .   L e   m o n t a n t   à   0   m a s q u e   d é s o r m a i s   c o r r e c t e m e n t   l e s   c h a m p s   i n u t i l e s   e t   v a l i d e   l ' a n n u l a t i o n   s a n s   e r r e u r . 
 
 -   S e r v e u r   ( A p i S a v e R e f u n d O p e r a t i o n )   :   R é s o l u t i o n   d e   l ' e r r e u r   5 0 0   l o r s   d e   l a   v a l i d a t i o n   d u   r e m b o u r s e m e n t   e n   c o n v e r t i s s a n t   a u t o m a t i q u e m e n t   l e s   m o n t a n t s   c o n t e n a n t   u n e   v i r g u l e   ( e x :   ' 0 , 0 0 ' )   a u   f o r m a t   n u m é r i q u e   c o r r e c t . 
 
 -   S e r v e u r   ( A p i S a v e R e f u n d O p e r a t i o n )   :   A j o u t   d e   l a   s u p p r e s s i o n   a u t o m a t i q u e   d e s   o p é r a t i o n s   b a n c a i r e s   ( c h è q u e s / v i r e m e n t s )   ' e n   a t t e n t e   d e   r e c o u v r e m e n t '   l o r s   d e   l a   v a l i d a t i o n   d ' u n   r e m b o u r s e m e n t   a v e c   a n n u l a t i o n   d ' i n s c r i p t i o n . 
 
 -   R e c o u v r e m e n t   ( L i s t e )   :   A j o u t   d ' u n   b o u t o n   d e   s u p p r e s s i o n   s é c u r i s é   ( v é r i f i c a t i o n   d e   l a   p e r m i s s i o n   ' d e l e t e '   d u   m o d u l e   T r é s o r e r i e )   p e r m e t t a n t   d ' e f f a c e r   e n   c a s   d ' e r r e u r   u n   p a i e m e n t   e n   a t t e n t e ,   a i n s i   q u e   s o n   i m p u t a t i o n   b a n c a i r e   l i é e . 
 
 -   I m p u t a t i o n   B a n c a i r e   :   A f f i c h a g e   d e s   a c t i o n s   s o u s   f o r m e   d ' i c ô n e s   d a n s   l e s   t a b l e a u x   ( E n c a i s s e m e n t   e t   D é c a i s s e m e n t ) .   A j o u t   d u   b o u t o n   d e   s u p p r e s s i o n   ( c o n d i t i o n n é   p a r   l a   p e r m i s s i o n   d e   s u p p r e s s i o n )   p e r m e t t a n t   d ' e f f a c e r   u n e   o p é r a t i o n   e t   s e s   e n t i t é s   a s s o c i é e s   e n   c a s   d ' e r r e u r . 
 
 -   B r o u i l l a r d   d e   B a n q u e / C a i s s e   :   E x c l u   l e s   q u i t t a n c e s   d ' a n n u l a t i o n   ( P a i e m e n t s   a v e c   i s _ r e f u n d = T r u e )   p o u r   c o r r i g e r   l ' a f f i c h a g e   e r r o n é   d ' e n c a i s s e m e n t s   a v e c   s o l d e s   n u l s .   A j o u t é   l a   p r i s e   e n   c h a r g e   d e s   v r a i s   r e m b o u r s e m e n t s   ( C h è q u e / V i r e m e n t )   d a n s   l e   B r o u i l l a r d   d e   B a n q u e   c o m m e   d é c a i s s e m e n t s . 
 
 -   B r o u i l l a r d   d e   B a n q u e / C a i s s e   :   C a s t   d u   c h a m p   u p d a t e d _ a t   ( D a t e   e t   H e u r e )   e n   D a t e   ( Y Y Y Y - M M - D D )   p o u r   l e s   R e m b o u r s e m e n t s   a f i n   d ' é v i t e r   l ' a f f i c h a g e   d e   l ' h e u r e   d a n s   l e s   g r o u p e s   d e   d a t e s   d u   t a b l e a u . 
 
 
- CRM : Ajout du bouton de suppression pour les rÃ©ductions appliquÃ©es (gestion-des-reductions) avec vÃ©rification de la permission de suppression.

- CRM : Correction de l'affichage du bouton de suppression des rÃ©ductions (utilisation de user.is_superuser en plus de request.user.is_superuser).

- CRM : Autorisation de la suppression des rÃ©ductions appliquÃ©es mÃªme aprÃ¨s validation et application.

- CRM : Remplacement de l'alerte navigateur par une modale Bootstrap Ã©lÃ©gante pour la confirmation de suppression d'une rÃ©duction.

- TrÃ©sorerie : Remplissage dynamique des formulaires de modification (Encaissement et DÃ©caissement) dans imputation_bancaire.html pour remplacer les donnÃ©es HTML statiques.

- TrÃ©sorerie : Remplacement du symbole â‚¬ par DA (Dinar AlgÃ©rien) dans imputation_bancaire.html pour s'adapter Ã  la monnaie locale.

- Tresorerie : Ajout du menu et de la page 'Suivi des cheques emis' dans la Banque.
-   A j o u t   d ' u n   f i l t r a g e   p a r   s p é c i a l i t é   ( s t a n d a r d   e t   d o u b l e )   d a n s   l a   p a g e   d e s   p r é i n s c r i t s 
 
 -   R o r g a n i s a t i o n   d e s   f i l t r e s   s u r   l a   p a g e   d e s   p r i n s c r i t s   a v e c   d e s   l a r g e u r s   m a x i m a l e s   p o u r   v i t e r   l e s   r e t o u r s     l a   l i g n e   n o n   d s i r s 
 
 -   A j o u t   d e   S e l e c t 2   s u r   l e   f i l t r e   d e s   s p c i a l i t s   p o u r   l e   r e n d r e   f i l t r a b l e 
 
 -   P e r s o n n a l i s a t i o n   C S S   d u   S e l e c t 2   p o u r   q u ' i l   c o r r e s p o n d e   e x a c t e m e n t   a u   d e s i g n   d e s   a u t r e s   c h a m p s   ' m o d e r n - s e l e c t ' 
 
 -   C o r r e c t i o n   d u   t h m e   S e l e c t 2   p o u r   s ' a s s u r e r   q u e   l e s   s t y l e s   p e r s o n n a l i s s   s ' a p p l i q u e n t   c o r r e c t e m e n t 
 
 -   A j o u t   d u   f i l t r e   d e   s p c i a l i t s   ( s t a n d a r d   &   d o u b l e )   a v e c   d e s i g n   a d a p t   s u r   l a   p a g e   d e s   p r o s p e c t s   ( / c r m / l i s t e - d e s - p r o s p e c t s ) 
 
 -   G é n é r a t i o n   a u t o m a t i q u e   d u   c o d e   d e   s e s s i o n   d ' e x a m e n   ( e n   m o d e   l e c t u r e   s e u l e )   l o r s   d e   l a   c r é a t i o n   d ' u n e   n o u v e l l e   s e s s i o n   d a n s   / e x a m e n s / l i s t e - d e s - s e s s i o n s / 
 
 -   A j o u t   d e   l a   l i a i s o n   e n t r e   ' A u t r e   P r o d u i t '   e t   ' C a t é g o r i e   d e   P a i e m e n t '   a u   l i e u   d e   ' T y p e   d e   P a i e m e n t '   p o u r   l e s   p a i e m e n t s   a u t r e s   d a n s   l a   c o m p t a b i l i t é . 
 
 -   R e n d u   r é c u r s i f   d e   t o u t e s   l e s   c a t é g o r i e s   e t   s o u s - c a t é g o r i e s   d a n s   l e   s e l e c t   ' C a t é g o r i e '   p o u r   l a   c r é a t i o n   d e   n o u v e a u x   p a i e m e n t s   ( N o u v e a u   P a i e m e n t   A u t r e ) . 
 
 -   R e n d u   d u   c h a m p   ' C a t é g o r i e   d e   p r o d u i t '   f i l t r a b l e   a v e c   l ' i n t é g r a t i o n   d e   S e l e c t 2   ( r e c h e r c h e   i n c l u s e )   d a n s   l a   c r é a t i o n   d ' u n   a u t r e   p a i e m e n t . 
 
 -   C o r r e c t i o n   d ' u n e   e r r e u r   d e   s y n t a x e   J a v a s c r i p t   ' U n e x p e c t e d   i d e n t i f i e r   $ '   i n t r o d u i t e   l o r s   d e   l ' i n t é g r a t i o n   d e   S e l e c t 2 . 
 
 -   R e m p l a c e m e n t   d e   l ' i c ô n e   L o r d i c o n   4 0 4   ( h c u x q l p u . j s o n )   m a n q u a n t e   p a r   u n e   U R L   v a l i d e   ( b w t k c f q y . j s o n )   d a n s   l e   h e a d e r . 
 
 -   A j o u t   d e   s t y l e s   C S S   p e r s o n n a l i s é s   p o u r   h a r m o n i s e r   l ' a f f i c h a g e   d e   S e l e c t 2   ( c h a m p   ' C a t é g o r i e   d e   P r o d u i t ' )   a v e c   l e   d e s i g n   d e s   I n p u t - G r o u p   B o o t s t r a p   5   d a n s   ' n o u v e a u _ a u t r e _ p a i e m e n t . h t m l ' . 
 
 -   É l a r g i s s e m e n t   d u   f o r m u l a i r e   d e   c r é a t i o n   d e   ' N o u v e a u   P a i e m e n t   A u t r e '   p o u r   o c c u p e r   t o u t e   l a   l a r g e u r   ( c o l - 1 2   a u   l i e u   d e   c o l - x l - 9 ) . 
 
 
 
 - Ajout de la gestion de multiples contacts pour les prospects entreprise (ModÃ¨le ContactEntreprise, API et Interface)
- Ajout des champs email et tÃ©lÃ©phone pour l'entreprise lors de la crÃ©ation d'un prospect
- Ajout de la possibilitÃ© de modifier la date d'Ã©mission et la date d'Ã©chÃ©ance dans la configuration d'un devis (Conseil)
- Affichage prioritaire du nom de l'entreprise dans la liste des prospects en instance et des clients s'il n'y a pas de nom de contact\n- Suppression de la colonne Prospect et remplacement par Entreprise dans la liste des prospects en instance
- Correction de l'affichage 'Sans Nom' en ajoutant le champ type_prospect dans ApiListeProspect et ApiListeClients\n- Correction de la gÃ©nÃ©ration du slug pour les prospects sans nom et prÃ©nom afin d'Ã©viter l'erreur 404 sur les dÃ©tails
- Restructuration de la page de dÃ©tails d'un prospect (type entreprise) : affichage prioritaire des informations de l'entreprise (avec numÃ©ro et email) suivi de la liste des contacts (principal puis autres)\n- AmÃ©lioration visuelle de l'affichage vide (Empty State) de la liste des contacts pour un prospect entreprise\n- Ajout de la fonctionnalitÃ© de crÃ©ation de contact depuis la fiche entreprise avec son modal dÃ©diÃ© et rechargement dynamique du tableau\n- Correction : Ajout du bouton manquant 'Ajouter Contact' dans l'en-tÃªte de la carte Contacts\n- Ajout de la possibilitÃ© de modifier et supprimer les contacts liÃ©s Ã  une entreprise depuis le tableau des contacts (avec modal d'Ã©dition dÃ©diÃ© et points de terminaison d'API)\n- Refonte de la fiche client (conseil/details-client/) pour y intÃ©grer la gestion des contacts liÃ©s Ã  l'entreprise avec les mÃªmes fonctionnalitÃ©s que la fiche prospect (affichage, ajout, modification, suppression)\n- Correction : RÃ©solution d'une erreur de syntaxe JS (Uncaught SyntaxError) dans details_client.html due Ã  une accolade mal positionnÃ©e lors de l'intÃ©gration de la gestion des contacts\n-   R é d u c t i o n   d e s   m a r g e s   ( m b - 4 ,   m b - 3   v e r s   m b - 2 )   e t   d e s   p a d d i n g s   ( p - 4 ,   p - 3   v e r s   p - 2 )   d a n s   l e s   t e m p l a t e s   C R M   d e t a i l s _ p r o s p e c t . h t m l   e t   d e t a i l s _ p r o s p e c t _ d o u b l e . h t m l 
 
 -   A n n u l a t i o n   d e   l a   r é d u c t i o n   d e s   m a r g e s   e t   d e s   p a d d i n g s   d a n s   d e t a i l s _ p r o s p e c t . h t m l   e t   d e t a i l s _ p r o s p e c t _ d o u b l e . h t m l   ( r e s t a u r a t i o n   à   l ' é t a t   i n i t i a l ) 
 
 -   C o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   d a n s   m e n u . h t m l   :   l e   m e n u   P r o s p e c t s   d e   E x e c u t i v e   E d u c a t i o n   s ' a c t i v a i t   à   t o r t   s u r   l a   p a g e   d é t a i l s - p r o s p e c t   d u   C R M   ( c o n f l i t   d e   s o u s - c h a î n e   e n t r e   D e t a i l s P r o s p e c t   e t   D e t a i l s P r o s p e c t C o n s e i l   r é s o l u ) . 
 
 -   A j o u t   d u   c h a m p   U n i t é   ( J o u r ,   G r o u p e ,   P a r t i c i p a n t ,   H e u r e )   p a r   l i g n e   d a n s   l a   c o n f i g u r a t i o n   d e s   d e v i s   ( m o d è l e s ,   t e m p l a t e   e t   v u e   m i s   à   j o u r ) . 
 
 -   A j o u t   d e   l a   p r o p o s i t i o n   d ' e n r e g i s t r e m e n t   d ' u n e   n o u v e l l e   t h é m a t i q u e   d a n s   l e   d e v i s   l o r s q u ' u n e   d é s i g n a t i o n   p e r s o n n a l i s é e   e s t   s a i s i e   s a n s   s é l e c t i o n   p r é a l a b l e . 
 
 -   C o r r e c t i o n   d e   l ' e r r e u r   N a m e E r r o r :   n a m e   ' m o d u l e _ p e r m i s s i o n '   i s   n o t   d e f i n e d   s u r   l a   v u e   A p i C r e a t e T h e m a t i q u e . 
 
 -   A j o u t   d e   l a   c o l o n n e   U n i t é   d a n s   l a   v u e   d e s   d é t a i l s   d u   d e v i s   ( d e t a i l s _ d e v i s . h t m l ) . 
 
 -   A p p l i c a t i o n   d e s   m ê m e s   m o d i f i c a t i o n s   à   l a   f a c t u r e   ( c o n f i g u r a t i o n   e t   d é t a i l s )   :   A j o u t   d e   l a   c o l o n n e   U n i t é   e t   p r o p o s i t i o n   d ' e n r e g i s t r e m e n t   d e   n o u v e l l e   t h é m a t i q u e . 
 
 -   C o p i e   d e   l ' u n i t é   ( L i g n e s D e v i s   - >   L i g n e s F a c t u r e )   l o r s   d e   l a   t r a n s f o r m a t i o n   d ' u n   d e v i s   e n   f a c t u r e . 
 
 
- Annulation des chèques non encaissés au lieu de suppression lors du remboursement pour garder la trace (Retourné au payeur)

- Ajout de la possibilité de renseigner manuellement la date de remise d'un chèque au payeur (remboursement) depuis l'interface de recouvrement.

- Correction d'un bug où un remboursement partiel (ou de 0 DA) sans annulation d'inscription ne marquait pas les chèques non encaissés comme étant en remboursement.

- Correction du formulaire de recouvrement pour renommer le champ en 'Date de recouvrement' et corriger le comportement : la date d'encaissement est désormais enregistrée dans l'opération bancaire (date_operation) sans écraser la date d'émission originale du chèque (date_paiement), et l'opération est correctement marquée comme encaissée (is_paid=True).

 
 -   A j o u t   d ' u n e   s e c t i o n   e t   d ' u n   t a b l e a u   ' H i s t o r i q u e   d e s   r e c o u v r e m e n t s '   d a n s   l a   p a g e   / c o m p t a b i l i t e / t r e s o r e r i e / r e c o u v r e m e n t /   p o u r   a f f i c h e r   l a   l i s t e   d e   t o u s   l e s   c h  q u e s   e t   v i r e m e n t s   d  j    r e c o u v e r t s ,   s  p a r  s   p a r   o n g l e t s . 
 
 
 
 -   P o u r   l e s   c h  q u e s   o u   v i r e m e n t s   d  j    e n c a i s s  s   p u i s   r e m b o u r s  s ,   i l s   g a r d e n t   l e u r   s t a t u t   e n c a i s s    m a i s   a f f i c h e n t   l a   m e n t i o n   ' R e m b o u r s  '   d a n s   l ' h i s t o r i q u e   d e s   r e c o u v r e m e n t s ,   s a n s   p o s s i b i l i t    d e   r e t o u r   a u   p a y e u r . 
 
 -   E x c l u r e   l e s   o p  r a t i o n s   r e m b o u r s  e s   d u   c a l c u l   d e s   t o t a u x   e t   s o l d e s   d a n s   l e   b r o u i l l a r d   d e   b a n q u e   ( f r o n t - e n d   e t   b a c k - e n d ,   y   c o m p r i s   e x p o r t s   E x c e l / P D F ) . 
 
-   A j o u t   d e   l ' h i s t o r i q u e   d e s   t h  m a t i q u e s   a f f e c t  e s   e t   d u   p l a n n i n g   p a r   g r o u p e   e f f e c t u    p o u r   c h a q u e   c o n s u l t a n t   ( E x e c u t i v e   E d u c a t i o n ) . 
 
 -   C o r r e c t i o n   d e   l '  t a t   a c t i f   d u   m e n u   l o r s   d e   l a   c o n s u l t a t i o n   d e   l ' h i s t o r i q u e   d ' u n   c o n s u l t a n t . 
 
 - Refonte de la vue /examens/generate-pv/ et du template preview_exam_pv.html pour un affichage en lecture seule (sans cration automatique de donnes ni boutons d'dition).
- Affichage du PV d'examen dans un Offcanvas au lieu d'une nouvelle page depuis la liste des rsultats d'examens (exams_results.html).
- Modernisation du design de preview_exam_pv.html (interface premium, typographie Inter, tableaux modernes, badges) et affichage de l'Offcanvas en plein cran (100vw) pour le PV d'examen.
- Rduction des marges latrales (gauche et droite) dans l'affichage du PV d'examen (preview_exam_pv.html) pour optimiser l'espace en plein cran.
- Correction de l'affichage du nom du Module et du Type d'Examen dans l'en-tte du PV (preview_exam_pv.html) en transmettant correctement l'objet exam_plan depuis la vue.
- Modification des boutons d'action dans exams_results.html : Remplacement de 'Grer le PV' par 'Consulter', et restriction d'accs (boutons dsactivs) tant que le PV n'est pas valid.
- Restructuration de la vue globale des PVs d'examens (exams_results.html) pour regrouper l'affichage par Groupe puis par Semestre via JavaScript, avec une hirarchie visuelle premium.
- exams_results.html : Rduction de la taille de police du nom de groupe et ajout d'un badge indiquant la formation, la spcialit et sa version  ct du titre du groupe.
- exam_plan.py : Ajout de la spcialit, de la formation et de la version dans les donnes JSON renvoyes par l'API ApiListPvExamen pour le regroupement.
- exam_plan.py et generate_pv.py : Ajout de la traabilit des actions utilisateurs (consultation, modification, validation, suppression des PVs d'examens et des planifications d'examens) dans la table UserActionLog pour un meilleur suivi pdagogique.

- Ajout d'un filtre de complétude (informations incomplètes / dossiers incomplets) dans la liste des préinscrits (	_crm/f_views/prinscrits.py et liste-des-preinscrits.html).

- Réorganisation de la disposition des filtres dans /crm/liste-des-preinscrits/ pour un alignement sur deux lignes distinctes.

- Ajout de l'affichage du nombre de résultats trouvés dans la barre de recherche des préinscrits (liste-des-preinscrits.html).

- Agrandissement de la barre de recherche dans /crm/liste-des-preinscrits/ pour occuper toute la largeur disponible (liste-des-preinscrits.html).

- Réduction de la hauteur des cartes KPI et déplacement des compteurs à droite de l'icône dans /crm/liste-des-preinscrits/ (liste-des-preinscrits.html).

- Reproduction des mêmes améliorations esthétiques dans /crm/liste-des-prospects/ (réduction de la hauteur des cartes KPI avec chiffres alignés à droite de l'icône, agrandissement de la barre de recherche sur toute la largeur avec affichage du nombre de résultats trouvés).
