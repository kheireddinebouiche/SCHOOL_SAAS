from django import forms
from .models import GlobalPaymentCategory, GlobalDepensesCategory

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
