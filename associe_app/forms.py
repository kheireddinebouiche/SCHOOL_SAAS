from django import forms
from .models import GlobalPaymentCategory, GlobalDepensesCategory, PostesBudgetaire, GlobalPaymentType

class GlobalPaymentTypeForm(forms.ModelForm):
    class Meta:
        model = GlobalPaymentType
        fields = ['name', 'payment_categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_categories': forms.SelectMultiple(attrs={'class': 'form-control select2', 'multiple': 'multiple'}),
        }

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
        fields = ['label', 'type', 'order', 'description', 'parent', 'depense_categories', 'payment_categories']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select', 'id': 'poste_type'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'depense_categories': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'payment_categories': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        poste_type = cleaned_data.get('type')
        depense_cats = cleaned_data.get('depense_categories')
        payment_cats = cleaned_data.get('payment_categories')
        parent = cleaned_data.get('parent')

        if poste_type == 'depense':
            if payment_cats:
                self.add_error('payment_categories', "Un poste de dépense ne peut pas avoir de catégories de recettes.")
        elif poste_type == 'recette':
            if depense_cats:
                self.add_error('depense_categories', "Un poste de recette ne peut pas avoir de catégories de dépenses.")

        if parent and parent.type != poste_type:
            self.add_error('parent', f"Le parent doit être de même type ({poste_type}).")

        return cleaned_data
