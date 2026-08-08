# ÃƒÆ’Ã‚Â°Ãƒâ€¦Ã‚Â¸ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬?ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã‚Â¯Ãƒâ€šÃ‚Â¸ÃƒÂ¯Ã‚Â¿Ã‚Â½ Journal des Mises ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  Jour (Changelog)

## [Unreleased]
- **Trésorerie / Remboursement** : Ajout d'un bouton de désinscription dans la vue détails (`details_rembourssement.html`) si l'étudiant est encore actif. Si l'étudiant est déjà désinscrit, une alerte d'information s'affiche.
- **Trésorerie / Remboursement** : Ajout d'un bouton "Retirer du groupe" à côté des informations du groupe actuel de l'étudiant, permettant de le supprimer manuellement de son groupe (`GroupeLine` et `AffectationGroupe`) via l'API existante. La récupération du groupe de l'étudiant a été corrigée pour utiliser `.first`.
- **SaaS Admin / Entreprise** : Ajout de la colonne "Actions" avec des boutons rapides (Détails, Modifier, Supprimer) dans la liste des entreprises (`mes_entreprises.html`). Le bouton "Modifier" ouvre un formulaire modal pré-rempli et sauvegarde les modifications via AJAX.
- **SaaS Admin / Entreprise** : Correction d'une erreur 500 (AttributeError) lors du chargement ou de la mise à jour des données de l'entreprise due à des champs `quittance_prefix` et `quittance_suffix` obsolètes. Ils ont été remplacés par `quittance_format` et `quittance_sequence_length`.
- **CRM / Liste des préinscrits** : Ajout d'une option de tri et de groupement par Promo & Spécialité.
- **TrÃ©sorerie / Suivi des paiements** : Ajout d'une pagination cÃ´tÃ© client pour la liste des paiements, avec un contrÃ´le pour sÃ©lectionner le nombre d'Ã©lÃ©ments par page.
- **TrÃ©sorerie / Liste des paiements** : Ajout d'un affichage visuel ("empty state" avec icÃ´ne) plus Ã©lÃ©gant dans le cas oÃ¹ aucun paiement n'est trouvÃ© ou enregistrÃ©.
- **TrÃ©sorerie / Imputation Bancaire** : Affichage de la rÃ©fÃ©rence du paiement sous le mode de paiement et du numÃ©ro de paiement (ID) sous le nom du client dans le tableau des encaissements.
- **TrÃ©sorerie / Imputation Bancaire** : Correction et intÃ©gration des filtres de recherche textuelle globale (client, entitÃ©, compte) et de sÃ©lection par mode de paiement.
- **TrÃ©sorerie / Imputation Bancaire** : Ajout d'une pagination cÃ´tÃ© client pour les tableaux des onglets "Encaissement" et "DÃ©caissement", limitant l'affichage Ã  10 Ã©lÃ©ments par page et amÃ©liorant les performances d'affichage.
- **CRM / Liste des prospects** : Alignement complet de la disposition de la barre de recherche et des filtres sur le modÃ¨le de "Liste des prÃ©inscrits" (barre de recherche et actions en haut, filtres modernes alignÃ©s Ã  droite en dessous).
- **CRM / Liste des prospects** : Remplacement du sÃ©lecteur de tri par date par une plage de dates (Date de dÃ©but, Date de fin) pour filtrer les prospects crÃ©Ã©s dans un intervalle prÃ©cis.
- **CRM / Liste des prospects** : Ajout d'un filtre par promotion (code et label) pour affiner la liste des prospects.
- **SaaS Admin / Campagne BudgÃ©taire** : Correction du filtre "Cible Finale (Annuel)" dans le tableau de bord global, qui ne mettait pas Ã  jour les taux de rÃ©alisation et consommation globaux.
- **Configuration / Statistiques CRM** : Remplacement du tableau "Analyse par Institut" par un affichage plus moderne sous forme de grille de cartes (cards) dÃ©taillant les prospects, opportunitÃ©s et le pipeline gÃ©nÃ©rÃ©.
- **Toutes les applications** : RÃ©duction globale des tailles, marges (margins) et espacements internes (paddings) sur tous les tableaux de bord (dashboards), banniÃ¨res et cartes de statistiques afin d'optimiser l'espace d'affichage de toutes les pages du SaaS.
- **SaaS Admin / Campagne BudgÃ©taire (Review)** : DÃ©placement des cartes de synthÃ¨se (Recettes, DÃ©penses, Solde) directement dans l'en-tÃªte de la matrice de suivi pour une meilleure lisibilitÃ©.
- **SaaS Admin / Campagne BudgÃ©taire (Review)** : Les sections "Suivi des Recettes" et "Suivi des DÃ©penses" de la matrice sont dÃ©sormais rÃ©tractables. Par dÃ©faut, seule la section "Suivi des Recettes" est dÃ©roulÃ©e.
- **SaaS Admin / Campagne BudgÃ©taire (Review)** : Ajout d'un menu dÃ©roulant pour filtrer et afficher la matrice de suivi des rÃ©alisations par trimestre (sÃ©lection automatique du trimestre en cours par dÃ©faut).
- **SaaS Admin / Campagne BudgÃ©taire** : Remplacement du tableau des instituts par un affichage sous forme de cartes.
- **SaaS Admin / Tableau de bord** : Remplacement du terme "Objectif AssignÃ©" par "Objectifs (Tous les campus)".
- **SaaS Admin / Menu Associe** : RÃ©organisation du menu (Tableau de bord, Gestion budgÃ©taire, Statistiques, Mesure de satisfaction).
- **Statistiques CRM** : Ajout de l'impression d'un rapport consolidÃ© listant le nombre total de prospects, le dÃ©tail par statut (visiteur, prÃ©-inscrit, instance, converti, annulÃ©) et le nombre de documents uploadÃ©s par institut.
- **SaaS Admin** : Ajout de l'historique complet des dates de connexions affichable via un menu deroulant, en plus du nombre de connexions (login_count) et de la date de la derniere connexion (last_login) par utilisateur dans le rapport de statistiques de taux d'utilisation de la plateforme.
- **Configuration:** Ajout de paramÃƒÂ¨tres de validation des champs requis CRM en fonction du profil (crm_required_fields_national, crm_required_fields_etranger, crm_required_fields_double).
- **CRM:** Validation dynamique cÃƒÂ´tÃƒÂ© client et ajout automatique d'astÃƒÂ©risques rouges pour les champs requis selon le contexte du partenaire.
- **Configuration:** Remplacement de la validation globale des onglets CRM par des verrous individuels (JSONField crm_field_locks) pour chaque champ de la fiche prÃƒÂ©-inscrit.
- **CRM:** Ajout de l'attribut disabled de maniÃƒÂ¨re dynamique sur les champs du profil prÃƒÂ©-inscrit selon la configuration.
- **NouveautÃƒÂ© (TrÃƒÂ©sorerie)** : SÃƒÂ©paration de l'affichage des chÃƒÂ¨ques et des virements dans le module "Recouvrement des paiements" (`/comptabilite/tresorerie/recouvrement/`) via l'ajout de deux onglets distincts.
- **NouveautÃƒÂ© (TrÃƒÂ©sorerie)** : SÃƒÂ©paration de l'affichage des chÃƒÂ¨ques et des virements dans le module "Suivi des chÃƒÂ¨ques et virements ÃƒÂ©mis" (`/comptabilite/tresorerie/caisse/suivi-cheques-emis/`) avec la crÃƒÂ©ation de deux onglets distincts pour un meilleur filtrage.
- **NouveautÃƒÂ© (TrÃƒÂ©sorerie)** : Adaptation des statuts pour les virements ÃƒÂ©mis. Les virements ont dÃƒÂ©sormais leurs propres statuts ("En attente" et "Virement effectuÃƒÂ©") distincts de ceux des chÃƒÂ¨ques ("Ãƒâ€°mis", "En attente de signature", "Remis", "DÃƒÂ©caissÃƒÂ©").
- **NouveautÃƒÂ© (Formateurs)** : CrÃƒÂ©ation de la vue `ChargeHoraireFormateur` pour calculer et afficher le dÃƒÂ©tail des charges horaires (hebdomadaire, mensuelle, semestrielle) des formateurs par groupe et par jour. RÃƒÂ©activation du lien dans le menu.
- **Correction (UI/Menu)** : Commentaire du lien vers `ChargeHoraireFormateur` dans `menu.html` pour corriger l'erreur `NoReverseMatch` suite ÃƒÂ  la dÃƒÂ©sactivation de cette vue non dÃƒÂ©finie.
- **Correction (Migrations)** : Fusion des migrations conflictuelles (merge) pour l'application `t_formations` (`0013_formateurs_is_particular_irg` et `0015_alter_planscadre_type_plan`).
- **Correction (Formations)** : Commentaire de la route `formateurs/charge-horaire/` qui appelait la vue non dÃ‡Â¸finie `ChargeHoraireFormateur` et provoquait une erreur au lancement du serveur.
- **FonctionnalitÃƒÆ’Ã‚Â© (Conseil/Devis)** : L'impression des devis (depuis la page des dÃƒÆ’Ã‚Â©tails) utilise dÃƒÆ’Ã‚Â©sormais le modÃƒÆ’Ã‚Â¨le `dolibare` de l'application `pdf_editor` pour gÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©rer le PDF avec les bonnes variables au lieu de l'impression basique du navigateur.
- **SÃƒÆ’Ã‚Â©curitÃƒÆ’Ã‚Â© (Conseil)** : Ajout de la permission manquante (`@module_permission_required`) sur la vue `ApiCreateRendezVousPipeline`.
- **Modification UI (Conseil/Prospects)** : Remplacement du menu dÃƒÆ’Ã‚Â©roulant d'actions par des icÃƒÆ’Ã‚Â´nes d'action alignÃƒÆ’Ã‚Â©es (consulter, modifier, supprimer) dans la liste des prospects en instance (`/conseil/prospects-en-instance/`).
- **Configuration** : DÃƒÆ’Ã‚Â©placement de la variable `DEBUG` de `settings.py` vers les variables d'environnement (`.env`).
- **NouveautÃƒÆ’Ã‚Â© (Conseil)** : CrÃƒÆ’Ã‚Â©ation d'un tableau de bord global et agrÃƒÆ’Ã‚Â©gÃƒÆ’Ã‚Â© pour Executive Education (`/conseil/dashboard/`) affichant les KPIs consolidÃƒÆ’Ã‚Â©s pour le CRM (prospects, pipeline), les Ventes (devis, factures, chiffre d'affaires) et la Formation (groupes, participants), incluant un graphique de rÃƒÆ’Ã‚Â©partition du pipeline.
- **FonctionnalitÃƒÆ’Ã‚Â© (Conseil/Groupes)** : Ajout d'une fonctionnalitÃƒÆ’Ã‚Â© de suivi des sÃƒÆ’Ã‚Â©ances dans l'onglet Planning (`/conseil/groupes/details-groupe/<id>/`), permettant de marquer une sÃƒÆ’Ã‚Â©ance comme tenue et de renseigner un compte-rendu des ÃƒÆ’Ã‚Â©lÃƒÆ’Ã‚Â©ments abordÃƒÆ’Ã‚Â©s avec un indicateur d'ÃƒÆ’Ã‚Â©tat (En attente / Tenue).
- **Alerte (Conseil/Groupes)** : Lors de la crÃƒÆ’Ã‚Â©ation d'un nouveau groupe, la sÃƒÆ’Ã‚Â©lection d'un client affiche dÃƒÆ’Ã‚Â©sormais une notification (alerte visuelle et message Alertify) si celui-ci possÃƒÆ’Ã‚Â¨de dÃƒÆ’Ã‚Â©jÃƒÆ’Ã‚Â  un groupe en cours.
- **AmÃƒÆ’Ã‚Â©lioration (Conseil/Groupes)** : Dans la page de dÃƒÆ’Ã‚Â©tails d'un groupe (`/conseil/groupes/details-groupe/<id>/`), le panneau latÃƒÆ’Ã‚Â©ral affiche dÃƒÆ’Ã‚Â©sormais la facture associÃƒÆ’Ã‚Â©e au devis si elle existe, en la mettant en ÃƒÆ’Ã‚Â©vidence (avec le devis liÃƒÆ’Ã‚Â© relÃƒÆ’Ã‚Â©guÃƒÆ’Ã‚Â© au second plan), permettant un accÃƒÆ’Ã‚Â¨s rapide ÃƒÆ’Ã‚Â  la facturation.
- **AmÃƒÆ’Ã‚Â©lioration (Conseil/Groupes)** : Dans l'assistant de crÃƒÆ’Ã‚Â©ation de groupe (ÃƒÆ’Ã¢â‚¬Â°tape 2), si le client possÃƒÆ’Ã‚Â¨de des factures, le systÃƒÆ’Ã‚Â¨me affiche dÃƒÆ’Ã‚Â©sormais les factures avec leurs devis liÃƒÆ’Ã‚Â©s en prioritÃƒÆ’Ã‚Â©, ainsi que les devis non facturÃƒÆ’Ã‚Â©s. Sinon, il n'affiche que les devis.
- **Modification (Conseil/Groupes)** : Harmonisation du design de la fenÃƒÆ’Ã‚Âªtre modale d'ajout rapide de participant (remplacement des `form-floating` par un style plus propre avec `input-group` et icÃƒÆ’Ã‚Â´nes, en accord avec le thÃƒÆ’Ã‚Â¨me premium "glass-card").
- **Correction (Conseil/Groupes)** : Le formulaire d'ajout rapide de participant dans l'assistant de crÃƒÆ’Ã‚Â©ation de groupe associe dÃƒÆ’Ã‚Â©sormais correctement le nouveau participant au devis sÃƒÆ’Ã‚Â©lectionnÃƒÆ’Ã‚Â©, ce qui lui permet d'apparaÃƒÆ’Ã‚Â®tre immÃƒÆ’Ã‚Â©diatement dans la liste.
- **Refonte UI (Conseil/Clients)** : Transformation de la page "DÃƒÆ’Ã‚Â©tails du Client" (`/conseil/details-client/<id>/`) en un vÃƒÆ’Ã‚Â©ritable "Tableau de Bord Client" premium :
  - CrÃƒÆ’Ã‚Â©ation d'une banniÃƒÆ’Ã‚Â¨re de profil dÃƒÆ’Ã‚Â©gradÃƒÆ’Ã‚Â©e avec l'avatar du client en chevauchement.
  - Remplacement des cartes KPI par un widget "Bilan Financier" ultra-compact et esthÃƒÆ’Ã‚Â©tique.
  - Suppression du "Workflow Stepper" (pipeline CRM) qui n'ÃƒÆ’Ã‚Â©tait plus pertinent pour un client confirmÃƒÆ’Ã‚Â©.
  - Refonte de la navigation par onglets (style "underline" minimaliste).
  - DÃƒÆ’Ã‚Â©placement de la liste des opportunitÃƒÆ’Ã‚Â©s vers un nouvel onglet dÃƒÆ’Ã‚Â©diÃƒÆ’Ã‚Â© "Dossiers & OpportunitÃƒÆ’Ã‚Â©s".
