import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django.db import connection
from app.models import Institut
from pdf_editor.models import DocumentTemplate
from django.utils.text import slugify

title = "Contrat de Travail (Standard)"
content = """
<div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
    <h1 style="text-align: center; text-decoration: underline;">CONTRAT DE TRAVAIL</h1>
    
    <p><strong>Entre les soussignés :</strong></p>
    
    <p><strong>L'Entreprise :</strong> {{ entreprise }}</p>
    
    <p><strong>D'une part,</strong></p>
    
    <p>Et :</p>
    
    <p><strong>L'Employé(e) :</strong> {{ employe.civilite|title }} {{ employe.nom }} {{ employe.prenom }}</p>
    <p><strong>Demeurant à :</strong> {{ employe.adresse }}</p>
    <p><strong>Né(e) le :</strong> {{ employe.date_naissance|date:"d/m/Y" }}</p>
    
    <p><strong>D'autre part,</strong></p>
    
    <p>Il a été convenu et arrêté ce qui suit :</p>
    
    <h3>Article 1 : Engagement</h3>
    <p>L'employé est engagé en qualité de <strong>{{ contrat.poste.label }}</strong> pour une durée <strong>{% if contrat.duree %}{{ contrat.duree }} mois{% else %}indéterminée{% endif %}</strong>.</p>
    <p>L'employé exercera ses fonctions au sein du service : <strong>{{ contrat.service.label }}</strong>.</p>
    
    <h3>Article 2 : Date d'embauche</h3>
    <p>Le présent contrat prend effet à compter du <strong>{{ contrat.date_embauche|date:"d/m/Y" }}</strong>.</p>
    
    <h3>Article 3 : Rémunération</h3>
    <p>En contrepartie de ses services, l'employé percevra une rémunération de base de <strong>{{ contrat.salaire_base }} DA</strong>.</p>
    
    <br><br><br>
    
    <div style="display: flex; justify-content: space-between; margin-top: 50px;">
        <div style="text-align: center;">
            <p><strong>Fait à _______________, le {{ date_impression }}</strong></p>
            <p><strong>L'Employeur</strong></p>
            <p><em>(Signature et cachet)</em></p>
        </div>
        <div style="text-align: center;">
            <p><strong>L'Employé(e)</strong></p>
            <p><em>(Signature précédée de la mention "Lu et approuvé")</em></p>
        </div>
    </div>
</div>
"""

description = "Variables disponibles: {{ employe }} (nom, prenom, adresse, date_naissance, civilite), {{ contrat }} (poste, service, date_embauche, duree, salaire_base), {{ entreprise }}, {{ date_impression }}"

for tenant in Institut.objects.exclude(schema_name='public'):
    connection.set_tenant(tenant)
    if not DocumentTemplate.objects.filter(title=title).exists():
        DocumentTemplate.objects.create(
            title=title,
            slug=slugify(title),
            template_type="contract",
            content=content,
            description=description,
            is_active=True
        )
        print(f"[{tenant.schema_name}] Modèle de contrat ajouté avec succès.")
    else:
        print(f"[{tenant.schema_name}] Le modèle de contrat existe déjà.")
