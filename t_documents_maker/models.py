from django.db import models
from django.contrib.auth.models import User

class DocumentTemplate(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_templates')
    layout = models.JSONField(default=dict)  # {"elements": [{"type": "text", "left": 100, "top": 50, "content": "{{nom}}"}] }
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class DocumentVariable(models.Model):
    """
    Model to store document variables that can be used in templates
    """
    # Predefined tags for document templates
    TAG_CHOICES = [
        ('formation', 'Formation'),
        ('specialite', 'Spécialité'),
        ('qualification', 'Qualification'),
        ('prix_formation', 'Prix de la formation'),
        ('annee_academique', 'Année académique'),
        ('ville', 'Ville'),
        ('date', 'Date'),
        ('institut', 'Institut'),
        ('date_naissance_etudiant', 'Date de naissance étudiant'),
        ('lieu_naissance_etudiant', 'Lieu de naissance étudiant'),
        ('adresse_etudiant', 'Adresse étudiant'),
        ('branche', 'Branche'),
    ]

    name = models.CharField(
        max_length=255,
        choices=TAG_CHOICES,
        help_text="Variable name without braces, e.g., 'formation' for {{formation}}"
    )
    label = models.CharField(max_length=255, help_text="Display label for the variable")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{{{{{self.name}}}}} - {self.label}"

    def save(self, *args, **kwargs):
        # Automatically set label if not provided
        if not self.label:
            for choice_name, choice_label in self.TAG_CHOICES:
                if choice_name == self.name:
                    self.label = choice_label
                    break
        super().save(*args, **kwargs)
