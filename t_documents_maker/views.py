import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import ContentFile
from django.urls import reverse
from .models import DocumentTemplate, GeneratedDocument
from .services.template_processor import TemplateProcessor
from .services.pdf_generator import PDFGenerator

@login_required
def template_list(request):
    templates = DocumentTemplate.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'tenant_folder/editor/template_list.html', {'templates': templates})

@login_required
def template_editor(request, template_id=None):
    template = None
    if template_id:
        template = get_object_or_404(DocumentTemplate, id=template_id, author=request.user)
        # For backward compatibility, if the template has no pages but had html_content in the past,
        # we need to handle the transition
        if not template.pages:
            # Create a default page with the old html_content if it exists
            template.add_page(content=template.get_first_page_content())

    # Ensure there's at least one page for editing
    if template and not template.pages:
        template.add_page()
    elif not template:
        # For new templates, initialize with one empty page
        pass

    return render(request, 'tenant_folder/editor/editor.html', {
        'template': template
    })

@login_required
def template_delete(request, template_id):
    template = get_object_or_404(DocumentTemplate, id=template_id, author=request.user)
    template.delete()
    return redirect('t_documents_maker:template_list')

@login_required
@require_http_methods(["POST"])
def save_template(request):
    try:
        # Vérifier si la requête contient des fichiers (multipart/form-data)
        if request.content_type.startswith('multipart/form-data'):
            # Récupérer les données JSON du champ 'data'
            data = json.loads(request.POST.get('data', '{}'))
            template_id = data.get('id')
            name = data.get('name', 'Nouveau template')
            # Get pages data instead of single html_content
            pages_data = data.get('pages', [])
            page_size = data.get('page_size', 'A4')
            page_orientation = data.get('page_orientation', 'portrait')
            config_str = data.get('config', '{}')  # Récupérer la configuration

            # Parser la configuration
            try:
                config = json.loads(config_str) if config_str else {}
            except json.JSONDecodeError:
                config = {}

            # Récupérer les fichiers de logo
            header_logo_file = request.FILES.get('header_logo')
            footer_logo_file = request.FILES.get('footer_logo')
        else:
            # Ancienne méthode pour les requêtes JSON
            data = json.loads(request.body)
            template_id = data.get('id')
            name = data.get('name', 'Nouveau template')
            # Get pages data instead of single html_content
            pages_data = data.get('pages', [])
            page_size = data.get('page_size', 'A4')
            page_orientation = data.get('page_orientation', 'portrait')
            config_str = data.get('config', '{}')  # Récupérer la configuration

            # Parser la configuration
            try:
                config = json.loads(config_str) if config_str else {}
            except json.JSONDecodeError:
                config = {}

            # Pas de fichiers dans ce cas
            header_logo_file = None
            footer_logo_file = None

        # Extract variables from all pages
        all_variables = set()
        for page_data in pages_data:
            html_content = page_data.get('content', '')
            processor = TemplateProcessor(html_content)
            page_variables = processor.extract_variables()
            all_variables.update(page_variables)

        if template_id and template_id != 'null':
            template = get_object_or_404(DocumentTemplate, id=template_id, author=request.user)
            template.name = name
            template.page_size = page_size
            template.page_orientation = page_orientation
            template.variables = {'variables': list(all_variables)}
            template.config = config
            # Update pages
            template.pages = pages_data
        else:
            template = DocumentTemplate.objects.create(
                author=request.user,
                name=name,
                page_size=page_size,
                page_orientation=page_orientation,
                variables={'variables': list(all_variables)},
                config=config,
                pages=pages_data  # Initialize with the pages data
            )

        # Handle header and footer configuration
        header_footer_config = data.get('header_footer', {})
        if header_footer_config:
            # Ne pas sauvegarder les logos dans la configuration puisque le support est supprimé
            if 'header' in header_footer_config:
                header_footer_config['header']['logo_path'] = ''
            if 'footer' in header_footer_config:
                header_footer_config['footer']['logo_path'] = ''
            template.set_header_footer_config(header_footer_config)

        template.save()
        # Vérifier que le template a été sauvegardé correctement
        template.refresh_from_db()
        return JsonResponse({
            'success': True,
            'id': template.id,
            'variables': list(all_variables),
            'page_count': len(template.pages)
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Erreur lors de l'enregistrement du template: {str(e)}")
        print(f"Détails de l'erreur: {error_details}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def preview_template(request):
    try:
        data = json.loads(request.body)
        # Handle both single html_content (for backward compatibility) and pages
        html_content = data.get('html_content', '')
        pages_data = data.get('pages', [])
        header_footer_config = data.get('header_footer', {})

        all_variables = set()
        rendered_html = ""

        if pages_data:
            # Process multiple pages
            for i, page_data in enumerate(pages_data):
                content = page_data.get('content', '')
                processor = TemplateProcessor(content)
                page_variables = processor.extract_variables()
                all_variables.update(page_variables)

                # Add page separator for preview
                if i > 0:
                    rendered_html += '<div style="page-break-before: always;"></div>'

                # Add header and footer if enabled
                page_html = ""
                if header_footer_config:
                    header_config = header_footer_config.get('header', {})
                    if header_config.get('enabled', False):
                        page_html += _generate_header_html(header_config)

                page_html += content

                footer_config = header_footer_config.get('footer', {})
                if footer_config.get('enabled', False):
                    page_html += _generate_footer_html(footer_config)

                rendered_html += page_html
        else:
            # Process single content for backward compatibility
            processor = TemplateProcessor(html_content)
            sample_data = processor.get_sample_data()
            rendered_html = processor.render(sample_data)
            all_variables = set(processor.extract_variables())

        return JsonResponse({
            'success': True,
            'rendered_html': rendered_html,
            'variables': list(all_variables)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def _generate_header_html(header_config):
    """Génère le HTML pour l'en-tête"""
    if not header_config.get('enabled', False):
        return ""

    logo_html = ""
    if header_config.get('logo_path'):
        logo_html = f'<img src="{header_config["logo_path"]}" style="height: 50px; max-width: 200px;" />'

    text_html = ""
    if header_config.get('text'):
        text_html = f'<div style="font-size: 14px; font-weight: bold;">{header_config["text"]}</div>'

    # Positionnement du logo
    logo_position = header_config.get('logo_position', 'left')
    text_position = header_config.get('text_position', 'right')

    # Créer le conteneur de l'en-tête
    header_style = "display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; border-bottom: 1px solid #ccc; margin-bottom: 20px;"

    if logo_position == 'left' and text_position == 'right':
        return f'<div class="header" style="{header_style}">{logo_html}<div></div>{text_html}</div>'
    elif logo_position == 'center' or text_position == 'center':
        return f'<div class="header" style="{header_style}"><div style="flex: 1;"></div>{logo_html}{text_html}<div style="flex: 1;"></div></div>'
    else:
        return f'<div class="header" style="{header_style}">{text_html}<div></div>{logo_html}</div>'


def _generate_footer_html(footer_config):
    """Génère le HTML pour le pied de page"""
    if not footer_config.get('enabled', False):
        return ""

    # Générer le HTML pour le logo
    logo_html = ""
    if footer_config.get('logo_path'):
        logo_html = f'<img src="{footer_config["logo_path"]}" style="height: 30px; max-width: 150px;" />'

    # Générer le HTML pour le texte
    text_html = ""
    if footer_config.get('text'):
        text_html = f'<div style="font-size: 12px;">{footer_config["text"]}</div>'

    # Positionnement du logo
    logo_position = footer_config.get('logo_position', 'center')
    text_position = footer_config.get('text_position', 'center')

    # Créer le conteneur du pied de page
    footer_style = "display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; border-top: 1px solid #ccc; margin-top: 20px; font-size: 12px;"

    if logo_position == 'left' and text_position == 'right':
        return f'<div class="footer" style="{footer_style}">{logo_html}<div></div>{text_html}</div>'
    elif logo_position == 'center' or text_position == 'center':
        return f'<div class="footer" style="{footer_style}"><div style="flex: 1;"></div>{logo_html}{text_html}<div style="flex: 1;"></div></div>'
    else:
        return f'<div class="footer" style="{footer_style}">{text_html}<div></div>{logo_html}</div>'

@login_required
@require_http_methods(["POST"])
def generate_pdf(request):
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        user_data = data.get('data', {})

        template = get_object_or_404(DocumentTemplate, id=template_id, author=request.user)

        # Get header and footer configuration
        header_footer_config = template.get_header_footer_config()

        # Clear logo paths since logo support has been removed
        header_footer_config['header']['logo_path'] = ''
        header_footer_config['footer']['logo_path'] = ''

        # Process all pages with the user data
        processed_pages = []
        for page in template.pages:
            content = page.get('content', '')
            processor = TemplateProcessor(content)
            rendered_content = processor.render(user_data)

            # Create a processed page object
            processed_page = {
                'content': rendered_content,
                'page_size': page.get('page_size', template.page_size),
                'orientation': page.get('orientation', template.page_orientation)
            }
            processed_pages.append(processed_page)

        # Use MultiPagePDFGenerator for multi-page documents
        from .services.pdf_generator import MultiPagePDFGenerator
        pdf_gen = MultiPagePDFGenerator(processed_pages, {
            'page_size': template.page_size,
            'page_orientation': template.page_orientation,
            'header_footer': header_footer_config
        })
        pdf_bytes, success, error = pdf_gen.generate()

        if not success:
            return JsonResponse({'error': error}, status=500)

        doc = GeneratedDocument.objects.create(
            template=template,
            data=user_data,
            author=request.user
        )
        filename = f"document_{doc.id}.pdf"
        doc.pdf_file.save(filename, ContentFile(pdf_bytes))
        doc.save()

        return JsonResponse({
            'success': True,
            'download_url': reverse('t_documents_maker:download_pdf', args=[doc.id])
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def download_pdf(request, document_id):
    doc = get_object_or_404(GeneratedDocument, id=document_id, author=request.user)
    return FileResponse(
        doc.pdf_file.open('rb'),
        as_attachment=True,
        filename=f"document_{doc.id}.pdf"
    )

@login_required
def document_list(request):
    documents = GeneratedDocument.objects.filter(author=request.user).select_related('template')
    return render(request, 'tenant_folder/editor/document_list.html', {'documents': documents})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('t_documents_maker:template_list'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
