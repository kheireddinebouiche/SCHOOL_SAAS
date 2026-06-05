# ðŸ“� Journal des Mises Ã  Jour (Changelog)

Ce fichier recense toutes les modifications, corrections de bugs et nouvelles fonctionnalitÃ©s apportÃ©es au projet `SCHOOL_SAAS` par l'assistant Antigravity. Ce journal peut Ãªtre utilisÃ© pour alimenter la vue "NouveautÃ©s" des superutilisateurs.

---

## [05/06/2026] - v1.2.x - Permissions Menus Associe App

- **Associe App** :
  - **Satisfaction** : Ajout d'un nouveau menu "Satisfaction" affichant une page "Fonctionnalité en attente de validation".
  - **Gestion des Permissions** : Ajout de conditions de permissions (`is_superuser` et `is_staff`) sur le menu horizontal `public_folder/menu.html` pour restreindre l'accès. Paramétrage et Administration sont réservés aux super-administrateurs, tandis que Dashboard, Stats CRM et Gestion Budgétaire sont accessibles aux membres du staff.
  - **Gestion des Utilisateurs** : Ajout d'un mécanisme (checkbox) pour activer ou désactiver le statut super-utilisateur lors de l'ajout ou de l'édition d'un utilisateur dans le panel d'administration (`associe_app`).

- **SaaS Admin** :
  - **Gestion du Changelog** : Correction d'une erreur 403 (CSRF) lors de la suppression d'une mise à jour dans le panel SaaS Admin. Le jeton CSRF était mal formaté dans la requête AJAX (`templates/saas_admin_app/saas_changelog.html`).

---

## [04/06/2026] - v1.2.0 - Refonte de l'IRG (ConformitÃ© LÃ©gale AlgÃ©rienne)

