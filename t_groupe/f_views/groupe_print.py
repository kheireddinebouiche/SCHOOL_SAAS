from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import Template, Context
from django.contrib import messages
from pdf_editor.models import DocumentTemplate, DocumentGeneration
from ..utils import get_student_context
import re
import json

class GenerateBulkStudentPdf(LoginRequiredMixin, View):
    """Génère un seul document PDF contenant les fiches de plusieurs étudiants concaténées"""

    def post(self, request):
        student_ids_str = request.POST.get('student_ids')
        template_slug = request.POST.get('template_slug')

        if not student_ids_str or not template_slug:
            messages.error(request, "Veuillez sélectionner des étudiants et un modèle.")
            # On ne peut pas facilement rediriger vers la page précédente sans connaitre le groupe
            # Mais comme c'est un post depuis la page de groupe, on peut utiliser HTTP_REFERER
            return redirect(request.META.get('HTTP_REFERER', '/'))

        try:
            student_ids = json.loads(student_ids_str)
        except json.JSONDecodeError:
            messages.error(request, "Erreur dans la liste des étudiants sélectionnés.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Sélection du template
        template_obj = get_object_or_404(DocumentTemplate, slug=template_slug, is_active=True)

        full_rendered_content = ""
        
        # Préparer le contenu brut du template (remplacement pagebreak)
        # On le fait une fois pour optimiser
        raw_content = template_obj.content
        # Remplace <!-- pagebreak --> par <div class="pagebreak"></div>
        raw_content = re.sub(
            r'<!--\s*pagebreak\s*-->',
            '<div class="pagebreak"></div>',
            raw_content,
            flags=re.IGNORECASE
        )
        django_template = Template(raw_content)

        count = 0
        total_students = len(student_ids)

        for index, student_id in enumerate(student_ids):
            try:
                # Génération du contexte pour cet étudiant
                context_data = get_student_context(student_id)
                
                # Rendu du template pour cet étudiant
                rendered_part = django_template.render(Context(context_data))
                
                full_rendered_content += rendered_part
                
                # Ajout d'un saut de page entre chaque étudiant, sauf le dernier
                if index < total_students - 1:
                    full_rendered_content += '<div class="pagebreak"></div>'
                
                count += 1
            except Exception as e:
                # En cas d'erreur sur un étudiant, on log ou on ignore, mais on continue pour les autres si possible
                # Ou on ajoute un message d'erreur dans le contenu ?
                print(f"Erreur génération PDF pour étudiant {student_id}: {str(e)}")
                continue

        if count == 0:
            messages.error(request, "Aucun PDF n'a pu être généré.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Enregistrer la génération globale
        # On stocke les infos minimales de contexte ou une info générique
        meta_context = {
            'type': 'bulk_student_print',
            'student_count': count,
            'source_template': template_obj.title
        }

        try:
            doc_gen = DocumentGeneration.objects.create(
                template=template_obj,
                context_data=meta_context, 
                rendered_content=full_rendered_content,
                generated_by=request.user
            )

            # Check for AJAX/Modal request
            if request.POST.get('modal') == 'true':
                return JsonResponse({
                    'status': 'success',
                    'preview_html': full_rendered_content,
                    'custom_css': template_obj.custom_css,
                    'download_url': reverse('pdf_editor:document-export', args=[doc_gen.pk])
                })

            return redirect('pdf_editor:document-preview', pk=doc_gen.pk)

        except Exception as e:
            messages.error(request, f"Erreur lors de la sauvegarde du document: {str(e)}")
            return redirect(request.META.get('HTTP_REFERER', '/'))
