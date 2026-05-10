from django.db.models import Q
from django.db import IntegrityError, transaction
from django_tenants.utils import schema_context, tenant_context
from .models import Formation, Specialites, Modules, DossierInscription, Partenaires
from django.db.models.signals import post_save, post_delete

@transaction.atomic
def update_or_create_formation_in_tenant(formation_master, target_tenant, master_tenant):
    """
    Crée ou met à jour une formation dans un tenant cible à partir d'une formation du master.
    """
    # Importation locale pour éviter les imports circulaires si nécessaire
    from .signals import log_prospect_save, log_prospect_delete
    
    # 1. Extraire les données du master dans le contexte master
    with schema_context(master_tenant.schema_name):
        nom = formation_master.nom
        defaults = {
            'code': formation_master.code,
            'type_formation': formation_master.type_formation,
            'prix_formation': formation_master.prix_formation,
            'frais_inscription': formation_master.frais_inscription,
            'duree': formation_master.duree,
            'description': formation_master.description,
            'qualification': formation_master.qualification,
            'is_visible': True, # Re-ajouté si vous voulez qu'elle soit visible par défaut, sinon retirez
        }
        # Re-vérification du modèle Formation pour is_visible (vu précédemment qu'il n'existe pas)
        if 'is_visible' in defaults:
             # On vérifie si le champ existe vraiment pour éviter FieldError
             if not hasattr(Formation, 'is_visible'):
                 del defaults['is_visible']

        partenaire_code = formation_master.partenaire.code if formation_master.partenaire else None

    # 2. Appliquer dans le tenant cible en désactivant les signaux de log
    # pour éviter les erreurs de clé étrangère User (ID inexistant dans le tenant)
    post_save.disconnect(log_prospect_save, sender=Formation)
    try:
        with schema_context(target_tenant.schema_name):
            target_partenaire = None
            if partenaire_code:
                target_partenaire = Partenaires.objects.filter(code=partenaire_code).first()
            
            defaults['partenaire'] = target_partenaire

            formation_tenant, created = Formation.objects.update_or_create(
                nom=nom,
                defaults=defaults
            )
            return formation_tenant
    finally:
        # Toujours reconnecter le signal
        post_save.connect(log_prospect_save, sender=Formation)

def update_or_create_specialite_in_tenant(specialite, sync_formation, institut_schema):
    try:
        with schema_context(institut_schema):
            # Determine visibility
            existing_spec = Specialites.objects.filter(code=specialite.code).first()
            if existing_spec:
                if specialite.is_visible:
                    new_visibility = existing_spec.is_visible
                else:
                    new_visibility = False
            else:
                new_visibility = specialite.is_visible

            sync_specialite, created = Specialites.objects.update_or_create(
                code=specialite.code,
                defaults={
                    'formation': sync_formation,
                    'label': specialite.label,
                    'duree': specialite.duree,
                    'version': specialite.version,
                    'condition_access': specialite.condition_access,
                    'nb_semestre': specialite.nb_semestre,
                    'branche': specialite.branche,
                    'abr': specialite.abr,
                    'nb_tranche': specialite.nb_tranche,
                    'is_visible': new_visibility,
                    'etat': 'last',
                }
            )
            
            if created:
                sync_specialite.prix = specialite.prix
                sync_specialite.prix_double_diplomation = specialite.prix_double_diplomation
                sync_specialite.save()

            return sync_specialite
    except Exception as e:
        raise ValueError(f"Erreur lors de la mise à jour de la spécialité {specialite.label}: {str(e)}")

def update_or_create_module_in_tenant(module, sync_specialite, institut_schema):
    try:
        with schema_context(institut_schema):
            label_clean = module.label.strip()
            
            if module.code_interne:
                q_lookup = Q(code_interne=module.code_interne)
            else:
                q_lookup = Q(label__iexact=label_clean)

            sync_module = Modules.objects.filter(q_lookup, specialite=sync_specialite).first()
            
            if sync_module:
                sync_module.label = label_clean
                sync_module.coef = module.coef
                sync_module.duree = module.duree
                sync_module.n_elimate = module.n_elimate
                sync_module.systeme_eval = module.systeme_eval
                sync_module.code_interne = module.code_interne
                sync_module.save()
            else:
                try:
                    sync_module = Modules.objects.create(
                        specialite=sync_specialite,
                        label=label_clean,
                        coef=module.coef,
                        duree=module.duree,
                        n_elimate=module.n_elimate,
                        systeme_eval=module.systeme_eval,
                        code_interne=module.code_interne
                    )
                except Exception as e:
                    raise ValueError(f"Erreur lors de la synchronisation du module {label_clean}: {str(e)}")
            
            return sync_module
    except Exception as e:
        raise ValueError(str(e))

def update_or_create_dossier_in_tenant(dossier, sync_formation, institut_schema):
    try:
        with schema_context(institut_schema):
            sync_dossier, created = DossierInscription.objects.update_or_create(
                formation=sync_formation,
                label=dossier.label,
                defaults={
                    'is_required': dossier.is_required,
                    'include_in_tracking': dossier.include_in_tracking,
                }
            )
            return sync_dossier
    except IntegrityError:
        raise ValueError("Une erreur d'intégrité s'est produite lors de la mise à jour du dossier d'inscription.")

def sync_formation_to_tenant(formation_master, target_tenant, master_tenant):
    """
    Synchronise une formation complète (dossiers, spécialités, modules) vers un tenant.
    """
    # 1. Formation de base
    sync_formation = update_or_create_formation_in_tenant(formation_master, target_tenant, master_tenant)

    # 2. Récupérer les données liées dans le MASTER
    with schema_context(master_tenant.schema_name):
        dossiers_master = list(DossierInscription.objects.filter(formation=formation_master))
        specialites_master = list(Specialites.objects.filter(formation=formation_master))
        
        # On pré-charge les modules pour chaque spécialité du master
        specs_data = []
        for spec in specialites_master:
            modules = list(Modules.objects.filter(specialite=spec))
            specs_data.append({'spec': spec, 'modules': modules})

    # 3. Synchroniser les Dossiers dans le TARGET
    for dossier in dossiers_master:
        update_or_create_dossier_in_tenant(dossier, sync_formation, target_tenant.schema_name)

    # 4. Synchroniser les Spécialités et leurs Modules dans le TARGET
    for item in specs_data:
        spec_master = item['spec']
        modules_master = item['modules']
        
        sync_specialite = update_or_create_specialite_in_tenant(spec_master, sync_formation, target_tenant.schema_name)
        
        for module in modules_master:
            update_or_create_module_in_tenant(module, sync_specialite, target_tenant.schema_name)
    
    return sync_formation
