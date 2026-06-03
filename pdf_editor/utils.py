from django.template.exceptions import TemplateSyntaxError
from django import template as django_template
import json
from .models import DocumentTemplate

def validate_template_content(content):
    """Valide le contenu du template"""
    try:
        template = django_template.Template(content)
        return True, "Template valide"
    except TemplateSyntaxError as e:
        return False, f"Erreur de syntaxe: {str(e)}"

from django.template import Engine, Context

def render_template_with_context(template_content, context_data):
    """Rend un template avec un contexte"""
    try:
        engine = Engine(string_if_invalid='<span style="background-color: #fef08a; color: #b45309; padding: 0 4px; border-radius: 2px; font-weight: bold; border: 1px dashed #b45309;">[MANQUANT : %s]</span>')
        template = engine.from_string(template_content)
        rendered = template.render(Context(context_data))
        return rendered, None
    except Exception as e:
        return None, str(e)

def get_mock_context_for_type(template_type):
    from django.utils import timezone
    today = timezone.now().date()
    
    context = {
        'date_impression': today.strftime("%d/%m/%Y"),
        'entreprise': {
            'designation': 'Établissement Test (Mock)',
            'adresse': '123 Rue de la Formation, Alger',
            'rc': 'RC-123456',
            'nif': 'NIF-987654',
            'nis': 'NIS-112233',
            'art': 'ART-5566',
            'rib': 'RIB-000011112222',
        },
        'current_user': 'Admin Test'
    }

    if template_type in ['student_info', 'certificate', 'stage']:
        context['etudiant'] = {
            'nom': 'Dupont', 'prenom': 'Jean', 'nom_arabe': 'ديبون', 'prenom_arabe': 'جان',
            'matricule': 'MAT-2023-001', 'sexe': 'M', 'date_naissance': '15/05/2000',
            'lieu_naissance': 'Alger', 'adresse': 'Cité des Oliviers, Alger',
            'commune': 'Alger Centre', 'wilaya': 'Alger', 'pays': 'Algérie',
            'email': 'jean.dupont@email.com', 'telephone': '0555001122',
            'groupe_sanguin': 'O+', 'situation_familiale': 'Célibataire',
            'prenom_pere': 'Pierre', 'nom_mere': 'Martin', 'prenom_mere': 'Marie',
            'tel_pere': '0555334455', 'tel_mere': '0555667788', 'date_inscription': '01/09/2023',
        }
        context['promo'] = {
            'specialite': {'label': 'Développement Web'},
            'label': 'Promo 2023-2024', 'date_debut': '01/10/2023', 'date_fin': '30/06/2024',
        }
        context['echeancier'] = {
            'total': '150 000 DA', 'paye': '50 000 DA', 'restant': '100 000 DA',
        }
        # Les listes mockées pour les boucles
        context['echeances'] = [
            {'date_echeance': '01/11/2023', 'montant': '50 000 DA', 'statut': 'Payé'},
            {'date_echeance': '01/12/2023', 'montant': '50 000 DA', 'statut': 'En attente'},
        ]
        context['documents'] = [
            {'nom': 'Extrait de naissance', 'fourni': 'Oui', 'date_depot': '01/09/2023'},
            {'nom': 'Diplôme précédent', 'fourni': 'Non', 'date_depot': ''},
        ]
        if template_type == 'stage':
            context['stage'] = {
                'entreprise': {'designation': 'Tech Solutions SARL', 'adresse': 'Parc Technologique'},
                'date_debut': '01/02/2024', 'date_fin': '30/05/2024',
                'theme': 'Conception d\'une API RESTful',
            }
            
    elif template_type == 'contract':
        context['employe'] = {
            'civilite': 'M.', 'nom': 'Benali', 'prenom': 'Karim',
            'adresse': 'Quartier des Affaires, Bab Ezzouar',
            'date_naissance': '20/08/1990', 'lieu_naissance': 'Oran',
            'cin': '1122334455', 'secu': '99887766',
        }
        context['contrat'] = {
            'poste': {'label': 'Formateur IT'}, 'service': {'label': 'Pédagogie'},
            'date_embauche': '15/01/2024', 'duree': '12', 'salaire_base': '80 000',
        }
        
    elif template_type == 'invoice':
        context['client'] = {
            'nom': 'SARL Exemple', 'prenom': '', 'adresse': 'Zone Industrielle, Rouiba',
            'telephone': '023112233', 'email': 'contact@exemple.dz',
        }
        context['facture'] = {
            'num_facture': 'FAC-2024-001', 'date_facture': '01/02/2024',
            'montant_ht': '100 000 DA', 'montant_tva': '19 000 DA',
            'montant_ttc': '119 000 DA', 'montant_lettre': 'Cent dix-neuf mille',
            'get_status_display': 'Non payée',
        }

    elif template_type == 'payment_receipt':
        context['paiement'] = {
            'num': 'REC-2024-105', 'date_paiement': '15/02/2024',
            'montant_paye': '25 000 DA', 'get_mode_paiement_display': 'Virement Bancaire',
        }
        context['prospect'] = {
            'nom': 'Ammar', 'prenom': 'Yassine',
        }

    return context

def serialize_templates(queryset):
    """Serialize a queryset of DocumentTemplate to a list of dicts"""
    templates_data = []
    for template in queryset:
        template_dict = {
            'title': template.title,
            'slug': template.slug,
            'template_type': template.template_type,
            'content': template.content,
            'description': template.description,
            'custom_css': template.custom_css,
            'is_active': template.is_active,
        }
        templates_data.append(template_dict)
    return templates_data

def process_template_import(json_data, user=None):
    """Process import of templates from JSON data"""
    if not isinstance(json_data, list):
        raise ValueError("Le fichier JSON doit contenir une liste d'objets.")
        
    count_created = 0
    count_updated = 0
    
    for item in json_data:
        # Recherche par slug
        obj, created = DocumentTemplate.objects.update_or_create(
            slug=item.get('slug'),
            defaults={
                'title': item.get('title'),
                'template_type': item.get('template_type'),
                'content': item.get('content'),
                'description': item.get('description'),
                'custom_css': item.get('custom_css', ''),
                'is_active': item.get('is_active', True),
            }
        )
        
        # Si c'est une création, on assigne l'utilisateur
        if created and user and user.is_authenticated:
            obj.created_by = user
            obj.save(update_fields=['created_by'])
            
        if created:
            count_created += 1
        else:
            count_updated += 1
            
    return count_created, count_updated
