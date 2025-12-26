from django.db import models
from django.contrib.auth.models import User

class DocumentTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    html_content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    page_size = models.CharField(max_length=20, default='A4')
    page_orientation = models.CharField(max_length=20, default='portrait')
    variables = models.JSONField(default=dict, blank=True)
    config = models.JSONField(default=dict, blank=True)  # Configuration supplémentaire (marges, etc.)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name

class GeneratedDocument(models.Model):
    template = models.ForeignKey(DocumentTemplate, on_delete=models.CASCADE, related_name='documents')
    data = models.JSONField()
    pdf_file = models.FileField(upload_to='pdfs/')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.template.name} - {self.created_at:%Y-%m-%d}"
