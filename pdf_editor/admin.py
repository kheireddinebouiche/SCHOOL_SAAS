from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import render
from django.contrib import messages
from django import forms
import json

from .models import DocumentTemplate, DocumentGeneration
from .utils import serialize_templates, process_template_import

# Action d'exportation
@admin.action(description='Exporter les templates sélectionnés en JSON')
def export_templates_to_json(modeladmin, request, queryset):
    templates_data = serialize_templates(queryset)
    
    response = HttpResponse(
        json.dumps(templates_data, indent=4, ensure_ascii=False),
        content_type='application/json'
    )
    response['Content-Disposition'] = 'attachment; filename="document_templates_export.json"'
    return response

# Formulaire d'importation simple
class JsonImportForm(forms.Form):
    json_file = forms.FileField(label='Fichier JSON')

@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'template_type', 'slug', 'is_active', 'usage_count', 'updated_at')
    list_filter = ('template_type', 'is_active', 'created_at')
    search_fields = ('title', 'slug', 'description')
    readonly_fields = ('usage_count', 'created_by', 'updated_at')
    actions = [export_templates_to_json]
    
    # Configuration du template personnalisé pour la liste
    change_list_template = "admin/pdf_editor/documenttemplate/change_list.html"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-templates/', self.admin_site.admin_view(self.import_templates_view), name='pdf_editor_import_templates'),
        ]
        return custom_urls + urls

    def import_templates_view(self, request):
        if request.method == 'POST':
            form = JsonImportForm(request.POST, request.FILES)
            if form.is_valid():
                json_file = request.FILES['json_file']
                try:
                    data = json.load(json_file)
                    count_created, count_updated = process_template_import(data, request.user)
                            
                    self.message_user(request, f"Import terminé : {count_created} créés, {count_updated} mis à jour.")
                    return HttpResponseRedirect(reverse('admin:pdf_editor_documenttemplate_changelist'))
                    
                except json.JSONDecodeError:
                    self.message_user(request, "Erreur de format JSON.", level=messages.ERROR)
                except Exception as e:
                    self.message_user(request, f"Erreur lors de l'import : {str(e)}", level=messages.ERROR)
        else:
            form = JsonImportForm()

        context = {
            'title': 'Importer des Templates',
            'form': form,
            'opts': self.model._meta,
            **self.admin_site.each_context(request),
        }
        return render(request, "admin/pdf_editor/documenttemplate/import_form.html", context)

@admin.register(DocumentGeneration)
class DocumentGenerationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'template', 'created_at', 'generated_by')
    list_filter = ('template', 'created_at')
    readonly_fields = ('created_at', 'generated_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.generated_by = request.user
        super().save_model(request, obj, form, change)
