import os
from django.utils import timezone
from django.db import connection


def tenant_directory_path(instance, filename):
    """
    Retourne un chemin du type :
    <schema_name>/documents_demande_inscription/dossiers/<année>/<mois>/<filename>
    """
    tenant = getattr(connection, "tenant", None)
    schema_name = tenant.schema_name if tenant else "public"

    return os.path.join(
        schema_name,
        "documents_demande_inscription",
        "dossiers",
        timezone.now().strftime("%Y/%m"),
        filename
    )

def tenant_directory_path_for_image(instance, filename):
    """
    Retourne un chemin du type :
    <schema_name>/documents_demande_inscription/images/<année>/<mois>/<filename>
    """
    tenant = getattr(connection, "tenant", None)
    schema_name = tenant.schema_name if tenant else "public"

    return os.path.join(
        schema_name,
        "documents_demande_inscription",
        "images",
        timezone.now().strftime("%Y/%m"),
        filename
    )

def tenant_directory_path_for_logos(instance, filename):
    """
    Retourne un chemin du type :
    <schema_name>/documents_demande_inscription/images/<année>/<mois>/<filename>
    """
    tenant = getattr(connection, "tenant", None)
    schema_name = tenant.schema_name if tenant else "public"

    return os.path.join(
        schema_name,
        "images",
        "logo",
        timezone.now().strftime("%Y/%m"),
        filename
    )

