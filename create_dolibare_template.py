import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from pdf_editor.models import DocumentTemplate

# Basic HTML structure for a Dolibarr-like quote (devis)
dolibarr_html = """
<div style="font-family: Arial, sans-serif; font-size: 12px; color: #333; max-width: 800px; margin: 0 auto; background: #fff; padding: 20px;">
    <!-- Header -->
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 30px;">
        <tr>
            <td style="width: 50%; vertical-align: top;">
                {% if entreprise_logo %}
                <img src="{{ entreprise_logo }}" alt="{{ entreprise_nom }}" style="max-width: 150px; max-height: 80px; margin-bottom: 10px;">
                {% else %}
                <h1 style="color: #2c3e50; font-size: 24px; margin: 0 0 10px 0;">{{ entreprise_nom }}</h1>
                {% endif %}
                <p style="margin: 0; line-height: 1.5;">
                    {{ entreprise_adresse }}<br>
                    {% if entreprise_telephone %}Tél: {{ entreprise_telephone }}<br>{% endif %}
                    {% if entreprise_email %}Email: {{ entreprise_email }}<br>{% endif %}
                    <br>
                    {% if entreprise_rc %}RC: {{ entreprise_rc }}{% endif %}
                    {% if entreprise_nif %} | NIF: {{ entreprise_nif }}{% endif %}
                    {% if entreprise_nis %} | NIS: {{ entreprise_nis }}{% endif %}
                    {% if entreprise_art_imp %} | Art. Imp: {{ entreprise_art_imp }}{% endif %}
                </p>
            </td>
            <td style="width: 50%; vertical-align: top; text-align: right;">
                <h2 style="color: #2c3e50; font-size: 20px; margin: 0 0 10px 0;">DEVIS / PROFORMA</h2>
                <p style="margin: 0; line-height: 1.5; font-weight: bold;">
                    Réf: {{ devis_numero }}<br>
                    Date: {{ date_emission }}<br>
                    {% if date_echeance %}Date d'échéance: {{ date_echeance }}{% endif %}
                </p>
                <div style="margin-top: 20px; text-align: left; background: #f8f9fa; padding: 15px; border: 1px solid #dee2e6; border-radius: 4px; display: inline-block; min-width: 250px;">
                    <h3 style="margin: 0 0 10px 0; font-size: 14px; color: #2c3e50;">Adressé à:</h3>
                    {% if client_logo %}
                    <img src="{{ client_logo }}" alt="{{ client_nom }}" style="max-width: 100px; max-height: 50px; margin-bottom: 5px;">
                    {% endif %}
                    <p style="margin: 0; font-weight: bold;">{{ client_nom }}</p>
                    <p style="margin: 5px 0 0 0; line-height: 1.4;">
                        {{ client_adresse }}<br>
                        {% if client_telephone %}Tél: {{ client_telephone }}<br>{% endif %}
                        {% if client_email %}Email: {{ client_email }}<br>{% endif %}
                        <br>
                        {% if client_rc %}RC: {{ client_rc }}<br>{% endif %}
                        {% if client_nif %}NIF: {{ client_nif }}<br>{% endif %}
                        {% if client_nis %}NIS: {{ client_nis }}<br>{% endif %}
                        {% if client_art_imp %}Art. Imp: {{ client_art_imp }}<br>{% endif %}
                    </p>
                </div>
            </td>
        </tr>
    </table>

    <!-- Items Table -->
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
        <thead>
            <tr style="background-color: #2c3e50; color: #fff;">
                <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Désignation / Description</th>
                <th style="padding: 10px; text-align: right; border: 1px solid #dee2e6; width: 10%;">Qté</th>
                <th style="padding: 10px; text-align: right; border: 1px solid #dee2e6; width: 15%;">P.U HT</th>
                {% if show_remise %}<th style="padding: 10px; text-align: right; border: 1px solid #dee2e6; width: 10%;">Remise</th>{% endif %}
                {% if show_tva %}<th style="padding: 10px; text-align: right; border: 1px solid #dee2e6; width: 10%;">TVA</th>{% endif %}
                <th style="padding: 10px; text-align: right; border: 1px solid #dee2e6; width: 15%;">Total HT</th>
            </tr>
        </thead>
        <tbody>
            {% for ligne in lignes %}
            <tr>
                <td style="padding: 10px; border: 1px solid #dee2e6;">
                    <strong>{{ ligne.designation }}</strong>
                    {% if ligne.description and ligne.description != ligne.designation %}
                    <br><span style="color: #666; font-size: 11px;">{{ ligne.description|linebreaksbr }}</span>
                    {% endif %}
                </td>
                <td style="padding: 10px; text-align: right; border: 1px solid #dee2e6;">{{ ligne.quantite|floatformat:2 }}</td>
                <td style="padding: 10px; text-align: right; border: 1px solid #dee2e6;">{{ ligne.prix_unitaire|floatformat:2 }}</td>
                {% if show_remise %}<td style="padding: 10px; text-align: right; border: 1px solid #dee2e6;">{{ ligne.remise_percent|floatformat:2 }}%</td>{% endif %}
                {% if show_tva %}<td style="padding: 10px; text-align: right; border: 1px solid #dee2e6;">{{ ligne.tva_percent|floatformat:2 }}%</td>{% endif %}
                <td style="padding: 10px; text-align: right; border: 1px solid #dee2e6;">{{ ligne.montant|floatformat:2 }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <!-- Totals -->
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 30px;">
        <tr>
            <td style="width: 60%; vertical-align: top;">
                {% if conditions_commerciales %}
                <div style="margin-top: 20px;">
                    <h4 style="margin: 0 0 5px 0; font-size: 13px;">Conditions de paiement / Notes :</h4>
                    <p style="margin: 0; font-size: 11px; color: #555; white-space: pre-wrap;">{{ conditions_commerciales }}</p>
                </div>
                {% endif %}
            </td>
            <td style="width: 40%;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 5px; text-align: right; font-weight: bold;">Total HT :</td>
                        <td style="padding: 5px; text-align: right; width: 40%;">{{ total_ht|floatformat:2 }}</td>
                    </tr>
                    {% if show_remise and total_remise > 0 %}
                    <tr>
                        <td style="padding: 5px; text-align: right;">Remise Globale :</td>
                        <td style="padding: 5px; text-align: right;">- {{ total_remise|floatformat:2 }}</td>
                    </tr>
                    {% endif %}
                    {% if show_tva %}
                    <tr>
                        <td style="padding: 5px; text-align: right;">Total TVA :</td>
                        <td style="padding: 5px; text-align: right;">{{ total_tva|floatformat:2 }}</td>
                    </tr>
                    {% endif %}
                    <tr>
                        <td style="padding: 10px 5px; text-align: right; font-weight: bold; font-size: 14px; border-top: 2px solid #2c3e50;">Total TTC :</td>
                        <td style="padding: 10px 5px; text-align: right; font-weight: bold; font-size: 14px; border-top: 2px solid #2c3e50; color: #2c3e50;">{{ total_ttc|floatformat:2 }}</td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>

    <!-- Footer -->
    <div style="margin-top: 50px; text-align: center; font-size: 10px; color: #777; border-top: 1px solid #eee; padding-top: 10px;">
        <p>Document généré le {% now "d/m/Y H:i" %}</p>
        <p>Merci pour votre confiance.</p>
    </div>
</div>
"""

from app.models import Institut
from django_tenants.utils import tenant_context

for tenant in Institut.objects.exclude(schema_name='public'):
    with tenant_context(tenant):
        doc, created = DocumentTemplate.objects.update_or_create(
            slug='dolibare',
            defaults={
                'title': 'Devis Dolibarr',
                'template_type': 'invoice',
                'content': dolibarr_html,
                'description': 'Modèle de devis style Dolibarr (Azur/Crabe)',
                'is_active': True,
                'custom_css': '@page { margin: 0.5cm; }'
            }
        )
        if created:
            print(f"[{tenant.schema_name}] Template 'dolibare' created.")
        else:
            print(f"[{tenant.schema_name}] Template 'dolibare' updated.")
