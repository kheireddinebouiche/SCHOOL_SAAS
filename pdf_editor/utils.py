# utils.py

from django.template.exceptions import TemplateSyntaxError
from django import template as django_template

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