- **Modification (Conseil/Ventes)** : Remplacement de l'alerte de confirmation (alertify) par une fenÃƒÆ’Ã‚Âªtre modale personnalisÃƒÆ’Ã‚Â©e (thÃƒÆ’Ã‚Â¨me "glass-card") lors du clic sur le bouton "Rendre en brouillon" dans les dÃƒÆ’Ã‚Â©tails d'un devis.
- **Modification (Conseil/Ventes)** : Harmonisation du design de la fenÃƒÆ’Ã‚Âªtre modale "Conversion en Facture" sur la page des dÃƒÆ’Ã‚Â©tails d'un devis (`/conseil/details-devis/<id>/`) avec le thÃƒÆ’Ã‚Â¨me "glass-card" (coins arrondis, icÃƒÆ’Ã‚Â´nes amÃƒÆ’Ã‚Â©liorÃƒÆ’Ã‚Â©es et typographie modernisÃƒÆ’Ã‚Â©e).
- **Modification (Conseil/Pipeline)** : Ajout d'une fenÃƒÆ’Ã‚Âªtre de confirmation (alertify) avertissant l'utilisateur qu'un devis brouillon sera gÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©rÃƒÆ’Ã‚Â© automatiquement lorsqu'il dÃƒÆ’Ã‚Â©place (glisser-dÃƒÆ’Ã‚Â©poser) une opportunitÃƒÆ’Ã‚Â© vers la colonne "NÃƒÆ’Ã‚Â©gociation". En cas de confirmation, le devis est crÃƒÆ’Ã‚Â©ÃƒÆ’Ã‚Â© et la page est actualisÃƒÆ’Ã‚Â©e.
- **Correction (Conseil/Pipeline)** : Lors de la conversion en devis, la carte est dÃƒÆ’Ã‚Â©sormais correctement positionnÃƒÆ’Ã‚Â©e dans la colonne "NÃƒÆ’Ã‚Â©gociation" au lieu de "Devis envoyÃƒÆ’Ã‚Â©" (le devis ÃƒÆ’Ã‚Â©tant crÃƒÆ’Ã‚Â©ÃƒÆ’Ã‚Â© en brouillon). Le texte de la modale a ÃƒÆ’Ã‚Â©tÃƒÆ’Ã‚Â© mis ÃƒÆ’Ã‚Â  jour en consÃƒÆ’Ã‚Â©quence.
- **Modification (Conseil/Ventes)** : RÃƒÆ’Ã‚Â©duction de la taille des ÃƒÆ’Ã‚Â©lÃƒÆ’Ã‚Â©ments (padding, boutons d'action et polices) dans les tableaux des listes de devis, factures et avoirs (`/conseil/liste-des-devis/`, `/conseil/liste-des-factures/`) pour un affichage plus compact et optimisÃƒÆ’Ã‚Â©.
- **Modification (Conseil/Pipeline)** : Harmonisation du design de la fenÃƒÆ’Ã‚Âªtre modale "Convertir en devis" avec le thÃƒÆ’Ã‚Â¨me de la page `/conseil/pipeline/` (style "glass-card", coins arrondis, icÃƒÆ’Ã‚Â´nes amÃƒÆ’Ã‚Â©liorÃƒÆ’Ã‚Â©es et espacement optimisÃƒÆ’Ã‚Â©).
- **Correction (Conseil/CRM)** : Correction de l'affichage "undefined" pour l'ÃƒÆ’Ã‚Â©tat des prospects dans la liste (`/conseil/prospects-en-instance/`) en ajoutant des valeurs par dÃƒÆ’Ã‚Â©faut pour les labels d'ÃƒÆ’Ã‚Â©tat ("En attente" et "ConfirmÃƒÆ’Ã‚Â©").
- **Ajout (Conseil/CRM)** : Affichage de la liste des opportunitÃƒÆ’Ã‚Â©s liÃƒÆ’Ã‚Â©es sur la page des dÃƒÆ’Ã‚Â©tails du client (`/conseil/details-client/<slug>/`). L'historique des opportunitÃƒÆ’Ã‚Â©s a ÃƒÆ’Ã‚Â©tÃƒÆ’Ã‚Â© intÃƒÆ’Ã‚Â©grÃƒÆ’Ã‚Â© sous l'onglet "RÃƒÆ’Ã‚Â©sumÃƒÆ’Ã‚Â©" pour un suivi centralisÃƒÆ’Ã‚Â©.
- **Ajout (Conseil/CRM)** : Affichage de la liste des opportunitÃƒÆ’Ã‚Â©s liÃƒÆ’Ã‚Â©es sur la page des dÃƒÆ’Ã‚Â©tails du prospect (`/conseil/details-prospect/<slug>/`). Les opportunitÃƒÆ’Ã‚Â©s sont prÃƒÆ’Ã‚Â©sentÃƒÆ’Ã‚Â©es sous forme de cartes premium avec leur statut, budget, probabilitÃƒÆ’Ã‚Â© et le commercial associÃƒÆ’Ã‚Â©.
- **Modification (Conseil/CRM)** : Modernisation de l'affichage de la liste des prospects en instance (`/conseil/prospects-en-instance/`) via l'amÃƒÆ’Ã‚Â©lioration du rendu JavaScript (ajout d'avatars avec initiales, badges arrondis, typographie affinÃƒÆ’Ã‚Â©e et effets de survol interactifs sur les lignes et boutons d'action).
- **Modification (Examens)** : Modernisation de l'affichage des cartes de groupes de sessions d'examens (`examens/deliberation/builltins/session/`) avec un design premium (icÃƒÆ’Ã‚Â´nes amÃƒÆ’Ã‚Â©liorÃƒÆ’Ã‚Â©es, statistiques internes sur fond clair, boutons arrondis et effets de survol dynamiques).
- **Correction (Examens/Logs)** : RÃƒÆ’Ã‚Â©solution de l'erreur `DoesNotExist` (500) lors de la suppression en cascade d'une session d'examen, causÃƒÆ’Ã‚Â©e par l'accÃƒÆ’Ã‚Â¨s ÃƒÆ’Ã‚Â  des objets liÃƒÆ’Ã‚Â©s inexistants lors de la journalisation de suppression (`log_exam_action_delete`).
- **Modification (Conseil)** : Modernisation des lignes du tableau de la page "Mapping DAS" (`/conseil/das/`) avec des effets de survol dynamiques (ÃƒÆ’Ã‚Â©lÃƒÆ’Ã‚Â©vation, ombrage, fond translucide) pour accentuer l'effet "glass-card".
- **Modification (Conseil)** : Harmonisation du design de la fenÃƒÆ’Ã‚Âªtre de crÃƒÆ’Ã‚Â©ation (modale DAS) avec le thÃƒÆ’Ã‚Â¨me "glass-card" de la page.
- **Ajout (Stages)** : MÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©canisme de suppression des sÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ances de Focus Group (historique des sÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ances) via une fenÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªtre modale de confirmation.
- **Ajout (Stages)** : MÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©canisme d'affectation de stages existants ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  un Focus Group directement depuis la vue de dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tail du Focus Group (`stage/focus-group/<id>/`) via une fenÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªtre modale.
- **Ajout (Stages)** : MÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©canisme de suppression des stages directement depuis la liste des stages (`stage/list/`) avec confirmation par fenÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªtre modale et journalisation.
- **SÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©curitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© & Audit (Stages)** : Ajout de la journalisation complÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨te (via `UserActionLog`) pour toutes les actions de mutation effectuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es dans le module des Stages (t_stage). Cela inclut les actions sur les stages (crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation, modification, suppression), les prÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sentations progressives (ajout, suppression), les focus groups (crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation, ajout/suppression de sÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ances, affectation de stages), les conseils de validation, les dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cisions, et les notes d'examen final.
- **SÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©curitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© & Audit (Executive Education)** : Ajout de la journalisation complÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨te (via `UserActionLog`) pour toutes les actions de mutation effectuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es dans le module Executive Education (t_conseil). Cela inclut les actions sur les prospects, les opportunitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s, les devis (crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation, validation, acceptation/rejet), les factures (crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation, validation, annulation, suppression), les groupes, les paiements, les thÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©matiques, et les informations liÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es (participants, DAS, infos bancaires).
- **SÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©curitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© & Audit** : Ajout de la journalisation complÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨te (logs d'accÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s et de modification via `UserActionLog`) pour toutes les actions effectuÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es dans le menu Configuration (gestion des utilisateurs, rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´les, modules, sessions actives, ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©dition des documents PDF, informations de l'entreprise et paramÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨tres gÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©raux).
- **Ajout** : FonctionnalitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© d'impression (gÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ration de rapport) du taux d'utilisation de l'ERP avec possibilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© de sÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©lectionner spÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cifiquement un ou plusieurs instituts via une fenÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªtre modale.
- **Modification** : Refonte de l'affichage de la page `platform_usage_rate` pour utiliser des onglets (tabs) par tenant et ajout de la pagination DataTables.
- **Modification** : Le menu "Satisfaction" a ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© renommÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© en "Mesure de satisfaction" dans `menu.html`.
- **Modification** : Remplacement de la pagination serveur des tenants par une pagination locale (DataTables) des logs ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  l'intÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rieur de chaque onglet tenant sur la page `crm_user_logs`.
- **Modification** : Refonte de l'affichage de la page `crm_user_logs` pour utiliser des onglets (tabs) par tenant au lieu d'une liste verticale.
- **Modification** : Regroupement de "Stats CRM", "Logs" et "Taux d'utilisation" sous un seul menu dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©roulant "Statistiques" dans `menu.html` et `saas_menu.html`.
- **Ajout** : Nouvelle vue et page `platform_usage_rate` (Taux d'utilisation de l'ERP) calculant les actions/jour par utilisateur depuis la crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation du tenant.
- **Ajout** : Mise en place de filtres par institut, par utilisateur et par type d'action sur la page `crm_user_logs`.
- **Modification** : Le titre de la vue `crm_user_logs` a ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© changÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© de "Logs Utilisateurs CRM par Institut" ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  "Logs".
- **Correction** : RÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©solution de l'erreur `ModuleNotFoundError` en utilisant `app.models` au lieu de `school.models` pour `Institut`.
- **Modification** : Le lien de menu a ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© renommÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© en "Logs" (dans `menu.html` et `saas_menu.html`).
- **Modification** : La vue `crm_user_logs` rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cupÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨re dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sormais tous les logs (sans limite de 100).
- **Ajout** : Lien vers `crm_user_logs` ajoutÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© dans le menu `saas_menu.html`.
- **Ajout** : Nouvelle vue et page `crm_user_logs` dans `associe_app` pour afficher les logs utilisateurs (`UserActionLog`) CRM par tenant.

---

## [07/06/2026] - v1.2.x - Harmonisation de la configuration Facture

- **SaaS Admin / Notifications Globales** :
  - **Gestion des annonces** : CrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation d'une interface superadmin permettant de crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©er, lister, activer ou supprimer des annonces (`SystemAnnouncement`).
  - **Ciblage granulaire** : PossibilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© de cibler l'ensemble des utilisateurs, un Tenant spÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cifique, ou un utilisateur prÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cis au sein d'un Tenant.
  - **Temps RÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©el via WebSockets (Channels)** : IntÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©gration au `NotificationConsumer` existant pour diffuser instantanÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ment les annonces (`announcement_trigger`) sans rafraÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â®chissement de page ni appels AJAX pÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©riodiques. Groupes de diffusions optimisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s (`global_all_users`, `{schema_name}_all_users`).
  - **Relance d'annonce** : Ajout d'un bouton "Relancer" permettant de rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©initialiser l'historique de lecture d'une annonce spÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cifique et de forcer sa rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©apparition en temps rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©el chez tous les utilisateurs ciblÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s.
  - **Suivi de lecture** : Affichage d'une modale pour les utilisateurs ciblÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s. Un systÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨me de validation ("J'ai lu cette annonce") enregistre la confirmation en base de donnÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es (`AnnouncementRead`) pour dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sactiver l'affichage.

- **SaaS Admin / Centre de Connaissance** :
  - Suppression de la mention de limitation de taille de fichier pour l'upload.
  - Ajout du support de lecture des vidÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©os (MP4) hÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©bergÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es localement directement depuis le modal vidÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©o existant.

- **TrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sorerie / ModÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨les d'ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©chÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ancier** :
  - **Frais d'inscription** : Ajout de la possibilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© d'activer/dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sactiver la configuration des frais d'inscription au niveau du modÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨le d'ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©chÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ancier (`ModelEcheancier.has_frais_inscription`).
  - **Interface utilisateur** : IntÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©gration de toggles "Activer la configuration des frais d'inscription" dans les formulaires de crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation et de modification des modÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨les d'ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©chÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ancier (`gestion_echeancier.html`).
  - **Assistant d'ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©chÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ancier** : Conditionnement de l'affichage et de l'obligation de saisie du montant des frais d'inscription et de l'entitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© associÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e dans le formulaire de crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation d'ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©chÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ancier (`creer-un-echeancier.html`), selon la configuration du modÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨le choisi.

- **CRM / Double Diplomation** :
  - **Modification des Voeux** : RÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©solution du bug empÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªchant la modification des voeux (bouton "Mettre ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  jour") pour les prospects en double cursus, notamment ceux ayant ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© annulÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s ou modifiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s sans changement de formation (rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cupÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ration directe de `id_formation` via `#formation_voeux`).
  - **Changement de Cursus** : Correction d'une erreur 500 (`FicheVoeuxDouble.DoesNotExist`) survenant lors du passage d'un cursus double ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  un cursus standard, particuliÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨rement pour les prospects annulÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s ayant des fiches de voeux dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©jÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  confirmÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es.
  - **RÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©initialisation des Voeux** : Ajout d'un nouveau mÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©canisme (bouton et modale de confirmation) permettant de supprimer complÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨tement les fiches de vÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œux d'un prospect (double et standard) et de rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©initialiser son orientation.

- **Facturation (Conseil)** :
  - **Design & UI** : Harmonisation complÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨te de la page `configure-facture.html` pour correspondre au design premium de `configure-devis.html`. Modification de la structure de la grille pour utiliser une barre latÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rale droite fixe (`.col-lg-4`) pour le rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©capitulatif, et une colonne principale (`.col-lg-8`) pour les informations gÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rales, la liste des articles et les modalitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s. Adaptation du code JavaScript de gÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ration du rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©capitulatif financier pour utiliser des ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©lÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ments HTML `<div class="d-flex ...">` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  la place de `<tr>`, afin de correspondre visuellement aux totaux du devis.
  - **Ligne d'ajout des articles** : Harmonisation de la ligne d'ajout (`tfoot`) avec les placeholders, les entÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªtes du tableau, la gestion des permissions (`disabled`) et le style Select2 (retrait du thÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨me bootstrap-5 pour appliquer le style premium customisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©).
  - **Conversion Devis en Facture** : Le prospect liÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© au devis devient automatiquement un client (avec le statut "convertit") lors de la conversion du devis en facture, s'il n'est pas dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©jÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  client.
  - **Liste des Devis** : Masquage de l'icÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´ne de modification (ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©dition) pour les devis qui ne sont plus ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  l'ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tat brouillon (dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©jÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  validÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s/envoyÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s/acceptÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s).
  - **Design & UI (Liste des Devis)** : Harmonisation complÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨te du design de la page `liste_des_devis.html` avec celui de `liste_des_factures.html`. Ajout des filtres par statut et par dates (JS dynamique), badges de statuts subtils arrondis (`bg-xxx-subtle`), boutons d'actions circulaires (32x32) et compteurs de rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sultats (pagination dynamique).

## [05/06/2026] - v1.2.x - Permissions Menus Associe App

- **Associe App** :
  - **Satisfaction** : Ajout d'un nouveau menu "Satisfaction" affichant une page "FonctionnalitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© en attente de validation".
  - **Gestion des Permissions** : Ajout de conditions de permissions (`is_superuser` et `is_staff`) sur le menu horizontal `public_folder/menu.html` pour restreindre l'accÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨s. ParamÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©trage et Administration sont rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©servÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s aux super-administrateurs, tandis que Dashboard, Stats CRM et Gestion BudgÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©taire sont accessibles aux membres du staff.
  - **Gestion des Utilisateurs** : Ajout d'un mÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©canisme (checkbox) pour activer ou dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©sactiver le statut super-utilisateur lors de l'ajout ou de l'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©dition d'un utilisateur dans le panel d'administration (`associe_app`).

- **SaaS Admin** :
  - **Gestion du Changelog** : Correction d'une erreur 403 (CSRF) lors de la suppression d'une mise ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  jour dans le panel SaaS Admin. Le jeton CSRF ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©tait mal formatÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© dans la requÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âªte AJAX (`templates/saas_admin_app/saas_changelog.html`).

---

## [04/06/2026] - v1.2.0 - Refonte de l'IRG (ConformitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© LÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©gale AlgÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©rienne)

- **Ressources Humaines (FiscalitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© & Paie)** :
  - **Prise en charge des Primes / Rubriques dans la Paie EmployÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s** :
    - IntÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©gration du calcul des rubriques/primes dynamiques (gains et retenues) dans la gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ration de la paie en masse via `assistantPaie`. La mÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©thode synchronise automatiquement le contrat `t_rh.models.Contrats` avec le contrat `t_ressource_humaine.models.Contrat` pour rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©cupÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©rer et appliquer la bonne configuration des rubriques et leurs valeurs par dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©faut ou personnalisÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es.
    - Persistance correcte des lignes de paie (`LignePaie`) associÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  chaque bulletin lors de la validation en masse, en ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©vitant les doublons (suppression prÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©alable des anciennes lignes de paie pour la mÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âªme fiche).
    - AmÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©lioration de la vue de dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©tail du bulletin de paie de l'employÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© (`fiche_paie_detail.html`) pour boucler sur `fiche.lignes_paie.all` (au lieu de la relation incorrecte `fiche.lignes.all`) et utiliser le libellÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© correct (`ligne.rubrique.libelle` au lieu de `ligne.rubrique.nom`).
    - Affichage des lignes de primes exceptionnelles, de l'indemnitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© de panier, de l'indemnitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© de transport et des retenues pour absences directement sous forme de lignes du tableau pour les employÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s.
    - Ajout des conditions pour charger le nom et l'identifiant de l'employÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© ou du formateur de maniÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨re dynamique dans `fiche_paie_print.html` et `_fiche_paie_detail.html` afin d'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©viter tout plantage `AttributeError` ou omission.
  - **Filtres & Gestion de l'Historique de Paie** : Modernisation de l'historique des fiches de paie (`liste_fiches_paie.html`). Ajout de filtres de recherche avancÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s par employÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©, entitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© lÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©gale, mois, annÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©e et statut de validation (ValidÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© ou Brouillon). Les filtres s'appliquent en temps rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©el (via l'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©vÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nement `onchange` sur tous les sÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©lecteurs) et mettent ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  jour l'historique du navigateur (`window.history.pushState`) pour des filtres persistants sans rechargement de page.
  - **Correction du chargement des rubriques** : RÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©solution d'une erreur 404 dans `details_employe.html` lors de l'ouverture du modal de gestion des rubriques/primes pour un employÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©. Remplacement du chemin d'accÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨s AJAX codÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© en dur par la balise Django dynamique `{% url %}` ciblant l'URL correcte sous le namespace `t_ressource_humaine`.
  - **Validation & Suppression Individuelle/En Masse** : IntÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©gration de checkboxes de sÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©lection et d'une barre d'actions groupÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es permettant de valider ou d'annuler la validation de plusieurs bulletins de paie simultanÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ment. Ajout d'un bouton de suppression sÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©curisÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© par SweetAlert2, accessible uniquement pour les bulletins de paie ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  l'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©tat de brouillon (non validÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s).
  - **PrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©-visualisation et Confirmation de Paie (Masse Salariale)** : Ajout d'une ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©tape de prÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©-visualisation/confirmation avant le scellement dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©finitif de la paie. Les pages d'assistant de paie (salariÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s et formateurs) calculent dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©sormais les totaux gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©raux (nombre de personnes, masse salariale brute globale, total cotisations SS, total retenues IRG et total Net ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  payer) et les prÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©sentent dans une fenÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âªtre de confirmation SweetAlert2 ergonomique et claire.
  - **Correction de l'assistant de paie** : RÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©solution d'un plantage `AttributeError` lors de la validation globale de la paie dans `t_rh/views.py::assistantPaie` oÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¹ le champ inexistant `date_debut` du modÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨le `Contrats` a ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©tÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© remplacÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© par le champ correct `date_embauche`.
  - **Moteur de calcul IRG** : Refonte totale de `calculer_irg` dans `t_ressource_humaine/logic.py` pour implÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©menter la mÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©thode officielle algÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©rienne (LF 2022 / LF 2026) :
    - Arrondi systÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©matique du salaire imposable ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  la dizaine de DA infÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©rieure avant le calcul du barÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨me.
    - Application du premier abattement proportionnel de 40% sur l'IRG brut (limitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© au minimum de 1 000 DA et maximum de 1 500 DA par mois).
    - Formule de lissage pour le **Cas GÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ral** (de 30 000 DA ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  35 000 DA) : $\text{IRG} = \text{IRG1} \times \frac{137}{51} - \frac{27925}{8}$.
    - Formule de lissage pour le **Cas Particulier** (RetraitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s & HandicapÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s, de 30 000 DA ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  42 500 DA) : $\text{IRG} = \text{IRG1} \times \frac{93}{61} - \frac{81213}{41}$.
    - Arrondi fiscal systÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©matique au dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©cime (dizaine de centimes).
  - **Correction du calcul CDI/CDD** : RÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©solution du bug appliquant incorrectement le taux flat de 10% des vacataires ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  tous les enseignants (mÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âªme sous CDD/CDI) ; dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©sormais, seuls les contrats de type `VACATION` sont soumis ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  ce taux flat.
  - **Base de donnÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es / ModÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨les** : Ajout du champ `is_particular_irg` dans les modÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨les `Employees` et `Formateurs`. IntÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©gration automatique dans les formulaires et les modals de crÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ation et modification (modals d'ajout/ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©dition dans `liste_des_formateur.html` et formulaire `NouveauEmploye`).
  - **Prise en charge Formateurs** : Adaptation de `PaieEngine.calculer_paie` pour rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©soudre et transmettre le drapeau `is_particular_irg` ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  partir du contrat de l'enseignant (CDI/CDD) et du formateur reliÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©, appliquant ainsi correctement le barÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨me de lissage particulier (retraitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s/handicapÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s) dans le calcul et la gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ration finale des fiches de paie.
  - **Migrations de Base de DonnÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es** : GÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ration et application de la migration `0013_formateurs_is_particular_irg.py` pour ajouter le champ dans le schÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ma et migration sur tous les schÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©mas locataires (multi-tenant isolation).
  - **Interface & Simulation ModernisÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©e (Design Premium)** : 
    - IntÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©gration de la description dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©taillÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©e du barÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨me, des abattements et des formules de lissage (cas gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ral et cas particulier) dans l'interface de configuration fiscale `templates/tenant_folder/rh/paie/config_fiscalite.html`.
    - Ajout d'un **Simulateur IRG InstantanÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©** interactif en Javascript, permettant de calculer en temps rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©el l'IRG pour n'importe quel montant imposable saisi, pour le cas gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ral et le cas particulier.
    - Refonte visuelle complÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨te sous forme de cartes en verre dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©poli (Glassmorphism) avec des dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©gradÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s fins, des ombres fluides et une disposition responsive.
    - AmÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©lioration de l'ergonomie des formulaires avec des focus adoucis (`soft-glow`), des tooltips informatifs et des styles de boutons raffinÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s.
    - Ajout d'une micro-animation de pulsation (`pulse-update` par transform scale) sur les cartes de rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©sultats du simulateur (Vert/ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°meraude pour le Cas GÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ral, Bleu/Info pour le Cas Particulier) dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©clenchÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©e ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  chaque frappe de clavier.
  - **Validation des tests** : Ajout de nouveaux tests unitaires pour valider les calculs exacts d'IRG pour les cas gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©raux et particuliers (ex: 30 900 DA & 30 930 DA imposable) et ajustement des assertions de test ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  l'abattement de 40% (ex: 45 500 DA imposable).

---

## [04/06/2026] - v1.1.0 - Refonte de StabilitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© (Executive Education & RH)

- **Global / Core** :
  - Correction d'une erreur fatale au dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©marrage du serveur (NameError) dans `school/settings.py` causÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©e par `DEBUG = F`.
- **Ressources Humaines (Paie, PrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©sences & Formateurs)** :
  - **Assistant de Paie Formateurs** : CrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ation d'une page dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©diÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©e "Assistant de Paie - Formateurs" permettant de gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©rer en masse les fiches de paie basÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es sur les fiches mensuelles validÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es.
  - **Historique DÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©diÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© & Redesign** : SÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©paration de l'historique des fiches de paie pour les formateurs avec un tout nouveau design premium (Glassmorphism, animations au survol, dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©gradÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s de couleurs).
  - **Taux IRG Vacataires** : Ajout d'une configuration globale (dans les ParamÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨tres RH) pour appliquer le taux IRG forfaitaire (sans abattement) spÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©cifique aux formateurs vacataires (par dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©faut 10%). Ce paramÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨tre est pris en charge par le moteur de paie de faÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§on automatique.
  - **Correction du systÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨me de paie formateur** : Correction de l'erreur d'attribut `types_contrat` vers `eligible_types` dans `generer_paie`.
  - **Liaison Paie-Formateur** : Ajout d'un bouton "GÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©rer Paie" dynamique sur les fiches mensuelles des formateurs.
  - **Validation des Fiches Mensuelles** : CrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ation du modÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨le `ValidationFicheMensuelleFormateur` avec bouton AJAX SweetAlert2 pour verrouiller et approuver une fiche mensuelle de formateur (affichage d'un badge "ValidÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©e").
  - Restructuration du menu principal "Ressources Humaines" pour sÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©parer clairement "Espace EmployÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s" et "Espace Formateurs" (et les garder ouverts au bon endroit).
  - Modification du formulaire d'ajout d'employÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© pour rendre tous les champs non obligatoires.
  - RÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©solution d'un bug empÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âªchant l'affichage des nouveaux employÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s dans les vues de prÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©sences et dans l'assistant de paie en autorisant les ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©tats (etat) non dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©finis ou vides.
  - RÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©solution d'un bug bloquant l'ajout d'un nouvel employÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â» ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  la validation silencieuse de champs manquants dans le formulaire (exclusion de `solde_conge`, `solde_conge_annee_prec`, `is_teacher`, etc.).
  - RÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©solution d'un bug similaire empÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âªchant la crÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ation d'un nouveau contrat pour un formateur (exclusion des champs non rendus comme `prime_transport`, `prime_panier`, `employee` du `ContratForm`).
  - RÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©solution de l'erreur `KeyError` dans le calcul des paies.
- **CRM / Prospects** :
  - Ajout de la fonctionnalitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© d'importation en masse de prospects particuliers via fichier Excel (`.xlsx`).
  - Ajout d'une fonctionnalitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© pour tÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©lÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©charger le modÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨le d'import. Les prospects importÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s ont le statut "pas de vÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œux formulÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s pour le moment".
- **SaaS Admin** :
  - Correction d'une erreur de syntaxe (`SyntaxError`) dans `urls.py` causÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©e par des caractÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨res `\n` mal formatÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s empÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âªchant l'accÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨s au portail.
  - Correction d'une erreur `NameError` due au dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©corateur `@saas_superuser_required` non dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©fini dans `views.py` (remplacÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© par `@user_passes_test(superadmin_only)`).
  - Correction de la localisation des noms de mois en anglais dans les fiches mensuelles de prÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©sence.
  - CrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ation des pages "Empty States" Premium pour les tableaux vides (CongÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s, PrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©sences, Fiches Mensuelles, EmployÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s).
- **Executive Education (`t_conseil`)** :
  - SÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©curisation complÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨te des API contre les plantages silencieux (`Erreur 500`) : Ajout de la gestion `DoesNotExist` pour plus de 30 requÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âªtes `.get()`.
  - Fixation d'une faille `KeyError` lors de l'accÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨s aux donnÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es JSON non fournies dans l'API de gestion des groupes.

### ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ AmÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©liorations (Optimisations)
- **Base de donnÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es (`@transaction.atomic`)** :
  - Application du verrouillage transactionnel sur toutes les fonctions critiques de crÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ation (`Devis`, `Factures`, `Clients`, `Groupes`) de l'Executive Education, garantissant qu'aucune donnÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©e fantÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â´me ne soit gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©e en cas d'erreur de rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©seau.
- **Ressources Humaines** :
  - Refonte de la suppression d'employÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s avec un effacement en cascade strict des contrats, piÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ces jointes et absences (`models.CASCADE`).
  - Restructuration visuelle de la configuration HUB en onglets modernes.

---
*(Ajoutez les prochaines entrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es ci-dessus)*
-   A j o u t   d e   l a   m o d i f i c a t i o n   e t   s u p p r e s s i o n   d e s   c o n t r a t s   ( i n t e r f a c e   L i s t e   d e s   c o n t r a t s )   d a n s   r h . 
 
 -   R e f o n t e   d e   l a   m o d i f i c a t i o n   d e s   c o n t r a t s   :   c r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© a t i o n   d ' u n e   p a g e   c o m p l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ t e   d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© d i ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   ( u p d a t e _ c o n t r a t . h t m l )   b a s ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   s u r   l ' a s s i s t a n t   d e   c r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© a t i o n   a v e c   p r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© - r e m p l i s s a g e   d e s   r u b r i q u e s . 
 
 -   C o r r e c t i o n   d u   p r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© - r e m p l i s s a g e   d e s   d o n n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e s   s u r   l a   p a g e   d e   m o d i f i c a t i o n   d u   c o n t r a t   ( p r o b l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ m e   d e   s ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© r i a l i s a t i o n   J S O N   d e s   d o n n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e s   P y t h o n ) . 
 
 -   M e n u   l a t ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© r a l   :   a j o u t   d e   l a   r o u t e   ' u p d a t e C o n t r a t P a g e '   p o u r   m a i n t e n i r   l e   m e n u   ' G e s t i o n   d e s   C o n t r a t s '   a c t i f   l o r s   d e   l a   m o d i f i c a t i o n   d ' u n   c o n t r a t . 
 
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n   m ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© c a n i s m e   d e   p r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© v i s u a l i s a t i o n   ( m o d a l )   p o u r   c h a q u e   l i g n e   d e   f i c h e   d e   p a i e . 
 
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d e   l a   f e n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âª t r e   m o d a l e   d e   p r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© v i s u a l i s a t i o n   d a n s   l ' a s s i s t a n t   d e   p a i e   ( d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© p l a c e m e n t   e n   d e h o r s   d u   c o n t e n e u r   d u   t a b l e a u   p o u r   ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© v i t e r   l e s   c o n f l i t s   C S S ) . 
 
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   a n i m a t i o n   d ' a l e r t e   s u r   l e   b o u t o n   d e   r e c h e r c h e   l o r s q u e   l e   m o i s   o u   l ' a n n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   e s t   m o d i f i ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©   a f i n   d ' i n c i t e r   l ' u t i l i s a t e u r   ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â    a c t u a l i s e r   l e s   d o n n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e s . 
 
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   s e c t i o n   d e   s y n t h ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ s e   g l o b a l e   a f f i c h a n t   l e   t o t a l   d e s   p a i e m e n t s   n e t s ,   l e   t o t a l   d e s   p r i m e s   e t   l e   t o t a l   d e   l a   f i s c a l i t ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©   ( S S   +   I R G ) . 
 
 -   M o t e u r   d e   p a i e   :   a j o u t   d ' u n   n o u v e a u   m o d e   d e   c a l c u l   p o u r   l e s   r u b r i q u e s   e t   p r i m e s   ( ' J O U R S '   :   P a r   j o u r   t r a v a i l l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© )   p e r m e t t a n t   d e   m u l t i p l i e r   l e   m o n t a n t   s a i s i   p a r   l e   n o m b r e   d e   j o u r s   d e   p r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© s e n c e   d e   l ' e m p l o y ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© . 
 
 -   C o r r e c t i o n   d u   m e n u   l a t ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© r a l   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   o ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¹   l e   s o u s - m e n u   d e s   f i c h e s   d e   p a i e   f o r m a t e u r s   s ' a f f i c h a i t   c o m m e   a c t i f   ( e n   s u r b r i l l a n c e )   l o r s q u ' o n   s e   t r o u v a i t   s u r   l ' a s s i s t a n t   d e   p a i e   d e s   e m p l o y ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© s   ( p r o b l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ m e   d e   m a t c h i n g   d e   c h a ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â® n e   d e   c a r a c t ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ r e s ) . 
 
 -   I n t e r f a c e   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   ( s c r o l l   h o r i z o n t a l   i n d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© s i r a b l e )   s u r   l a   p a g e   d ' h i s t o r i q u e   d e s   f i c h e s   d e   p a i e   d e s   f o r m a t e u r s ,   c a u s ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©   p a r   u n   ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© m e n t   d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© c o r a t i f   q u i   d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© p a s s a i t   d e   l ' ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© c r a n . 
 
 -   A s s i s t a n t   d e   p a i e   :   e x c l u s i o n   a u t o m a t i q u e   d e s   e m p l o y ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© s   d o n t   l a   f i c h e   d e   p a i e   a   d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© j ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â    ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© t ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©   g ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   p o u r   l e   m o i s   e n   c o u r s   a f i n   d ' ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© v i t e r   l e s   d o u b l o n s   ( i l s   r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© a p p a r a ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â® t r o n t   s i   l e u r   f i c h e   e s t   a n n u l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e ) . 
 
 -   A s s i s t a n t   d e   p a i e   :   a f f i c h a g e   d ' u n e   v u e   d e   s y n t h ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ s e   ' P a i e   c l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â´ t u r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   p o u r   c e   m o i s '   l o r s q u e   t o u t e s   l e s   f i c h e s   d e   p a i e   o n t   d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© j ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â    ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© t ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©   g ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e s   p o u r   l e   m o i s   s ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© l e c t i o n n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© ,   r e m p l a ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ a n t   l e   m e s s a g e   d ' e r r e u r   ' A u c u n e   d o n n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   d i s p o n i b l e ' . 
 
 -   C o r r e c t i o n   d e   l ' i n t e r f a c e   :   l ' i c ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â´ n e   d u   m e n u   ' A s s i s t a n t   d e   P a i e '   n e   s ' a f f i c h a i t   p a s   e n   r a i s o n   d ' u n e   c l a s s e   d ' i c ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â´ n e   i n e x i s t a n t e   d a n s   l a   b i b l i o t h ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ q u e   u t i l i s ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e .   R e m p l a c ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   p a r   u n e   i c ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â´ n e   f o n c t i o n n e l l e   ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© q u i v a l e n t e . 
 
 
- IntÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©gration Paie-Finance : crÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ation d'un nouvel espace dans ComptabilitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©/Finance pour lister les ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©tats de paie et lancer les dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©penses associÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es de maniÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨re globale.

- Gestion des permissions : ajout de la vÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©rification de permission spÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©cifique (sous-menu paie_salaires) sur les vues de la paie dans ComptabilitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©/Finance, assurant le mÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âªme niveau de sÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©curitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© que les autres vues.

- Ajout d'un bouton de validation globale du mois dans /rh/paie/fiches/ avec envoi de notification au personnel configurÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© dans les paramÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨tres gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©raux.

-   A j o u t   d e   l a   m o d i f i c a t i o n   e t   s u p p r e s s i o n   d e s   c o n t r a t s   ( i n t e r f a c e   L i s t e   d e s   c o n t r a t s )   d a n s   r h .  
 -   R e f o n t e   d e   l a   m o d i f i c a t i o n   d e s   c o n t r a t s   :   c r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© a t i o n   d ' u n e   p a g e   c o m p l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ t e   d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© d i ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   ( u p d a t e _ c o n t r a t . h t m l )   b a s ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   s u r   l ' a s s i s t a n t   d e   c r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© a t i o n   a v e c   p r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© - r e m p l i s s a g e   d e s   r u b r i q u e s .  
 -   C o r r e c t i o n   d u   p r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© - r e m p l i s s a g e   d e s   d o n n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e s   s u r   l a   p a g e   d e   m o d i f i c a t i o n   d u   c o n t r a t   ( p r o b l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ m e   d e   s ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© r i a l i s a t i o n   J S O N   d e s   d o n n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e s   P y t h o n ) .  
 -   M e n u   l a t ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© r a l   :   a j o u t   d e   l a   r o u t e   ' u p d a t e C o n t r a t P a g e '   p o u r   m a i n t e n i r   l e   m e n u   ' G e s t i o n   d e s   C o n t r a t s '   a c t i f   l o r s   d e   l a   m o d i f i c a t i o n   d ' u n   c o n t r a t .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n   m ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© c a n i s m e   d e   p r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© v i s u a l i s a t i o n   ( m o d a l )   p o u r   c h a q u e   l i g n e   d e   f i c h e   d e   p a i e .  
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d e   l a   f e n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âª t r e   m o d a l e   d e   p r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© v i s u a l i s a t i o n   d a n s   l ' a s s i s t a n t   d e   p a i e   ( d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© p l a c e m e n t   e n   d e h o r s   d u   c o n t e n e u r   d u   t a b l e a u   p o u r   ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© v i t e r   l e s   c o n f l i t s   C S S ) .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   a n i m a t i o n   d ' a l e r t e   s u r   l e   b o u t o n   d e   r e c h e r c h e   l o r s q u e   l e   m o i s   o u   l ' a n n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   e s t   m o d i f i ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©   a f i n   d ' i n c i t e r   l ' u t i l i s a t e u r   ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â    a c t u a l i s e r   l e s   d o n n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e s .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   s e c t i o n   d e   s y n t h ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ s e   g l o b a l e   a f f i c h a n t   l e   t o t a l   d e s   p a i e m e n t s   n e t s ,   l e   t o t a l   d e s   p r i m e s   e t   l e   t o t a l   d e   l a   f i s c a l i t ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©   ( S S   +   I R G ) .  
 -   M o t e u r   d e   p a i e   :   a j o u t   d ' u n   n o u v e a u   m o d e   d e   c a l c u l   p o u r   l e s   r u b r i q u e s   e t   p r i m e s   ( ' J O U R S '   :   P a r   j o u r   t r a v a i l l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© )   p e r m e t t a n t   d e   m u l t i p l i e r   l e   m o n t a n t   s a i s i   p a r   l e   n o m b r e   d e   j o u r s   d e   p r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© s e n c e   d e   l ' e m p l o y ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© .  
 -   C o r r e c t i o n   d u   m e n u   l a t ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© r a l   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   o ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¹   l e   s o u s - m e n u   d e s   f i c h e s   d e   p a i e   f o r m a t e u r s   s ' a f f i c h a i t   c o m m e   a c t i f   ( e n   s u r b r i l l a n c e )   l o r s q u ' o n   s e   t r o u v a i t   s u r   l ' a s s i s t a n t   d e   p a i e   d e s   e m p l o y ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© s   ( p r o b l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ m e   d e   m a t c h i n g   d e   c h a ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â® n e   d e   c a r a c t ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ r e s ) .  
 -   I n t e r f a c e   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   ( s c r o l l   h o r i z o n t a l   i n d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© s i r a b l e )   s u r   l a   p a g e   d ' h i s t o r i q u e   d e s   f i c h e s   d e   p a i e   d e s   f o r m a t e u r s ,   c a u s ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©   p a r   u n   ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© m e n t   d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© c o r a t i f   q u i   d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© p a s s a i t   d e   l ' ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© c r a n .  
 -   A s s i s t a n t   d e   p a i e   :   e x c l u s i o n   a u t o m a t i q u e   d e s   e m p l o y ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© s   d o n t   l a   f i c h e   d e   p a i e   a   d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© j ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â    ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© t ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©   g ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   p o u r   l e   m o i s   e n   c o u r s   a f i n   d ' ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© v i t e r   l e s   d o u b l o n s   ( i l s   r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© a p p a r a ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â® t r o n t   s i   l e u r   f i c h e   e s t   a n n u l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e ) .  
 -   A s s i s t a n t   d e   p a i e   :   a f f i c h a g e   d ' u n e   v u e   d e   s y n t h ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ s e   ' P a i e   c l ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â´ t u r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   p o u r   c e   m o i s '   l o r s q u e   t o u t e s   l e s   f i c h e s   d e   p a i e   o n t   d ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© j ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â    ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© t ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©   g ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© r ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e s   p o u r   l e   m o i s   s ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© l e c t i o n n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© ,   r e m p l a ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ a n t   l e   m e s s a g e   d ' e r r e u r   ' A u c u n e   d o n n ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   d i s p o n i b l e ' .  
 -   C o r r e c t i o n   d e   l ' i n t e r f a c e   :   l ' i c ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â´ n e   d u   m e n u   ' A s s i s t a n t   d e   P a i e '   n e   s ' a f f i c h a i t   p a s   e n   r a i s o n   d ' u n e   c l a s s e   d ' i c ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â´ n e   i n e x i s t a n t e   d a n s   l a   b i b l i o t h ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨ q u e   u t i l i s ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e .   R e m p l a c ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© e   p a r   u n e   i c ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â´ n e   f o n c t i o n n e l l e   ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© q u i v a l e n t e .  
 
- IntÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©gration Paie-Finance : crÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ation d'un nouvel espace dans ComptabilitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©/Finance pour lister les ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©tats de paie et lancer les dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©penses associÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es de maniÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨re globale.

- Gestion des permissions : ajout de la vÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©rification de permission spÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©cifique (sous-menu paie_salaires) sur les vues de la paie dans ComptabilitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©/Finance, assurant le mÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âªme niveau de sÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©curitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© que les autres vues.

- Ajout d'un bouton de validation globale du mois dans /rh/paie/fiches/ avec envoi de notification au personnel configurÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© dans les paramÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨tres gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©raux.

- RÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©organisation de l'ordre des groupes dans l'onglet Gestion des modules (ParamÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨tres gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©raux) pour suivre un workflow plus logique : CRM -> Inscriptions -> TrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©sorerie -> ScolaritÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© -> Communication.

- Correction de la fenÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Âªtre modale de paiement dans /comptabilite/tresorerie/paies/liste/ qui ne s'ouvrait pas ou ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©tait bloquÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©e (dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©placement du code HTML de la modale en dehors de la balise 	able-responsive pour corriger les problÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨mes de z-index et d'overflow de Bootstrap).

- Ajout d'un champ 'Date de paiement effective' dans la modale de paiement de la paie (/comptabilite/tresorerie/paies/liste/) afin de permettre ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  l'utilisateur de spÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©cifier la date rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©elle du rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨glement (met ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  jour la dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©pense et les fiches de paie).

- CrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ation automatique d'une entrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©e OperationsBancaire lors du lancement de la dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©pense de paie (mode 'vir') pour que la dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©pense remonte dans le module d'Imputation Bancaire.

- TrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©sorerie : Regroupement des lignes par compte comptable associÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© dans la liste des imputations comptables des spÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©cialitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s (/comptabilite/tresorerie/imputation-comptable/specialite/liste/). Ajout d'une fonctionnalitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© d'accordÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©on (fermÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© par dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©faut) pour masquer/afficher les spÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©cialitÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©s liÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©es ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  chaque compte.
-   S ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© p a r a t i o n   d u   ' T o t a l   P r o p o s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© '   e n   ' R e c e t t e s   P r o p o s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e s '   e t   ' D ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© p e n s e s   P r o p o s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e s '   d a n s   l a   v u e    u d g e t _ c a m p a i g n _ r e v i e w   e t   s o n   t e m p l a t e   a s s o c i ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© . 
 
 -   C o r r e c t i o n   d u   c a l c u l   d e   l a   p r o g r e s s i o n   e t   d e   l ' ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© c a r t   r e s t a n t   d a n s   l a   v u e    u d g e t _ c a m p a i g n _ r e v i e w   :   l e   c a l c u l   e s t   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s o r m a i s   b a s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   u n i q u e m e n t   s u r   l e s   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© p e n s e s   p r o p o s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e s   a u   l i e u   d e   l a   s o m m e   d e s   r e c e t t e s   e t   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© p e n s e s . 
 
 -   A j o u t   d ' u n e   m e n t i o n   e x p l i c a t i v e   s o u s   l a   b a r r e   d e   p r o g r e s s i o n   d a n s   l a   v u e    u d g e t _ c a m p a i g n _ r e v i e w   p o u r   p r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© c i s e r   q u e   l e   c a l c u l   e s t   b a s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   s u r   l e s   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© p e n s e s . 
 
 -   A j o u t   d ' u n   t i t r e   d y n a m i q u e   ( ' D e m a n d e   d e   r a l l o n g e   -   { n o m _ c a m p a g n e } ' )   p o u r   l a   p a g e   d e   d e m a n d e   d e   r a l l o n g e   b u d g ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© t a i r e   ( 
 e q u e s t _ e x t e n s i o n ) . 
 
 -   D a n s   l a   l i s t e   d e s   c a m p a g n e s   b u d g ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© t a i r e s   (  u d g e t _ c a m p a i g n _ l i s t . h t m l ) ,   r e m p l a c e m e n t   d u   b o u t o n   ' C o n f i g u r e r   l e s   o b j e c t i f s '   p a r   ' C o n s u l t e r   l e s   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© t a i l s '   ( a v e c   u n e   i c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´ n e   d ' Si l )   l o r s q u e   l a   c a m p a g n e   e s t   a c t i v e . 
 
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d e s   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© t a i l s   d e   l a   d e m a n d e   d e   r a l l o n g e   ( 
 e v i e w _ e x t e n s i o n )   :   a f f i c h a g e   d u   n o m   d e   l ' e n t r e p r i s e   v i a   u n e   m a p   d e   c l ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s   e n   c h a ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â® n e s   d e   c a r a c t ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ r e s   e t   a j o u t   d u   m o n t a n t   t o t a l   d e m a n d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   d a n s   l a   s e c t i o n   ' D ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© t a i l s   d e   l a   d e m a n d e ' . 
 
 -   M o d e r n i s a t i o n   c o m p l ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ t e   d u   d e s i g n   d e   l a   p a g e   d ' e x a m e n   d e s   r a l l o n g e s   ( 
 e v i e w _ e x t e n s i o n . h t m l )   :   s t y l e   p r e m i u m   a v e c   g l a s s m o r p h i s m   a m ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© l i o r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© ,   n o u v e l l e s   p a l e t t e s   d e   c o u l e u r s ,   e f f e t s   d e   s u r v o l ,   b a d g e s   m o d e r n i s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s   e t   i n t ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© g r a t i o n   d e   n o m b r e u s e s   i c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´ n e s . 
 
 
- DÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©placement de la rubrique 'Gestion des ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â°chÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©anciers' sous la rubrique 'ParamÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¨tres Financiers' dans le menu de navigation (menu.html).

- TrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sorerie : Ajout de la configuration des rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rences de paiements dans le brouillard de banque (brouillard_banque.html) avec une interface modale calquÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e sur le fonctionnement du brouillard de caisse.

- TrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sorerie : Correction d'un problÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨me empÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âªchant la modification de la rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rence de paiement dans le brouillard de banque (ajout des champs item_id et model_type dans l'API json).

- Correction de l'affichage du montant total demandÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© dans la page de rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©vision des rallonges budgÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©taires (associe_app).

- TrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sorerie : Retrait des dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©corateurs de permission (@module_permission_required) sur les actions de suppression et modification des ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©chÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©anciers configurÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s (ApiDeleteEcheancier, ApiBulkDeleteEcheanciers, ApiUpdateEcheancier).

- TrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sorerie : Restauration des dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©corateurs de permission (@module_permission_required) sur les actions de suppression et modification des ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©chÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©anciers configurÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s suite ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  une erreur (ApiDeleteEcheancier, ApiBulkDeleteEcheanciers, ApiUpdateEcheancier).


### [Fixed] - 2026-06-06
- **TrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sorerie** : Correction du bug oÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¹ l'application d'une remise ne mettait pas ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  jour les montants des ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©chÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ances dans la base de donnÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es (DuePaiements) si l'inscription ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tait dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©jÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  confirmÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e. ModifiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© ApiApplyRemiseToPaiement dans 	_tresorerie/f_views/preinscrit_paiements.py pour recalculer et mettre ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  jour montant_due et montant_restant des tranches.
- **UI** : Deplacement du sous-menu Paie & Salaires juste en dessous du sous-menu Depenses dans le menu principal Comptabilite/Finance (menu.html).
- **UI** : Remplacement du menu deroulant d'actions par des boutons d'icones dans la liste des fournisseurs (liste_des_fournisseurs.html). Correction egalement des colonnes du filtre de recherche.
- **Backend** : Modification de l'assistant de paie (assistantPaie) pour prendre en compte et filtrer par entite_legal. Le dropdown 'entreprise' a ete ajoute a l'interface (assistant_paie.html).
- **Finance** : Mise ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  jour de la liste des paies (liste_paie_finance) pour grouper et afficher l'entitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© (entreprise) associÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  chaque fiche de paie. L'opÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ration de paiement (lancer_depense_paie) a ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©galement ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© ajustÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e pour crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©er des dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©penses distinctes par entitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©.
- **Finance** : Ajout d'une balise titre (title) sur la page des listes de paie Finance (liste_paie_finance.html). Ajout d'un formulaire de filtres complets (mois, annee, entreprise, statut de paiement) dans l'interface et gestion de ces filtres depuis la vue (views_paie.py).
- **Finance / Interface** : DÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©placement du formulaire des filtres de la liste des paies (liste_paie_finance.html) juste au-dessus du tableau des donnÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es, pour une meilleure clartÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© visuelle et ergonomie.
- **RH / Finance** : VÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rification complÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨te du traitement de la paie par entitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©. La notification envoyÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e par ApiValiderPaieMois inclut dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sormais le nom de l'entitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© si celle-ci a ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© spÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©cifiÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e lors de la validation.
- **TrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sorerie / Banque** : Ajout d'un tableau de bord affichant la situation de l'imputation bancaire (total opÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©rations, rapprochÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es, en attente) et la situation de recouvrement des chÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ques/virements sur la page du brouillard de banque. Ajout de raccourcis rapides vers les pages concernÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es.
- **RH / Formateurs** : Modernisation de l'interface des contrats (intÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©gration de DataTables pour la recherche/pagination, dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©placement du filtre d'entitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©, ajout d'actions rapides inline pour un workflow plus fluide).
- **RH / Formateurs** : Harmonisation du design de la modal de crÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ation/ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©dition de contrat pour un aspect plus premium (espacement, fonds teintÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s, bords arrondis, et icÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´nes).
- **RH / Formateurs** : Correction du design et de l'alignement des filtres DataTables (Affichage et Recherche) dans la liste des contrats.
- **RH / Formateurs** : Refonte totale de la disposition des filtres pour la liste des contrats. Les filtres (EntitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©, Recherche, Pagination) sont dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sormais placÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©s dans une carte dÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©diÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e au-dessus du tableau (Filter Section), harmonisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©e avec la vue fiches-mensuelles.
-   H a r m o n i s a t i o n   d e s   i c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´ n e s   d e   l ' E s p a c e   e m p l o y ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   a v e c   l ' E s p a c e   f o r m a t e u r   ( u t i l i s a t i o n   d e   B o x i c o n s   a u   l i e u   d e   R e m i x   I c o n s   d a n s   l e   m e n u   R H ) . 
 
 -   S u p p r e s s i o n   d e s   c e r c l e s   d e   c o u l e u r   a u t o u r   d e s   i c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´ n e s   d e s   s o u s - m e n u s   d e   l ' E s p a c e   e m p l o y ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   p o u r   c o r r e s p o n d r e   a u   s t y l e   s i m p l e   d e   l ' E s p a c e   f o r m a t e u r . 
 
 -   A j o u t   d e s   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© c o r a t e u r s   d e   p e r m i s s i o n s   m a n q u a n t s   ( @ m o d u l e _ p e r m i s s i o n _ r e q u i r e d   e t   @ r o l e _ r e q u i r e d )   s u r   l e s   v u e s   b u d g e t _ c a m p a i g n _ d i s p a t c h ,   r e q u e s t _ e x t e n s i o n   e t   b u d g e t _ c a m p a i g n _ r e a l i z a t i o n . 
 
 -   S u p p r e s s i o n   d e   l ' o n g l e t   F o r m a t i o n s   d a n s   l a   p a g e   / c o n s e i l / l i s t e - d e s - t h e m a t i q u e s / 
 
 -   A j o u t   d ' u n e   m o d a l e   p o u r   c o n f i g u r e r   e t   a j o u t e r   r a p i d e m e n t   d e s   p a r t i c i p a n t s   d e p u i s   l a   v u e   d e   c r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© a t i o n   d ' u n   n o u v e a u   g r o u p e   c o n s e i l . 
 
 -   M o d e r n i s a t i o n   d u   d e s i g n   d e   l a   m o d a l e   d ' a j o u t   r a p i d e   d ' u n   p a r t i c i p a n t   ( l a b e l s   f l o t t a n t s ,   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© g r a d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s ,   i c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´ n e s ,   g l a s s m o r p h i s m ) . 
 
 -   S u p p r e s s i o n   d e s   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© g r a d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s   d a n s   l a   m o d a l e   d ' a j o u t   r a p i d e   d e   p a r t i c i p a n t   p o u r   l ' h a r m o n i s e r   a v e c   l e   d e s i g n   g l o b a l   d u   p r o j e t   ( u t i l i s a t i o n   d e s   c l a s s e s   b g - p r i m a r y   e t   t e x t - p r i m a r y   s t a n d a r d ) . 
 
 -   A j o u t   d e s   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© c o r a t e u r s   @ m o d u l e _ p e r m i s s i o n _ r e q u i r e d   m a n q u a n t s   s u r   l ' e n s e m b l e   d e s   v u e s   e t   A P I s   d u   m o d u l e   C o n s e i l   ( t _ c o n s e i l )   p o u r   s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© c u r i s e r   l ' a c c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ s   a u x   p a g e s   e t   a u x   a c t i o n s . 
 
 -   A j o u t   d e   l a   s u p p r e s s i o n   e n   c a s c a d e   d e s   f a c t u r e s   d e   c o n s e i l   ( m ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âª m e   c e l l e s   v a l i d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e s ) ,   e n   s u p p r i m a n t   l e s   p a i e m e n t s ,   l e t t r a g e s   b a n c a i r e s   e t   r e m b o u r s e m e n t s   l i ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s ,   t o u t   e n   p r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s e r v a n t   l e   d e v i s   s o u r c e . 
 
 -   R ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© i n i t i a l i s a t i o n   d e   l ' ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© t a t   d u   c l i e n t   d a n s   l e   p i p e l i n e   ( r e t o u r   ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â    ' d e v i s _ e n v o y e '   o u   ' n e g o c i a t i o n ' )   l o r s   d e   l a   s u p p r e s s i o n   d ' u n e   f a c t u r e   d e   c o n s e i l . 
 
 -   S u p p r e s s i o n   d e   l a   c o n f i g u r a t i o n   d e s   d r o i t s   d e   t i m b r e   d a n s   l e   m o d u l e   C o n s e i l .   L a   g e s t i o n   e t   l e   c a l c u l   d e s   d r o i t s   d e   t i m b r e   s ' e f f e c t u e n t   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s o r m a i s   d e   m a n i ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ r e   c e n t r a l i s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e   v i a   l e s   p a r a m ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ t r e s   f i n a n c i e r s   d e   l a   T r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s o r e r i e . 
 
 -   I s o l a t i o n   d e   l a   c o n f i g u r a t i o n   d e s   T a x e s   &   F i s c a l i t ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   d a n s   l e   m o d u l e   C o n s e i l   :   l a   s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© l e c t i o n   d e   l ' e n t r e p r i s e   n ' i m p a c t e   p l u s   q u e   l e s   o n g l e t s   D o c u m e n t s ,   O f f r e s   R e m i s e s   e t   M e n t i o n s   L ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© g a l e s .   L a   T V A   e s t   g ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e   d e   m a n i ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ r e   g l o b a l e . 
 
 -   A m ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© l i o r a t i o n   d e   l ' e x p ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© r i e n c e   u t i l i s a t e u r   d a n s   l a   c r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© a t i o n   d e   d e v i s   ( c o n s e i l / n o u v e a u - d e v i s / )   :   l e   c h a m p   d e   s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© l e c t i o n   d u   c l i e n t   e s t   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s o r m a i s   f i l t r a b l e   v i a   S e l e c t 2 . 
 
 -   C o r r e c t i o n   d e   l ' e n c o d a g e   d e s   m e s s a g e s   ( A l e r t i f y   e t   D j a n g o   M e s s a g e s )   d a n s   l ' e n s e m b l e   d u   m o d u l e   C o n s e i l . 
 
 -   L e   c h a m p   d e   s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© l e c t i o n   d e   l a   t h ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© m a t i q u e   d a n s   l a   c o n f i g u r a t i o n   d ' u n   d e v i s   e s t   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s o r m a i s   f i l t r a b l e   v i a   S e l e c t 2 . 
 
 -   B l o c a g e   d e   l ' a c c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ s   a u x   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© t a i l s   d ' u n   d e v i s   t a n t   q u ' i l   n ' e s t   p a s   v a l i d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   ( b o u t o n   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s a c t i v ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   d a n s   l a   l i s t e   e t   r e d i r e c t i o n   s e r v e u r   s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© c u r i s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e ) . 
 
 -   A u t o - r e m p l i s s a g e   d e s   c o n d i t i o n s   c o m m e r c i a l e s   :   l o r s   d e   l a   c r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© a t i o n   d ' u n   d e v i s   o u   d ' u n e   f a c t u r e ,   l e s   c o n d i t i o n s   c o m m e r c i a l e s   p a r   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© f a u t   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© f i n i e s   d a n s   l a   c o n f i g u r a t i o n   g l o b a l e   s ' a p p l i q u e n t   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s o r m a i s   a u t o m a t i q u e m e n t . 
 
 -   M o d e r n i s a t i o n   d u   d e s i g n   d e s   l i g n e s   d e   d e v i s   ( i c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´ n e s ,   b a d g e s ,   b o u t o n s   a r r o n d i s )   d a n s   l e   f o r m u l a i r e   d e   c o n f i g u r a t i o n . 
 
 -   L e   c h a m p   d e   s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© l e c t i o n   d u   c l i e n t / p r o s p e c t   d a n s   l a   c r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© a t i o n   d ' u n e   n o u v e l l e   f a c t u r e   e s t   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s o r m a i s   f i l t r a b l e   v i a   S e l e c t 2 . 
 
 -   B l o c a g e   d e   l ' a c c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ s   a u x   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© t a i l s   d ' u n e   f a c t u r e   t a n t   q u ' e l l e   n ' e s t   p a s   v a l i d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e   ( b o u t o n   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s a c t i v ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   d a n s   l a   l i s t e   e t   r e d i r e c t i o n   s e r v e u r   s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© c u r i s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e ,   c o m m e   p o u r   l e s   d e v i s ) . 
 
 -   B l o c a g e   d e   l ' a c c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ s   ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â    l a   g ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© n ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© r a t i o n   d u   P D F   p o u r   l e s   f a c t u r e s   n o n   v a l i d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e s   ( b o u t o n   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s a c t i v ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   e t   r o u t e   s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© c u r i s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e ) . 
 
 -   A j u s t e m e n t   d u   d e s i g n   d e   l a   c o n f i g u r a t i o n   d e   f a c t u r e   :   r e p o s i t i o n n e m e n t   p r o p r e   d u   b a d g e   d e   s t a t u t   ( B r o u i l l o n )   d a n s   l e   c o i n   s u p ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© r i e u r   d r o i t   e t   r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© o r g a n i s a t i o n   d u   c h a m p   ' M o d e   d e   p a i e m e n t   a t t e n d u '   a u - d e s s u s   d e s   c o n d i t i o n s . 
 
 -   R e p o s i t i o n n e m e n t   d u   b a d g e   d e   s t a t u t   ( B r o u i l l o n )   :   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© p l a c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â    c ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â´ t ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   d u   t i t r e   p r i n c i p a l   p o u r   ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© v i t e r   t o u t   c h e v a u c h e m e n t   a v e c   l e   c o n t e n u   d u   d o c u m e n t . 
 
 -   I n t ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© g r a t i o n   d e   S e l e c t 2   d a n s   l a   c o n f i g u r a t i o n   d e s   f a c t u r e s   ( c o n s e i l / c o n f i g u r e - f a c t u r e . h t m l )   p o u r   r e n d r e   l a   s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© l e c t i o n   d e   l a   t h ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© m a t i q u e   f i l t r a b l e   a v e c   b a r r e   d e   r e c h e r c h e   i n t ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© g r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© e . 
 
 -   C o r r e c t i o n   d u   d e s i g n   d u   c h a m p   T h ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© m a t i q u e   ( S e l e c t 2 )   p o u r   q u ' i l   a d o p t e   l e   m ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âª m e   s t y l e   v i s u e l   q u e   l e s   a u t r e s   i n p u t s   ( f o r m - c o n t r o l - c u s t o m ) . 
 
 -   H a r m o n i s a t i o n   d u   d e s i g n   d e s   l i g n e s   d e   f a c t u r a t i o n   p o u r   c o r r e s p o n d r e   e x a c t e m e n t   ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â    c e l u i   d e s   d e v i s   ( a j o u t   d ' a v a t a r s   p o u r   l e s   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s i g n a t i o n s ,   s t y l e   d e s   b a d g e s   p o u r   q u a n t i t ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s / r e m i s e s ,   e t   b o u t o n s   d ' a c t i o n s   a r r o n d i s ) . 
 
 -   A j u s t e m e n t   C S S   d e   S e l e c t 2   ( T h ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© m a t i q u e )   :   f o r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â§ a g e   d e   l a   l a r g e u r   ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â    1 0 0 % ,   a j o u t   d u   m a r g i n - b o t t o m   m a n q u a n t   e t   a l i g n e m e n t   f l e x   p o u r   m a t c h e r   p a r f a i t e m e n t   l e s   d i m e n s i o n s   d e s   a u t r e s   c h a m p s   d u   f o r m u l a i r e . 
 
 -   C o r r e c t i o n   d u   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© b o r d e m e n t   d e   t e x t e   d a n s   l e   c h a m p   T h ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© m a t i q u e   S e l e c t 2   l o r s   d e   l a   s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© l e c t i o n   :   r e m p l a c e m e n t   d u   d i s p l a y :   f l e x   p a r   u n   p o s i t i o n n e m e n t   a b s o l u   p o u r   l e   b o u t o n   d e   s u p p r e s s i o n   ( x )   e t   l a   f l ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ c h e ,   a v e c   u n   t e x t - o v e r f l o w   ( p o i n t s   d e   s u s p e n s i o n )   p o u r   l e s   t e x t e s   t r o p   l o n g s . 
 
 -   N o u v e l l e   c o r r e c t i o n   S e l e c t 2   :   R e t o u r   ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â    l a   m ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© t h o d e   n a t i v e   d e   S e l e c t 2   ( v i a   l i n e - h e i g h t )   s a n s   f o r c e r   l e   f l e x   o u   l e   p o s i t i o n n e m e n t   a b s o l u ,   c e   q u i   r ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ g l e   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© f i n i t i v e m e n t   l e   b u g   v i s u e l   d u   b o u t o n   d e   s u p p r e s s i o n   ' x '   e t   l e   c h e v a u c h e m e n t   d u   t e x t e . 
 
 -   A j o u t   d ' u n   e s p a c e m e n t   ( m a r g i n - b o t t o m )   e n t r e   l e   c h a m p   S e l e c t 2   d e   T h ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© m a t i q u e   e t   l e   c h a m p   D ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s i g n a t i o n . 
 
 -   R e f o n t e   t o t a l e   d e   l a   z o n e   d ' a j o u t   d e   l i g n e   d e   f a c t u r a t i o n   :   i n t ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© g r a t i o n   d i r e c t e   d a n s   l e   t a b l e a u   e n   < t f o o t > ,   r e m p l a c e m e n t   d e s   d i v   p a r   u n   F l e x b o x   g a p - 2   p o u r   u n   e s p a c e m e n t   i n f a i l l i b l e   e t   a l i g n e m e n t   p a r f a i t   a v e c   l e   d e s i g n   d e s   d e v i s . 
 
 -   C o r r e c t i o n   d u   c e n t r a g e   v e r t i c a l   d u   t e x t e   d a n s   S e l e c t 2   :   s u p p r e s s i o n   d e s   m a r g e s   e t   p a d d i n g s   p a r   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© f a u t   q u i   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© c a l a i e n t   l e   t e x t e   v e r s   l e   b a s   a v e c   l a   h a u t e u r   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© f i n i e . 
 
 -   H a r m o n i s a t i o n   d e   l a   t a i l l e   d u   c h a m p   S e l e c t 2   ( T h ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© m a t i q u e )   p o u r   c o r r e s p o n d r e   e x a c t e m e n t   ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â    l a   h a u t e u r   e t   l a   t a i l l e   d e   p o l i c e   ( 1 2 p x )   d e s   c h a m p s   D ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© s i g n a t i o n   e t   D e s c r i p t i o n . 
 
 -   R e f o n t e   g l o b a l e   d e   l a   p a g e   C o n f i g u r a t i o n   F a c t u r e   p o u r   a d o p t e r   l e   d e s i g n   P r e m i u m   ( h a r m o n i s ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©   a v e c   l e   d e v i s )   :   s u p p r e s s i o n   d u   C S S   f a i t   m a i s o n   e t   a d o p t i o n   d e   c a r d - p r e m i u m ,   t a b l e - p r e m i u m ,   e t   d u   C S S   S e l e c t 2   o f f i c i e l   q u i   c o r r i g e   d ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© f i n i t i v e m e n t   l e   b u g   d e   l a   c r o i x . 
 
 
- **Refonte Workflow Conseil de Validation** : Modification du modÃƒÆ’Ã‚Â¨le ConseilValidation (ajout de statut 'ouvert'/'cloture'). Refonte de la page stage/council/ avec blocage de l'affichage des stages et des dÃƒÆ’Ã‚Â©cisions rapides si aucun conseil n'est actif. ImplÃƒÆ’Ã‚Â©mentation du design Premium (Glassmorphism) pour cette interface.

- **Design** : Harmonisation des interfaces d'Examens Finaux (Liste des groupes, Saisie des notes, Bulletins) avec le design Premium (Glassmorphism, bords arrondis) utilisÃƒÆ’Ã‚Â© sur la page Conseil de Validation.

- **Design** : Alignement de la CSS des tableaux et badges de council.html, list_groupes.html, saisie_notes.html, et bulletins.html avec la charte graphique de list_stages.html (Premium Look & Feel).

- **Bugfix** : Correction de l'erreur AttributeError ('str' object has no attribute 'strftime') lors de la crÃƒÆ’Ã‚Â©ation d'un Conseil de Validation. Le modÃƒÆ’Ã‚Â¨le gÃƒÆ’Ã‚Â¨re dÃƒÆ’Ã‚Â©sormais les dates transmises sous forme de chaÃƒÆ’Ã‚Â®ne de caractÃƒÆ’Ã‚Â¨res lors de l'enregistrement.

- **Conseil de Validation** : Modification de la vue et du template pour enregistrer et afficher les dÃƒÆ’Ã‚Â©cisions dÃƒÆ’Ã‚Â©jÃƒÆ’Ã‚Â  prises pour les stages lors d'un conseil (avec update_or_create pour ÃƒÆ’Ã‚Â©viter les doublons).

- **Conseil de Validation** : Ajout de la sÃƒÆ’Ã‚Â©lection des stages et groupes focus ÃƒÆ’Ã‚Â©valuÃƒÆ’Ã‚Â©s lors de la crÃƒÆ’Ã‚Â©ation d'un conseil. Mise ÃƒÆ’Ã‚Â  jour du modÃƒÆ’Ã‚Â¨le ConseilValidation (ManyToMany) et ajout des Select2 dans la modale.

- **Conseil de Validation** : Modification de la modale de crÃƒÆ’Ã‚Â©ation pour rendre la sÃƒÆ’Ã‚Â©lection des stages et groupes focus mutuellement exclusive via des boutons radio et du JavaScript.

- **Design** : Harmonisation de l'affichage des tableaux dans council.html avec le style premium de list_stages.html (avatars, barre de progression arrondie, espacements et boutons d'action).

- **Design (Refonte Totale)** : Remplacement des tableaux de la page Conseil par un espace de travail Kanban interactif. IntÃƒÆ’Ã‚Â©gration d'un panneau latÃƒÆ’Ã‚Â©ral (Offcanvas) pour la saisie des dÃƒÆ’Ã‚Â©cisions afin de ne pas perdre le contexte visuel du board Kanban.
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
 - Ajout de la possibilitÃƒÂ© de dÃƒÂ©finir un compte bancaire par dÃƒÂ©faut dans la configuration de conseil, et affichage de ses coordonnÃƒÂ©es (Nom et IBAN) sur la facture dolibare.

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
- Ajout de la gestion des Consultants pour le module Executive Education (Conseil). CRUD complet et intÃƒÆ’Ã‚Â©gration au Wizard de crÃƒÆ’Ã‚Â©ation de groupes conseil.

- Deplacement du menu Consultants sous Groupes et Sessions et harmonisation du header de la page.

- Correction du comportement de la modale de modification/suppression des consultants (dÃƒÆ’Ã‚Â©placement des divs hors de la balise table pour ÃƒÆ’Ã‚Â©viter les bugs Bootstrap de backdrop).

- IntÃƒÆ’Ã‚Â©gration de Select2 dans la phase 4 du Wizard de crÃƒÆ’Ã‚Â©ation de groupes conseil pour rendre la sÃƒÆ’Ã‚Â©lection des intervenants filtrable (recherchable).

- Correction de l'erreur NoReverseMatch sur la page des dÃƒÆ’Ã‚Â©tails du groupe lorsque le groupe est rattachÃƒÆ’Ã‚Â© uniquement ÃƒÆ’Ã‚Â  une facture (sans devis).