- **Ressources Humaines (FiscalitÃ© & Paie)** :
  - **Prise en charge des Primes / Rubriques dans la Paie EmployÃ©s** :
    - IntÃ©gration du calcul des rubriques/primes dynamiques (gains et retenues) dans la gÃ©nÃ©ration de la paie en masse via `assistantPaie`. La mÃ©thode synchronise automatiquement le contrat `t_rh.models.Contrats` avec le contrat `t_ressource_humaine.models.Contrat` pour rÃ©cupÃ©rer et appliquer la bonne configuration des rubriques et leurs valeurs par dÃ©faut ou personnalisÃ©es.
    - Persistance correcte des lignes de paie (`LignePaie`) associÃ©es Ã  chaque bulletin lors de la validation en masse, en Ã©vitant les doublons (suppression prÃ©alable des anciennes lignes de paie pour la mÃªme fiche).
    - AmÃ©lioration de la vue de dÃ©tail du bulletin de paie de l'employÃ© (`fiche_paie_detail.html`) pour boucler sur `fiche.lignes_paie.all` (au lieu de la relation incorrecte `fiche.lignes.all`) et utiliser le libellÃ© correct (`ligne.rubrique.libelle` au lieu de `ligne.rubrique.nom`).
    - Affichage des lignes de primes exceptionnelles, de l'indemnitÃ© de panier, de l'indemnitÃ© de transport et des retenues pour absences directement sous forme de lignes du tableau pour les employÃ©s.
    - Ajout des conditions pour charger le nom et l'identifiant de l'employÃ© ou du formateur de maniÃ¨re dynamique dans `fiche_paie_print.html` et `_fiche_paie_detail.html` afin d'Ã©viter tout plantage `AttributeError` ou omission.
  - **Filtres & Gestion de l'Historique de Paie** : Modernisation de l'historique des fiches de paie (`liste_fiches_paie.html`). Ajout de filtres de recherche avancÃ©s par employÃ©, entitÃ© lÃ©gale, mois, annÃ©e et statut de validation (ValidÃ© ou Brouillon). Les filtres s'appliquent en temps rÃ©el (via l'Ã©vÃ©nement `onchange` sur tous les sÃ©lecteurs) et mettent Ã  jour l'historique du navigateur (`window.history.pushState`) pour des filtres persistants sans rechargement de page.
  - **Correction du chargement des rubriques** : RÃ©solution d'une erreur 404 dans `details_employe.html` lors de l'ouverture du modal de gestion des rubriques/primes pour un employÃ©. Remplacement du chemin d'accÃ¨s AJAX codÃ© en dur par la balise Django dynamique `{% url %}` ciblant l'URL correcte sous le namespace `t_ressource_humaine`.
  - **Validation & Suppression Individuelle/En Masse** : IntÃ©gration de checkboxes de sÃ©lection et d'une barre d'actions groupÃ©es permettant de valider ou d'annuler la validation de plusieurs bulletins de paie simultanÃ©ment. Ajout d'un bouton de suppression sÃ©curisÃ© par SweetAlert2, accessible uniquement pour les bulletins de paie Ã  l'Ã©tat de brouillon (non validÃ©s).
  - **PrÃ©-visualisation et Confirmation de Paie (Masse Salariale)** : Ajout d'une Ã©tape de prÃ©-visualisation/confirmation avant le scellement dÃ©finitif de la paie. Les pages d'assistant de paie (salariÃ©s et formateurs) calculent dÃ©sormais les totaux gÃ©nÃ©raux (nombre de personnes, masse salariale brute globale, total cotisations SS, total retenues IRG et total Net Ã  payer) et les prÃ©sentent dans une fenÃªtre de confirmation SweetAlert2 ergonomique et claire.
  - **Correction de l'assistant de paie** : RÃ©solution d'un plantage `AttributeError` lors de la validation globale de la paie dans `t_rh/views.py::assistantPaie` oÃ¹ le champ inexistant `date_debut` du modÃ¨le `Contrats` a Ã©tÃ© remplacÃ© par le champ correct `date_embauche`.
  - **Moteur de calcul IRG** : Refonte totale de `calculer_irg` dans `t_ressource_humaine/logic.py` pour implÃ©menter la mÃ©thode officielle algÃ©rienne (LF 2022 / LF 2026) :
    - Arrondi systÃ©matique du salaire imposable Ã  la dizaine de DA infÃ©rieure avant le calcul du barÃ¨me.
    - Application du premier abattement proportionnel de 40% sur l'IRG brut (limitÃ© au minimum de 1 000 DA et maximum de 1 500 DA par mois).
    - Formule de lissage pour le **Cas GÃ©nÃ©ral** (de 30 000 DA Ã  35 000 DA) : $\text{IRG} = \text{IRG1} \times \frac{137}{51} - \frac{27925}{8}$.
    - Formule de lissage pour le **Cas Particulier** (RetraitÃ©s & HandicapÃ©s, de 30 000 DA Ã  42 500 DA) : $\text{IRG} = \text{IRG1} \times \frac{93}{61} - \frac{81213}{41}$.
    - Arrondi fiscal systÃ©matique au dÃ©cime (dizaine de centimes).
  - **Correction du calcul CDI/CDD** : RÃ©solution du bug appliquant incorrectement le taux flat de 10% des vacataires Ã  tous les enseignants (mÃªme sous CDD/CDI) ; dÃ©sormais, seuls les contrats de type `VACATION` sont soumis Ã  ce taux flat.
  - **Base de donnÃ©es / ModÃ¨les** : Ajout du champ `is_particular_irg` dans les modÃ¨les `Employees` et `Formateurs`. IntÃ©gration automatique dans les formulaires et les modals de crÃ©ation et modification (modals d'ajout/Ã©dition dans `liste_des_formateur.html` et formulaire `NouveauEmploye`).
  - **Prise en charge Formateurs** : Adaptation de `PaieEngine.calculer_paie` pour rÃ©soudre et transmettre le drapeau `is_particular_irg` Ã  partir du contrat de l'enseignant (CDI/CDD) et du formateur reliÃ©, appliquant ainsi correctement le barÃ¨me de lissage particulier (retraitÃ©s/handicapÃ©s) dans le calcul et la gÃ©nÃ©ration finale des fiches de paie.
  - **Migrations de Base de DonnÃ©es** : GÃ©nÃ©ration et application de la migration `0013_formateurs_is_particular_irg.py` pour ajouter le champ dans le schÃ©ma et migration sur tous les schÃ©mas locataires (multi-tenant isolation).
  - **Interface & Simulation ModernisÃ©e (Design Premium)** : 
    - IntÃ©gration de la description dÃ©taillÃ©e du barÃ¨me, des abattements et des formules de lissage (cas gÃ©nÃ©ral et cas particulier) dans l'interface de configuration fiscale `templates/tenant_folder/rh/paie/config_fiscalite.html`.
    - Ajout d'un **Simulateur IRG InstantanÃ©** interactif en Javascript, permettant de calculer en temps rÃ©el l'IRG pour n'importe quel montant imposable saisi, pour le cas gÃ©nÃ©ral et le cas particulier.
    - Refonte visuelle complÃ¨te sous forme de cartes en verre dÃ©poli (Glassmorphism) avec des dÃ©gradÃ©s fins, des ombres fluides et une disposition responsive.
    - AmÃ©lioration de l'ergonomie des formulaires avec des focus adoucis (`soft-glow`), des tooltips informatifs et des styles de boutons raffinÃ©s.
    - Ajout d'une micro-animation de pulsation (`pulse-update` par transform scale) sur les cartes de rÃ©sultats du simulateur (Vert/Ã‰meraude pour le Cas GÃ©nÃ©ral, Bleu/Info pour le Cas Particulier) dÃ©clenchÃ©e Ã  chaque frappe de clavier.
  - **Validation des tests** : Ajout de nouveaux tests unitaires pour valider les calculs exacts d'IRG pour les cas gÃ©nÃ©raux et particuliers (ex: 30 900 DA & 30 930 DA imposable) et ajustement des assertions de test Ã  l'abattement de 40% (ex: 45 500 DA imposable).

---

## [04/06/2026] - v1.1.0 - Refonte de StabilitÃ© (Executive Education & RH)

- **Global / Core** :
  - Correction d'une erreur fatale au dÃ©marrage du serveur (NameError) dans `school/settings.py` causÃ©e par `DEBUG = F`.
- **Ressources Humaines (Paie, PrÃ©sences & Formateurs)** :
  - **Assistant de Paie Formateurs** : CrÃ©ation d'une page dÃ©diÃ©e "Assistant de Paie - Formateurs" permettant de gÃ©nÃ©rer en masse les fiches de paie basÃ©es sur les fiches mensuelles validÃ©es.
  - **Historique DÃ©diÃ© & Redesign** : SÃ©paration de l'historique des fiches de paie pour les formateurs avec un tout nouveau design premium (Glassmorphism, animations au survol, dÃ©gradÃ©s de couleurs).
  - **Taux IRG Vacataires** : Ajout d'une configuration globale (dans les ParamÃ¨tres RH) pour appliquer le taux IRG forfaitaire (sans abattement) spÃ©cifique aux formateurs vacataires (par dÃ©faut 10%). Ce paramÃ¨tre est pris en charge par le moteur de paie de faÃ§on automatique.
  - **Correction du systÃ¨me de paie formateur** : Correction de l'erreur d'attribut `types_contrat` vers `eligible_types` dans `generer_paie`.
  - **Liaison Paie-Formateur** : Ajout d'un bouton "GÃ©nÃ©rer Paie" dynamique sur les fiches mensuelles des formateurs.
  - **Validation des Fiches Mensuelles** : CrÃ©ation du modÃ¨le `ValidationFicheMensuelleFormateur` avec bouton AJAX SweetAlert2 pour verrouiller et approuver une fiche mensuelle de formateur (affichage d'un badge "ValidÃ©e").
  - Restructuration du menu principal "Ressources Humaines" pour sÃ©parer clairement "Espace EmployÃ©s" et "Espace Formateurs" (et les garder ouverts au bon endroit).
  - Modification du formulaire d'ajout d'employÃ© pour rendre tous les champs non obligatoires.
  - RÃ©solution d'un bug empÃªchant l'affichage des nouveaux employÃ©s dans les vues de prÃ©sences et dans l'assistant de paie en autorisant les Ã©tats (etat) non dÃ©finis ou vides.
  - RÃ©solution d'un bug bloquant l'ajout d'un nouvel employÃ© dÃ» Ã  la validation silencieuse de champs manquants dans le formulaire (exclusion de `solde_conge`, `solde_conge_annee_prec`, `is_teacher`, etc.).
  - RÃ©solution d'un bug similaire empÃªchant la crÃ©ation d'un nouveau contrat pour un formateur (exclusion des champs non rendus comme `prime_transport`, `prime_panier`, `employee` du `ContratForm`).
  - RÃ©solution de l'erreur `KeyError` dans le calcul des paies.
- **CRM / Prospects** :
  - Ajout de la fonctionnalitÃ© d'importation en masse de prospects particuliers via fichier Excel (`.xlsx`).
  - Ajout d'une fonctionnalitÃ© pour tÃ©lÃ©charger le modÃ¨le d'import. Les prospects importÃ©s ont le statut "pas de vÅ“ux formulÃ©s pour le moment".
- **SaaS Admin** :
  - Correction d'une erreur de syntaxe (`SyntaxError`) dans `urls.py` causÃ©e par des caractÃ¨res `\n` mal formatÃ©s empÃªchant l'accÃ¨s au portail.
  - Correction d'une erreur `NameError` due au dÃ©corateur `@saas_superuser_required` non dÃ©fini dans `views.py` (remplacÃ© par `@user_passes_test(superadmin_only)`).
  - Correction de la localisation des noms de mois en anglais dans les fiches mensuelles de prÃ©sence.
  - CrÃ©ation des pages "Empty States" Premium pour les tableaux vides (CongÃ©s, PrÃ©sences, Fiches Mensuelles, EmployÃ©s).
- **Executive Education (`t_conseil`)** :
  - SÃ©curisation complÃ¨te des API contre les plantages silencieux (`Erreur 500`) : Ajout de la gestion `DoesNotExist` pour plus de 30 requÃªtes `.get()`.
  - Fixation d'une faille `KeyError` lors de l'accÃ¨s aux donnÃ©es JSON non fournies dans l'API de gestion des groupes.

### âœ¨ AmÃ©liorations (Optimisations)
- **Base de donnÃ©es (`@transaction.atomic`)** :
  - Application du verrouillage transactionnel sur toutes les fonctions critiques de crÃ©ation (`Devis`, `Factures`, `Clients`, `Groupes`) de l'Executive Education, garantissant qu'aucune donnÃ©e fantÃ´me ne soit gÃ©nÃ©rÃ©e en cas d'erreur de rÃ©seau.
- **Ressources Humaines** :
  - Refonte de la suppression d'employÃ©s avec un effacement en cascade strict des contrats, piÃ¨ces jointes et absences (`models.CASCADE`).
  - Restructuration visuelle de la configuration HUB en onglets modernes.

---
*(Ajoutez les prochaines entrÃ©es ci-dessus)*
-   A j o u t   d e   l a   m o d i f i c a t i o n   e t   s u p p r e s s i o n   d e s   c o n t r a t s   ( i n t e r f a c e   L i s t e   d e s   c o n t r a t s )   d a n s   r h .  
 -   R e f o n t e   d e   l a   m o d i f i c a t i o n   d e s   c o n t r a t s   :   c r é a t i o n   d ' u n e   p a g e   c o m p l è t e   d é d i é e   ( u p d a t e _ c o n t r a t . h t m l )   b a s é e   s u r   l ' a s s i s t a n t   d e   c r é a t i o n   a v e c   p r é - r e m p l i s s a g e   d e s   r u b r i q u e s .  
 -   C o r r e c t i o n   d u   p r é - r e m p l i s s a g e   d e s   d o n n é e s   s u r   l a   p a g e   d e   m o d i f i c a t i o n   d u   c o n t r a t   ( p r o b l è m e   d e   s é r i a l i s a t i o n   J S O N   d e s   d o n n é e s   P y t h o n ) .  
 -   M e n u   l a t é r a l   :   a j o u t   d e   l a   r o u t e   ' u p d a t e C o n t r a t P a g e '   p o u r   m a i n t e n i r   l e   m e n u   ' G e s t i o n   d e s   C o n t r a t s '   a c t i f   l o r s   d e   l a   m o d i f i c a t i o n   d ' u n   c o n t r a t .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n   m é c a n i s m e   d e   p r é v i s u a l i s a t i o n   ( m o d a l )   p o u r   c h a q u e   l i g n e   d e   f i c h e   d e   p a i e .  
 -   C o r r e c t i o n   d e   l ' a f f i c h a g e   d e   l a   f e n ê t r e   m o d a l e   d e   p r é v i s u a l i s a t i o n   d a n s   l ' a s s i s t a n t   d e   p a i e   ( d é p l a c e m e n t   e n   d e h o r s   d u   c o n t e n e u r   d u   t a b l e a u   p o u r   é v i t e r   l e s   c o n f l i t s   C S S ) .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   a n i m a t i o n   d ' a l e r t e   s u r   l e   b o u t o n   d e   r e c h e r c h e   l o r s q u e   l e   m o i s   o u   l ' a n n é e   e s t   m o d i f i é   a f i n   d ' i n c i t e r   l ' u t i l i s a t e u r   à   a c t u a l i s e r   l e s   d o n n é e s .  
 -   A s s i s t a n t   d e   p a i e   :   a j o u t   d ' u n e   s e c t i o n   d e   s y n t h è s e   g l o b a l e   a f f i c h a n t   l e   t o t a l   d e s   p a i e m e n t s   n e t s ,   l e   t o t a l   d e s   p r i m e s   e t   l e   t o t a l   d e   l a   f i s c a l i t é   ( S S   +   I R G ) .  
 -   M o t e u r   d e   p a i e   :   a j o u t   d ' u n   n o u v e a u   m o d e   d e   c a l c u l   p o u r   l e s   r u b r i q u e s   e t   p r i m e s   ( ' J O U R S '   :   P a r   j o u r   t r a v a i l l é )   p e r m e t t a n t   d e   m u l t i p l i e r   l e   m o n t a n t   s a i s i   p a r   l e   n o m b r e   d e   j o u r s   d e   p r é s e n c e   d e   l ' e m p l o y é .  
 -   C o r r e c t i o n   d u   m e n u   l a t é r a l   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   o ù   l e   s o u s - m e n u   d e s   f i c h e s   d e   p a i e   f o r m a t e u r s   s ' a f f i c h a i t   c o m m e   a c t i f   ( e n   s u r b r i l l a n c e )   l o r s q u ' o n   s e   t r o u v a i t   s u r   l ' a s s i s t a n t   d e   p a i e   d e s   e m p l o y é s   ( p r o b l è m e   d e   m a t c h i n g   d e   c h a î n e   d e   c a r a c t è r e s ) .  
 -   I n t e r f a c e   :   c o r r e c t i o n   d ' u n   b u g   d ' a f f i c h a g e   ( s c r o l l   h o r i z o n t a l   i n d é s i r a b l e )   s u r   l a   p a g e   d ' h i s t o r i q u e   d e s   f i c h e s   d e   p a i e   d e s   f o r m a t e u r s ,   c a u s é   p a r   u n   é l é m e n t   d é c o r a t i f   q u i   d é p a s s a i t   d e   l ' é c r a n .  
 -   A s s i s t a n t   d e   p a i e   :   e x c l u s i o n   a u t o m a t i q u e   d e s   e m p l o y é s   d o n t   l a   f i c h e   d e   p a i e   a   d é j à   é t é   g é n é r é e   p o u r   l e   m o i s   e n   c o u r s   a f i n   d ' é v i t e r   l e s   d o u b l o n s   ( i l s   r é a p p a r a î t r o n t   s i   l e u r   f i c h e   e s t   a n n u l é e ) .  
 -   A s s i s t a n t   d e   p a i e   :   a f f i c h a g e   d ' u n e   v u e   d e   s y n t h è s e   ' P a i e   c l ô t u r é e   p o u r   c e   m o i s '   l o r s q u e   t o u t e s   l e s   f i c h e s   d e   p a i e   o n t   d é j à   é t é   g é n é r é e s   p o u r   l e   m o i s   s é l e c t i o n n é ,   r e m p l a ç a n t   l e   m e s s a g e   d ' e r r e u r   ' A u c u n e   d o n n é e   d i s p o n i b l e ' .  
 -   C o r r e c t i o n   d e   l ' i n t e r f a c e   :   l ' i c ô n e   d u   m e n u   ' A s s i s t a n t   d e   P a i e '   n e   s ' a f f i c h a i t   p a s   e n   r a i s o n   d ' u n e   c l a s s e   d ' i c ô n e   i n e x i s t a n t e   d a n s   l a   b i b l i o t h è q u e   u t i l i s é e .   R e m p l a c é e   p a r   u n e   i c ô n e   f o n c t i o n n e l l e   é q u i v a l e n t e .  
 
- IntÃ©gration Paie-Finance : crÃ©ation d'un nouvel espace dans ComptabilitÃ©/Finance pour lister les Ã©tats de paie et lancer les dÃ©penses associÃ©es de maniÃ¨re globale.

- Gestion des permissions : ajout de la vÃ©rification de permission spÃ©cifique (sous-menu paie_salaires) sur les vues de la paie dans ComptabilitÃ©/Finance, assurant le mÃªme niveau de sÃ©curitÃ© que les autres vues.

- Ajout d'un bouton de validation globale du mois dans /rh/paie/fiches/ avec envoi de notification au personnel configuré dans les paramètres généraux.

- Réorganisation de l'ordre des groupes dans l'onglet Gestion des modules (Paramètres généraux) pour suivre un workflow plus logique : CRM -> Inscriptions -> Trésorerie -> Scolarité -> Communication.

- Correction de la fenêtre modale de paiement dans /comptabilite/tresorerie/paies/liste/ qui ne s'ouvrait pas ou était bloquée (déplacement du code HTML de la modale en dehors de la balise 	able-responsive pour corriger les problèmes de z-index et d'overflow de Bootstrap).

- Ajout d'un champ 'Date de paiement effective' dans la modale de paiement de la paie (/comptabilite/tresorerie/paies/liste/) afin de permettre à l'utilisateur de spécifier la date réelle du règlement (met à jour la dépense et les fiches de paie).

- Création automatique d'une entrée OperationsBancaire lors du lancement de la dépense de paie (mode 'vir') pour que la dépense remonte dans le module d'Imputation Bancaire.
