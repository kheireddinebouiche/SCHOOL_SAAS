# Project: KPIs Menu — SaaS de gestion pour un groupe d'instituts

**But du fichier** : fournir une structure de menus claire et navigable (Markdown) listant les KPIs à implémenter dans la web app SaaS. Ce fichier est conçu pour être utilisé comme *contexte / prompt file* dans un CLI d'IA (par ex. qwen CLI).

---

## Menu Principal
- [Vue Groupe (Dashboard consolidé)](#vue-groupe)
- [KPI Académiques & Pédagogiques](#kpi-academiques--pedagogiques)
- [KPI Financiers](#kpi-financiers)
- [Inscriptions & Recrutement](#inscriptions--recrutement)
- [Ressources Humaines](#ressources-humaines)
- [Marketing & Notoriété](#marketing--notoriete)
- [Qualité & Conformité](#qualite--conformite)
- [Widgets & Visualisations suggérés](#widgets--visualisations-suggeres)
- [Implémentation — Backend / Frontend](#implementation)
- [Usage avec Qwen CLI](#usage-qwen-cli)

---

## <a name="vue-groupe"></a> Menu: Vue Groupe (Dashboard consolidé)
- Synthèse KPI (taux de réussite, MRR, croissance, abandon)
- Classement des instituts (CA, réussite)
- Alertes & exceptions (instituts sous seuil, impayés)

---

## <a name="kpi-academiques--pedagogiques"></a> Menu: KPI Académiques & Pédagogiques
- Taux de réussite
- Taux de diplomation
- Assiduité / Présence
- Taux d’abandon
- Progression académique
- Satisfaction des étudiants

---

## <a name="kpi-financiers"></a> Menu: KPI Financiers
- Chiffre d’affaires par institut
- MRR et ARR
- Taux d’impayés
- Marge nette par institut
- ARPU (revenu moyen par étudiant)

---

## <a name="inscriptions--recrutement"></a> Menu: Inscriptions & Recrutement
- Taux de conversion (lead → inscrit)
- Préinscriptions vs inscriptions confirmées
- CAC (coût d’acquisition étudiant)
- Taux d’occupation des classes

---

## <a name="ressources-humaines"></a> Menu: Ressources Humaines
- Ratio étudiants / formateur
- Taux de rétention des formateurs
- Charge horaire moyenne
- Satisfaction des formateurs

---

## <a name="marketing--notoriete"></a> Menu: Marketing & Notoriété
- Nombre de leads
- Visiteurs uniques site / plateforme
- Engagement réseaux sociaux
- Taux de conversion par campagne

---

## <a name="qualite--conformite"></a> Menu: Qualité & Conformité
- Taux de conformité dossiers étudiants
- Respect des normes d’accréditation
- Nombre de réclamations / litiges

---

## <a name="widgets--visualisations-suggeres"></a> Menu: Widgets & Visualisations suggérés
- Jauge : MRR, taux de réussite, abandon
- Courbe : CA, MRR, évolution inscrits
- Tableau comparatif : instituts vs KPI
- Heatmap : présences / rétention
- Diagramme barres : conversion par canal
- Carte : localisation et performance

---

## <a name="implementation"></a> Menu: Implémentation — Backend / Frontend
- Backend : Endpoints, jobs périodiques, tables agrégées
- Frontend : Dashboard multi-roles, composants réutilisables, export
- Sécurité & Multi-tenancy : isolation données, rôles et permissions

---

## <a name="usage-qwen-cli"></a> Menu: Usage avec Qwen CLI
- Exemple 1 : `qwen chat --context-file project.md --query "Affiche le menu principal"`
- Exemple 2 : `qwen chat --context-file project.md --query "Montre-moi les KPI Financiers"`
- Exemple 3 : `qwen chat --context-file project.md --query "Génère un layout de dashboard Vue Groupe"`

---

### Notes finales
Chaque menu correspond à une section fonctionnelle de la web app SaaS. Les sous-points sont les éléments à suivre, afficher ou implémenter sous forme de widgets ou rapports.

