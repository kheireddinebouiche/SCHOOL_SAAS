# models.py

from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from django.utils import timezone

class DocumentTemplate(models.Model):

    """Modèle pour les templates de documents imprimables"""

    TEMPLATE_TYPES = [
        ('invoice', 'Facture'),
        ('contract', 'Contrat'),
        ('certificate', 'Certificat'),
        ('report', 'Rapport'),
        ('letter', 'Lettre'),
        ('student_info', 'Fiche Étudiant'),  # Ajout du type pour les étudiants
        ('payment_receipt', 'Reçu de Paiement'),  # Type pour les reçus de paiement
        ('payment_statement', 'Relevé de Paiement'),  # Type pour les relevés de paiement
    ]

    title = models.CharField(max_length=255, verbose_name="Titre du template")
    slug = models.SlugField(unique=True, verbose_name="URL-friendly name")
    template_type = models.CharField(
        max_length=20,
        choices=TEMPLATE_TYPES,
        verbose_name="Type de template"
    )

    # Contenu HTML éditable avec TinyMCE
    content = HTMLField(
        verbose_name="Contenu du template",
        help_text="Utilisez TinyMCE pour éditer le template"
    )

    # Variables de template Django disponibles
    description = models.TextField(
        blank=True,
        verbose_name="Description des variables disponibles"
    )

    # CSS personnalisé pour l'impression
    custom_css = models.TextField(
        blank=True,
        default='',
        verbose_name="CSS personnalisé pour impression"
    )

    # Métadonnées
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    usage_count = models.PositiveIntegerField(default=0, verbose_name="Nombre d'utilisations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='document_templates'
    )

    class Meta:
        verbose_name = "Template de Document"
        verbose_name_plural = "Templates de Documents"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_template_type_display()})"

    def increment_usage(self):
        """Incrémente le compteur d'utilisation"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])

class DocumentGeneration(models.Model):
    """Modèle pour enregistrer les documents générés"""

    template = models.ForeignKey(
        DocumentTemplate,
        on_delete=models.CASCADE,
        related_name='generated_documents'
    )

    # Données contextuelles pour le rendu
    context_data = models.JSONField(default=dict, verbose_name="Données de contexte")

    # Contenu généré
    rendered_content = models.TextField(verbose_name="Contenu rendu")

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = "Document Généré"
        verbose_name_plural = "Documents Générés"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.template.title} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