- Ajout de la possibilitÃƒÆ’Ã‚Â© de crÃƒÆ’Ã‚Â©er un groupe conseil ÃƒÆ’Ã‚Â  partir d'un devis ÃƒÆ’Ã‚Â  l'ÃƒÆ’Ã‚Â©tat 'envoyÃƒÆ’Ã‚Â©' (en plus de l'ÃƒÆ’Ã‚Â©tat 'acceptÃƒÆ’Ã‚Â©').

- Ajout d'un avertissement lors de la conversion d'un devis en facture pour rappeler ÃƒÆ’Ã‚Â  l'utilisateur si les informations lÃƒÆ’Ã‚Â©gales de l'entreprise (RC, NIF, NIS, NÃƒâ€šÃ‚Â° ART) sont manquantes.

- Harmonisation du design de la fenÃƒÆ’Ã‚Âªtre modale de saisie d'un paiement sur la page des dÃƒÆ’Ã‚Â©tails de la facture (look premium et alignement avec le reste de l'UI).

- Ajout d'un CSS personnalisÃƒÆ’Ã‚Â© (@page { margin: 0.5cm; }) pour les modÃƒÆ’Ã‚Â¨les de factures et devis gÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©rÃƒÆ’Ã‚Â©s par l'ÃƒÆ’Ã‚Â©diteur de documents.


### 2026-06-10
- **TrÃƒÆ’Ã‚Â©sorerie/Configuration**: Ajout de la configuration du format de numÃƒÆ’Ã‚Â©rotation des quittances (prÃƒÆ’Ã‚Â©fixe et suffixe) au niveau des entitÃƒÆ’Ã‚Â©s (Entreprise). Le modÃƒÆ’Ã‚Â¨le Paiements formatte dÃƒÆ’Ã‚Â©sormais automatiquement le numÃƒÆ’Ã‚Â©ro selon cette configuration de l'entitÃƒÆ’Ã‚Â©.
- **TrÃƒÆ’Ã‚Â©sorerie/Configuration**: DÃƒÆ’Ã‚Â©placement de la configuration de la numÃƒÆ’Ã‚Â©rotation des quittances vers la page de configuration de paiement/facturation (config_paiement_facturation.html). Ajout de la vue ApiUpdateQuittanceFormat.
- **TrÃƒÆ’Ã‚Â©sorerie/Configuration**: Modification du systÃƒÆ’Ã‚Â¨me de configuration de numÃƒÆ’Ã‚Â©rotation des quittances pour utiliser un format complet avec tag {seq}. Ajout de la longueur configurable de sÃƒÆ’Ã‚Â©quence.
- **UI/UX TrÃƒÆ’Ã‚Â©sorerie**: Refonte complÃƒÆ’Ã‚Â¨te du design de la page de configuration de paiement/facturation en utilisant une navigation par onglets verticaux (Premium Look & Feel).
- Normalisation des icÃƒÆ’Ã‚Â´nes dans menu.html (public et tenant) : utilisation exclusive de boxicons (x-*) et suppression des couleurs (	ext-*) sur les icÃƒÆ’Ã‚Â´nes.

- Nettoyage supplmentaire : suppression des couleurs de fond (g-*) appliques aux conteneurs d'icnes (.submenu-icon) dans les menus, en particulier dans la section RH / Espace Employ.

