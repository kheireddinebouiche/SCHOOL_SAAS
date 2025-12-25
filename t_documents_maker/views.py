from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from .models import *

@login_required
def editor_home(request):
    """Main editor page"""
    templates = DocumentTemplate.objects.filter(user=request.user).distinct()
    return render(request, 'tenant_folder/editor/editor.html', {
        'templates': templates
    })

@login_required
def template_list(request):
    """List all document templates"""
    templates = DocumentTemplate.objects.filter(user=request.user).distinct()
    return render(request, 'tenant_folder/editor/template_list.html', {
        'templates': templates
    })

@login_required
def create_template(request):
    """Create a new document template"""
    if request.method == 'POST':
        name = request.POST.get('name', 'Nouveau modèle')
        description = request.POST.get('description', '')

        template = DocumentTemplate.objects.create(
            name=name,
            description=description,
            user=request.user,
            layout={}
        )
        return JsonResponse({'success': True, 'id': template.id})

    return render(request, 'tenant_folder/editor/create_template.html')

@login_required
def edit_template(request, template_id):
    """Edit an existing document template"""
    template = get_object_or_404(DocumentTemplate,
                                id=template_id,
                                user=request.user,)
    return render(request, 'tenant_folder/editor/editor.html', {
        'template': template
    })

@csrf_exempt
@login_required
def save_template(request):
    """Save document template layout"""
    if request.method == 'POST':
        data = json.loads(request.body)
        template_id = data.get('id')

        if template_id:
            # Update existing template
            template = get_object_or_404(DocumentTemplate,
                                        id=template_id,
                                        user=request.user,
                                       )
            template.name = data['name']
            template.layout = data['layout']
            template.save()
        else:
            # Create new template
            template = DocumentTemplate.objects.create(
                name=data['name'],
                user=request.user,
                layout=data['layout']
            )

        return JsonResponse({'id': template.id, 'success': True})

    return JsonResponse({'error': 'POST required'}, status=400)

@login_required
def load_template(request, template_id):
    """Load document template layout"""
    
    template = get_object_or_404(DocumentTemplate,
                                id=template_id,
                                user=request.user,
                                )
    return JsonResponse({
        'id': template.id,
        'name': template.name,
        'layout': template.layout,
        'description': template.description
    })

@csrf_exempt
@login_required
def delete_template(request, template_id):
    """Delete a document template"""
    if request.method == 'POST':
        template = get_object_or_404(DocumentTemplate,
                                    id=template_id,
                                    user=request.user)
        template.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'POST required'}, status=400)

@login_required
def list_variables(request):
    """List all available document variables"""
    try:
        # Return all document variables
        variables = DocumentVariable.objects.all().distinct()

        # If no variables exist, return the predefined tags
        if not variables.exists():
            # Predefined tags for document templates
            predefined_tags = [
                ('formation', 'Formation', 'Nom de la formation'),
                ('specialite', 'Spécialité', 'Spécialité de l\'étudiant'),
                ('qualification', 'Qualification', 'Qualification de la formation'),
                ('prix_formation', 'Prix de la formation', 'Prix de la formation'),
                ('annee_academique', 'Année académique', 'Année académique en cours'),
                ('ville', 'Ville', 'Ville de l\'établissement'),
                ('date', 'Date', 'Date du document'),
                ('institut', 'Institut', 'Nom de l\'institut'),
                ('date_naissance_etudiant', 'Date de naissance étudiant', 'Date de naissance de l\'étudiant'),
                ('lieu_naissance_etudiant', 'Lieu de naissance étudiant', 'Lieu de naissance de l\'étudiant'),
                ('adresse_etudiant', 'Adresse étudiant', 'Adresse de l\'étudiant'),
                ('branche', 'Branche', 'Branche de la formation'),
            ]

            # Return predefined tags as variables
            return JsonResponse({
                'variables': [
                    {
                        'name': name,
                        'label': label,
                        'description': description
                    }
                    for name, label, description in predefined_tags
                ]
            })

        return JsonResponse({
            'variables': [
                {
                    'name': var.name,
                    'label': var.label,
                    'description': var.description
                }
                for var in variables
            ]
        })
    except Exception as e:
        # In case of any error, return predefined tags
        predefined_tags = [
            ('formation', 'Formation', 'Nom de la formation'),
            ('specialite', 'Spécialité', 'Spécialité de l\'étudiant'),
            ('qualification', 'Qualification', 'Qualification de la formation'),
            ('prix_formation', 'Prix de la formation', 'Prix de la formation'),
            ('annee_academique', 'Année académique', 'Année académique en cours'),
            ('ville', 'Ville', 'Ville de l\'établissement'),
            ('date', 'Date', 'Date du document'),
            ('institut', 'Institut', 'Nom de l\'institut'),
            ('date_naissance_etudiant', 'Date de naissance étudiant', 'Date de naissance de l\'étudiant'),
            ('lieu_naissance_etudiant', 'Lieu de naissance étudiant', 'Lieu de naissance de l\'étudiant'),
            ('adresse_etudiant', 'Adresse étudiant', 'Adresse de l\'étudiant'),
            ('branche', 'Branche', 'Branche de la formation'),
        ]

        return JsonResponse({
            'variables': [
                {
                    'name': name,
                    'label': label,
                    'description': description
                }
                for name, label, description in predefined_tags
            ]
        })

@login_required
def export_template(request, template_id):
    """Export a document template"""
    template = get_object_or_404(DocumentTemplate,
                                id=template_id,
                                user=request.user)

    # Return template data as JSON for export
    response = JsonResponse({
        'name': template.name,
        'description': template.description,
        'layout': template.layout,
        'created_at': template.created_at.isoformat(),
    })
    response['Content-Disposition'] = f'attachment; filename="{template.name}.json"'
    return response

@login_required
def generate_document(request, template_id):
    """Generate a document from a template with provided data"""
    template = get_object_or_404(DocumentTemplate,
                                id=template_id,
                                user=request.user)

    if request.method == 'POST':
        data = json.loads(request.body)
        # Get the template layout
        layout = template.layout.copy()

        # Replace variables in layout objects
        if 'objects' in layout:
            for obj in layout['objects']:
                if 'text' in obj and obj['text'].startswith('{{') and obj['text'].endswith('}}'):
                    # This is a variable field like {{formation}}
                    variable_name = obj['text'][2:-2]  # Extract name from {{name}}
                    if variable_name in data.get('replacements', {}):
                        obj['text'] = data['replacements'][variable_name]

        return JsonResponse({
            'success': True,
            'message': 'Document généré avec succès',
            'layout': layout
        })

    return JsonResponse({'error': 'POST required'}, status=400)
