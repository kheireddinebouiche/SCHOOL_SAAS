
import os
import django
import sys

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from pdf_editor.models import DocumentTemplate

def create_contract_template():
    title = "Contrat de Formation Professionnelle"
    slug = "contrat-formation-professionnelle"
    template_type = "contract"
    
    html_content = """
<div class="header">
    <h3 class="republic">REPUBLIQUE ALGERIENNE DEMOCRATIQUE ET POPULAIRE</h3>
    <h4 class="ministry">MINISTERE DE LA FORMATION ET DE L'ENSEIGNEMENT PROFESSIONNELS</h4>
    <h4 class="school">Ecole Privée de Formation Professionnelle INSIM</h4>
</div>

<div class="title-section">
    <h1>CONTRAT</h1>
    <h2>DE FORMATION PROFESSIONNELLE</h2>
</div>

<div class="reference-text">
    (Réf : Décret exécutif n° 18-162 du 29 Ramadhan 1439 correspondant au 14 juin 2018 fixant les conditions de création, d’ouverture et de contrôle de l’établissement privé de formation professionnel, notamment son article 35).
</div>

<div class="school-info">
    <div class="separator"></div>
    <p>Dénomination sociale de l'EPFP :</p>
    <h2 class="insim-title">INSIM</h2>
    <p>Sis à :</p>
    <p class="address">19, boulevard Mohamed BOUDIAF, lot N°214, Chéraga – Alger</p>
</div>

<div class="agreement-info">
    <p>Numéro et date de l'agrément</p>
    <p class="agreement-number">Agrément N°45 du 22/01/1995</p>
</div>
"""

    custom_css = """
body {
    font-family: 'Times New Roman', Times, serif;
    color: #000;
}
.header {
    text-align: center;
    margin-bottom: 40px;
}
.republic {
    text-decoration: underline;
    text-transform: uppercase;
    font-weight: bold;
    font-size: 14pt;
    margin-bottom: 10px;
}
.ministry {
    text-transform: uppercase;
    font-size: 11pt;
    font-weight: bold;
    margin: 5px 0;
}
.school {
    font-size: 12pt;
    font-weight: normal;
    margin-top: 10px;
}
.title-section {
    text-align: center;
    margin: 50px 0;
}
.title-section h1 {
    font-size: 36pt;
    font-weight: bold;
    text-transform: uppercase;
    margin: 0;
}
.title-section h2 {
    font-size: 18pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 10px;
}
.reference-text {
    font-size: 10pt;
    text-align: justify;
    margin: 0 40px 50px 40px;
    line-height: 1.4;
}
.school-info {
    text-align: center;
}
.separator {
    width: 200px;
    border-top: 2pt solid #000;
    margin: 0 auto 20px auto;
}
.school-info p {
    margin: 5px 0;
    font-size: 12pt;
}
.insim-title {
    font-size: 24pt;
    font-weight: bold;
    text-transform: uppercase;
    margin: 10px 0;
}
.address {
    font-weight: bold;
}
.agreement-info {
    text-align: center;
    margin-top: 40px;
}
.agreement-number {
    font-weight: bold;
    margin-top: 10px;
    font-size: 12pt;
}
"""

    description = "Template généré automatiquement basé sur le modèle officiel."

    document, created = DocumentTemplate.objects.update_or_create(
        slug=slug,
        defaults={
            'title': title,
            'template_type': template_type,
            'content': html_content,
            'custom_css': custom_css,
            'description': description,
            'is_active': True
        }
    )

    if created:
        print(f"SUCCESS: Template '{title}' created successfully.")
    else:
        print(f"SUCCESS: Template '{title}' updated successfully.")

if __name__ == '__main__':
    create_contract_template()
