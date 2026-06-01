---
trigger: always_on
---

<RULE[architecture_saas]>
### Architecture & Règles de Développement du Projet (SaaS Multi-tenant)

1. **Structure des Applications** :
   - **`school`** : Cœur du projet (settings, urls principales). Ne pas y ajouter de logique métier.
   - **`app`** : Logique globale ou publique.
   - **`saas_admin_app`** : Espace d'administration centralisé (Superadmin SaaS).
   - **`institut_app` / `associe_app`** : Espaces dédiés aux instituts et partenaires.
   - **Apps Locataires (Tenants)** : Toutes les applications préfixées par `t_` (ex: `t_etudiants`, `t_formations`, `t_rh`, `t_timetable`) contiennent la logique spécifique aux clients. Respecter impérativement cette séparation thématique.
2. **Conventions et Réutilisation** :
   - Ne jamais dupliquer de code. Avant de créer une fonction, chercher via `grep_search` si un utilitaire existe déjà.
   - Respecter le pattern Django MVC (Modèles, Vues, Templates).
3. **Isolation Multi-tenant** :
   - Toute nouvelle requête (QuerySet) ou vue doit filtrer et isoler les données selon le locataire (Tenant/Institut) actuel. Ne jamais croiser les données entre écoles.
4. **Base de Données et Migrations** : 
   - Base utilisée : PostgreSQL. Ne jamais altérer les schémas existants sans une vérification minutieuse des dépendances.
5. **Exécution des Commandes** :
   - Toujours s'assurer que l'environnement virtuel (ex: `venv/Scripts/activate`) est sourcé avant toute commande `python manage.py` ou `pip`.
</RULE[architecture_saas]>
