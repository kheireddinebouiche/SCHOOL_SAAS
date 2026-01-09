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

def render_template_with_context(template_content, context_data):
    """Rend un template avec un contexte"""
    try:
        template = django_template.Template(template_content)
        rendered = template.render(django_template.Context(context_data))
        return rendered, None
    except Exception as e:
        return None, str(e)

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
