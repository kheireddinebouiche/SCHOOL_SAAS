import os
import subprocess
from datetime import datetime
from django.conf import settings
from .models import DatabaseBackup

def perform_backup(tenant=None):
    """
    Exécute une sauvegarde de la base de données.
    Si tenant est fourni, sauvegarde uniquement son schéma.
    """
    db_config = settings.DATABASES['default']
    db_name = db_config['NAME']
    db_user = db_config['USER']
    db_password = db_config['PASSWORD']
    db_host = db_config['HOST']
    db_port = db_config['PORT']
    
    # Créer le répertoire de sauvegarde s'il n'existe pas
    backup_dir = os.path.join(settings.MEDIA_ROOT, 'backups')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
    
    # Générer le nom du fichier
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if tenant:
        filename = f"backup_{tenant.schema_name}_{timestamp}.sql"
        backup_type = 'TENANT'
    else:
        filename = f"backup_global_{timestamp}.sql"
        backup_type = 'GLOBAL'
    
    filepath = os.path.join(backup_dir, filename)
    
    # Préparer la commande pg_dump
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password
    
    pg_dump_path = getattr(settings, 'PG_DUMP_PATH', 'pg_dump')
    
    cmd = [
        pg_dump_path,
        '-U', db_user,
        '-h', db_host,
        '-p', str(db_port),
        '-f', filepath,
        db_name
    ]
    
    if tenant:
        cmd.extend(['-n', tenant.schema_name])
    
    try:
        # Exécuter la commande
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
        
        # Vérifier si le fichier a été créé et n'est pas vide
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            
            # Créer l'entrée dans la base de données
            backup_obj = DatabaseBackup.objects.create(
                file=f"backups/{filename}",
                backup_type=backup_type,
                tenant=tenant,
                size=file_size,
                filename=filename
            )
            return True, backup_obj
        else:
            return False, "Le fichier de sauvegarde n'a pas été créé."
            
    except subprocess.CalledProcessError as e:
        error_msg = f"Erreur pg_dump : {e.stderr}"
        return False, error_msg
    except Exception as e:
        return False, str(e)

def perform_restore(backup_obj):
    """
    Restaure une sauvegarde de tenant.
    Implique de supprimer le schéma actuel et d'importer le fichier SQL.
    """
    if backup_obj.backup_type != 'TENANT':
        return False, "Seules les restaurations de tenants sont supportées via cette interface."
    
    tenant = backup_obj.tenant
    if not tenant:
        return False, "Tenant non associé à cette sauvegarde."

    db_config = settings.DATABASES['default']
    db_name = db_config['NAME']
    db_user = db_config['USER']
    db_password = db_config['PASSWORD']
    db_host = db_config['HOST']
    db_port = db_config['PORT']
    
    # Chemin du fichier de sauvegarde
    filepath = backup_obj.file.path
    if not os.path.exists(filepath):
        return False, f"Le fichier de sauvegarde est introuvable : {filepath}"

    schema_name = tenant.schema_name
    
    # Préparer l'environnement
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password
    psql_path = getattr(settings, 'PSQL_PATH', 'psql')

    try:
        # 1. Supprimer le schéma existant
        # On utilise CASCADE pour supprimer tous les objets dépendants (tables, index, etc.)
        drop_cmd = [
            psql_path,
            '-U', db_user,
            '-h', db_host,
            '-p', str(db_port),
            '-d', db_name,
            '-c', f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"
        ]
        subprocess.run(drop_cmd, env=env, check=True, capture_output=True)

        # 2. Recréer le schéma vide
        create_cmd = [
            psql_path,
            '-U', db_user,
            '-h', db_host,
            '-p', str(db_port),
            '-d', db_name,
            '-c', f"CREATE SCHEMA {schema_name};"
        ]
        subprocess.run(create_cmd, env=env, check=True, capture_output=True)

        # 3. Importer le fichier SQL
        # La sauvegarde effectuée avec pg_dump -n schema_name contient généralement 
        # les instructions SET search_path TO schema_name;
        restore_cmd = [
            psql_path,
            '-U', db_user,
            '-h', db_host,
            '-p', str(db_port),
            '-d', db_name,
            '-f', filepath
        ]
        result = subprocess.run(restore_cmd, env=env, check=True, capture_output=True, text=True)
        
        return True, "Restauration terminée avec succès."

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return False, f"Erreur psql : {error_msg}"
    except Exception as e:
        return False, str(e)

def delete_old_backups(days=30):
    """Optionnel: Supprimer les sauvegardes de plus de X jours."""
    from django.utils import timezone
    cutoff = timezone.now() - timezone.timedelta(days=days)
    old_backups = DatabaseBackup.objects.filter(created_at__lt=cutoff)
    count = old_backups.count()
    for backup in old_backups:
        backup.delete()
    return count
