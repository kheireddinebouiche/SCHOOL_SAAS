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

        print(f"Requête de sauvegarde reçue:")
        print(f"  - template_id: {template_id}")
        print(f"  - name: {name}")
        print(f"  - pages count: {len(pages_data)}")
        print(f"  - page_size: {page_size}")
        print(f"  - page_orientation: {page_orientation}")
        print(f"  - config: {config}")

        # Extract variables from all pages
        all_variables = set()
        for page_data in pages_data:
            html_content = page_data.get('content', '')
            processor = TemplateProcessor(html_content)
            page_variables = processor.extract_variables()
            all_variables.update(page_variables)

        if template_id:
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

        template.save()
        # Vérifier que le template a été sauvegardé correctement
        template.refresh_from_db()
        print(f"Template sauvegardé avec succès. ID: {template.id}")
        print(f"Pages dans la base de données: {len(template.pages)}")
        print(f"Configuration dans la base de données: {template.config}")
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
                rendered_html += content
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

@login_required
@require_http_methods(["POST"])
def generate_pdf(request):
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        user_data = data.get('data', {})

        template = get_object_or_404(DocumentTemplate, id=template_id, author=request.user)

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
            'page_orientation': template.page_orientation
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
