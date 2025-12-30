# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template import Template, Context
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.text import slugify
from django.db import models
import json
from .models import DocumentTemplate, DocumentGeneration
from .forms import DocumentTemplateForm, DocumentTemplateBasicForm, DocumentGenerationForm


class TemplateListView(LoginRequiredMixin, ListView):
    """Affiche la liste des templates"""

    model = DocumentTemplate
    template_name = 'documents/template_list.html'
    context_object_name = 'templates'
    paginate_by = 20

    def get_queryset(self):
        queryset = DocumentTemplate.objects.all()

        # Filtrer par type de template
        template_type = self.request.GET.get('template_type')
        if template_type:
            queryset = queryset.filter(template_type=template_type)

        # Recherche par titre ou description
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(description__icontains=search)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template_types'] = DocumentTemplate.TEMPLATE_TYPES
        # Calculate statistics
        context['active_count'] = self.get_queryset().filter(is_active=True).count()
        return context


class TemplateDetailView(LoginRequiredMixin, DetailView):
    """Affiche les détails d'un template"""

    model = DocumentTemplate
    template_name = 'documents/template_detail.html'
    slug_field = 'slug'
    context_object_name = 'template'


class TemplateCreateBasicView(LoginRequiredMixin, CreateView):
    """Crée un nouveau template - étape 1: informations de base"""

    model = DocumentTemplate
    form_class = DocumentTemplateBasicForm
    template_name = 'documents/template_basic_form.html'
    success_url = reverse_lazy('pdf_editor:template-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # Redirect to the edit view to complete the template with content
        return redirect('pdf_editor:template-update', slug=self.object.slug)

class TemplateCreateView(LoginRequiredMixin, CreateView):
    """Crée un nouveau template - ancienne méthode (tout en un)"""

    model = DocumentTemplate
    form_class = DocumentTemplateForm
    template_name = 'documents/template_form.html'
    success_url = reverse_lazy('pdf_editor:template-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TemplateUpdateView(LoginRequiredMixin, UpdateView):
    """Met à jour un template existant"""

    model = DocumentTemplate
    form_class = DocumentTemplateForm
    template_name = 'documents/template_form.html'
    slug_field = 'slug'
    success_url = reverse_lazy('pdf_editor:template-list')


class TemplateDeleteView(LoginRequiredMixin, DeleteView):
    """Supprime un template"""

    model = DocumentTemplate
    template_name = 'documents/template_confirm_delete.html'
    slug_field = 'slug'
    success_url = reverse_lazy('pdf_editor:template-list')


class DocumentGenerationView(LoginRequiredMixin, View):
    """Génère et affiche un document"""
    
    def get(self, request, slug):
        template_obj = get_object_or_404(DocumentTemplate, slug=slug, is_active=True)
        form = DocumentGenerationForm()
        
        return render(request, 'documents/generate_document.html', {
            'template': template_obj,
            'form': form
        })
    
    def post(self, request, slug):
        template_obj = get_object_or_404(DocumentTemplate, slug=slug, is_active=True)
        form = DocumentGenerationForm(request.POST)
        
        if form.is_valid():
            # Préparer les données de contexte
            context_data = {
                'recipient_name': form.cleaned_data.get('recipient_name', ''),
                'recipient_email': form.cleaned_data.get('recipient_email', ''),
                'document_date': form.cleaned_data.get('document_date', ''),
                'company_name': 'SALDAE SYSTEMS',  # À personnaliser
                'current_user': request.user.get_full_name() or request.user.username,
            }
            
            # Rendre le template Django
            try:
                django_template = Template(template_obj.content)
                rendered_content = django_template.render(Context(context_data))
                
                # Enregistrer la génération
                doc_gen = DocumentGeneration.objects.create(
                    template=template_obj,
                    context_data=context_data,
                    rendered_content=rendered_content,
                    generated_by=request.user
                )
                
                return redirect('pdf_editor:document-preview', pk=doc_gen.pk)
            except Exception as e:
                form.add_error(None, f"Erreur lors du rendu: {str(e)}")
        
        return render(request, 'documents/generate_document.html', {
            'template': template_obj,
            'form': form
        })


class DocumentPreviewView(LoginRequiredMixin, DetailView):
    """Affiche un aperçu du document généré"""
    
    model = DocumentGeneration
    template_name = 'documents/document_preview.html'
    context_object_name = 'document'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Rendre le contenu HTML en brut
        context['rendered_html'] = self.object.rendered_content
        context['custom_css'] = self.object.template.custom_css
        return context


class DocumentExportView(LoginRequiredMixin, View):
    """Exporte un document en PDF"""

    def get(self, request, pk):
        document = get_object_or_404(DocumentGeneration, pk=pk)

        try:
            # Utiliser weasyprint pour convertir HTML en PDF
            from weasyprint import HTML, CSS
            from io import BytesIO
            import os
            from django.conf import settings

            # Inclure le CSS personnalisé du template et les styles de base dans le PDF
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    /* Styles de base pour le PDF */
                    body {{
                        font-family: 'Arail', system-ui, sans-serif;
                        margin: 0;
                        padding: 0mm;
                        line-height: 1.6;
                        background-color: white;
                        color: #1e293b;
                    }}

                    /* Styles Bootstrap simplifiés pour le PDF */
                    .container {{
                        width: 100%;
                        padding-right: 1px;
                        padding-left: 1px;
                        margin-right: auto;
                        margin-left: auto;
                    }}

                    .row {{
                        display: flex;
                        flex-wrap: wrap;
                        margin-right: -15px;
                        margin-left: -15px;
                    }}

                    .col-md-4, .col-md-6, .col-md-12 {{
                        position: relative;
                        width: 100%;
                        padding-right: 15px;
                        padding-left: 15px;
                    }}

                    .card {{
                        position: relative;
                        display: flex;
                        flex-direction: column;
                        min-width: 0;
                        word-wrap: break-word;
                        background-clip: border-box;
                        border: 1px solid rgba(0,0,0,.125);
                        border-radius: 0.25rem;
                        background-color: white;
                    }}

                    .card-body {{
                        flex: 1 1 auto;
                        min-height: 1px;
                        padding: 1.25rem;
                    }}

                    /* Styles pour les boutons et éléments d'interface à cacher */
                    .btn, .no-print {{
                        display: none !important;
                    }}

                    img {{
                        
                        max-width: 100%;
                        height: auto;
                        
                    }}

                    .logo {{
                        width: 120px;
                        height: auto;
                    }}

                    .signature {{
                        width: 200px;
                        margin-top: 20px;
                    }}

                    /* Appliquer le CSS personnalisé du template */
                    {document.template.custom_css}
                </style>
            </head>
            <body>
                {document.rendered_content}
            </body>
            </html>
            """

            pdf_file = BytesIO()

            # Créer le PDF avec le contenu HTML et les styles
            HTML(string=html_content,base_url=request.build_absolute_uri('/')).write_pdf(pdf_file)
            pdf_file.seek(0)

            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="document_{document.pk}.pdf"'
            return response

        except ImportError:
            # Si weasyprint n'est pas installé, retourner HTML à imprimer
            return redirect('pdf_editor:document-preview', pk=document.pk)


# from playwright.sync_api import sync_playwright
# from django.conf import settings

# from playwright.sync_api import sync_playwright

# class DocumentExportView(LoginRequiredMixin, View):

#     def get(self, request, pk):
#         document = get_object_or_404(DocumentGeneration, pk=pk)

#         try:
#             html_content = f"""
#             <!DOCTYPE html>
#             <html>
#             <head>
#                 <meta charset="utf-8">
#                 <style>
#                     body {{
#                         font-family: Arial, system-ui, sans-serif;
#                         margin: 0;
#                         padding: 0;
#                         background: white;
#                     }}
#                     .btn, .no-print {{ display: none !important; }}
#                     img {{ max-width: 100%; height: auto; }}
#                     {document.template.custom_css}
#                 </style>
#             </head>
#             <body>
#                 {document.rendered_content}
#             </body>
#             </html>
#             """

#             with sync_playwright() as p:
#                 browser = p.chromium.launch(
#                     headless=True,
#                     args=["--no-sandbox", "--disable-dev-shm-usage"]
#                 )

#                 page = browser.new_page()
#                 page.set_default_timeout(10000)

#                 page.set_content(
#                     html_content,
#                     base_url=request.build_absolute_uri('/'),
#                     wait_until="load"   # 🔥 correction clé
#                 )

#                 pdf_bytes = page.pdf(
#                     format="A4",
#                     print_background=True,
#                     margin={"top": "0mm", "bottom": "0mm"}
#                 )

#                 browser.close()

#             return HttpResponse(pdf_bytes, content_type="application/pdf")

#         except Exception as e:
#             print("PDF ERROR:", e)
#             return redirect("pdf_editor:document-preview", pk=document.pk)



class DocumentPrintView(LoginRequiredMixin, View):
    """Affiche le document en mode impression"""

    def get(self, request, pk):
        document = get_object_or_404(DocumentGeneration, pk=pk)

        return render(request, 'documents/document_print.html', {
            'document': document,
            'rendered_html': document.rendered_content,
            
        })