- Correction : Ajout de rgles CSS spcifiques dans menu.html pour forcer les icnes (.bx) et les arrire-plans .submenu-icon  prendre une couleur neutre (gris #6a7187 et #f3f6f9) afin d'craser le bleu par dfaut du thme.

- Correction (Bug) : Rparation de l'erreur de syntaxe de template Django caus par la modification prcdente (les apostrophes de fin pour les conditions url_name in avaient t accidentellement remplaces par des guillemets).

 
 - **TrÃƒÆ’Ã‚Â©sorerie/DÃƒÆ’Ã‚Â©penses** : Transformation du systÃƒÆ’Ã‚Â¨me d'enregistrement des dÃƒÆ’Ã‚Â©penses pour supporter un format multi-lignes. Ajout d'une gestion dynamique des taux de TVA par article (0%, 9%, 19%) et calcul automatique du Droit de Timbre (1% du TTC, min 5 DA, max 2500 DA) pour les paiements en espÃƒÆ’Ã‚Â¨ces. Refonte complÃƒÆ’Ã‚Â¨te de la page de crÃƒÆ’Ã‚Â©ation (
ouvelle_depense.html) et des vues de l'API.
- **TrÃƒÆ’Ã‚Â©sorerie/DÃƒÆ’Ã‚Â©penses** : Suppression du champ 'CatÃƒÆ’Ã‚Â©gorie' global de la dÃƒÆ’Ã‚Â©pense. Les catÃƒÆ’Ã‚Â©gories sont dÃƒÆ’Ã‚Â©sormais affectÃƒÆ’Ã‚Â©es uniquement au niveau de chaque ligne d'article.
- **TrÃƒÆ’Ã‚Â©sorerie/DÃƒÆ’Ã‚Â©penses** : Correction de l'erreur 500 sur ApiListeDepenses due ÃƒÆ’Ã‚Â  la rÃƒÆ’Ã‚Â©fÃƒÆ’Ã‚Â©rence rÃƒÆ’Ã‚Â©siduelle ÃƒÆ’Ã‚Â  \category__name\ aprÃƒÆ’Ã‚Â¨s la suppression du champ.
- **TrÃƒÆ’Ã‚Â©sorerie/DÃƒÆ’Ã‚Â©penses** : ÃƒÆ’Ã¢â‚¬Â°largissement du formulaire de crÃƒÆ’Ã‚Â©ation de dÃƒÆ’Ã‚Â©pense pour utiliser toute la largeur de l'ÃƒÆ’Ã‚Â©cran (\col-12\).
- **TrÃƒÆ’Ã‚Â©sorerie/DÃƒÆ’Ã‚Â©penses** : Ajout de la fonctionnalitÃƒÆ’Ã‚Â© de filtrage (recherche) sur le champ CatÃƒÆ’Ã‚Â©gorie pour chaque ligne de dÃƒÆ’Ã‚Â©pense grÃƒÆ’Ã‚Â¢ce ÃƒÆ’Ã‚Â  Select2.
- **TrÃƒÆ’Ã‚Â©sorerie/DÃƒÆ’Ã‚Â©penses** : Ajout du champ \
eference_document\ pour permettre de saisir la rÃƒÆ’Ã‚Â©fÃƒÆ’Ã‚Â©rence du document d'achat (ex: NÃƒâ€šÃ‚Â° Facture, BL) en plus de la piÃƒÆ’Ã‚Â¨ce justificative. Le champ a ÃƒÆ’Ã‚Â©tÃƒÆ’Ã‚Â© intÃƒÆ’Ã‚Â©grÃƒÆ’Ã‚Â© dans la crÃƒÆ’Ã‚Â©ation, modification et affichage des dÃƒÆ’Ã‚Â©tails.
- **TrÃƒÆ’Ã‚Â©sorerie/DÃƒÆ’Ã‚Â©penses** : Suppression temporaire de la section \Paiement & DÃƒÆ’Ã‚Â©tails\ du formulaire de crÃƒÆ’Ã‚Â©ation de dÃƒÆ’Ã‚Â©pense, car la gestion des paiements sera traitÃƒÆ’Ã‚Â©e sÃƒÆ’Ã‚Â©parÃƒÆ’Ã‚Â©ment dans une ÃƒÆ’Ã‚Â©tape ultÃƒÆ’Ã‚Â©rieure.
- **TrÃƒÆ’Ã‚Â©sorerie/DÃƒÆ’Ã‚Â©penses** : Remplacement de la fenÃƒÆ’Ã‚Âªtre modale par une page complÃƒÆ’Ã‚Â¨te (\/comptabilite/tresorerie/depenses/details/\) pour la consultation des dÃƒÆ’Ã‚Â©tails d'une dÃƒÆ’Ã‚Â©pense. Ajout de l'affichage dÃƒÆ’Ã‚Â©taillÃƒÆ’Ã‚Â© de toutes les lignes associÃƒÆ’Ã‚Â©es ÃƒÆ’Ã‚Â  la dÃƒÆ’Ã‚Â©pense dans cette nouvelle vue.
- **TrÃƒÆ’Ã‚Â©sorerie/DÃƒÆ’Ã‚Â©penses** : Harmonisation de l'interface de la page \details_depense.html\ pour qu'elle corresponde exactement au design moderne et ÃƒÆ’Ã‚Â©purÃƒÆ’Ã‚Â© de \
ouvelle_depense.html\ (carte pleine largeur, en-tÃƒÆ’Ã‚Âªte premium, rÃƒÆ’Ã‚Â©sumÃƒÆ’Ã‚Â© financier clair).
- **Menu de Navigation** : Mise ÃƒÆ’Ã‚Â  jour du fichier \menu.html\ pour s'assurer que le sous-menu \DÃƒÆ’Ã‚Â©penses\ et le lien \Liste des dÃƒÆ’Ã‚Â©penses\ restent visuellement actifs lors de la consultation de la nouvelle page de dÃƒÆ’Ã‚Â©tails d'une dÃƒÆ’Ã‚Â©pense (\PageDetailDepense\).
- **Fournisseurs** : Harmonisation du design de la page \liste_des_fournisseurs.html\ (en-tÃƒÆ’Ã‚Âªte, section KPI, boutons d'action et filtres) pour qu'elle corresponde au style \glass-card\ haut de gamme de la page \ttentes_de_paiements.html\.
- **Fournisseurs** : Harmonisation du design de la page \details_fournisseur.html\ avec la page de dÃƒÆ’Ã‚Â©tails client (style glass-card, banniÃƒÆ’Ã‚Â¨re de profil, KPIs financiers, navigation par onglets).
- **Fournisseurs / DÃƒÆ’Ã‚Â©penses** : Ajout de la rÃƒÆ’Ã‚Â©cupÃƒÆ’Ã‚Â©ration et de l'affichage de l'historique des dÃƒÆ’Ã‚Â©penses liÃƒÆ’Ã‚Â©es au fournisseur dans la page de dÃƒÆ’Ã‚Â©tails (\PageDetailsFournisseur\), incluant le calcul dynamique des KPIs (Total AchetÃƒÆ’Ã‚Â©, Total PayÃƒÆ’Ã‚Â©, Reste ÃƒÆ’Ã‚Â  Payer).
- **TrÃƒÆ’Ã‚Â©sorerie** : DÃƒÆ’Ã‚Â©couplage complet de la logique de Remboursements par rapport aux DÃƒÆ’Ã‚Â©penses. Ajout du lien \
emboursement\ dans \OperationsBancaire\. Mise ÃƒÆ’Ã‚Â  jour des journaux de caisse (Brouillards EspÃƒÆ’Ã‚Â¨ce et Banque) et de l'imputation bancaire pour traiter nativement les remboursements.
- **TrÃƒÆ’Ã‚Â©sorerie** : DÃƒÆ’Ã‚Â©sactivation et masquage du bouton de demande de remboursement dans les pages de dÃƒÆ’Ã‚Â©tails de demande de paiement (standard et double).
- **TrÃƒÆ’Ã‚Â©sorerie** : Remplacement de l'affectation automatique LIFO par une ventilation manuelle (input modifiable) dans le modal de confirmation de remboursement (details_rembourssement.html).
- **TrÃƒÆ’Ã‚Â©sorerie** : ÃƒÆ’Ã¢â‚¬Â°largissement de la fenÃƒÆ’Ã‚Âªtre modale de confirmation de remboursement (modal-lg vers modal-xl) pour un meilleur affichage de la ventilation manuelle.
- **TrÃƒÆ’Ã‚Â©sorerie** : Nettoyage du template details_rembourssement.html (retrait de la sÃƒÆ’Ã‚Â©lection de la 'CatÃƒÆ’Ã‚Â©gorie de dÃƒÆ’Ã‚Â©pense' et remplacement des mentions 'DÃƒÆ’Ã‚Â©clencher la dÃƒÆ’Ã‚Â©pense' par 'Traiter le remboursement') suite au dÃƒÆ’Ã‚Â©couplage des remboursements et des dÃƒÆ’Ã‚Â©penses.
- **TrÃƒÆ’Ã‚Â©sorerie** : Ajout du champ category au modÃƒÆ’Ã‚Â¨le Rembourssements et restauration de la sÃƒÆ’Ã‚Â©lection du Compte / CatÃƒÆ’Ã‚Â©gorie dans la modale de remboursement, permettant un regroupement analytique des sorties sans crÃƒÆ’Ã‚Â©er de dÃƒÆ’Ã‚Â©pense.
- **TrÃƒÆ’Ã‚Â©sorerie** : Correction d'une erreur fatale (\TypeError: __str__ returned non-string\) sur la page d'exploration de donnÃƒÆ’Ã‚Â©es causÃƒÆ’Ã‚Â©e par les mÃƒÆ’Ã‚Â©thodes \__str__\ des modÃƒÆ’Ã‚Â¨les \Rembourssements\, \SeuilPaiements\ et \PromoRembourssement\ qui retournaient des objets (ForeignKeys) ou des Decimal au lieu de chaÃƒÆ’Ã‚Â®nes de caractÃƒÆ’Ã‚Â¨res.
- **Global** : Correction d'autres erreurs fatales \TypeError\ similaires causÃƒÆ’Ã‚Â©es par la mÃƒÆ’Ã‚Â©thode \__str__\ dans d'autres modÃƒÆ’Ã‚Â¨les de trÃƒÆ’Ã‚Â©sorerie (ex: \ClientPaiementsRequest\, \clientPaiementsRequestLine\, \EcheancierPaiementLine\, \EcheancierPaiementSpecialLine\).
- **Global** : Automatisation de la correction de TOUS les modÃƒÆ’Ã‚Â¨les Django du projet pour qu'aucune mÃƒÆ’Ã‚Â©thode \__str__\ ne retourne un objet ou \None\ lorsqu'elle est appelÃƒÆ’Ã‚Â©e sur un enregistrement vide (notamment avec les champs \get_..._display()\, \label\, \designation\, \
om\, etc.). L'explorateur de donnÃƒÆ’Ã‚Â©es est dÃƒÆ’Ã‚Â©sormais parfaitement stable.
- **TrÃƒÆ’Ã‚Â©sorerie / Remboursements** : Correction du ciblage de la fenÃƒÆ’Ã‚Âªtre modale \
efundModal\ lors d'une demande de remboursement pour qu'elle se ferme correctement et que le tableau se rafraÃƒÆ’Ã‚Â®chisse automatiquement via \loadRemboursementsData()\.
- **TrÃƒÆ’Ã‚Â©sorerie / Liste des Remboursements** : DÃƒÆ’Ã‚Â©sactivation de la possibilitÃƒÆ’Ã‚Â© d'effectuer un remboursement tant que celui-ci n'a pas ÃƒÆ’Ã‚Â©tÃƒÆ’Ã‚Â© traitÃƒÆ’Ã‚Â© (ApprouvÃƒÆ’Ã‚Â©) dans la section principale des remboursements.
- **TrÃƒÆ’Ã‚Â©sorerie / Liste des Remboursements** : Masquage du bouton 'DÃƒÆ’Ã‚Â©tails' pour les remboursements dont le statut est 'En cours de traitement'.
- **TrÃƒÆ’Ã‚Â©sorerie / Liste des Remboursements** : Ajout du badge 'En attente de traitement' dans la colonne Action lorsque le remboursement est ÃƒÆ’Ã‚Â  l'ÃƒÆ’Ã‚Â©tat 'enc'.
- **Tableau de Bord / Configuration (SaaS Admin)** : Correction d'une erreur \FieldError: Cannot resolve keyword 'category' into field\ sur la page de configuration, survenue suite ÃƒÆ’Ã‚Â  la restructuration des dÃƒÆ’Ã‚Â©penses. Les calculs budgÃƒÆ’Ã‚Â©taires parcourent dÃƒÆ’Ã‚Â©sormais les catÃƒÆ’Ã‚Â©gories associÃƒÆ’Ã‚Â©es aux lignes de chaque dÃƒÆ’Ã‚Â©pense (\DepenseLigne\) plutÃƒÆ’Ã‚Â´t qu'ÃƒÆ’Ã‚Â  la dÃƒÆ’Ã‚Â©pense globale.
- **Tableau de Bord Budget** : IntÃƒÆ’Ã‚Â©gration des remboursements (traitÃƒÆ’Ã‚Â©s et catÃƒÆ’Ã‚Â©gorisÃƒÆ’Ã‚Â©s) dans le calcul du suivi de rÃƒÆ’Ã‚Â©alisation budgÃƒÆ’Ã‚Â©taire. Les remboursements partiels ou intÃƒÆ’Ã‚Â©graux apparaissent dÃƒÆ’Ã‚Â©sormais automatiquement en tant que *DÃƒÆ’Ã‚Â©pense* sous leur poste budgÃƒÆ’Ã‚Â©taire correspondant, reflÃƒÆ’Ã‚Â©tant ainsi la sortie d'argent rÃƒÆ’Ã‚Â©elle dans le budget.
- **Tableau de Bord Budget** : Ajustement du calcul du budget : Les remboursements sont dÃƒÆ’Ã‚Â©sormais dÃƒÆ’Ã‚Â©duits directement des recettes (paiements initiaux) au lieu d'ÃƒÆ’Ã‚Âªtre comptabilisÃƒÆ’Ã‚Â©s comme dÃƒÆ’Ã‚Â©penses. Cela permet d'afficher la recette nette rÃƒÆ’Ã‚Â©elle sans fausser le solde global par un double comptage.
- **Tableau de Bord Budget** : RÃƒÆ’Ã‚Â©intÃƒÆ’Ã‚Â©gration des remboursements dans la section DÃƒÆ’Ã‚Â©penses du budget. Ainsi, le montant est dÃƒÆ’Ã‚Â©duit de la recette (pour afficher la recette nette) ET apparaÃƒÆ’Ã‚Â®t en tant que dÃƒÆ’Ã‚Â©pense sous la catÃƒÆ’Ã‚Â©gorie choisie, rÃƒÆ’Ã‚Â©pondant ÃƒÆ’Ã‚Â  la demande d'affichage spÃƒÆ’Ã‚Â©cifique de l'utilisateur.
- **ComptabilitÃƒÆ’Ã‚Â© / DÃƒÆ’Ã‚Â©penses** : Correction d'une erreur \TypeError: unexpected keyword arguments 'category_id'\ lors de la crÃƒÆ’Ã‚Â©ation d'une nouvelle dÃƒÆ’Ã‚Â©pense, due ÃƒÆ’Ã‚Â  un reliquat de l'ancienne structure oÃƒÆ’Ã‚Â¹ la catÃƒÆ’Ã‚Â©gorie ÃƒÆ’Ã‚Â©tait liÃƒÆ’Ã‚Â©e ÃƒÆ’Ã‚Â  la dÃƒÆ’Ã‚Â©pense globale au lieu de ses lignes.
-   A c t u a l i s a t i o n   d e   l a   p a g e   a p r ÃƒÂ¨ s   g ÃƒÂ© n ÃƒÂ© r a t i o n   d ' u n e   f a c t u r e   d a n s   l e s   d ÃƒÂ© t a i l s   d e   p a i e m e n t   ( s t a n d a r d   e t   d o u b l e ) 
 
 -   A j o u t   d e s   r e m b o u r s e m e n t s   e n   e s p ÃƒÂ¨ c e s   d a n s   l e   b r o u i l l a r d   d e   c a i s s e 
 
 -   C o r r e c t i o n   d ' u n e   e r r e u r   5 0 0   ( T y p e E r r o r )   l o r s   d u   t r i   c h r o n o l o g i q u e   d e s   m o u v e m e n t s   d e   c a i s s e 
 
 -   F o r m a t a g e   d e   l a   d a t e   d e   r e m b o u r s e m e n t   p o u r   n ' a f f i c h e r   q u e   l a   d a t e   s a n s   l ' h e u r e   d a n s   l e   J S O N 
 
 -   C o r r e c t i o n   d e   l ' e s p a c e m e n t   p o u r   l e   m o d e   d e   p a i e m e n t   e t   l e   s t a t u t   ( D ÃƒÂ© p e n s e   d ÃƒÂ© c l e n c h ÃƒÂ© e )   d a n s   l a   l i s t e   d e s   r e m b o u r s e m e n t s 
 
 -   C o r r e c t i o n   d e s   p r o b l ÃƒÂ¨ m e s   d ' e n c o d a g e   s u r   l e   m o d ÃƒÂ¨ l e   R e m b o u r s e m e n t s   ( E s p ÃƒÂ¨ c e ,   C h ÃƒÂ¨ q u e ,   e t c . ) 
 
 -   I m p l ÃƒÂ© m e n t a t i o n   d e   l a   p r o c ÃƒÂ© d u r e   l ÃƒÂ© g a l e   d e   c o n t r e - p a s s a t i o n   ( g ÃƒÂ© n ÃƒÂ© r a t i o n   d e   q u i t t a n c e   n ÃƒÂ© g a t i v e   a u   l i e u   d e   s u p p r e s s i o n )   l o r s   d e   l ' a n n u l a t i o n   d ' u n   c h ÃƒÂ¨ q u e   o u   v i r e m e n t   n o n   e n c a i s s ÃƒÂ© 
 
 -   C o r r e c t i o n   d e   l ' e n c o d a g e   d u   m o d e   d e   p a i e m e n t   e t   d u   c o n t e x t e   p o u r   l e   m o d ÃƒÂ¨ l e   P a i e m e n t s 
 
 -   C o r r e c t i o n   d e   l a   f e r m e t u r e   d e   l a   m o d a l e   d e   d e m a n d e   d e   r e m b o u r s e m e n t   ( B o o t s t r a p   5 )   e t   r a f r a ÃƒÂ® c h i s s e m e n t   d e   l a   l i s t e 
 
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d u   m o n t a n t   a b s o l u   d a n s   l e s   b r o u i l l a r d s   d e   c a i s s e   e t   b a n q u e   p o u r   ÃƒÂ© v i t e r   l ' a p p a r i t i o n   d u   s i g n e   + - 
 
 -   P r i s e   e n   c o m p t e   d e   l ' a n n u l a t i o n   d ' u n   c h ÃƒÂ¨ q u e   n o n   e n c a i s s ÃƒÂ©   d a n s   l ' i m p u t a t i o n   b a n c a i r e   ( m a s q u a g e   d e   l ' o p ÃƒÂ© r a t i o n   d ' e n t r ÃƒÂ© e   e t   n o n   c r ÃƒÂ© a t i o n   d ' u n e   s o r t i e ) 
 
 -   C o r r e c t i o n   d e   l ' e r r e u r   l o a d R e m b o u r s e m e n t s D a t a   i s   n o t   d e f i n e d   d a n s   l i s t e - d e s - r e m b o u r s s e m e n t . h t m l   e n   r e n d a n t   l a   f o n c t i o n   g l o b a l e . 
 
 -   R a j o u t   d u   m o d e   d e   p a i e m e n t   d a n s   l a   l i s t e   d e s   p a i e m e n t s   d e   l a   f e n ÃƒÂª t r e   d e   v e n t i l a t i o n   d e   r e m b o u r s e m e n t   ( d e t a i l s _ r e m b o u r s s e m e n t . h t m l ) . 
 
 -   T r i   c h r o n o l o g i q u e   i n v e r s ÃƒÂ©   ( d u   p l u s   r ÃƒÂ© c e n t   a u   p l u s   a n c i e n )   d e s   o p ÃƒÂ© r a t i o n s   d e   c a i s s e   ( e t   b a n q u e )   p o u r   c h a q u e   j o u r n ÃƒÂ© e   a f f i c h ÃƒÂ© e   d a n s   l e   b r o u i l l a r d . 
 
 -   C o r r e c t i o n   d e   l ' o r d r e   d ' a f f i c h a g e   d a n s   l e   b r o u i l l a r d   :   U t i l i s a t i o n   d u   t i m e s t a m p   ( c r e a t e d _ a t )   p o u r   t r i e r   v ÃƒÂ© r i t a b l e m e n t   l e s   o p ÃƒÂ© r a t i o n s   d e   m a n i ÃƒÂ¨ r e   c h r o n o l o g i q u e   a v a n t   d e   l e s   i n v e r s e r . 
 
 -   C o r r e c t i o n   d e s   s t a t i s t i q u e s   d u   b r o u i l l a r d   b a n q u e   :   e x c l u s i o n   d e s   p a i e m e n t s   r e m b o u r s ÃƒÂ© s   ( p a i e m e n t _ _ i s _ r e f u n d = T r u e )   p o u r   r e f l ÃƒÂ© t e r   c o r r e c t e m e n t   l e   n o m b r e   r ÃƒÂ© e l   d ' i m p u t a t i o n s   b a n c a i r e s   e n   a t t e n t e . 
 
 -   F e n ÃƒÂª t r e   m o d a l e   d e   r e m b o u r s e m e n t   :   E x c l u s i o n   d e s   p a i e m e n t s   c o r r e s p o n d a n t   a u x   f r a i s   d ' i n s c r i p t i o n   p o u r   ÃƒÂ© v i t e r   t o u t e   a l l o c a t i o n   a c c i d e n t e l l e   s u r   c e s   m o n t a n t s . 
 
 -   I m p u t a t i o n   B a n c a i r e   :   I n t ÃƒÂ© g r a t i o n   d e s   o p ÃƒÂ© r a t i o n s   b a n c a i r e s   d e   t y p e   r e m b o u r s e m e n t   ( s o r t i e s )   d a n s   l a   p a g e   d ' i m p u t a t i o n .   C e s   o p ÃƒÂ© r a t i o n s   ÃƒÂ© t a i e n t   a u p a r a v a n t   m a s q u ÃƒÂ© e s ,   c e   q u i   c r ÃƒÂ© a i t   u n e   i n c o h ÃƒÂ© r e n c e   e n t r e   l e s   s t a t i s t i q u e s   d u   b r o u i l l a r d   e t   l a   l i s t e   d e s   o p ÃƒÂ© r a t i o n s   ÃƒÂ    i m p u t e r . 
 
 -   L i s t e   d e s   r e m b o u r s e m e n t s   :   A f f i c h a g e   e x c l u s i f   d e s   m o n t a n t s   e n c a i s s ÃƒÂ© s   ( e s p ÃƒÂ¨ c e s   o u   c h ÃƒÂ¨ q u e s / v i r e m e n t s   m a r q u ÃƒÂ© s   c o m m e   r ÃƒÂ© g l ÃƒÂ© s )   d a n s   l e   c a l c u l   d u   t o t a l   p a y ÃƒÂ©   p o u r   c h a q u e   l i g n e ,   y   c o m p r i s   d a n s   l a   m o d a l e   d e   d e m a n d e   d e   r e m b o u r s e m e n t . 
 
 -   L i s t e   d e s   r e m b o u r s e m e n t s   :   A f f i c h a g e   d u   m o n t a n t   ' E n   a t t e n t e   d ' e n c a i s s e m e n t '   ( c h ÃƒÂ¨ q u e s   o u   v i r e m e n t s   n o n   e n c o r e   v a l i d ÃƒÂ© s )   e n   d e s s o u s   d u   t o t a l   e n c a i s s ÃƒÂ© ,   ÃƒÂ    l a   f o i s   d a n s   l e   t a b l e a u   p r i n c i p a l   e t   d a n s   l a   f e n ÃƒÂª t r e   m o d a l e   d e   r e c h e r c h e . 
 
 -   D ÃƒÂ© t a i l s   d u   r e m b o u r s e m e n t   &   M o d a l e   d ÃƒÂ© t a i l s   ( L i s t e )   :   D a n s   l ' o n g l e t   Ãƒâ€° c h ÃƒÂ© a n c i e r ,   l a   c o l o n n e   ' M o n t a n t   P a y ÃƒÂ© '   a   ÃƒÂ© t ÃƒÂ©   r e n o m m ÃƒÂ© e   ' M o n t a n t   E n c a i s s ÃƒÂ© '   p o u r   n ' a f f i c h e r   q u e   l e s   p a i e m e n t s   v a l i d ÃƒÂ© s ,   e t   u n e   n o u v e l l e   c o l o n n e   ' E n   A t t e n t e '   a   ÃƒÂ© t ÃƒÂ©   a j o u t ÃƒÂ© e   p o u r   l e s   p a i e m e n t s   n o n   e n c o r e   v a l i d ÃƒÂ© s . 
 
 -   L i s t e   &   D ÃƒÂ© t a i l s   d e s   r e m b o u r s e m e n t s   :   M i s e   ÃƒÂ    j o u r   d e s   m o d a l e s   d e   ' D e m a n d e   d e   r e m b o u r s e m e n t '   e t   ' T r a i t e m e n t   d e   r e m b o u r s e m e n t '   p o u r   q u ' e l l e s   n ' a f f i c h e n t   e t   n ' a u t o r i s e n t   l e   r e m b o u r s e m e n t   q u e   s u r   l a   b a s e   d u   ' M o n t a n t   e n c a i s s ÃƒÂ© '   ( e x c l u a n t   l e s   c h ÃƒÂ¨ q u e s / v i r e m e n t s   e n   a t t e n t e ) . 
 
 -   M o d a l   d e   D ÃƒÂ© t a i l s   ( R e m b o u r s e m e n t )   :   L ' o n g l e t   Ãƒâ€° c h ÃƒÂ© a n c i e r   a   ÃƒÂ© t ÃƒÂ©   s u p p r i m ÃƒÂ©   e t   s o n   c o n t e n u   a   ÃƒÂ© t ÃƒÂ©   i n t ÃƒÂ© g r ÃƒÂ©   d i r e c t e m e n t   d a n s   l ' o n g l e t   ' R ÃƒÂ© s u m ÃƒÂ©   &   D e m a n d e '   a v e c   u n e   p r ÃƒÂ© s e n t a t i o n   m o d e r n i s ÃƒÂ© e . 
 
 -   M o d a l   d e   D ÃƒÂ© t a i l s   ( R e m b o u r s e m e n t )   :   M o d e r n i s a t i o n   d e   l ' a f f i c h a g e   d e s   s e c t i o n s   ' I n f o r m a t i o n s   Ãƒâ€° t u d i a n t '   e t   ' D ÃƒÂ© t a i l s   R e m b o u r s e m e n t '   ( r e m p l a c e m e n t   d e s   c h a m p s   f o r m u l a i r e s   p a r   u n   d e s i g n   s o u s   f o r m e   d e   c a r t e s   ÃƒÂ© l ÃƒÂ© g a n t e s ) . 
 
 -   G e s t i o n   d e s   R e m b o u r s e m e n t s   :   P o s s i b i l i t ÃƒÂ©   d e   t r a i t e r   e t   a c c e p t e r   u n e   d e m a n d e   d e   r e m b o u r s e m e n t   ( c o m m e   u n e   s i m p l e   c o n f i r m a t i o n   d ' a n n u l a t i o n )   m ÃƒÂª m e   s i   l e   m o n t a n t   p a y ÃƒÂ©   e s t   d e   0   D A   ( p a r   e x e m p l e   s i   s e u l s   l e s   f r a i s   d ' i n s c r i p t i o n   o n t   ÃƒÂ© t ÃƒÂ©   r ÃƒÂ© g l ÃƒÂ© s ) .   L e   b o u t o n   r e s t e   a c t i f   e t   l e s   c h a m p s   d e   p a i e m e n t   s o n t   m a s q u ÃƒÂ© s   l o r s   d e   l ' a c c e p t a t i o n . 
 
 -   D ÃƒÂ© t a i l s   d u   R e m b o u r s e m e n t   ( P a g e   d ÃƒÂ© d i ÃƒÂ© e )   :   A j o u t   d e   l a   p o s s i b i l i t ÃƒÂ©   d e   v a l i d e r   l ' a n n u l a t i o n   ( c o n f i r m a t i o n   d e   r e m b o u r s e m e n t   ÃƒÂ    0   D A )   s a n s   o b l i g e r   l ' u t i l i s a t e u r   ÃƒÂ    s ÃƒÂ© l e c t i o n n e r   u n e   e n t i t ÃƒÂ© ,   u n   c o m p t e   o u   ÃƒÂ    f a i r e   u n e   r ÃƒÂ© p a r t i t i o n   f i n a n c i ÃƒÂ¨ r e . 
 
 -   D ÃƒÂ© t a i l s   d u   R e m b o u r s e m e n t   ( P a g e   d ÃƒÂ© d i ÃƒÂ© e )   :   E x c l u s i o n   t o t a l e   d e s   p a i e m e n t s   l i ÃƒÂ© s   a u x   f r a i s   d ' i n s c r i p t i o n   ( h i s t o r i q u e ,   c a l c u l   d u   t o t a l ,   e t   t a b l e a u   d e   r ÃƒÂ© p a r t i t i o n )   d e p u i s   l e   b a c k e n d   ( v i e w s ) . 
 
 -   L i s t e   d e s   R e m b o u r s e m e n t s   ( M o d a l e   d e   T r a i t e m e n t )   :   C o r r e c t i o n   d u   c a l c u l   d u   ' M o n t a n t   d ÃƒÂ© j ÃƒÂ    p a y ÃƒÂ© '   p o u r   e x c l u r e   s y s t ÃƒÂ© m a t i q u e m e n t   l e s   f r a i s   d ' i n s c r i p t i o n   ( p a r   c o n t e x t e ,   b o o l ÃƒÂ© e n   e t   l i b e l l ÃƒÂ© ) .   L e   m o n t a n t   ÃƒÂ    0   m a s q u e   d ÃƒÂ© s o r m a i s   c o r r e c t e m e n t   l e s   c h a m p s   i n u t i l e s   e t   v a l i d e   l ' a n n u l a t i o n   s a n s   e r r e u r . 
 
 -   S e r v e u r   ( A p i S a v e R e f u n d O p e r a t i o n )   :   R ÃƒÂ© s o l u t i o n   d e   l ' e r r e u r   5 0 0   l o r s   d e   l a   v a l i d a t i o n   d u   r e m b o u r s e m e n t   e n   c o n v e r t i s s a n t   a u t o m a t i q u e m e n t   l e s   m o n t a n t s   c o n t e n a n t   u n e   v i r g u l e   ( e x :   ' 0 , 0 0 ' )   a u   f o r m a t   n u m ÃƒÂ© r i q u e   c o r r e c t . 
 
 -   S e r v e u r   ( A p i S a v e R e f u n d O p e r a t i o n )   :   A j o u t   d e   l a   s u p p r e s s i o n   a u t o m a t i q u e   d e s   o p ÃƒÂ© r a t i o n s   b a n c a i r e s   ( c h ÃƒÂ¨ q u e s / v i r e m e n t s )   ' e n   a t t e n t e   d e   r e c o u v r e m e n t '   l o r s   d e   l a   v a l i d a t i o n   d ' u n   r e m b o u r s e m e n t   a v e c   a n n u l a t i o n   d ' i n s c r i p t i o n . 
 
 -   R e c o u v r e m e n t   ( L i s t e )   :   A j o u t   d ' u n   b o u t o n   d e   s u p p r e s s i o n   s ÃƒÂ© c u r i s ÃƒÂ©   ( v ÃƒÂ© r i f i c a t i o n   d e   l a   p e r m i s s i o n   ' d e l e t e '   d u   m o d u l e   T r ÃƒÂ© s o r e r i e )   p e r m e t t a n t   d ' e f f a c e r   e n   c a s   d ' e r r e u r   u n   p a i e m e n t   e n   a t t e n t e ,   a i n s i   q u e   s o n   i m p u t a t i o n   b a n c a i r e   l i ÃƒÂ© e . 
 
 -   I m p u t a t i o n   B a n c a i r e   :   A f f i c h a g e   d e s   a c t i o n s   s o u s   f o r m e   d ' i c ÃƒÂ´ n e s   d a n s   l e s   t a b l e a u x   ( E n c a i s s e m e n t   e t   D ÃƒÂ© c a i s s e m e n t ) .   A j o u t   d u   b o u t o n   d e   s u p p r e s s i o n   ( c o n d i t i o n n ÃƒÂ©   p a r   l a   p e r m i s s i o n   d e   s u p p r e s s i o n )   p e r m e t t a n t   d ' e f f a c e r   u n e   o p ÃƒÂ© r a t i o n   e t   s e s   e n t i t ÃƒÂ© s   a s s o c i ÃƒÂ© e s   e n   c a s   d ' e r r e u r . 
 
 -   B r o u i l l a r d   d e   B a n q u e / C a i s s e   :   E x c l u   l e s   q u i t t a n c e s   d ' a n n u l a t i o n   ( P a i e m e n t s   a v e c   i s _ r e f u n d = T r u e )   p o u r   c o r r i g e r   l ' a f f i c h a g e   e r r o n ÃƒÂ©   d ' e n c a i s s e m e n t s   a v e c   s o l d e s   n u l s .   A j o u t ÃƒÂ©   l a   p r i s e   e n   c h a r g e   d e s   v r a i s   r e m b o u r s e m e n t s   ( C h ÃƒÂ¨ q u e / V i r e m e n t )   d a n s   l e   B r o u i l l a r d   d e   B a n q u e   c o m m e   d ÃƒÂ© c a i s s e m e n t s . 
 
 -   B r o u i l l a r d   d e   B a n q u e / C a i s s e   :   C a s t   d u   c h a m p   u p d a t e d _ a t   ( D a t e   e t   H e u r e )   e n   D a t e   ( Y Y Y Y - M M - D D )   p o u r   l e s   R e m b o u r s e m e n t s   a f i n   d ' ÃƒÂ© v i t e r   l ' a f f i c h a g e   d e   l ' h e u r e   d a n s   l e s   g r o u p e s   d e   d a t e s   d u   t a b l e a u . 
 
 
- CRM : Ajout du bouton de suppression pour les rÃƒÆ’Ã‚Â©ductions appliquÃƒÆ’Ã‚Â©es (gestion-des-reductions) avec vÃƒÆ’Ã‚Â©rification de la permission de suppression.

- CRM : Correction de l'affichage du bouton de suppression des rÃƒÆ’Ã‚Â©ductions (utilisation de user.is_superuser en plus de request.user.is_superuser).

- CRM : Autorisation de la suppression des rÃƒÆ’Ã‚Â©ductions appliquÃƒÆ’Ã‚Â©es mÃƒÆ’Ã‚Âªme aprÃƒÆ’Ã‚Â¨s validation et application.

- CRM : Remplacement de l'alerte navigateur par une modale Bootstrap ÃƒÆ’Ã‚Â©lÃƒÆ’Ã‚Â©gante pour la confirmation de suppression d'une rÃƒÆ’Ã‚Â©duction.

- TrÃƒÆ’Ã‚Â©sorerie : Remplissage dynamique des formulaires de modification (Encaissement et DÃƒÆ’Ã‚Â©caissement) dans imputation_bancaire.html pour remplacer les donnÃƒÆ’Ã‚Â©es HTML statiques.

- TrÃƒÆ’Ã‚Â©sorerie : Remplacement du symbole ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ par DA (Dinar AlgÃƒÆ’Ã‚Â©rien) dans imputation_bancaire.html pour s'adapter ÃƒÆ’Ã‚Â  la monnaie locale.

- Tresorerie : Ajout du menu et de la page 'Suivi des cheques emis' dans la Banque.
-   A j o u t   d ' u n   f i l t r a g e   p a r   s p ÃƒÂ© c i a l i t ÃƒÂ©   ( s t a n d a r d   e t   d o u b l e )   d a n s   l a   p a g e   d e s   p r ÃƒÂ© i n s c r i t s 
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
 -   G ÃƒÂ© n ÃƒÂ© r a t i o n   a u t o m a t i q u e   d u   c o d e   d e   s e s s i o n   d ' e x a m e n   ( e n   m o d e   l e c t u r e   s e u l e )   l o r s   d e   l a   c r ÃƒÂ© a t i o n   d ' u n e   n o u v e l l e   s e s s i o n   d a n s   / e x a m e n s / l i s t e - d e s - s e s s i o n s / 
 
 -   A j o u t   d e   l a   l i a i s o n   e n t r e   ' A u t r e   P r o d u i t '   e t   ' C a t ÃƒÂ© g o r i e   d e   P a i e m e n t '   a u   l i e u   d e   ' T y p e   d e   P a i e m e n t '   p o u r   l e s   p a i e m e n t s   a u t r e s   d a n s   l a   c o m p t a b i l i t ÃƒÂ© . 
 
 -   R e n d u   r ÃƒÂ© c u r s i f   d e   t o u t e s   l e s   c a t ÃƒÂ© g o r i e s   e t   s o u s - c a t ÃƒÂ© g o r i e s   d a n s   l e   s e l e c t   ' C a t ÃƒÂ© g o r i e '   p o u r   l a   c r ÃƒÂ© a t i o n   d e   n o u v e a u x   p a i e m e n t s   ( N o u v e a u   P a i e m e n t   A u t r e ) . 
 
 -   R e n d u   d u   c h a m p   ' C a t ÃƒÂ© g o r i e   d e   p r o d u i t '   f i l t r a b l e   a v e c   l ' i n t ÃƒÂ© g r a t i o n   d e   S e l e c t 2   ( r e c h e r c h e   i n c l u s e )   d a n s   l a   c r ÃƒÂ© a t i o n   d ' u n   a u t r e   p a i e m e n t . 
 
 -   C o r r e c t i o n   d ' u n e   e r r e u r   d e   s y n t a x e   J a v a s c r i p t   ' U n e x p e c t e d   i d e n t i f i e r   $ '   i n t r o d u i t e   l o r s   d e   l ' i n t ÃƒÂ© g r a t i o n   d e   S e l e c t 2 . 
 
 -   R e m p l a c e m e n t   d e   l ' i c ÃƒÂ´ n e   L o r d i c o n   4 0 4   ( h c u x q l p u . j s o n )   m a n q u a n t e   p a r   u n e   U R L   v a l i d e   ( b w t k c f q y . j s o n )   d a n s   l e   h e a d e r . 
 
 -   A j o u t   d e   s t y l e s   C S S   p e r s o n n a l i s ÃƒÂ© s   p o u r   h a r m o n i s e r   l ' a f f i c h a g e   d e   S e l e c t 2   ( c h a m p   ' C a t ÃƒÂ© g o r i e   d e   P r o d u i t ' )   a v e c   l e   d e s i g n   d e s   I n p u t - G r o u p   B o o t s t r a p   5   d a n s   ' n o u v e a u _ a u t r e _ p a i e m e n t . h t m l ' . 
 
 -   Ãƒâ€° l a r g i s s e m e n t   d u   f o r m u l a i r e   d e   c r ÃƒÂ© a t i o n   d e   ' N o u v e a u   P a i e m e n t   A u t r e '   p o u r   o c c u p e r   t o u t e   l a   l a r g e u r   ( c o l - 1 2   a u   l i e u   d e   c o l - x l - 9 ) . 
 
 
 
 - Ajout de la gestion de multiples contacts pour les prospects entreprise (ModÃƒÆ’Ã‚Â¨le ContactEntreprise, API et Interface)
- Ajout des champs email et tÃƒÆ’Ã‚Â©lÃƒÆ’Ã‚Â©phone pour l'entreprise lors de la crÃƒÆ’Ã‚Â©ation d'un prospect
- Ajout de la possibilitÃƒÆ’Ã‚Â© de modifier la date d'ÃƒÆ’Ã‚Â©mission et la date d'ÃƒÆ’Ã‚Â©chÃƒÆ’Ã‚Â©ance dans la configuration d'un devis (Conseil)
- Affichage prioritaire du nom de l'entreprise dans la liste des prospects en instance et des clients s'il n'y a pas de nom de contact\n- Suppression de la colonne Prospect et remplacement par Entreprise dans la liste des prospects en instance
- Correction de l'affichage 'Sans Nom' en ajoutant le champ type_prospect dans ApiListeProspect et ApiListeClients\n- Correction de la gÃƒÆ’Ã‚Â©nÃƒÆ’Ã‚Â©ration du slug pour les prospects sans nom et prÃƒÆ’Ã‚Â©nom afin d'ÃƒÆ’Ã‚Â©viter l'erreur 404 sur les dÃƒÆ’Ã‚Â©tails
- Restructuration de la page de dÃƒÆ’Ã‚Â©tails d'un prospect (type entreprise) : affichage prioritaire des informations de l'entreprise (avec numÃƒÆ’Ã‚Â©ro et email) suivi de la liste des contacts (principal puis autres)\n- AmÃƒÆ’Ã‚Â©lioration visuelle de l'affichage vide (Empty State) de la liste des contacts pour un prospect entreprise\n- Ajout de la fonctionnalitÃƒÆ’Ã‚Â© de crÃƒÆ’Ã‚Â©ation de contact depuis la fiche entreprise avec son modal dÃƒÆ’Ã‚Â©diÃƒÆ’Ã‚Â© et rechargement dynamique du tableau\n- Correction : Ajout du bouton manquant 'Ajouter Contact' dans l'en-tÃƒÆ’Ã‚Âªte de la carte Contacts\n- Ajout de la possibilitÃƒÆ’Ã‚Â© de modifier et supprimer les contacts liÃƒÆ’Ã‚Â©s ÃƒÆ’Ã‚Â  une entreprise depuis le tableau des contacts (avec modal d'ÃƒÆ’Ã‚Â©dition dÃƒÆ’Ã‚Â©diÃƒÆ’Ã‚Â© et points de terminaison d'API)\n- Refonte de la fiche client (conseil/details-client/) pour y intÃƒÆ’Ã‚Â©grer la gestion des contacts liÃƒÆ’Ã‚Â©s ÃƒÆ’Ã‚Â  l'entreprise avec les mÃƒÆ’Ã‚Âªmes fonctionnalitÃƒÆ’Ã‚Â©s que la fiche prospect (affichage, ajout, modification, suppression)\n- Correction : RÃƒÆ’Ã‚Â©solution d'une erreur de syntaxe JS (Uncaught SyntaxError) dans details_client.html due ÃƒÆ’Ã‚Â  une accolade mal positionnÃƒÆ’Ã‚Â©e lors de l'intÃƒÆ’Ã‚Â©gration de la gestion des contacts\n-   R ÃƒÂ© d u c t i o n   d e s   m a r g e s   ( m b - 4 ,   m b - 3   v e r s   m b - 2 )   e t   d e s   p a d d i n g s   ( p - 4 ,   p - 3   v e r s   p - 2 )   d a n s   l e s   t e m p l a t e s   C R M   d e t a i l s _ p r o s p e c t . h t m l   e t   d e t a i l s _ p r o s p e c t _ d o u b l e . h t m l 
 
 -   A n n u l a t i o n   d e   l a   r ÃƒÂ© d u c t i o n   d e s   m a r g e s   e t   d e s   p a d d i n g s   d a n s   d e t a i l s _ p r o s p e c t . h t m l   e t   d e t a i l s _ p r o s p e c t _ d o u b l e . h t m l   ( r e s t a u r a t i o n   ÃƒÂ    l ' ÃƒÂ© t a t   i n i t i a l ) 
 
 -   C o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   d a n s   m e n u . h t m l   :   l e   m e n u   P r o s p e c t s   d e   E x e c u t i v e   E d u c a t i o n   s ' a c t i v a i t   ÃƒÂ    t o r t   s u r   l a   p a g e   d ÃƒÂ© t a i l s - p r o s p e c t   d u   C R M   ( c o n f l i t   d e   s o u s - c h a ÃƒÂ® n e   e n t r e   D e t a i l s P r o s p e c t   e t   D e t a i l s P r o s p e c t C o n s e i l   r ÃƒÂ© s o l u ) . 
 
 -   A j o u t   d u   c h a m p   U n i t ÃƒÂ©   ( J o u r ,   G r o u p e ,   P a r t i c i p a n t ,   H e u r e )   p a r   l i g n e   d a n s   l a   c o n f i g u r a t i o n   d e s   d e v i s   ( m o d ÃƒÂ¨ l e s ,   t e m p l a t e   e t   v u e   m i s   ÃƒÂ    j o u r ) . 
 
 -   A j o u t   d e   l a   p r o p o s i t i o n   d ' e n r e g i s t r e m e n t   d ' u n e   n o u v e l l e   t h ÃƒÂ© m a t i q u e   d a n s   l e   d e v i s   l o r s q u ' u n e   d ÃƒÂ© s i g n a t i o n   p e r s o n n a l i s ÃƒÂ© e   e s t   s a i s i e   s a n s   s ÃƒÂ© l e c t i o n   p r ÃƒÂ© a l a b l e . 
 
 -   C o r r e c t i o n   d e   l ' e r r e u r   N a m e E r r o r :   n a m e   ' m o d u l e _ p e r m i s s i o n '   i s   n o t   d e f i n e d   s u r   l a   v u e   A p i C r e a t e T h e m a t i q u e . 
 
 -   A j o u t   d e   l a   c o l o n n e   U n i t ÃƒÂ©   d a n s   l a   v u e   d e s   d ÃƒÂ© t a i l s   d u   d e v i s   ( d e t a i l s _ d e v i s . h t m l ) . 
 
 -   A p p l i c a t i o n   d e s   m ÃƒÂª m e s   m o d i f i c a t i o n s   ÃƒÂ    l a   f a c t u r e   ( c o n f i g u r a t i o n   e t   d ÃƒÂ© t a i l s )   :   A j o u t   d e   l a   c o l o n n e   U n i t ÃƒÂ©   e t   p r o p o s i t i o n   d ' e n r e g i s t r e m e n t   d e   n o u v e l l e   t h ÃƒÂ© m a t i q u e . 
 
 -   C o p i e   d e   l ' u n i t ÃƒÂ©   ( L i g n e s D e v i s   - >   L i g n e s F a c t u r e )   l o r s   d e   l a   t r a n s f o r m a t i o n   d ' u n   d e v i s   e n   f a c t u r e . 
 
 
- Annulation des chÃƒÂ¨ques non encaissÃƒÂ©s au lieu de suppression lors du remboursement pour garder la trace (RetournÃƒÂ© au payeur)

- Ajout de la possibilitÃƒÂ© de renseigner manuellement la date de remise d'un chÃƒÂ¨que au payeur (remboursement) depuis l'interface de recouvrement.

- Correction d'un bug oÃƒÂ¹ un remboursement partiel (ou de 0 DA) sans annulation d'inscription ne marquait pas les chÃƒÂ¨ques non encaissÃƒÂ©s comme ÃƒÂ©tant en remboursement.

- Correction du formulaire de recouvrement pour renommer le champ en 'Date de recouvrement' et corriger le comportement : la date d'encaissement est dÃƒÂ©sormais enregistrÃƒÂ©e dans l'opÃƒÂ©ration bancaire (date_operation) sans ÃƒÂ©craser la date d'ÃƒÂ©mission originale du chÃƒÂ¨que (date_paiement), et l'opÃƒÂ©ration est correctement marquÃƒÂ©e comme encaissÃƒÂ©e (is_paid=True).

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

- Ajout d'un filtre de complÃƒÂ©tude (informations incomplÃƒÂ¨tes / dossiers incomplets) dans la liste des prÃƒÂ©inscrits (	_crm/f_views/prinscrits.py et liste-des-preinscrits.html).

- RÃƒÂ©organisation de la disposition des filtres dans /crm/liste-des-preinscrits/ pour un alignement sur deux lignes distinctes.

- Ajout de l'affichage du nombre de rÃƒÂ©sultats trouvÃƒÂ©s dans la barre de recherche des prÃƒÂ©inscrits (liste-des-preinscrits.html).

- Agrandissement de la barre de recherche dans /crm/liste-des-preinscrits/ pour occuper toute la largeur disponible (liste-des-preinscrits.html).

- RÃƒÂ©duction de la hauteur des cartes KPI et dÃƒÂ©placement des compteurs ÃƒÂ  droite de l'icÃƒÂ´ne dans /crm/liste-des-preinscrits/ (liste-des-preinscrits.html).

- Reproduction des mÃƒÂªmes amÃƒÂ©liorations esthÃƒÂ©tiques dans /crm/liste-des-prospects/ (rÃƒÂ©duction de la hauteur des cartes KPI avec chiffres alignÃƒÂ©s ÃƒÂ  droite de l'icÃƒÂ´ne, agrandissement de la barre de recherche sur toute la largeur avec affichage du nombre de rÃƒÂ©sultats trouvÃƒÂ©s).

## 2026-06-18
- Correction du problÃ¨me de division/recrÃ©ation de l'Ã©chÃ©ancier dans la configuration des Ã©chÃ©anciers. L'Ã©dition d'un groupe d'Ã©chÃ©anciers met dÃ©sormais correctement Ã  jour les tranches de tous les Ã©chÃ©anciers du groupe via leur index (au lieu de leur ID unique qui n'appartenait qu'au premier Ã©lÃ©ment).


- Ajout du champ `date_frais_inscription` pour la date d'Ã©chÃ©ance des frais d'inscription dans les Ã©chÃ©anciers.
- Mise Ã  jour de l'interface de crÃ©ation d'Ã©chÃ©ancier pour exiger une date d'Ã©chÃ©ance si le modÃ¨le inclut des frais d'inscription.
- Mise Ã  jour de l'interface de configuration/Ã©dition d'Ã©chÃ©ancier pour permettre la modification de cette date d'Ã©chÃ©ance des frais.


- Correction du bug 
ame 'remise' is not defined lors de la modification de l'Ã©chÃ©ancier dans l'interface de configuration.


- Correction d'une erreur lors de la suppression groupÃ©e des Ã©chÃ©anciers. Le bloc @transaction.atomic a Ã©tÃ© retirÃ© et une gestion des erreurs individuelle (via 	ry...except) a Ã©tÃ© ajoutÃ©e pour Ã©viter qu'une contrainte de base de donnÃ©es (ex: lien avec une autre table) ne fasse Ã©chouer toute la transaction de suppression groupÃ©e.


- Mise Ã  jour de l'affichage de la promotion dans la section Orientation AcadÃ©mique des dÃ©tails du prÃ©-inscrit (standard et double diplomation) pour afficher dÃ©sormais le code de la promotion au lieu du format session-annÃ©e.


- Correction du modal de dÃ©tails des modÃ¨les d'Ã©chÃ©ancier : suppression du tableau des tranches (car le modÃ¨le ne dÃ©finit que le nombre de tranches et non les pourcentages/dÃ©lais), ajout du nombre de tranches dans les informations gÃ©nÃ©rales et correction de l'erreur JS qui bloquait l'affichage.


- Modification de l'affichage de la promotion dans la section Orientation AcadÃ©mique des dÃ©tails du prospect (standard et double diplomation) pour afficher dÃ©sormais le libellÃ© de la promotion.


- Prise en compte de la date des frais d'inscription configurÃ©e dans le modÃ¨le d'Ã©chÃ©ancier lors de l'affichage de la demande de paiement (pour les cursus standards et en double diplomation).

-   A j o u t   d e   l ' i n d i c a t e u r   ' Ã‰ c h Ã© a n c i e r   e n   a t t e n t e   d e   s Ã© l e c t i o n '   d a n s   l e s   d Ã© t a i l s   d e   l a   d e m a n d e   d e   p a i e m e n t   ( s i m p l e   e t   d o u b l e )   s i   a u c u n   Ã© c h Ã© a n c i e r   n ' e s t   a p p l i q u Ã© . 
 
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d u   s t a t u t   ' A c t u e l l e m e n t   a p p l i q u Ã© '   d a n s   l a   l i s t e   d e s   Ã© c h Ã© a n c i e r s   d i s p o n i b l e s   p o u r   q u ' i l   n e   s ' a f f i c h e   q u e   s i   u n   m o d Ã¨ l e   e s t   r Ã© e l l e m e n t   e n r e g i s t r Ã© . 
 
 -   A j o u t   d u   b o u t o n   ' D Ã© t a i l s '   p o u r   c h a q u e   Ã© c h Ã© a n c i e r   d i s p o n i b l e   ( c a s   s t a n d a r d   e t   d o u b l e )   p e r m e t t a n t   d e   v i s u a l i s e r   l e s   t r a n c h e s   s a n s   a f f i c h e r   l e   b o u t o n   d ' a p p l i c a t i o n . 
 
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d u   m o n t a n t   d e s   t r a n c h e s   d a n s   l e   m o d a l   d e s   d Ã© t a i l s   d e   l ' Ã© c h Ã© a n c i e r   ( u t i l i s a t i o n   d e   m o n t a n t _ t r a n c h e   a u   l i e u   d e   m o n t a n t ) . 
 
 -   A j o u t   d e   l ' a f f i c h a g e   d e s   f r a i s   d ' i n s c r i p t i o n   c o m m e   l i g n e   d a n s   l e   t a b l e a u   d u   m o d a l   d e s   d Ã© t a i l s ,   i n c l u a n t   s a   d a t e . 
 
 -   A j o u t   d ' u n e   c o l o n n e   ' D a t e '   p o u r   a f f i c h e r   l e s   d a t e s   d ' Ã© c h Ã© a n c e   d e   c h a q u e   t r a n c h e . 
 
 -   M o d i f i c a t i o n   d e s   m o d a l s   d ' Ã© c h Ã© a n c i e r s   p o u r   u t i l i s e r   l a   d a t e   e t   l e   m o n t a n t   d e s   f r a i s   d ' i n s c r i p t i o n   t e l s   q u e   c o n f i g u r Ã© s   d a n s   l e   m o d Ã¨ l e   E c h e a n c i e r P a i e m e n t   ( Ã© c h Ã© a n c i e r s   c o n f i g u r Ã© s )   a u   l i e u   d e s   v a l e u r s   p a r   d Ã© f a u t   d u   v o e u . 
 
 
- Correction de la mise en page et du style pour le champ 'Date d'Ã©chÃ©ance des frais' dans le modal d'Ã©dition de l'Ã©chÃ©ancier (echeancier-configurer.html) pour un affichage alignÃ© avec les autres champs.

- Ajustement de l'alignement de 'Date d'Ã©chÃ©ance des frais' avec 'Frais d'inscription' sur la mÃªme ligne (col-md-3) dans la fenÃªtre de modification de l'Ã©chÃ©ancier pour un rendu parfaitement Ã©quilibrÃ©.

- Griser et dÃ©sactiver les champs 'Frais d'inscription' et 'Date d'Ã©chÃ©ance des frais' dans la fenÃªtre de modification de l'Ã©chÃ©ancier si le modÃ¨le d'Ã©chÃ©ancier n'a pas l'option activÃ©e.

- Harmonisation du thÃ¨me des en-tÃªtes (headers) des fenÃªtres modales 'DÃ©tails du Plan de Paiement' et 'Modifier le Plan de Paiement' avec le thÃ¨me principal de la page (remplacement du gradient sombre par un fond clair bleutÃ©).

- Correction de l'affichage de la dÃ©signation de la formation dans les fenÃªtres modales de dÃ©tails et modification de l'Ã©chÃ©ancier pour inclure toutes les spÃ©cialitÃ©s concernÃ©es par le groupe d'Ã©chÃ©anciers (au lieu d'une seule).

- Modernisation de l'affichage de la dÃ©signation de la formation dans les fenÃªtres modales : remplacement de la longue liste textuelle entre parenthÃ¨ses par une prÃ©sentation propre sous forme de badges bleutÃ©s (tags) pour chaque spÃ©cialitÃ© concernÃ©e.

- Modification de la logique JS dans les pages de dÃ©tails de paiement (standard et double) : les Ã©chÃ©ances Ã  payer dans le menu dÃ©roulant de la fenÃªtre modale 'Enregistrement de paiement' sont dÃ©sormais systÃ©matiquement triÃ©es par ordre chronologique (via leur ID) avant affichage, sans altÃ©rer la structure des donnÃ©es rÃ©cupÃ©rÃ©es.

- Suppression du champ global 'DÃ©signation' en trop sur la page de crÃ©ation d'une dÃ©pense. Le backend utilise dÃ©sormais automatiquement la dÃ©signation de la premiÃ¨re ligne de dÃ©pense saisie.

- Correction du bug \FieldError\ (Invalid field name) dans le profil Ã©tudiant (\	_groupe/f_views/student.py\) : remplacement de \payment_type\ par \payment_category\ dans la requÃªte \select_related\ du modÃ¨le \AutreProduit\.

- Correction du mÃªme bug \FieldError\ (Invalid field name) sur le modÃ¨le \AutreProduit\ dans l'API \ApiListeAutresPaiements\ (\	_tresorerie/f_views/autre_paiement.py\) : remplacement de \payment_type\ par \payment_category\.

- Fusion de la colonne 'Type' avec la colonne 'Description' dans la liste des autres paiements (\liste_autre_paiements.html\). Le type (badge) s'affiche dÃ©sormais directement en dessous de la description de l'opÃ©ration pour un affichage plus condensÃ©.

- Correction des problÃ¨mes d'encodage (erreurs de typologie comme 'NÃ‚Â°' ou 'EspÃƒÂ¨ce') dans l'affichage du tableau de la liste des autres paiements (\liste_autre_paiements.html\).

- Remplacement du menu dÃ©roulant (dropdown) des actions par des boutons d'icÃ´nes alignÃ©s (DÃ©tails, Modifier, Supprimer) dans la liste des autres paiements (\liste_autre_paiements.html\) pour un accÃ¨s plus rapide.

- Correction des erreurs de typologie d'encodage (ex: NÃ‚Â° et ChÃƒÂ¨que) dans les tableaux de la page de recouvrement (\
ecouvrement_paiement.html\).

- Correction de l'affichage des avatars des clients dans les tableaux de la page de recouvrement. Les badges ont dÃ©sormais une couleur de fond dynamique avec un texte blanc pour garantir que les initiales soient toujours bien lisibles.
- Correction : Le numero de quittance genere pour les nouveaux autres paiements respecte desormais la configuration definie dans la page Parametres de Facturation (onglet Numerotation quittance de l'entite). 
- UI/UX : Ajout des initiales du client (avatar colore) dans la colonne client de la page des attentes de paiements (attentes-de-paiements). 
- UI/UX : Ajout des initiales du client (avatar colore) dans la colonne client de la page liste des paiements (liste-des-paiements). Correction des colonnes du filtre de recherche de la page. 
- Scolarite : Ajout de la fonctionnalite de demande de remboursement dans le profil etudiant (profile_etudiant.html et profile_etudiant_double.html) avec verification pour empecher les demandes multiples si une demande est deja en cours. 
- Scolarite : Deplacement du bouton de demande de remboursement vers l'onglet Paiements dans profile_etudiant.html et profile_etudiant_double.html 
-   * * T r Ã© s o r e r i e * *   :   A j o u t   d u   s u p p o r t   d e   l ' i m p r e s s i o n   d e   t i c k e t   d e   c a i s s e   ( f o r m a t   8 0 m m )   p o u r   l e s   p a i e m e n t s   a v e c   o p t i o n   d ' a c t i v a t i o n   d a n s   l e s   p a r a m Ã¨ t r e s   f i n a n c i e r s . 
 
 -   * * T r Ã© s o r e r i e * *   :   C o r r e c t i o n   d e   l ' U R L   p o u r   l ' i m p r e s s i o n   d u   t i c k e t   d e   c a i s s e   ( 4 0 4 ) . 
 
 -   * * T r Ã© s o r e r i e * *   :   C o r r e c t i o n   d e   l ' e r r e u r   T e m p l a t e S y n t a x E r r o r   c a u s Ã© e   p a r   l e   f i l t r e   f o r m a t _ m o n t a n t   d a n s   l e   t i c k e t   d e   c a i s s e . 
 
 -   * * T r Ã© s o r e r i e * *   :   C o r r e c t i o n   d e   l ' e r r e u r   V a r i a b l e D o e s N o t E x i s t   c a u s Ã© e   p a r   l ' a b s e n c e   d ' a t t r i b u t   ' e n t r e p r i s e '   d a n s   l ' o b j e t   t e n a n t   p o u r   l e   t i c k e t   d e   c a i s s e . 
 
 -   * * T r Ã© s o r e r i e * *   :   C o r r e c t i o n   d e   l ' e r r e u r   T y p e E r r o r   c a u s Ã© e   p a r   l e   f o r m a t a g e   a v e c   h e u r e s / m i n u t e s   s u r   u n   D a t e F i e l d   d a n s   l e   t i c k e t   d e   c a i s s e . 
 
 -   * * T r Ã© s o r e r i e * *   :   R Ã© d u c t i o n   d e   l a   t a i l l e   d u   l o g o   d a n s   l e   t i c k e t   d e   c a i s s e   e t   a j o u t   d e   l a   f o r m a t i o n   e t   d e   l a   s p Ã© c i a l i t Ã©   d a n s   l a   l i g n e   d u   t i c k e t . 
 
 -   * * T r Ã© s o r e r i e * *   :   C o r r e c t i o n   d e   l ' a f f i c h a g e   d e   l a   s p Ã© c i a l i t Ã©   d a n s   l e   t i c k e t   d e   c a i s s e   e n   r Ã© c u p Ã© r a n t   l e   l a b e l   v i a   l a   F i c h e   d e   V o e u x   d u   p r o s p e c t   s i   a b s e n t   d e   l ' Ã© c h Ã© a n c i e r . 
 
 
- Fix empty string parsing for frais_inscription in ApiSaveEcheancier and ApiUpdateEcheancier to prevent EcheancierPaiement from silently failing to save and disappearing from echeanciers configures.

- Rendre le filtre par promo directement visible dans la page des ÃƒÂ©chÃƒÂ©anciers configurÃƒÂ©s et dÃƒÂ©clencher le filtrage au changement (onchange).

- Ajout d'une pagination cÃƒÂ´tÃƒÂ© client (10 ÃƒÂ©lÃƒÂ©ments par page) dans la vue des modÃƒÂ¨les d'ÃƒÂ©chÃƒÂ©anciers (gestion_echeancier.html).

- Correction: masquage des frais d'inscription dans les dÃƒÂ©tails de la demande de paiement (ApiGetDetailsDemandePaiement et ApiGetDetailsDemandePaiementDouble) si le modÃƒÂ¨le d'ÃƒÂ©chÃƒÂ©ancier associÃƒÂ© a l'option frais d'inscription dÃƒÂ©sactivÃƒÂ©e.

- Activation de la pagination native de DataTables (10 ÃƒÂ©lÃƒÂ©ments par page) dans la vue des attentes de paiements (attentes_de_paiement.html).

- AmÃƒÂ©lioration visuelle (Premium Design) de la pagination DataTables dans attentes_de_paiement.html avec des coins arrondis, ombres et effets de survol harmonisÃƒÂ©s.

- Ajout d'une colonne 'Cursus' (Standard ou Double Diplomation) dans le tableau des attentes de paiements (attentes_de_paiement.html).

- Fix: stabilisation de l'ordre d'affichage de la liste des ÃƒÂ©chÃƒÂ©anciers configurÃƒÂ©s en forÃƒÂ§ant un tri .order_by('-id') afin d'ÃƒÂ©viter qu'un ÃƒÂ©chÃƒÂ©ancier ne remonte en tÃƒÂªte de liste aprÃƒÂ¨s une modification (comportement par dÃƒÂ©faut de PostgreSQL aprÃƒÂ¨s un UPDATE).
A j o u t   v Ã© r i f i c a t i o n   Ã© c h Ã© a n c i e r   a p p l i q u Ã©   a v a n t   s o u m i s s i o n   r e m i s e 
 
 A f f i c h a g e   c o n d i t i o n n e l   d e s   m o n t a n t s   d e   l ' Ã© c h Ã© a n c i e r   e t   r e c a l c u l   d e s   r e m i s e s   d a n s   l e   m o d a l   D Ã© t a i l s   d e   l a   R Ã© d u c t i o n   ( s t a n d a r d   e t   d o u b l e ) 
 
 C o r r e c t i o n :   m a s q u a g e   c o m p l e t   d e s   m o n t a n t s   ( i n i t i a l   e t   f i n a l )   d a n s   l e   m o d a l   d e   r Ã© d u c t i o n   l o r s q u e   l ' Ã© c h Ã© a n c i e r   n ' e s t   p a s   e n c o r e   a p p l i q u Ã©   ( f i c h i e r s   s t a n d a r d   e t   d o u b l e ) . 
 
 A j o u t   d e   l ' a f f i c h a g e   d e   l a   r e m i s e   o u   d e   l a   m a j o r a t i o n   d a n s   l e   m o d a l   d e   ' D Ã© t a i l s   d u   m o d Ã¨ l e   d ' Ã© c h Ã© a n c i e r '   p o u r   l e s   p a g e s   d e   d e m a n d e   d e   p a i e m e n t   ( s t a n d a r d   e t   d o u b l e ) . 
 
 C o r r e c t i o n   d u   b l o c a g e   e m p Ãª c h a n t   l ' a p p l i c a t i o n   d e   l a   r e m i s e   a p r Ã¨ s   l a   s Ã© l e c t i o n   d ' u n   Ã© c h Ã© a n c i e r .   L a   v a l i d a t i o n   v Ã© r i f i e   d Ã© s o r m a i s   c o r r e c t e m e n t   l ' Ã© t a t   d e   ' h a s _ s a v e d _ e c h e a n c i e r '   e n   p l u s   d e   ' h a s _ d u e _ p a i e m e n t '   ( f i c h i e r s   s t a n d a r d   e t   d o u b l e   d i p l o m a t i o n ) . 
 
 C o r r e c t i o n   d e   l ' e r r e u r   N a m e E r r o r   ( ' e n t i t e _ s t r '   i s   n o t   d e f i n e d )   l o r s   d e   l ' e n r e g i s t r e m e n t   d ' u n   ' A u t r e P r o d u i t '   d a n s   l e   m o d u l e   d e   t r Ã© s o r e r i e   e n   u t i l i s a n t   l a   v a r i a b l e   c o r r e c t e   ' e n t i t e _ n o m ' . 
 
 S u p p r e s s i o n   d e s   b o Ã® t e s   d e   n o t i f i c a t i o n   ' I n s t r u c t i o n s   d ' u t i l i s a t i o n   d e s   Ã© c h Ã© a n c i e r s '   e t   ' I m p o r t a n t   -   C o n f i r m a t i o n   d ' i n s c r i p t i o n '   d a n s   l e s   p a g e s   d e t a i l s _ a t t e n t e _ p a i e m e n t . h t m l   e t   d e t a i l s _ a t t e n t e _ p a i e m e n t _ d o u b l e . h t m l . 
 
 -   [ t _ t r e s o r e r i e / f _ v i e w s / p r e i n s c r i t _ p a i e m e n t s . p y ]   C o r r e c t i o n   d u   c a l c u l   d e   p r i x _ f o r m a t i o n   p o u r   l a   D o u b l e   D i p l o m a t i o n   l o r s   d e   l ' a p p l i c a t i o n   d ' u n e   r e m i s e   e n   u t i l i s a n t   l e   c h a m p   p r i x   s i   p r i x _ s p e c 1   e t   p r i x _ s p e c 2   s o n t   n u l s . 
 
 -   [ t e m p l a t e s / t e n a n t _ f o l d e r / c o m p t a b i l i t e / t r e s o r e r i e / d e t a i l s _ a t t e n t e _ p a i e m e n t _ d o u b l e . h t m l ]   C o r r e c t i o n   d e   l a   r Ã© c u p Ã© r a t i o n   d e   m o n t a n t F i n a l   d e   l a   3 Ã¨ m e   c o l o n n e   a u   l i e u   d e   l a   4 Ã¨ m e   l o r s q u e   l a   r e m i s e   e s t   a p p l i q u Ã© e . 
 
 -   [ t _ t r e s o r e r i e / f _ v i e w s / p r e i n s c r i t _ p a i e m e n t s . p y ]   A j o u t   d e   l ' e n d p o i n t   A p i C a n c e l R e m i s e T o P a i e m e n t   p o u r   a n n u l e r   l ' a p p l i c a t i o n   d ' u n e   r e m i s e   e t   r e s t a u r e r   l e s   a n c i e n s   p r i x   d e s   e c h e a n c i e r s . 
 
 -   [ t _ t r e s o r e r i e / u r l s . p y ]   A j o u t   d e   l a   r o u t e   A p i C a n c e l R e m i s e T o P a i e m e n t . 
 
 -   [ t e m p l a t e s / t e n a n t _ f o l d e r / c o m p t a b i l i t e / t r e s o r e r i e / d e t a i l s _ a t t e n t e _ p a i e m e n t . h t m l ,   d e t a i l s _ a t t e n t e _ p a i e m e n t _ d o u b l e . h t m l ]   A j o u t   d u   b o u t o n   d ' a n n u l a t i o n   d e   r e m i s e   d a n s   l a   m o d a l e   d e   d e t a i l s   e t   d e   l a   l o g i q u e   J a v a s c r i p t   a s s o c i Ã© e . 
 
 -   [ t e m p l a t e s / t e n a n t _ f o l d e r / c o m p t a b i l i t e / t r e s o r e r i e / d e t a i l s _ a t t e n t e _ p a i e m e n t . h t m l ,   d e t a i l s _ a t t e n t e _ p a i e m e n t _ d o u b l e . h t m l ]   D Ã© p l a c e m e n t   d u   b o u t o n   d ' a n n u l a t i o n   d e   r Ã© d u c t i o n   v e r s   l ' e n t Ãª t e   d e   l a   c a r t e   Ã‰ c h Ã© a n c i e r   d e   p a i e m e n t ,   a f f i c h Ã©   u n i q u e m e n t   l o r s q u e   l a   r Ã© d u c t i o n   e s t   a p p l i q u Ã© e . 
 
 -   [ t e m p l a t e s / t e n a n t _ f o l d e r / c o m p t a b i l i t e / t r e s o r e r i e / d e t a i l s _ a t t e n t e _ p a i e m e n t . h t m l ,   d e t a i l s _ a t t e n t e _ p a i e m e n t _ d o u b l e . h t m l ]   C o r r e c t i o n   d u   d Ã© c a l a g e   d ' a f f i c h a g e   d e s   m o n t a n t s   f i n a u x   d e s   Ã© c h Ã© a n c i e r s   ( m i s e   Ã    j o u r   d e   r e d u c t i o n A p p r o u v e d   e t   r e d u c t i o n A p p l i c e d   a v a n t   l a   b o u c l e   d e   g Ã© n Ã© r a t i o n   d e s   t r a n c h e s ) . 
 
 -   [ t e m p l a t e s / t e n a n t _ f o l d e r / c o m p t a b i l i t e / t r e s o r e r i e / d e t a i l s _ a t t e n t e _ p a i e m e n t . h t m l ,   d e t a i l s _ a t t e n t e _ p a i e m e n t _ d o u b l e . h t m l ]   C o r r e c t i o n   d u   b u g   o Ã¹   l a   n o t i f i c a t i o n   ' R Ã© d u c t i o n   a p p l i q u Ã© e   a v e c   s u c c Ã¨ s '   n e   d i s p a r a i s s a i t   p a s   Ã    l ' a n n u l a t i o n . 
 
 -   [ t e m p l a t e s / t e n a n t _ f o l d e r / c o m p t a b i l i t e / t r e s o r e r i e / d e t a i l s _ a t t e n t e _ p a i e m e n t . h t m l ,   d e t a i l s _ a t t e n t e _ p a i e m e n t _ d o u b l e . h t m l ]   A j o u t   d u   b o u t o n   ' R Ã© i n i t i a l i s e r   l ' Ã© c h Ã© a n c i e r '   d a n s   l a   c a r t e   d e s   Ã© c h Ã© a n c i e r s   d i s p o n i b l e s ,   d Ã© c l e n c h a n t   l a   m o d a l   d ' a n n u l a t i o n   d e s   m o n t a n t s   d u s . 
 
 -   [ t _ t r e s o r e r i e / f _ v i e w s / p r e i n s c r i t _ p a i e m e n t s . p y ]   M o d i f i c a t i o n   d e   A p i C a n c e l D u e P a i e m e n t s   p o u r   r e m e t t r e   l a   s Ã© l e c t i o n   d e   l ' Ã© c h Ã© a n c i e r   Ã    n u l l   ( o b j . r e f _ e c h e a n c i e r   =   N o n e ) ,   c e   q u i   d Ã© s Ã© l e c t i o n n e   l e   m o d Ã¨ l e   a c t u e l l e m e n t   a p p l i q u Ã©   s u r   l ' i n t e r f a c e . 
 
 -   [ t e m p l a t e s / t e n a n t _ f o l d e r / c o m p t a b i l i t e / t r e s o r e r i e / d e t a i l s _ a t t e n t e _ p a i e m e n t . h t m l ,   d e t a i l s _ a t t e n t e _ p a i e m e n t _ d o u b l e . h t m l ]   C o r r e c t i o n   d u   c a l c u l   d e   l a   r Ã© d u c t i o n   p a r   m o n t a n t   f i x e   s u r   l ' Ã© c h Ã© a n c i e r   :   l a   r Ã© p a r t i t i o n   e s t   d Ã© s o r m a i s   c a l c u l Ã© e   s u r   l e   m o n t a n t   t o t a l   d e s   t r a n c h e s   a p p l i c a b l e s   p l u t Ã´ t   q u e   s u r   l e   p r i x   t o t a l   d e   l a   f o r m a t i o n ,   g a r a n t i s s a n t   u n e   d Ã© d u c t i o n   e x a c t e . 
 
 -   [ t e m p l a t e s / t e n a n t _ f o l d e r / c r m / r e m i s e s / l i s t e _ r e m i s e _ a p p l i q u e r . h t m l ]   A j o u t   d ' u n   s y s t Ã¨ m e   d e   p a g i n a t i o n   c Ã´ t Ã©   c l i e n t   p o u r   l a   l i s t e   d e s   r Ã© d u c t i o n s   a p p l i q u Ã© e s   e t   c o r r e c t i o n   d e s   f i l t r e s   ( r e c h e r c h e ,   s t a t u t ,   d a t e ) . 
 
 
## 2026-06-23 13:27 - Pagination et Correctif

- **Correction de bug** : RÃƒÂ©solution de l'erreur de syntaxe (`missing ) after argument list`) introduite dans `liste_remise_appliquer.html` suite ÃƒÂ  un problÃƒÂ¨me de fusion de code lors de l'intÃƒÂ©gration de la pagination.
- **Ajout de fonctionnalitÃƒÂ©** : ImplÃƒÂ©mentation du systÃƒÂ¨me de pagination (cÃƒÂ´tÃƒÂ© client) dans la vue `liste_des_remises.html` avec un affichage de 10 ÃƒÂ©lÃƒÂ©ments par page et rÃƒÂ©ÃƒÂ©criture du filtrage.

## 2026-06-23 13:56 - Correctif Syntax Error

- **Correction de bug** : RÃƒÂ©solution de l'erreur de syntaxe (`Unexpected token ';'`) dans `liste_des_remises.html` due ÃƒÂ  des lignes de code orphelines dans l'objet `$.ajax`.

- Correction du bug des montants Ã  zÃ©ro lors de la validation de l'Ã©chÃ©ancier avec remise : amÃ©lioration de la fonction clean_montant pour gÃ©rer correctement les espaces insÃ©cables et autres caractÃ¨res d'espacement gÃ©nÃ©rÃ©s par le formatage JavaScript.
# #   [ ]   -   C o r r e c t i o n   d e   l ' e r r e u r   R e q u e s t   L i n e   i s   t o o   l a r g e 
 -   M o d i f i c a t i o n   d e   \ A p i G e t P a i e m e n t R e q u e s t D e t a i l s \   e t   \ A p i G e t P a i e m e n t R e q u e s t D e t a i l s D o u b l e \   d a n s   \ p r e i n s c r i t _ p a i e m e n t s . p y \   p o u r   u t i l i s e r   l a   m Ã© t h o d e   P O S T   a u   l i e u   d e   G E T . 
 -   M i s e   Ã    j o u r   d e s   a p p e l s   A J A X   d a n s   \ d e t a i l s _ a t t e n t e _ p a i e m e n t . h t m l \   e t   \ d e t a i l s _ a t t e n t e _ p a i e m e n t _ d o u b l e . h t m l \   p o u r   e n v o y e r   l e s   d o n n Ã© e s   v i a   P O S T   ( a v e c   l e   t o k e n   C S R F )   a f i n   d ' Ã© v i t e r   l a   l i m i t e   d e   t a i l l e   d e   l ' U R L   l o r s   d e   l a   c o n f i r m a t i o n   d ' u n   Ã© c h Ã© a n c i e r   a v e c   b e a u c o u p   d e   l i g n e s . 
 
 
## [2026-06-24] - Correction de l'erreur Request Line is too large
- Modification de ApiGetPaiementRequestDetails et ApiGetPaiementRequestDetailsDouble pour utiliser POST au lieu de GET.
- Mise Ã  jour des appels AJAX pour envoyer les donnÃ©es de l'Ã©chÃ©ancier via POST avec le token CSRF.

## [2026-06-24] - Ajout d'un scroll vertical Ã  l'Ã©chÃ©ancier
- Ajout d'une limite de hauteur (max-height: 350px) et d'un dÃ©filement vertical (overflow-y: auto) sur la table de l'Ã©chÃ©ancier de paiement dans les vues standard et double pour faciliter la lecture lorsqu'il y a plus de 6 lignes.

## [2026-06-24] - Correction du scroll de l'Ã©chÃ©ancier
- Ajout de la rÃ¨gle !important Ã  overflow-y: auto sur table-responsive pour forcer le scroll vertical et corriger le dÃ©bordement (overflow) des lignes de la table.

## [2026-06-24] - Harmonisation du modal de confirmation de l'Ã©chÃ©ancier
- Suppression de la section 'Informations de la formation' dans le modal de dÃ©tails de confirmation pour les vues standard et double.
- Harmonisation du design de la table 'Ã‰chÃ©ancier de paiement' dans ce modal pour correspondre au design Ã©purÃ© de la page principale (suppression des bordures de la carte, ajout d'une icÃ´ne avec dÃ©gradÃ© et d'un scroll interne).

## [2026-06-24] - Ajout de l'export Excel pour les logs utilisateurs
- Ajout d'un bouton 'Exporter' dans la vue 'crm_user_logs' (configuration/crm-user-logs/) permettant de tÃ©lÃ©charger l'historique complet ou filtrÃ© des actions sous format Excel (.xlsx).
- ImplÃ©mentation du mÃ©canisme d'export avec la librairie 'openpyxl' dans associe_app/views.py.

## [2026-06-24] - Ajout de l'export CSV pour les logs utilisateurs
- Ajout d'une fonctionnalitÃ© d'export en format CSV dans la vue crm_user_logs.
- Ajout d'un bouton dÃ©diÃ© (icÃ´ne CSV) Ã  cÃ´tÃ© de l'export Excel dans l'interface.

## [2026-06-24] - Correction du formatage de l'export CSV
- Utilisation de io.StringIO() et du dÃ©limiteur ',' standard pour garantir la compatibilitÃ© universelle du format CSV.
- Nettoyage des sauts de ligne (\n, \r) dans les dÃ©tails pour Ã©viter la casse des lignes lors de l'export.

## [2026-06-25] - Modification KPI page review budget
- Suppression de la KPI 'Progression' et renommage de 'Objectif AllouÃƒÂ©' en 'Objectif' dans la vue udget_campaign_review.html.

## [2026-06-25] - Masquage onglet RÃƒÂ©partition pour les campagnes actives
- Masquage de l'onglet 'RÃƒÂ©partition & PrÃƒÂ©visions' et de son contenu si la campagne budgÃƒÂ©taire est active.
- DÃƒÂ©finition de l'onglet 'Suivi des RÃƒÂ©alisations' comme actif par dÃƒÂ©faut lorsque la campagne est active.

## [2026-06-26] - Affichage du premier onglet si la validation est en attente
- Modification de associe_app/budget_campaign_review.html pour forcer l'affichage de l'onglet 'RÃƒÂ©partition & PrÃƒÂ©visions' (et son contenu) lorsque le statut de la ligne budgÃƒÂ©taire est 'submitted' (en attente), mÃƒÂªme si la campagne est dÃƒÂ©jÃƒÂ  active.
- Ajout de l'affichage du code de la promotion dans le champ promotion/session de la modal createVoeuxDoubleModal dans la page details prospect standard.
- Ajout du badge Standard a cote du titre de la page de details d'un prospect (version standard).


## 2026-06-30
- [TrÃ©sorerie] EchÃ©anciers configurÃ©s : Ajout du calcul inversÃ© (mise Ã  jour du pourcentage lors de la modification du montant de la tranche).
- [TrÃ©sorerie] EchÃ©anciers configurÃ©s : Ajout d'un systÃ¨me de vÃ©rification visuelle (footer) validant la rÃ©partition manuelle (total part et montant) et bloquant la sauvegarde en cas d'incohÃ©rence.
- [TrÃ©sorerie] EchÃ©anciers configurÃ©s : Modification du backend (ApiUpdateEcheancier) pour utiliser l'ID explicite des tranches lors des mises Ã  jour, Ã©vitant ainsi toute duplication ou Ã©crasement liÃ© Ã  l'ordre.
# # #   3 0 / 0 6 / 2 0 2 6   -   C R M   :   V a l i d a t i o n   p r é - i n s c r i p t i o n 
 -   A j o u t   d e   l ' e n r e g i s t r e m e n t   d e   l ' a c t i o n   d e   v a l i d a t i o n   d ' u n   p r é - i n s c r i t   ( s t a n d a r d   e t   d o u b l e )   d a n s   \ c r m / u s e r - l o g s / \   ( U s e r A c t i o n L o g )   a u   n i v e a u   d e   l a   v u e   \ A p i V a l i d a t e P r e i n s c r i t \ . 
 
 -   A j o u t   d e   l ' e n r e g i s t r e m e n t   d e   l ' a c t i o n   d e   g é n é r a t i o n   d ' u n e   d e m a n d e   d e   p a i e m e n t   s u i t e   à   l a   v a l i d a t i o n   d ' u n   p r é - i n s c r i t   d a n s   \ c r m / u s e r - l o g s / \   ( U s e r A c t i o n L o g ) . 
 
 
### Modification - 2026-07-01
- Mise Ã  jour des mois des trimestres (de Juillet Ã  Juin) dans institut_app/views.py.
- Mise Ã  jour des filtres, en-tÃªtes et logique JS dans 	emplates/tenant_folder/budget/realization_budget.html pour correspondre Ã  l'annÃ©e fiscale (Juillet-Juin).
- Mise Ã  jour des filtres de dates pour les calculs budgÃ©taires dans ssocie_app/budget_utils.py (utilisation de la pÃ©riode Juillet-Juin au lieu des dates de la campagne).
M i s e   a   j o u r   d e s   f i l t r e s   d a n s   r e v i e w _ b u d g e t   p a r   r a p p o r t   à   l a   n o u v e l l e   c o n f i g u r a t i o n . 
 
 
 # #   2 0 2 6 - 0 7 - 0 1 
 -   R e m p l a c e m e n t   d e   ' O b j e c t i f   R e c e t t e s '   p a r   ' O b j e c t i f   a s s i g n é   p a r   l e   C A '   d a n s   d i s p a t c h _ b u d g e t . h t m l 
 
 -   A j o u t   d ' u n e   K P I   ' R é s u l t a t   N e t   P r é v u '   q u i   c a l c u l e   d y n a m i q u e m e n t   ( r e c e t t e s   -   d é p e n s e s )   e t   a j u s t e m e n t   d e s   c o l o n n e s   d a n s   d i s p a t c h _ b u d g e t . h t m l 
 
 -   R é d u c t i o n   d u   p a d d i n g   e t   d e s   m a r g e s   d e s   c a r t e s   K P I   ( p - 4   v e r s   p - 3 ,   m b - 4   v e r s   m b - 3 ,   f s - 4   v e r s   f s - 5 )   d a n s   d i s p a t c h _ b u d g e t . h t m l 
 
 -   D é s a c t i v a t i o n   d u   b o u t o n   e n r e g i s t r e r P a i e m e n t B t n   l o r s   d u   c l i c   d a n s   d e t a i l s _ a t t e n t e _ p a i e m e n t . h t m l   e t   d e t a i l s _ a t t e n t e _ p a i e m e n t _ d o u b l e . h t m l   p o u r   é v i t e r   l e s   d o u b l e s   c l i c s . 
 
 -   A j o u t   d ' u n e   v é r i f i c a t i o n   s t r i c t e   ( e a r l y   r e t u r n )   s u r   l e   b o u t o n   c o n f i r m e r P a i e m e n t B t n   p o u r   b l o q u e r   t o t a l e m e n t   l e s   d o u b l e s   c l i c s . 
 
 -   A p p l i c a t i o n   d e   l a   d é s a c t i v a t i o n   ( a n t i - d o u b l e   c l i c )   s u r   e n r e g i s t r e r P a i e m e n t B t n   e t   c o n f i r m e r P a i e m e n t B t n   d a n s   d e t a i l s - s u i v i e - e c h e a n c i e r . h t m l   e t   d e t a i l s - s u i v i e - e c h e a n c i e r - d o u b l e . h t m l . 
 
 -   M a s q u a g e   d u   b o u t o n   ' S o u m e t t r e   p o u r   v a l i d a t i o n '   d a n s   l a   v u e   d i s p a t c h _ b u d g e t . h t m l   t a n t   q u ' a u c u n   b r o u i l l o n   d e   b u d g e t   n ' a   é t é   e n r e g i s t r é . 
 
 -   A j o u t   d e   l ' é t a t   ' P r é - v a l i d é '   e t   d e s   b o u t o n s   V a l i d e r   /   R e m e t t r e   e n   b r o u i l l o n   d a n s   l a   v u e   d i s p a t c h _ b u d g e t . h t m l . 
 
 -   C o r r e c t i o n   d e   l ' e r r e u r   ' C e   b u d g e t   e s t   d é j à   s o u m i s '   l o r s   d e   l a   r e m i s e   e n   b r o u i l l o n . 
 
 -   R e m p l a c e m e n t   d e   l a   v a l i d a t i o n   p a r   S w e e t A l e r t   l o r s   d e   l a   s o u m i s s i o n   p a r   u n e   f e n ê t r e   m o d a l e   B o o t s t r a p   s t a n d a r d   d a n s   d i s p a t c h _ b u d g e t . h t m l . 
 
 -   C o r r e c t i o n   d e   l ' e r r e u r   J a v a S c r i p t   ' s u b m i t F o r m   i s   n o t   d e f i n e d '   d a n s   l a   m o d a l e   d e   c o n f i r m a t i o n   d e   s o u m i s s i o n   ( m i s e   e n   s c o p e   g l o b a l ) . 
 
 -   C r é a t i o n   d u   f i c h i e r   t e m p l a t e s / t e n a n t _ f o l d e r / e x e c u t i v e _ e d u c a t i o n _ n a v b a r . h t m l   a v e c   l a   s t r u c t u r e   d e   b a s e   d u   m e n u   p o u r   E x e c u t i v e   E d u c a t i o n . 
 
 -   I n t é g r a t i o n   d u   m e n u   e x e c u t i v e _ e d u c a t i o n _ n a v b a r . h t m l   d a n s   t o u t e s   l e s   p a g e s   d e   l a   s e c t i o n   E x e c u t i v e   E d u c a t i o n   ( d o s s i e r   c o n s e i l ) . 
 
 -   M i s e   à   j o u r   d e   e x e c u t i v e _ e d u c a t i o n _ n a v b a r . h t m l   p o u r   u t i l i s e r   l ' a r b o r e s c e n c e   e t   l e s   v u e s   ( U R L s )   e x i s t a n t e s   d a n s   m e n u . h t m l   ( T a b l e a u   d e   b o r d ,   P i p e l i n e ,   P r o d u i t s   &   S e r v i c e s ,   C l i e n t s ,   D e v i s ,   F a c t u r e s ,   G r o u p e s ,   P a r a m è t r e s ) . 
 
 -   R é d u c t i o n   d e   l a   t a i l l e   d u   h e a d e r   ( p a d d i n g s ,   m a r g e s ,   i c ô n e s )   d a n s   l e s   p a g e s   G e s t i o n   d e s   C l i e n t s   e t   G e s t i o n   d e s   P r o s p e c t s   p o u r   p l u s   d e   c o m p a c i t é . 
 
 -   R é d u c t i o n   d e   l ' e s p a c e   ( m a r g e s )   e n t r e   l e s   i n d i c a t e u r s   K P I   e t   l e   t a b l e a u   d a n s   l a   p a g e   G e s t i o n   d e s   P r o s p e c t s . 
 
 -   S u p p r e s s i o n   d u   h e a d e r   r e d o n d a n t   e t   é l a r g i s s e m e n t   d u   f o r m u l a i r e   à   1 0 0 %   d e   l a   l a r g e u r   ( c o l - 1 2 )   d a n s   l a   p a g e   d e   c r é a t i o n   d ' u n   N o u v e a u   D e v i s . 
 
 -   R é d u c t i o n   d e   l a   t a i l l e   d u   h e a d e r   e t   d e s   m a r g e s   d a n s   l a   p a g e   L i s t e   d e s   D e v i s   p o u r   p l u s   d e   c o m p a c i t é . 
 
 -   R é d u c t i o n   d e   l a   h a u t e u r   d e s   c a r t e s   K P I   d a n s   l a   p a g e   L i s t e   d e s   D e v i s   ( d i m i n u t i o n   d e s   m a r g e s ,   d e s   p a d d i n g s   e t   d e   l a   t a i l l e   d e s   i c ô n e s / t e x t e s ) . 
 
 -   A j o u t   d u   c e n t r a g e   v e r t i c a l   ( d - f l e x   f l e x - c o l u m n   j u s t i f y - c o n t e n t - c e n t e r )   p o u r   l e   c o n t e n u   d e s   c a r t e s   K P I   d a n s   l a   p a g e   L i s t e   d e s   D e v i s . 
 
 -   R é d u c t i o n   d e   l a   t a i l l e   d u   h e a d e r ,   d e s   m a r g e s   e t   d e s   c a r t e s   K P I   ( a v e c   c e n t r a g e   v e r t i c a l )   d a n s   l a   p a g e   L i s t e   d e s   F a c t u r e s . 
 
 -   S u p p r e s s i o n   d u   h e a d e r   r e d o n d a n t   e t   é l a r g i s s e m e n t   d u   f o r m u l a i r e   à   1 0 0 %   d e   l a   l a r g e u r   ( c o l - 1 2 )   d a n s   l a   p a g e   N o u v e l l e   F a c t u r e   ( m ê m e   c h o s e   q u e   p o u r   l e   D e v i s ) . 
 
 -   R é d u c t i o n   d e   l a   t a i l l e   d u   h e a d e r ,   d e s   m a r g e s   e t   d e s   c a r t e s   K P I   ( a v e c   i c ô n e s   a j u s t é e s )   d a n s   l a   p a g e   L i s t e   d e s   G r o u p e s . 
 
 -   R é d u c t i o n   d e s   m a r g e s ,   p a d d i n g s   e t   t a i l l e s   d e   t e x t e   d a n s   l ' e n - t ê t e   e t   l a   b a r r e   d ' a c t i o n   d e   l a   p a g e   C a t a l o g u e   d e s   T h é m a t i q u e s . 
 
 -   R é d u c t i o n   d e   l a   t a i l l e   e t   d e s   e s p a c e m e n t s   i n t e r n e s   d e s   c a r t e s   t h é m a t i q u e s   g é n é r é e s   d y n a m i q u e m e n t   d a n s   C a t a l o g u e   d e s   T h é m a t i q u e s . 
 
 -   R e m p l a c e m e n t   d e   t o u t e   l ' a r b o r e s c e n c e   E x e c u t i v e   E d u c a t i o n   d a n s   l a   b a r r e   l a t é r a l e   p r i n c i p a l e   ( m e n u . h t m l )   p a r   u n   l i e n   d i r e c t   v e r s   l e   T a b l e a u   d e   b o r d ,   v u   q u ' u n e   b a r r e   d e   n a v i g a t i o n   h o r i z o n t a l e   d é d i é e   e x i s t e   d é s o r m a i s . 
 
 -   C r é a t i o n   d u   T a b l e a u   d e   b o r d   C o n f i g u r a t i o n   c e n t r a l i s é   a v e c   K P I   e t   h i s t o r i q u e   r é c e n t . 
 
 -   E x t r a c t i o n   d e s   s o u s - m e n u s   C o n f i g u r a t i o n   v e r s   u n e   n a v b a r   h o r i z o n t a l e   d é d i é e   ( c o n f i g u r a t i o n _ n a v b a r . h t m l ) . 
 
 -   M i s e   à   j o u r   d u   m e n u . h t m l   p o u r   r e d i r i g e r   l ' a c c è s   p r i n c i p a l   v e r s   l e   n o u v e a u   t a b l e a u   d e   b o r d . 
 
 -   C o r r e c t i o n   d e   l ' e r r e u r   d ' i m p o r t a t i o n   ( R o l e   d e p u i s   i n s t i t u t _ a p p   a u   l i e u   d e   t _ c r m )   d a n s   l e   t a b l e a u   d e   b o r d   d e   c o n f i g u r a t i o n . 
 
 -   H a r m o n i s a t i o n   d u   d e s i g n   d u   d a s h b o a r d   d e   c o n f i g u r a t i o n   a v e c   l e   s t y l e   m o d e r n - c a r d   d e s   a u t r e s   m o d u l e s . 
 
 -   R é d u c t i o n   d e s   m a r g e s   e t   p a d d i n g s   ( m b - 4   - >   m b - 3 ,   p - 4   - >   p - 3 )   s u r   t o u t e s   l e s   p a g e s   d e   c o n f i g u r a t i o n   p o u r   m i n i m i s e r   l ' e s p a c e   p e r d u . 
 
 -   R é d u c t i o n   d e   l a   h a u t e u r   d e s   e n - t ê t e s   ( t i t r e   d e   l a   p a g e )   d a n s   t o u t e s   l e s   p a g e s   d e   c o n f i g u r a t i o n . 
 
 -   B l o c a g e   d e   l a   s u p p r e s s i o n   d e s   r é d u c t i o n s   ( R e m i s e A p p l i q u e r )   s ' i l   y   a   d é j à   d e s   p a i e m e n t s   ( P a i e m e n t s )   e n r e g i s t r é s   p o u r   l e s   p r o s p e c t s   l i é s . 
 
 -   R é d u c t i o n   d e   l a   t a i l l e   d e   l ' e n - t ê t e   e t   d e s   e s p a c e s   p e r d u s   d a n s   l a   p a g e   d e   d é t a i l s   d u   p r o s p e c t   ( C o n s e i l ) . 
 
 -   R é d u c t i o n   d e   l a   t a i l l e   d e s   c a r t e s   K P I   e t   d e s   e s p a c e m e n t s   g l o b a u x   d a n s   l a   p a g e   d e   s u i v i   d e s   d o s s i e r s   ( C R M ) . 
 
 -   R é d u c t i o n   s u p p l é m e n t a i r e   e t   a g r e s s i v e   d e   l a   t a i l l e   d e s   c a r t e s   K P I   d a n s   l e   s u i v i   d e s   d o s s i e r s   ( p - 2 ,   t i t r e s   H 4 ,   m b - 2 ,   e t c . ) . 
 
 -   É l i m i n a t i o n   d e s   e s p a c e s   p e r d u s   d a n s   l a   v u e   l i s t e   d e s   p r o s p e c t s   ( C R M )   ( m a r g e s   e t   p a d d i n g s   r é d u i t s ) . 
 
 -   É l i m i n a t i o n   d e s   e s p a c e s   p e r d u s   d a n s   l a   v u e   l i s t e   d e s   p r é i n s c r i t s   ( C R M )   ( m a r g e s   e t   p a d d i n g s   r é d u i t s ) . 
 
 -   H a r m o n i s a t i o n   d u   d e s i g n   d e s   c a r t e s   K P I   d e   l a   L i s t e   d e s   P r o s p e c t s   a v e c   c e l l e s   d e   l a   L i s t e   d e s   P r é i n s c r i t s   ( a f f i c h a g e   F l e x b o x   h o r i z o n t a l ,   c o m p a c i t é   m a x i m a l e ) . 
 
 
- Réduction des marges, des paddings et de la taille du header et des cartes KPI sur la page calendrier (communication/calendar/)

- Espacement des boutons (switches de filtre et boutons du calendrier) sur la page calendrier (communication/calendar/) pour une meilleure disposition et lisibilité.

- Correction de l'espacement des boutons du calendrier (Mois, Semaine, Jour) via CSS (!important) pour s'assurer qu'ils ne sont plus collés.

- Réduction des marges verticales, du gap, et du padding interne dans les sections du formulaire (crm/inscription-particulier/) pour éliminer les espaces perdus.

- Déplacement de la page de gestion des réductions (gestion-des-reductions/) du module CRM vers le module Comptabilité/Trésorerie. Suppression de la barre de navigation CRM pour cette page.

- Restauration de l'en-tête de la page de gestion des réductions (comptabilite/tresorerie/gestion-des-reductions/) contenant le bouton d'application de réduction, adapté avec le fil d'Ariane Trésorerie.

### 07-07-2026
- **Trésorerie** : Ajout du montant total des dus et des montants déjà payés pour les instances de paiements dans la vue AttentesPaiements et le template ttentes_de_paiement.html.
- **Trésorerie** : Modification pour afficher le montant total des dus et les montants déjà payés pour **chaque ligne** (au niveau du tableau) au lieu de KPIs globaux.
- **Trésorerie** : Inclusion des rais_inscription (de la Spécialité ou Double Diplomation) dans le calcul du montant dû par ligne pour les instances de paiements.
- **Trésorerie** : Ajout d'un filtre par spécialité dans la page Suivi des paiements.
- **Trésorerie** : Activation de la recherche (Select2) sur les filtres de la page Suivi des paiements.
- **Trésorerie** : Correction du design CSS de Select2 pour correspondre au style 'btn-rounded' de la page Suivi des paiements.
- **Trésorerie** : Synchronisation automatique de la spécialité sélectionnée lorsqu'un groupe est choisi dans la page Suivi des paiements.
- **Conseil** : Harmonisation du design des boutons (ajout de l'aspect arrondi 'btn-rounded' et des ombres 'shadow-primary') sur la page Pipeline.
- **Conseil** : Ajustement de la mise en page de la page Pipeline pour l'aligner parfaitement avec le menu de navigation (utilisation de 'container-fluid' et 'page-content').
- **Conseil** : Correction du bug d'affichage sur les boutons de bascule de vue (Kanban/Liste) dans la page Pipeline.
- **Conseil** : Implémentation fonctionnelle de la vue Liste pour les opportunités du Pipeline (table avec détails, budget, dates et actions), et activation du bouton de bascule Kanban/Liste avec mémorisation du choix.
- **Conseil** : Correction de l'arrière-plan de la vue Liste du Pipeline (ajout de la classe CSS 'glass-card' manquante).
- **Conseil** : La validation des prospects (transformation en client) nécessite désormais la permission spécifique 'approuver' sur le module Conseil au lieu de la simple permission de modification. Le bouton de validation dans les détails du prospect a également été masqué pour les utilisateurs ne possédant pas ce privilège dans leur rôle.
- **Trésorerie** : Sur la page des détails d'une demande de paiement, la vue n'est plus bloquée si aucun échéancier n'est configuré. L'affichage normal des informations est préservé et un bandeau rouge est rajouté en haut pour signaler l'absence d'échéancier, avec un bouton permettant d'en configurer un spécial.
- **Trésorerie** : Extension de l'amélioration de l'affichage en cas d'absence d'échéancier (bandeau rouge non bloquant) pour la vue des paiements de Double Diplomation.
- **Trésorerie** : Correction d'une erreur 500 (\AttributeError\) sur l'API \ApiListeDemandePaiement\ causée par une tentative de lecture des frais d'inscription sur l'objet Spécialité. Les frais d'inscription sont désormais correctement lus depuis l'échéancier configuré (normal ou spécial) de la demande.
- **Trésorerie** : Résolution de l'erreur \AttributeError: 'NoneType' object has no attribute 'id'\ sur \ApiGetDetailsDemandePaiementDouble\ qui survenait lorsqu'aucun échéancier n'était trouvé, permettant ainsi à la notification (bandeau rouge) d'absence d'échéancier de fonctionner correctement sur le front-end.
- **Trésorerie** : Ajout de la définition des entités pour chaque tranche dans la génération de l'échéancier spécial pour le cas de Double Diplomation. La colonne cachée Entité est désormais visible avec un menu déroulant permettant la sélection correcte des entités pour chaque tranche.
- **Trésorerie** : Ajout de la pré-sélection automatique intelligente de la tranche à payer dans la modale d'enregistrement de paiement (cas standard et double). Le système trie désormais la liste déroulante par date d'échéance puis par ordre, et sélectionne automatiquement la tranche non payée la plus ancienne, tout en laissant la liste déroulante accessible pour un choix manuel.

- Ajout d'une nouvelle API (ApiStoreSingleReduction) pour l'application directe d'une rÃ©duction Ã  un prospect depuis les pages de dÃ©tails de paiement.
- IntÃ©gration du bouton et de la modale de rÃ©duction dans details_attente_paiement.html et details_attente_paiement_double.html.

- Harmonisation du design de la modale d'application de rÃ©duction (configureRemiseModal) avec le style premium des autres modales (utilisation de glass-modal-content, modern-label, etc.) dans les templates standard et double.

- Correction de l'affichage des boutons Annuler/Appliquer dans la modale de rÃ©duction (remplacement de tn-premium-action par les classes tn-modern appropriÃ©es pour afficher correctement le texte et l'icÃ´ne).

- RÃ©solution de l'erreur 500 sur ApiApplyRemiseToPaiement : changement de l'identifiant du bouton d'application dans configureRemiseModal (de pplyReductionBtn vers submitDirectReductionBtn) pour Ã©viter un conflit avec le bouton d'application de remise standard existant qui dÃ©clenchait une double requÃªte AJAX erronÃ©e.

- Correction de l'Ã©vÃ©nement de clic sur submitDirectReductionBtn : passage Ã  une dÃ©lÃ©gation d'Ã©vÃ©nement ($(document).on(...)) car le script s'exÃ©cute avant que la modale ne soit rendue dans le DOM, ce qui rendait le bouton non cliquable.

- Correction de l'erreur JavaScript clientId is not defined lors de la soumission de la remise directe : utilisation de la variable de template Django {{ prospect.id }} Ã  la place.

- Correction de l'erreur 400 (Bad Request) lors de la crÃ©ation d'une remise : l'ID du prospect Ã©tait manquant car la variable de template {{ prospect.id }} n'Ã©tait pas dÃ©finie dans ce contexte. RÃ©cupÃ©ration sÃ©curisÃ©e via le champ cachÃ© $('#clientIdInput').val().

- Ajout d'un rafraÃ®chissement des donnÃ©es du prospect (via loadDatas()) Ã  la suite d'une crÃ©ation de remise directe, ce qui permet d'afficher immÃ©diatement la notification de remise en attente sans nÃ©cessiter de rechargement manuel de la page.

- Regroupement des champs Fournisseur, Entite et Date sur la meme ligne dans le formulaire de creation de depense (col-lg-4).

- AmÃ©lioration visuelle dans la configuration du devis (configure-devis.html) : modification du fond de la zone d'ajout d'une prestation (	foot) avec une couleur bleutÃ©e douce (#f4f7fb) et une bordure en pointillÃ©s pour la distinguer plus clairement du fond blanc de la carte.

- Correction de la prioritÃ© CSS sur le fond de la zone d'ajout dans configure-devis.html (application de la couleur #f4f7fb directement sur les 	d pour surcharger le fond par dÃ©faut de Bootstrap).

- Ajout de marges intÃ©rieures (padding) Ã  la carte des Prestations & Articles dans configure-devis.html pour l'aligner avec les autres blocs et l'encadrer correctement sur le fond blanc.

- RÃ©solution de l'erreur 500 (AttributeError: \'NoneType\' object has no attribute \'entite\') dans l'API ApiGetDetailsDemandePaiement : gestion sÃ©curisÃ©e lorsque l'Ã©chÃ©ancier (echeancierId) est inexistant ou non dÃ©fini, avec affichage de la mention 'DonnÃ©es manquantes (EntitÃ©)' au lieu de faire planter la requÃªte.

- RÃ©solution de l'erreur 500 (TypeError: unsupported operand type(s) for +=: \'decimal.Decimal\' and \'NoneType\') dans la vue AttentesPaiements : sÃ©curisation du calcul du total des attentes (	otal_dus += (amount or 0)) pour Ã©viter un plantage lorsqu'une spÃ©cialitÃ© ou une instance n'a pas de prix dÃ©fini.

- Correction de l'affichage du montant dÃ» dans /comptabilite/tresorerie/attentes-de-paiements/ : le montant affichÃ© et le total global sont dÃ©sormais calculÃ©s Ã  partir des Ã©chÃ©ances rÃ©ellement gÃ©nÃ©rÃ©es (DuePaiements) pour chaque prospect. Si l'Ã©chÃ©ancier n'est pas encore gÃ©nÃ©rÃ©, le montant est Ã©valuÃ© Ã  0 (affichÃ© comme Non disponible), Ã©vitant ainsi d'afficher un prix thÃ©orique trompeur.

- Correction d'un bug potentiel dans l'API ApiListeDemandePaiement et la vue AttentesPaiements : suppression du filtre sur la promo lors de la rÃ©cupÃ©ration des DuePaiements (ce modÃ¨le ne possÃ¨de pas de champ promo), ce qui permet aux Ã©tudiants en double diplomation (et standards) d'avoir un total affichÃ© strictement identique Ã  celui de leur page de dÃ©tails.

- AmÃ©lioration de l'expÃ©rience utilisateur (UX) dans /comptabilite/tresorerie/attentes-de-paiements/ : ajout d'une animation de chargement (spinner) dans le tableau lors de la rÃ©cupÃ©ration asynchrone des donnÃ©es (loadItems), permettant d'indiquer visuellement que les donnÃ©es sont en cours de traitement.

- Correction du comportement de l'animation de chargement dans /comptabilite/tresorerie/attentes-de-paiements/ : ajout d'une sÃ©curitÃ© (flag isLoading) pour empÃªcher les autres Ã©vÃ©nements de la page (comme l'initialisation des filtres de date, promo ou spÃ©cialitÃ©) d'interrompre l'animation en redessinant le tableau trop tÃ´t avec un message de liste vide.

- Finalisation de l'animation de chargement du tableau dans /comptabilite/tresorerie/attentes-de-paiements/ : utilisation de l'API native de DataTables (sEmptyTable) pour afficher le spinner. Cela permet aux filtres de rester fonctionnels pendant le chargement sans faire disparaÃ®tre l'animation prÃ©maturÃ©ment.

- Correction critique du calcul de la SynthÃ¨se FinanciÃ¨re dans les dÃ©tails des demandes de paiement (Standard et Double Diplomation) : le Total initial/dÃ» est dÃ©sormais calculÃ© et affichÃ© correctement mÃªme lorsque l'Ã©tudiant a rÃ©glÃ© toutes ses Ã©chÃ©ances (has_due_paiement = False), et s'appuie dynamiquement sur le prix de la formation (+ frais - remises) si l'Ã©chÃ©ancier n'a pas encore Ã©tÃ© gÃ©nÃ©rÃ©.

- Changement du nom du menu 'Relation Client' en 'Gestion des admissions' dans templates/tenant_folder/menu.html et templates/public_folder/menu_.html
-   C o r r e c t i o n   d u   f o r m a t a g e   d e   l ' a f f i c h a g e   d u   p o u r c e n t a g e   d e   p r o g r e s s i o n   d a n s   d i s p a t c h _ b u d g e t . h t m l   ( a j o u t   d e   s é p a r a t e u r s   d e   m i l l i e r s ) 
 
 -   A u g m e n t a t i o n   d e   l a   p r é c i s i o n   d e s   m o n t a n t s   b u d g é t a i r e s   ( m a x _ d i g i t s   d e   1 2   à   2 0 )   p o u r   é v i t e r   l ' e r r e u r   d e   d é p a s s e m e n t   d e   l i m i t e   ( o v e r f l o w )   a v e c   l e s   g r a n d s   m o n t a n t s 
 
 -   S u p p r e s s i o n   d e s   c o n t o u r s   c o l o r é s   e t   d e   l a   b a r r e   d e   p r o g r e s s i o n   s u r   l e s   c a r t e s   K P I   d a n s   d i s p a t c h _ b u d g e t . h t m l 
 
 -   A f f i c h a g e   d e   l a   d e s c r i p t i o n   d e s   p o s t e s   b u d g é t a i r e s   s o u s   l e u r s   l a b e l s   d a n s   l e s   t a b l e a u x   ( R e c e t t e s   e t   D é p e n s e s ) 
 
 -   A f f i c h a g e   d e   l a   d e s c r i p t i o n   p o u r   l e s   p o s t e s   p a r e n t s   ( l i g n e s   d e s   t o t a u x )   d a n s   l e s   t a b l e a u x   b u d g é t a i r e s 
 
 -   A f f i c h a g e   d e   l a   d e s c r i p t i o n   p o u r   l e s   p o s t e s   b u d g é t a i r e s   ( p a r e n t s   e t   e n f a n t s )   d a n s   l a   v u e   d e   s u i v i   d e   r é a l i s a t i o n   d u   b u d g e t 
 
 -   C o r r e c t i o n   d u   c h a m p   d e   s é l e c t i o n   d e   l a   T h é m a t i q u e   d a n s   l a   c o n f i g u r a t i o n   d u   d e v i s   p o u r   p e r m e t t r e   l a   c r é a t i o n   d e   n o u v e l l e s   t h é m a t i q u e s   n o n   e x i s t a n t e s   ( t a g s :   t r u e   a j o u t é ) 
 
 -   S u p p r e s s i o n   d e s   e s p a c e s   p e r d u s   e t   d e   l ' o n g l e t   ' S p é c i a l i t é s   A c a d e m i c '   d a n s   l a   v u e   d e   l i s t e   d e s   t h é m a t i q u e s   ( f u s i o n   d e   l ' a c t i o n   b a r   a v e c   l ' e n t ê t e ) 
 
 -   S u p p r e s s i o n   d e   l a   s e c t i o n   d e s   K P I s   d a n s   l a   p a g e   d e s   p r o s p e c t s   e n   i n s t a n c e 
 
 -   S u p p r e s s i o n   d u   h e a d e r   ' G e s t i o n   d e s   D e v i s '   e t   d é p l a c e m e n t   d u   b o u t o n   ' N o u v e a u   D e v i s '   d a n s   l a   b a r r e   d ' a c t i o n   d e   l a   t a b l e   ( c o n s e i l / l i s t e - d e s - d e v i s / ) 
 
 -   A j o u t   d u   m e n u   ' N o u v e l l e   f a c t u r e '   s o u s   l ' o n g l e t   F a c t u r e s   ( n a v b a r   c o n s e i l )   e t   s u p p r e s s i o n   d u   h e a d e r   a v e c   d é p l a c e m e n t   d u   b o u t o n   d a n s   l a   p a g e   d e s   f a c t u r e s   ( c o n s e i l / l i s t e - d e s - f a c t u r e s / ) 
 
 -   A f f i c h a g e   d e s   d é t a i l s   ( t o t a l )   d e   c h a q u e   s o u s - p o s t e   b u d g é t a i r e   d a n s   l a   p a g e   d e   r é v i s i o n   d e s   c a m p a g n e s   b u d g é t a i r e s   d e   l ' a d m i n i s t r a t i o n   ( c o n f i g u r a t i o n / b u d g e t - c a m p a i g n s / . . . / r e v i e w / . . . ) 
 
 -   A j o u t   d e   l ' i n t e r a c t i o n   ( d é r o u l e m e n t / c o l l a p s e )   p o u r   a f f i c h e r / m a s q u e r   l e s   d é t a i l s   d e s   s o u s - p o s t e s   d a n s   l a   p a g e   r e v i e w   d u   b u d g e t   ( y   c o m p r i s   d a n s   l a   M a t r i c e   d e   S u i v i ) 
 
 -   A f f i c h a g e   d é t a i l l é   ( P r é v u ,   R é a l i s é ,   É c a r t )   d e   c h a q u e   c o m p t e / c a t é g o r i e   d a n s   l a   M a t r i c e   d e   S u i v i   ( b u d g e t   r e v i e w ) 
 
 -   A j o u t   d e   l ' o n g l e t   d e   c o m p a r a i s o n   B u d g e t   N   v s   N - 1   p a r   t r i m e s t r e   d a n s   l ' i n t e r f a c e   d e   r é v i s i o n   b u d g é t a i r e 
 
 - Fix NameError 'tenants is not defined' in budget_campaign_review view (associe_app\views.py). Updated context dictionary to match actual local variables and template requirements.
- Fix empty 'Matrice de Suivi' by adding missing 'combined_postes' to the context in budget_campaign_review.
- Removed the deduction of refunded amounts from revenues in budget realization calculation (associe_app\budget_utils.py) to prevent double-counting when calculating net totals.
- Excluded registration fees ('frais d''inscription') from the collected amount (total_paye) in the refunds list API (ApiLoadRemboursements) to avoid refunding registration fees.
- Modified ApiLoadRemboursements to include all payments made by a prospect (regardless of context or frais d'inscription) in the total collected amount (total_paye).
- Added ApiGetClientPaiementsForRefund to fetch payments for a client. Updated refund request modal in liste-des-rembourssement.html to fetch and display this list of payments.
- Widened the refund request modal in liste-des-rembourssement.html by adding the 'modal-lg' class to accommodate the new payments table.
- Fixed total calculation in ApiSearchProspectForRefund to include 'frais d''inscription', and added the payment label (paiement_label) column to the refund modal's payments table.
- Removed exclusions for 'frais d''inscription' in DetailsRembourssement (t_tresorerie/f_views/rembourssement.py) and ApiLoadRefundDetails (t_tresorerie/views.py) to ensure all payments are counted in the refund module.
- Reduced the size of the background icons in the refund details modal (remboursement.html) from 4rem to 2rem.
- Replaced the generic user icon in the refund details modal (remboursement.html) with a badge displaying the client's initials.
- Added initials badges to the clients list in the main refunds page (remboursement.html).
- Fixed deletion procedure in 'modeles-echeancier': created a dedicated API endpoint (ApiDeleteModeleEcheancier) to delete ModelEcheancier instances instead of incorrectly calling the EcheancierPaiement delete API. Backend delete permissions ('tre', 'delete') are fully enforced on the new endpoint.
- Made the 'Frais d''inscription' toggle in the 'Create Echeancier Model' modal checked and disabled by default so it cannot be toggled off.
- In 'configuration-des-echeancier' (edit echeancier modal), added a delete button (trash icon) to each tranche row so users can remove unwanted tranches. Also updated the backend save logic to actually delete the omitted EcheancierPaiementLine from the database upon save.
- Corrected the 'delete tranche' feature to apply to the 'creer-un-echeancier.html' template as well, adding a trash button next to the date for dynamically created tranche blocks.
- Restricted the 'delete tranche' feature to only be available when the model is in 'double diplomation' mode. Hidden (via d-none class) for standard models in both creation and edit interfaces.
- Removed the percentage (Part) column/input from the schedule (échéancier) creation and configuration modals. Made the amount (Montant) fields directly editable. Added a total verification footer that ensures the sum of the installments matches the expected net total.
- Ensured the verification footer in the creation modal is generated per-block (per specialty) instead of globally. This allows independent verification for double diplomation models where specialties have different prices.
- Fixed an issue where the 'Total Montant' footer in the schedule creation modal displayed '0 DA' initially. It now correctly calculates and displays the totals immediately after the schedule is generated.
- Fixed validation tolerance in schedule creation: the total amount must now match exactly to the centime (0.01 DA precision) instead of allowing a 1 DA margin of error.
- Removed the 'Répartition' (Part/Percentage) column from the schedule details modal (Détails du Plan de Paiement) in the 'echeanciers configurés' page.
- Removed the notification banners ('Information Importante' and 'Liaison Entité Légale') from the 'echeanciers configurés' page.
- Replaced the 'ID' column with the client's initials in the 'echeanciers spéciaux' page.
- Removed the 'Informations importantes' notification banner and added the display of the promotion code under the promotion name in the 'Suivi des échéanciers' page.
- Updated the 'Suivi des échéanciers' page to display the promotion's 'libellé' (label) instead of the session and year, while maintaining the promo code display.
- Removed the 'Vue par Prospect' section and its toggle buttons from the 'Suivi des échéanciers' page.
- Added a 'cursor: pointer' CSS rule to the rows of the 'Suivi des échéanciers' table so the cursor changes on hover.
- Removed the hover animation (transform and shadow change) from the section cards in both standard and double 'Détails du suivi des échéanciers' pages.
- Reduced the bottom margin of section cards (from 1.5rem to 0.5rem) to eliminate wasted space between sections in both 'Détails du suivi des échéanciers' pages.
- Modified KPI card column classes in 'Demandes de Paiement' page (added col-xl) so they are displayed on the same line on large screens.
- Reduced the content size inside KPI cards (padding, font sizes, icons) in the 'Demandes de Paiement' page to keep them coherent and proportionate when displayed on a single line.

- [2026-07-11] Correction du template 'dolibare' pour le tenant 'alger' (Erreur de génération : Could not parse the remainder: '>' from '>') : Remplacement de '{% if show_remise and total_remise > 0 %}' par '{% if show_remise and total_remise %}'.

- [2026-07-11] Correction des chemins relatifs (assets/...) dans app.js vers des chemins absolus (/static/assets/...) pour eviter les erreurs 404 hors de la racine.

- [2026-07-11] Retrait du doublon d'importation de 'alertify.min.js' dans 'details_devis.html' (générant une erreur 404), car déjà chargé via CDN dans 'base.html'.

- [2026-07-11] Correction réelle du template 'dolibare' (alger) : L'erreur persistait car le symbole > était encodé en HTML (&gt;) en base de données, empêchant le parser Django de l'interpréter.

- [2026-07-11] Restructuration de la table HTML du template 'dolibare' (alger) : L'éditeur WYSIWYG avait déplacé la balise {% for ligne in lignes %} hors du tableau HTML car elle n'était pas placée dans un conteneur valide comme <tbody>. Je l'ai replacée à l'intérieur de <tbody> pour entourer correctement la balise <tr>, résolvant ainsi les [MANQUANT: ligne.xxx] sur le devis généré.

- [2026-07-11] Correction de la mise en page PDF globale : Suppression de l'en-tête (header) et du pied de page (footer) génériques forcés par 'pdf_base.html' (qui causaient une ligne grise vide en haut du document) afin de laisser les templates personnalisés gérer entièrement leur propre affichage.

- [2026-07-11] Personnalisation du nom de fichier PDF généré : Ajout d'une logique dans 'DocumentExportView' pour nommer le fichier téléchargé avec la référence correspondante (ex: 'Devis_DEVIS-0001.pdf' ou 'Facture_XXXX.pdf') à la place d'un nom générique ('document_XX.pdf') en récupérant les données depuis le contexte.

- [2026-07-11] Correction de l'affichage du logo sur le PDF : Remplacement des URLs HTTP vers les images (ex: http://localhost:8000/media/...) par des chemins locaux (file:///) dans DocumentExportView afin de permettre à WeasyPrint de charger les logos correctement. Suppression du footer (Date générée et remerciement) dans le template 'dolibare'.

- [2026-07-11] Correction de l'erreur TypeError 'Path.replace() takes 2 positional arguments but 3 were given' : conversion de 'settings.MEDIA_ROOT' (qui est un objet Path) en chaîne de caractères (str) dans pdf_editor/views.py avant d'appliquer la méthode .replace().

- [2026-07-11] Ajustement du modèle 'dolibare' (Alger) : Modification de la logique conditionnelle de l'en-tête pour afficher la désignation de l'entreprise (en titre h1) systématiquement, même lorsque le logo est présent (auparavant, la présence du logo masquait le nom de l'entreprise).

- [2026-07-11] Ajout de la colonne 'Unité' dans le devis (et facture) : Ajout du champ 'unite' dans le contexte retourné par les vues 'PrintDevisConseil' et 'PrintFactureConseil' de t_conseil. Modification du modèle de document 'dolibare' (Alger) pour insérer la nouvelle colonne Unité (en-tête et valeur) juste après la quantité.

- [2026-07-11] Masquage intelligent de la remise dans le PDF : Ajout d'une condition dans les vues 'PrintDevisConseil' et 'PrintFactureConseil' pour désactiver dynamiquement l'affichage de la remise (colonne 'Remise' et ligne 'Remise Globale') si la remise totale est égale à zéro, afin de ne pas encombrer le document de zéros inutiles.

- [2026-07-11] Affichage de la devise Algérienne (DA) : Modification du modèle 'dolibare' (Alger) pour inclure ' DA' à côté de chaque montant monétaire (Prix unitaire, Total ligne, Total HT, Remise Globale, TVA, Total TTC) afin d'afficher la devise explicitement.

- [2026-07-11] Correction des sauts de ligne pour la devise (DA) : Remplacement de l'espace classique par un espace insécable (&nbsp;) et ajout de la règle CSS 'white-space: nowrap' dans le modèle 'dolibare' (Alger) pour s'assurer que le montant et sa devise (ex: 313920,00 DA) restent toujours attachés sur la même ligne.

- [2026-07-12] Restriction du bouton de suppression de l'Ã©chÃ©ancier spÃ©cial : Le bouton a Ã©tÃ© retirÃ© des pages dÃ©tails_attente_paiement (standard et double) pour n'Ãªtre disponible que sur la page liste_echeancier_special, avec une vÃ©rification de la permission de suppression ('tre', 'delete').

- [2026-07-12] Ajout des logs d'actions (UserActionLog) : Les actions d'approbation, de rejet et de suppression des Ã©chÃ©anciers spÃ©ciaux sont dÃ©sormais tracÃ©es et enregistrÃ©es dans administration/user-logs.

- [2026-07-12] PrÃ©vention de la double crÃ©ation d'Ã©chÃ©ancier spÃ©cial : Ajout d'une sÃ©curitÃ© (dÃ©sactivation temporaire et suivi d'Ã©tat) sur les boutons saveSpecialEcheancierBtn et confirmSaveEcheancierBtn dans les vues details_attente_paiement (standard et double) afin d'empÃªcher les soumissions multiples accidentelles (double-clic).

- [2026-07-12] Correction de la mise Ã  jour des Ã©chÃ©anciers : Ajout de la possibilitÃ© de crÃ©er de nouvelles tranches lors de la modification d'un Ã©chÃ©ancier configurÃ©, ce qui n'Ã©tait pas pris en compte auparavant et bloquait l'affichage des modifications dans les dÃ©tails de la demande de paiement.

- [2026-07-12] Correction de la modification d'échéanciers : Correction d'un bug majeur où la modification d'un échéancier configuré supprimait par erreur les tranches des autres modèles (ex: double diplomation) et n'appliquait pas correctement les changements de date pour les échéanciers secondaires. La mise à jour est désormais basée sur l'ordre indexé des tranches au lieu d'IDs partagés, ce qui préserve l'intégrité de toutes les tranches des modèles.
-   C o r r e c t i o n   d u   b u g   c a u s a n t   l a   d øs a c t i v a t i o n   a c c i d e n t e l l e   d e s   øc h øa n c i e r s   ( i s _ a c t i v e = F a l s e )   l o r s   d e   l a   m o d i f i c a t i o n   d e p u i s   l ' i n t e r f a c e   ( d e t a i l s - p a i e m e n t - r e q u e s t ) . 
 
 - [2026-07-13] Désactivation du bouton 'Appliquer une réduction' (btnConfigureRemiseDirect) dans details_attente_paiement.html et details_attente_paiement_double.html une fois que les paiements dus sont générés.
- [2026-07-13] Désactivation du bouton 'Appliquer une réduction' (btnConfigureRemiseDirect) dans details_attente_paiement.html et details_attente_paiement_double.html si une demande de réduction existe (qu'elle soit en attente, approuvée ou appliquée).
- [2026-07-14] Ajout du menu de la scolarité dans la page d'affectation au groupe (affectation_au_groupe.html).
- [2026-07-14] Ajout de l'affichage du code de la spécialité dans les cartes de la liste des groupes (liste_des_groupes.html).
- [2026-07-14] Ajout de l'affichage des codes de spécialité dans le menu déroulant de sélection des spécialités sur la page de création d'un nouveau groupe (nouveau_groupe.html) et mise à jour de l'API (ApiSelectSpecialite) correspondante.
- [2026-07-14] Correction de l'erreur NameError 'statuses' is not defined dans la vue crm_user_logs (associe_app/views.py) en supprimant le code copié inutilement et en corrigeant les variables du dictionnaire context.
- [2026-07-14] Correction du filtrage par formation dans la page 'attentes-de-paiements' (t_tresorerie/views.py) en prenant en compte la formation liée à la spécialité lorsqu'elle n'est pas définie directement sur la demande de paiement.
- [2026-07-14] Correction définitive du filtrage par formation dans les attentes de paiements : utilisation de l'ID entier de la formation au lieu du code texte de la spécialité (t_tresorerie/views.py).
- [2026-07-14] Ajout de l'affichage du code de la spécialité dans la colonne Formation/Spécialité de la liste des attentes de paiement (attentes_de_paiement.html et t_tresorerie/views.py).
- [2026-07-14] Déblocage du bouton 'Confirmer l'inscription' (btnConfirmInscription) même lorsqu'il n'y a pas de paiements effectués, pour les cursus standards (details_attente_paiement.html) et double diplomation (details_attente_paiement_double.html).
- [2026-07-14] Correction d'une erreur NameError ('statuses' is not defined) dans la vue 'platform_usage_rate' (associe_app/views.py) en supprimant du code mort copié de la vue des statistiques et en corrigeant le dictionnaire de contexte.
- [2026-07-14] Ajout de la date de création dans le tableau de la liste des promotions (t_formations/views.py et templates/tenant_folder/formations/promos/list_promos.html).
- [2026-07-14] Ordonnancement explicite de la liste des promotions par date de création ('-created_at') pour afficher les plus récentes en premier (t_formations/views.py).
- [2026-07-14] Mise à jour du tableau de bord de la scolarité (scolarite/etudiants/dashboard/) pour afficher la formation et le code de la spécialité dans l'aperçu des groupes récents, avec optimisation de la requête (select_related) pour éviter le problème N+1.
- [2026-07-14] Ajout d'une pagination au tableau 'Aperçu des Groupes Récents' du tableau de bord de la scolarité et correction de l'affichage de la formation pour utiliser 'nom' au lieu de 'label' (t_etudiants/f_views/dashboard.py et scolarite_dashboard.html).
- [2026-07-14] Création et intégration du menu de navigation 'Direction' (direction_navbar.html) sur les pages du tableau de bord directeur et de gestion des budgets.
- [2026-07-14] Création du menu déroulant 'Manager' dans menu.html regroupant le Tableau de bord et les Campagnes budgétaires.
- [2026-07-14] Simplification du menu dans menu.html : le lien 'Manager' est désormais un accès direct (sans sous-menu), similaire aux autres modules.
- [2026-07-14] Réduction des espaces perdus dans le contenu des pages du module Manager (directeur.html, my_campaigns.html, dispatch_budget.html, request_extension.html, realization_budget.html) tout en préservant la taille de la barre de navigation.
- [2026-07-14] Suppression des effets de survol (transform, box-shadow) sur les cartes et les lignes de tableau du tableau de bord directeur.
- [2026-07-14] Suppression du titre et du fil d'Ariane sur la page du tableau de bord directeur pour réduire les espaces perdus.
- [2026-07-14] Suppression de l'effet de survol sur les cartes dans la page mes-campagnes-budgetaires.
- [2026-07-14] Suppression du badge de date (Aujourd'hui) et de la rangée correspondante sur le tableau de bord directeur pour éliminer totalement les espaces perdus sous la barre de navigation.
- [2026-07-14] Migration du référentiel des postes budgétaires : remplacement de la fenêtre modale par une page dédiée, avec ajout d'un lien dans le menu de navigation Direction (sous Budget).
- [2026-07-14] Correction d'une erreur (NameError: PostesBudgetaire is not defined) en ajoutant l'import du modèle PostesBudgetaire dans institut_app/views.py.
- [2026-07-14] Correction d'un bug de style sur la page du référentiel des postes budgétaires (le CSS .tree-content manquait le display: flex et align-items: center suite à la migration).
- [2026-07-14] Alignement des sections du référentiel des postes budgétaires avec le menu de navigation en retirant les sur-couches 'row' et 'col-12' qui créaient un décalage dû au padding.
- [2026-07-14] Réduction de l'espacement entre les différentes sections sur le tableau de bord directeur (remplacement des marges mb-4 par mb-3 et des gouttières g-4 par g-3).
- [2026-07-14] Suppression de l'en-tête (Header) de la page calendrier dans le module communication.
- [2026-07-14] Suppression de l'en-tête (Header) de la page du tableau de bord dans le module configuration.
- [2026-07-14] Correction d'un dysfonctionnement lors de l'application de la réduction (remise) en pourcentage dans la configuration des échéanciers : résolution d'un problème de conversion des nombres à virgules (JS parseFloat ne gérait pas les virgules) et ajout de la logique backend pour récupérer dynamiquement le tarif de la formation si le champ n'est pas rempli au départ.
- [2026-07-14] CRM (Détails Prospect) : Maintien de l'affichage du bouton de Double Diplomation même dans le cas d'une annulation d'inscription pour permettre la réinitialisation ou le changement de cursus.
- [2026-07-14] CRM (Détails Prospect) : Correction de l'affichage du bouton de Double Diplomation pour les prospects annulés mais qui étaient initialement dans l'état accepté (priorisation du statut annulé sur l'état accepté).
- [2026-07-14] CRM (Détails Prospect) : Amélioration de la détection de l'annulation d'un prospect en se basant sur la présence du motif d'annulation (même si le statut principal n'est pas explicitement mis à jour) afin de garantir le bon affichage du bouton Double Diplomation.
- [2026-07-14] CRM (Liste des préinscrits) : Ajout du code et de la version de la spécialité dans le menu déroulant du filtre par spécialité (pour les spécialités simples et les doubles diplomations).
- [2026-07-14] Trésorerie (Échéanciers) : Correction de l'affichage de la valeur de la remise dans le formulaire de modification de l'échéancier (ajout de la donnée manquante dans la réponse de l'API backend).
- [2026-07-14] Trésorerie (Échéanciers) : Ajout d'une sécurité UX forçant la valeur par défaut à 0 pour les champs de remise et majoration s'ils sont laissés vides par l'utilisateur.
- [2026-07-14] Trésorerie (Échéanciers) : Correction du système de recalcul des tranches qui figeait les montants à leurs anciennes valeurs en cas d'annulation de la remise ; le calcul se base désormais strictement sur le taux et le tarif initial de chaque tranche.
- [2026-07-14] Trésorerie (Échéanciers) : Rétro-compatibilité : recalcul dynamique du taux de la tranche dans le backend (si le taux enregistré en base de données était 0 ou invalide suite à de précédentes modifications manuelles), permettant de restaurer le montant initial théorique complet (Tarif de base) lors de l'annulation d'une remise.
- [2026-07-14] CRM (Prospects) : Correction de l'erreur 500 sur l'API ApiCreateVoeux causée par des requêtes GET inattendues (vérification de la méthode POST et des champs obligatoires ajoutée).
- [2026-07-15] Trésorerie : Correction de la nomenclature des tranches lors de l'application d'un échéancier pour une double diplomation. Les libellés d'origine du modèle sont désormais conservés au lieu d'être renommés séquentiellement en 'Tranche N'.
- [2026-07-15] ScolaritÃ© (Affectation) : Ajout d'une colonne listant le total des Ã©tudiants dÃ©jÃ  affectÃ©s aux groupes pour chaque spÃ©cialitÃ© de la promotion (les Ã©tudiants en double diplomation sont comptabilisÃ©s une fois pour chaque groupe concernÃ©).
- [2026-07-15] ScolaritÃ© (Affectation) : Correction du dÃ©compte des Ã©tudiants affectÃ©s dans la modale en se basant sur l'existence rÃ©elle des affectations aux groupes (AffectationGroupe) au lieu de l'attribut prospect__is_affected qui pouvait Ãªtre dÃ©synchronisÃ©.
- [2026-07-15] ScolaritÃ© (Affectation) : Uniformisation du dÃ©compte des Ã©tudiants en attente avec la mÃªme logique que les affectÃ©s (basÃ©e sur l'absence d'enregistrement dans AffectationGroupe au lieu du statut is_affected). Les spÃ©cialitÃ©s sans aucun Ã©tudiant en attente sont correctement filtrÃ©es.
- [2026-07-15] ScolaritÃ© (Affectation) : Correction de l'erreur qui masquait les spÃ©cialitÃ©s de la modale. Les spÃ©cialitÃ©s s'affichent dÃ©sormais tant qu'il y a des Ã©tudiants (en attente ou dÃ©jÃ  affectÃ©s) et mise Ã  jour du message d'information correspondant.
- [2026-07-15] ScolaritÃ© (Affectation) : Harmonisation du design de la modale avec la page principale (retrait du double effet glass-card, ajustement des espacements de la table et harmonisation du bouton d'action en btn-soft-primary).

- Ajout de la possibilité de supprimer les tranches d'échéancier (Montants dus) individuellement si elles ne sont pas associées à des paiements.

- Correction de l'erreur NoReverseMatch causée par un mauvais espace de nom (namespace) 'tre' au lieu de 't_tresorerie' pour la route de suppression de tranche.

- Remplacement de la confirmation de suppression Alertify par une fenêtre modale Bootstrap plus ergonomique pour la suppression d'une tranche d'échéancier.

- Application du mécanisme de suppression de tranches et de la modale Bootstrap à l'interface double (details-suivie-echeancier-double.html).

- Correction du problème de double validation sur le bouton finalConfirmBtn dans les interfaces d'échéancier standard et double (désactivation du bouton pendant l'envoi AJAX et suppression des doublons d'événements jQuery).
- Correction de l'affichage du montant 'déjà payé' dans attentes-de-paiements (prise en compte des paiements des préinscrits via le modèle Paiements).
- Correction du montant total payé dans suivi-des-paiements pour intégrer à la fois Paiements et clientPaiementsRequestLine.
- Correction d'une erreur (TypeError) dans le calcul du montant restant lors du suivi des paiements.
- Correction du total payé dans le suivi des paiements pour les étudiants convertis en incluant les paiements dont le champ is_refund est NULL.
- Correction : suppression complète du filtre is_refund dans le calcul du total_paid pour le suivi des paiements, car les remboursements utilisent déjà des montants négatifs pour équilibrer, et certaines entrées de paiement classiques ont is_refund=True par erreur dans la base.
- Correction : résolution du bug d'affichage des montants dans details-suivie-echeancier (standard et double diplomation) en calculant les totaux (dû, payé, solde) indépendamment du fait que toutes les tranches soient payées ou qu'il n'y ait encore aucun paiement.
- Correction : inclusion des frais d'inscription dans la ventilation du montant (dispatch LIFO) lors du remboursement dans details_rembourssement.html.
- Correction : résolution du bug d'affichage de la liste déroulante (select2) pour la sélection de l'entité et de la catégorie dans la modale de remboursement en ajoutant le thème bootstrap-5.
- Correction : résolution du bug de sélection dans la liste déroulante select2 de l'entité (ajout de trigger('change') lors de l'affectation programmatique).
- Optimisation : blocage du bouton de confirmation de remboursement lors de la soumission pour éviter les doubles validations et affichage d'un indicateur de chargement.
- Fix: Exclusion des contacts d'Executive Education (context='con') de la liste des �tudiants de la scolarit� dans t_etudiants/views.py.
- UI: Affichage de la vue liste par d�faut pour la liste des �tudiants (Scolarit�) au lieu de la vue grille.
- UI: Ajout de l'affichage de l'avatar (ou des initiales) des �tudiants dans la vue liste.
- UI: Suppression de l'en-t�te et des animations de survol (hover) sur le tableau de bord RH.
- UI: Suppression de l'en-t�te et des animations de survol (hover) sur la liste des employ�s (RH).

## Modification �ch�anciers Configur�s
- Ajout de la possibilit� de modifier ou supprimer les formations (sp�cialit�s) concern�es lors de l'�dition d'un �ch�ancier configur� standard.

## Correctif �ch�anciers Configur�s
- Utilisation du code de la formation au lieu de l'ID pour le filtrage des sp�cialit�s lors du chargement des �ch�anciers.

## Am�lioration UI �ch�anciers Configur�s
- Correction de la lisibilit� des tags Select2 (couleurs du texte et de l'arri�re-plan) dans la s�lection des sp�cialit�s.

## Fonctionnalit� Attentes de Paiement
- Ajout d'un filtre par sp�cialit� (qui se charge dynamiquement lors de la s�lection d'une formation) sur la page des attentes de paiements.
- UI: Suppression des animations de survol (hover) sur le tableau de bord de configuration.
- UI: Suppression des animations de survol (hover) sur la page liste des utilisateurs.
\n### Ajout de la page Gestion des donn�es\n- Cr�ation de la page **Gestion des donn�es** sous le menu Configuration > Param�tres syst�me permettant d'afficher l'historique complet d'un prospect (CRM, Inscriptions, P�dagogie, Tr�sorerie).\n- Impl�mentation d'une barre de recherche asynchrone (Select2) pour r�cup�rer tous les prospects depuis \	_crm.Prospets\.\n- Ajout des routes API \pi/search-prospects/\ et \pi/prospect/<id>/history/\ pour servir les donn�es consolid�es.
\n- Remplacement de la barre de recherche par un tableau interactif listant tous les prospects dans la page Gestion des donn�es.
\n- Correction de l'URL de l'API dans gestion_donnees.html (suppression du pr�fixe /institut_app/ qui causait une erreur 404).
\n- Remplacement du tableau des �ch�anciers (Montants Dus) par un affichage sous forme de liste visuelle (.timeline-card) dans la vue historique.
\n- Correction de l'import manquant DuePaiements dans config.py causant l'absence de l'affichage des �ch�anciers.
\n- Ajout de l'affichage du champ Statut (visiteur, prinscrit, etc.) en plus de l'Etat dans la page Gestion des donn�es.
\n- Ajout d'un bouton de r�initialisation du prospect dans la page Gestion des donn�es pour supprimer les donn�es li�es (scolarit�, tr�sorerie) et r�initialiser son statut.
\n- Lors de la r�initialisation d'un prospect, les fiches de v�ux (Standard et Double) sont d�sormais conserv�es mais repassent � l'�tat 'en attente' (is_confirmed=False) au lieu d'�tre supprim�es.
\n- Correction de la r�initialisation: Suppression des objets EcheancierSpecial li�s au prospect.
\n- Ajout de la pagination et d'un filtre de recherche (via DataTables) sur la liste des �ch�anciers sp�ciaux (comptabilite/tresorerie/echeanciers-specials/).
\n- Ajout d'une fonctionnalit� de suppression de paiement dans configuration/gestion-donnees/ (r�initialise le montant d� associ� et rafra�chit l'historique de la tr�sorerie).
