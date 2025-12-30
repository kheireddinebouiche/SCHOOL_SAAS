# forms.py

from django import forms
from django.utils.text import slugify
from tinymce.widgets import TinyMCE
from .models import DocumentTemplate

class DocumentTemplateBasicForm(forms.ModelForm):
    """Form for basic template information (step 1)"""

    class Meta:
        model = DocumentTemplate
        fields = ['title', 'slug', 'template_type', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_slug'}),
            'template_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_slug(self):
        """Ensure the slug is properly formatted"""
        slug = self.cleaned_data.get('slug')
        if slug:
            return slugify(slug)
        return slug

    def clean(self):
        """Override clean method to auto-generate slug if not provided"""
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        slug = cleaned_data.get('slug')

        # If no slug is provided, auto-generate from title
        if title and not slug:
            cleaned_data['slug'] = slugify(title)
        elif title and slug:
            # If both title and slug are provided, only auto-generate if slug is empty or default
            if not self.instance.pk or self.instance.slug != slug:
                # If it's a new instance or slug has changed, ensure it's properly formatted
                cleaned_data['slug'] = slugify(slug) if slug else slugify(title)

        return cleaned_data


class DocumentTemplateForm(forms.ModelForm):
    """Form for full template information (step 2)"""

    content = forms.CharField(
        widget=TinyMCE(
            attrs={
                'cols': 80,
                'rows': 30,
                'class': 'tinymce-editor'
            }
        ),
        label="Contenu du template",
        help_text="Éditez le template HTML avec TinyMCE. Utilisez les variables: {{ variable_name }}"
    )

    class Meta:
        model = DocumentTemplate
        fields = ['title', 'slug', 'template_type', 'content', 'description', 'custom_css', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_slug'}),
            'template_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'custom_css': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_slug(self):
        """Ensure the slug is properly formatted"""
        slug = self.cleaned_data.get('slug')
        if slug:
            return slugify(slug)
        return slug

    def clean(self):
        """Override clean method to auto-generate slug if not provided"""
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        slug = cleaned_data.get('slug')

        # If no slug is provided, auto-generate from title
        if title and not slug:
            cleaned_data['slug'] = slugify(title)
        elif title and slug:
            # If both title and slug are provided, only auto-generate if slug is empty or default
            if not self.instance.pk or self.instance.slug != slug:
                # If it's a new instance or slug has changed, ensure it's properly formatted
                cleaned_data['slug'] = slugify(slug) if slug else slugify(title)

        return cleaned_data

class DocumentGenerationForm(forms.Form):
    """Formulaire pour générer un document avec contexte personnalisé"""
    
    template = forms.ModelChoiceField(
        queryset=DocumentTemplate.objects.filter(is_active=True),
        label="Sélectionner un template",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Champs de contexte dynamiques (optionnel, peut être étendu)
    recipient_name = forms.CharField(
        required=False,
        label="Nom du destinataire",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Jean Dupont'})
    )
    recipient_email = forms.EmailField(
        required=False,
        label="Email du destinataire",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    document_date = forms.DateField(
        required=False,
        label="Date du document",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
