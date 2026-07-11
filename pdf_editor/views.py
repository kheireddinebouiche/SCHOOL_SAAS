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
from django.contrib import messages
import json
from .models import DocumentTemplate, DocumentGeneration
from .forms import DocumentTemplateForm, DocumentTemplateBasicForm, DocumentGenerationForm
from .utils import serialize_templates, process_template_import

class TemplateExportView(LoginRequiredMixin, View):
    """Exporte un ou plusieurs templates en JSON"""

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        if slug:
            queryset = DocumentTemplate.objects.filter(slug=slug)
            filename = f"template_{slug}.json"
        else:
            # Export all active templates or filtered
            queryset = DocumentTemplate.objects.all()
            filename = "document_templates_export.json"

        data = serialize_templates(queryset)
        
        response = HttpResponse(
            json.dumps(data, indent=4, ensure_ascii=False),
            content_type='application/json'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

class TemplateImportView(LoginRequiredMixin, View):
    """Importe des templates depuis un fichier JSON"""

    def get(self, request):
        return render(request, 'documents/template_import.html')

    def post(self, request):
        if 'json_file' not in request.FILES:
            messages.error(request, "Veuillez sélectionner un fichier.")
            return redirect('pdf_editor:template-import')

        json_file = request.FILES['json_file']
        try:
            data = json.load(json_file)
            count_created, count_updated = process_template_import(data, request.user)
            messages.success(request, f"Import réussi : {count_created} créés, {count_updated} mis à jour.")
            return redirect('pdf_editor:template-list')
        except json.JSONDecodeError:
            messages.error(request, "Fichier JSON invalide.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {str(e)}")
            
        return redirect('pdf_editor:template-import')


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

        # Filtrer par statut
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .variables import get_variables_for_type
        context['template_variables'] = get_variables_for_type(self.object.template_type)
        return context


class TemplateCreateBasicView(LoginRequiredMixin, CreateView):
    """Crée un nouveau template - étape 1: informations de base"""

    model = DocumentTemplate
    form_class = DocumentTemplateBasicForm
    template_name = 'documents/template_basic_form.html'
    success_url = reverse_lazy('pdf_editor:template-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=self.request.user,
            action_type='CREATE',
            target_model='DocumentTemplate',
            target_id=str(self.object.id),
            details=f"Création (base) du template PDF: {self.object.title}",
            ip_address=self.request.META.get('REMOTE_ADDR')
        )

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
        response = super().form_valid(form)
        
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=self.request.user,
            action_type='CREATE',
            target_model='DocumentTemplate',
            target_id=str(self.object.id),
            details=f"Création complète du template PDF: {self.object.title}",
            ip_address=self.request.META.get('REMOTE_ADDR')
        )
        
        return response


class TemplateUpdateView(LoginRequiredMixin, UpdateView):
    """Met à jour un template existant"""

    model = DocumentTemplate
    form_class = DocumentTemplateForm
    template_name = 'documents/template_form.html'
    slug_field = 'slug'
    success_url = reverse_lazy('pdf_editor:template-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .variables import get_variables_for_type
        context['template_variables'] = get_variables_for_type(self.object.template_type)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=self.request.user,
            action_type='UPDATE',
            target_model='DocumentTemplate',
            target_id=str(self.object.id),
            details=f"Mise à jour du template PDF: {self.object.title}",
            ip_address=self.request.META.get('REMOTE_ADDR')
        )
        
        return response


class TemplateDeleteView(LoginRequiredMixin, DeleteView):
    """Supprime un template"""

    model = DocumentTemplate
    template_name = 'documents/template_confirm_delete.html'
    slug_field = 'slug'
    success_url = reverse_lazy('pdf_editor:template-list')

    def form_valid(self, form):
        # Pour Django 4+ où delete() utilise form_valid
        obj = self.get_object()
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=self.request.user,
            action_type='DELETE',
            target_model='DocumentTemplate',
            target_id=str(obj.id),
            details=f"Suppression du template PDF: {obj.title}",
            ip_address=self.request.META.get('REMOTE_ADDR')
        )
        return super().form_valid(form)

    def delete(self, request, *args, **kwargs):
        # Pour compatibilité avec les anciennes versions de Django
        obj = self.get_object()
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=self.request.user,
            action_type='DELETE',
            target_model='DocumentTemplate',
            target_id=str(obj.id),
            details=f"Suppression du template PDF: {obj.title}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        return super().delete(request, *args, **kwargs)


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
            # Préparer les données de contexte avec Mock
            from .utils import get_mock_context_for_type
            context_data = get_mock_context_for_type(template_obj.template_type)
            
            # Surcharger avec les données du formulaire si fournies
            if form.cleaned_data.get('recipient_name'):
                context_data['recipient_name'] = form.cleaned_data.get('recipient_name')
            if form.cleaned_data.get('recipient_email'):
                context_data['recipient_email'] = form.cleaned_data.get('recipient_email')
            if form.cleaned_data.get('document_date'):
                context_data['document_date'] = form.cleaned_data.get('document_date').strftime("%d/%m/%Y")
            
            # Rendre le template Django
            try:
                from .utils import render_template_with_context
                rendered_content, error = render_template_with_context(template_obj.content, context_data)
                
                if error:
                    form.add_error(None, f"Erreur lors du rendu: {error}")
                    return render(request, 'documents/generate_document.html', {'template': template_obj, 'form': form})
                
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
            from django.template.loader import render_to_string
            from django.conf import settings
            
            entreprise = None
            if hasattr(request, 'tenant'):
                entreprise = request.tenant

            context = {
                'document': document,
                'entreprise': entreprise,
            }
            html_content = render_to_string('documents/pdf_base.html', context)

            # Convertir les URLs des médias pour WeasyPrint (car runserver bloque sur les requêtes HTTP locales)
            media_url = request.build_absolute_uri(settings.MEDIA_URL)
            media_root_uri = 'file:///' + str(settings.MEDIA_ROOT).replace('\\', '/') + '/'
            html_content = html_content.replace(media_url, media_root_uri)

            pdf_file = BytesIO()

            # Créer le PDF avec le contenu HTML et les styles
            HTML(string=html_content, base_url=request.build_absolute_uri('/')).write_pdf(pdf_file)
            pdf_file.seek(0)

            # Déterminer le nom du fichier en fonction du contexte
            filename = f"document_{document.pk}.pdf"
            if document.context_data:
                if 'devis_numero' in document.context_data:
                    filename = f"Devis_{document.context_data['devis_numero']}.pdf"
                elif 'num_facture' in document.context_data:
                    filename = f"Facture_{document.context_data['num_facture']}.pdf"
                elif 'reference' in document.context_data:
                    filename = f"Document_{document.context_data['reference']}.pdf"

            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except ImportError:
            # Si weasyprint n'est pas installé, retourner HTML à imprimer
            return redirect('pdf_editor:document-preview', pk=document.pk)


class DocumentPrintView(LoginRequiredMixin, View):
    """Affiche le document en mode impression"""

    def get(self, request, pk):
        document = get_object_or_404(DocumentGeneration, pk=pk)

        return render(request, 'documents/document_print.html', {
            'document': document,
            'rendered_html': document.rendered_content,
            
        })