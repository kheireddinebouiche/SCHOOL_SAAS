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
        html_content = data.get('html_content', '')
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
        print(f"  - html_content length: {len(html_content)}")
        print(f"  - html_content preview: {html_content[:200] if html_content else 'VIDE'}")
        print(f"  - page_size: {page_size}")
        print(f"  - page_orientation: {page_orientation}")
        print(f"  - config: {config}")

        processor = TemplateProcessor(html_content)
        variables = processor.extract_variables()

        if template_id:
            template = get_object_or_404(DocumentTemplate, id=template_id, author=request.user)
            template.name = name
            template.html_content = html_content
            template.page_size = page_size
            template.page_orientation = page_orientation
            template.variables = {'variables': variables}
            template.config = config
        else:
            template = DocumentTemplate.objects.create(
                author=request.user,
                name=name,
                html_content=html_content,
                page_size=page_size,
                page_orientation=page_orientation,
                variables={'variables': variables},
                config=config
            )

        template.save()
        # Vérifier que le template a été sauvegardé correctement
        template.refresh_from_db()
        print(f"Template sauvegardé avec succès. ID: {template.id}")
        print(f"Contenu HTML dans la base de données: {template.html_content[:200] if template.html_content else 'VIDE'} (longueur: {len(template.html_content) if template.html_content else 0})")
        print(f"Configuration dans la base de données: {template.config}")
        return JsonResponse({
            'success': True,
            'id': template.id,
            'variables': variables
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
        html_content = data.get('html_content', '')
        
        processor = TemplateProcessor(html_content)
        sample_data = processor.get_sample_data()
        rendered = processor.render(sample_data)
        
        return JsonResponse({
            'success': True,
            'rendered_html': rendered,
            'variables': processor.extract_variables()
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
        
        processor = TemplateProcessor(template.html_content)
        rendered_html = processor.render(user_data)
        
        pdf_gen = PDFGenerator(rendered_html, {
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
