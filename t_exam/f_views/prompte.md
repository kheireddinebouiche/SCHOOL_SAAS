Tu es un expert Django + logique de notation académique.

Voici mon contexte métier :

J’ai un système de notation basé sur des modèles configurables (ModelBuiltins).
Chaque modèle contient plusieurs types de notes (BuiltinTypeNote), regroupées par blocs (NoteBloc).

Un type de note peut être :
- une note saisie manuellement
- une note composée de sous-notes
- une note calculée (SUM ou AVG) basée sur d’autres types de notes via des dépendances

Les relations importantes :
- BuiltinTypeNoteDependency définit quelles notes sont utilisées pour calculer une autre
- BuiltinSousNote définit les sous-notes avec leur max_note
- La somme des max des sous-notes ne peut pas dépasser le max_note du type parent

Lorsqu’un examen est planifié :
- Le modèle Builtin est copié dans un PV d’examen (PvExamen)
- Les BuiltinTypeNote deviennent des ExamTypeNote
- Les dépendances sont aussi copiées

Pour chaque étudiant :
- Une ExamNote existe par ExamTypeNote
- Une ExamNote peut avoir plusieurs ExamSousNote
- Les valeurs sont stockées dans ExamNote.valeur
- Les calculs sont effectués côté frontend (JavaScript) en utilisant :
  - type_calcul (NONE, SUM, AVG)
  - les dépendances
  - les sous-notes

Contraintes :
- Si pv.est_valide = true, aucune modification n’est autorisée
- Le backend ne calcule pas, il valide et persiste uniquement
- Le frontend doit savoir quelles notes recalculer automatiquement

Tâche demandée :
Explique clairement la logique de remplissage des notes d’un étudiant,
l’ordre de calcul des notes,
et comment le frontend peut détecter quelles notes sont dépendantes d’autres.