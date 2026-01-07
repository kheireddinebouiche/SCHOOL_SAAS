Contexte : L'utilisateur veut une SYNTHÈSE DES NOTES des étudiants selon l'affichage des étudiants dans le PV de délibération.
- Un PV de délibération correspond à un PvExamen (lié à ExamPlanification, module, groupe via SessionExamLine).
- Pour un PvExamen donné, récupérer TOUS les étudiants (Prospets) qui ont des ExamNote dans ce PV (via ExamDecisionEtudiant ou ExamNote pour filtrer ceux présents).
- Pour CHAQUE TYPE DE NOTE (ExamTypeNote du PV), afficher :
  - Le libelle du type de note (self.libelle)
  - La liste des notes liées aux étudiants : pour chaque étudiant, son nom + la valeur de note (ExamNote.valeur), triée par étudiant. (ExamTypeNote dont le bloc is_pv_deliberation est True)
- Affichage structuré comme dans un PV : grouper par type de note, puis lister les étudiants avec leurs notes.
- Inclure la moyenne générale si possible (via ExamDecisionEtudiant.moyenne).
- Gérer les notes calculées (is_calculee), sous-notes (ExamSousNote), et décisions (ExamDecisionEtudiant).
- Gère les cas vides (pas d'étudiants, pas de notes).



Génère le code prêt à intégrer dans views.py et un template notes_synthese.html.