import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from pdf_editor.models import DocumentTemplate

html_content = """
<div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; max-width: 800px; margin: 0 auto; padding: 20px;">
    <!-- Header -->
    <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #0056b3; padding-bottom: 20px; margin-bottom: 30px;">
        <div style="flex: 1;">
            <h1 style="color: #0056b3; margin: 0; font-size: 24px; text-transform: uppercase;">{{ entreprise.designation }}</h1>
            <p style="margin: 5px 0 0; font-size: 14px; color: #666;">{{ entreprise.adresse }}</p>
        </div>
        <div style="flex: 1; text-align: right;">
            <h2 style="margin: 0; font-size: 28px; color: #333; text-transform: uppercase; letter-spacing: 2px;">Bulletin de Notes</h2>
            <p style="margin: 5px 0 0; font-size: 14px; color: #666;">Édité le : {{ date_impression }}</p>
        </div>
    </div>

    <!-- Student Info & Session Info -->
    <div style="display: flex; justify-content: space-between; margin-bottom: 30px; gap: 20px;">
        <div style="flex: 1; background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6;">
            <h3 style="margin: 0 0 10px; font-size: 16px; color: #0056b3; border-bottom: 1px solid #dee2e6; padding-bottom: 5px;">Informations Étudiant</h3>
            <p style="margin: 5px 0; font-size: 14px;"><strong>Nom et Prénom :</strong> {{ etudiant.nom }} {{ etudiant.prenom }}</p>
            <p style="margin: 5px 0; font-size: 14px;"><strong>Matricule :</strong> {{ etudiant.matricule }}</p>
            <p style="margin: 5px 0; font-size: 14px;"><strong>Né(e) le :</strong> {{ etudiant.date_naissance }} à {{ etudiant.lieu_naissance }}</p>
        </div>
        <div style="flex: 1; background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6;">
            <h3 style="margin: 0 0 10px; font-size: 16px; color: #0056b3; border-bottom: 1px solid #dee2e6; padding-bottom: 5px;">Informations Session</h3>
            <p style="margin: 5px 0; font-size: 14px;"><strong>Session :</strong> {{ session_line.session.nom_session }}</p>
            <p style="margin: 5px 0; font-size: 14px;"><strong>Semestre :</strong> {{ session_line.semestre }}</p>
            <p style="margin: 5px 0; font-size: 14px;"><strong>Groupe :</strong> {{ groupe.nom_groupe }}</p>
        </div>
    </div>

    <!-- Marks Table -->
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 30px; font-size: 14px;">
        <thead>
            <tr>
                <th style="background-color: #0056b3; color: #fff; padding: 10px; text-align: left; border: 1px solid #0056b3; width: 35%;">Module</th>
                <th style="background-color: #0056b3; color: #fff; padding: 10px; text-align: left; border: 1px solid #0056b3; width: 25%;">Professeur</th>
                <th style="background-color: #0056b3; color: #fff; padding: 10px; text-align: center; border: 1px solid #0056b3; width: 10%;">Coef.</th>
                <th style="background-color: #0056b3; color: #fff; padding: 10px; text-align: center; border: 1px solid #0056b3; width: 15%;">Moyenne</th>
                <th style="background-color: #0056b3; color: #fff; padding: 10px; text-align: center; border: 1px solid #0056b3; width: 15%;">Total</th>
            </tr>
        </thead>
        <tbody>
            {% for module in modules_data %}
            <tr>
                <td style="padding: 10px; border: 1px solid #dee2e6; border-bottom: 1px solid #dee2e6;">
                    <strong>{{ module.matiere }}</strong><br>
                    <span style="font-size: 12px; color: #666; font-style: italic;">{{ module.observation }}</span>
                </td>
                <td style="padding: 10px; border: 1px solid #dee2e6;">{{ module.professeur }}</td>
                <td style="padding: 10px; border: 1px solid #dee2e6; text-align: center;">{{ module.coef }}</td>
                <td style="padding: 10px; border: 1px solid #dee2e6; text-align: center; font-weight: bold;">{{ module.moyenne_matiere }}</td>
                <td style="padding: 10px; border: 1px solid #dee2e6; text-align: center;">{{ module.total_points }}</td>
            </tr>
            {% endfor %}
        </tbody>
        <tfoot>
            <tr style="background-color: #f8f9fa; font-weight: bold;">
                <td colspan="2" style="padding: 12px 10px; border: 1px solid #dee2e6; text-align: right; text-transform: uppercase;">Total</td>
                <td style="padding: 12px 10px; border: 1px solid #dee2e6; text-align: center; color: #0056b3;">{{ total_coef }}</td>
                <td style="padding: 12px 10px; border: 1px solid #dee2e6; text-align: right; color: #0056b3;">Moyenne Générale :</td>
                <td style="padding: 12px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 16px; color: #0056b3; background-color: #e9ecef;">{{ moyenne_semestre }}</td>
            </tr>
        </tfoot>
    </table>

    <!-- Final Decision -->
    <div style="background-color: #e8f4fd; padding: 15px; border-radius: 8px; border-left: 5px solid #0056b3; margin-bottom: 40px;">
        <h3 style="margin: 0 0 5px; font-size: 16px; color: #0056b3;">Décision du Jury</h3>
        <p style="margin: 0; font-size: 18px; font-weight: bold;">{{ deliberation.decision }}</p>
    </div>

    <!-- Signatures -->
    <div style="display: flex; justify-content: space-between; margin-top: 50px;">
        <div style="text-align: center; flex: 1;">
            <p style="margin: 0 0 50px; font-weight: bold; font-size: 14px;">Le Directeur des Études</p>
            <p style="margin: 0; font-size: 12px; color: #666;">(Cachet et Signature)</p>
        </div>
        <div style="text-align: center; flex: 1;">
            <p style="margin: 0 0 50px; font-weight: bold; font-size: 14px;">Le Directeur de l'Établissement</p>
            <p style="margin: 0; font-size: 12px; color: #666;">(Cachet et Signature)</p>
        </div>
    </div>
</div>
"""

def create_template():
    template, created = DocumentTemplate.objects.update_or_create(
        slug="bulletin-de-notes-standard",
        defaults={
            "title": "Bulletin de Notes Standard (Pro)",
            "template_type": "bulletin",
            "content": html_content,
            "description": "Modèle professionnel pour les relevés de notes / bulletins.",
            "is_active": True
        }
    )
    if created:
        print("Template 'bulletin-de-notes-standard' created successfully.")
    else:
        print("Template 'bulletin-de-notes-standard' updated successfully.")

if __name__ == "__main__":
    create_template()
