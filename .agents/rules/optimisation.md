---
trigger: always_on
---

3. Règles du Projet - Optimisées pour Antigravity (IDE)

Ces règles sont conçues pour être ajoutées aux instructions globales de l'utilisateur pour Antigravity afin de maximiser l'efficacité de l'agent, réduire la consommation de tokens et exploiter ses outils natifs de manière optimale.

<RULE[optimisation_antigravity]>
1. **Concision Maximale** : Sois extrêmement direct dans le chat. Fournis uniquement un résumé très bref des actions effectuées à la fin de ton tour. Pas d'explications superflues ni de salutations.
2. **Édition Précise (Économie de Tokens)** : Pour modifier un fichier existant, utilise EXCLUSIVEMENT les outils `replace_file_content` ou `multi_replace_file_content`. Cible précisément les lignes à changer. N'utilise jamais `write_to_file` pour mettre à jour un fichier, sauf s'il est entièrement nouveau.
3. **Exploration Ciblée** : Utilise `list_dir` et `grep_search` pour t'orienter dans le projet avant de lire le contenu des fichiers. Limite l'utilisation de `view_file` aux fichiers strictement indispensables pour résoudre la tâche en cours.
4. **Mode Planification Actif** : Pour toute tâche complexe (nouvelle architecture, refactoring majeur), entre en mode Planification. Crée l'artefact `implementation_plan.md` (avec request_feedback=true) et attends mon approbation explicite (STOP) avant de modifier la moindre ligne de code.
5. **Réutilisation et KI (Knowledge Items)** : Vérifie systématiquement les Knowledge Items et le code existant via `grep_search` avant de créer de nouvelles fonctions ou composants. Réutilise au maximum les patterns du projet.
6. **Vérification Autonome** : Utilise l'outil `run_command` pour vérifier de manière autonome si ton code fonctionne (ex: tests, vérification de syntaxe) avant de me dire que la tâche est terminée.
7. **Pas de Code Boilerplate** : Ne génère pas de code "boilerplate" par défaut. Si une configuration ou un boilerplate est nécessaire, demande d'abord confirmation.
</RULE[optimisation_antigravity]>