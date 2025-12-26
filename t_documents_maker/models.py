from django.db import models
from django.contrib.auth.models import User

class DocumentTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # Change from single html_content to pages (JSON field storing array of page objects)
    pages = models.JSONField(default=list, blank=True)  # Array of page objects: [{'content': '...', 'page_size': 'A4', 'orientation': 'portrait'}, ...]
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    page_size = models.CharField(max_length=20, default='A4')  # Default page size for new pages
    page_orientation = models.CharField(max_length=20, default='portrait')  # Default orientation for new pages
    variables = models.JSONField(default=dict, blank=True)
    config = models.JSONField(default=dict, blank=True)  # Configuration supplémentaire (marges, etc.)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name

    def get_first_page_content(self):
        """Get content of the first page for backward compatibility"""
        if self.pages and len(self.pages) > 0:
            return self.pages[0].get('content', '')
        return ''

    def add_page(self, content='', page_size=None, orientation=None):
        """Add a new page to the template"""
        if page_size is None:
            page_size = self.page_size
        if orientation is None:
            orientation = self.page_orientation

        self.pages.append({
            'content': content,
            'page_size': page_size,
            'orientation': orientation
        })
        self.save()

    def update_page(self, page_index, content=None, page_size=None, orientation=None):
        """Update a specific page in the template"""
        if 0 <= page_index < len(self.pages):
            if content is not None:
                self.pages[page_index]['content'] = content
            if page_size is not None:
                self.pages[page_index]['page_size'] = page_size
            if orientation is not None:
                self.pages[page_index]['orientation'] = orientation
            self.save()

    def delete_page(self, page_index):
        """Delete a specific page from the template"""
        if 0 <= page_index < len(self.pages) and len(self.pages) > 1:  # Ensure at least one page remains
            del self.pages[page_index]
            self.save()

    def get_page_count(self):
        """Get the number of pages in the template"""
        return len(self.pages)


class GeneratedDocument(models.Model):
    template = models.ForeignKey(DocumentTemplate, on_delete=models.CASCADE, related_name='documents')
    data = models.JSONField()
    pdf_file = models.FileField(upload_to='pdfs/')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.template.name} - {self.created_at:%Y-%m-%d}"
