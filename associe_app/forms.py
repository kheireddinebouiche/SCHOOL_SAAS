from django import forms
from .models import GlobalPaymentCategory, GlobalDepensesCategory, PostesBudgetaire

class GlobalPaymentCategoryForm(forms.ModelForm):
    class Meta:
        model = GlobalPaymentCategory
        fields = ['name', 'parent', 'category_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'category_type': forms.Select(attrs={'class': 'form-control'}),
        }

class GlobalDepensesCategoryForm(forms.ModelForm):
    class Meta:
        model = GlobalDepensesCategory
        fields = ['name', 'parent', 'payment_category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'payment_category': forms.Select(attrs={'class': 'form-control'}),
        }

class PostesBudgetaireForm(forms.ModelForm):
    class Meta:
        model = PostesBudgetaire
        fields = ['label', 'type', 'description', 'parent', 'depense_categories', 'payment_categories']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select', 'id': 'poste_type'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'depense_categories': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'payment_categories': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        }
