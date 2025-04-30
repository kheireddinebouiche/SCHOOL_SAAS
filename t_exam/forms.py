from  django import forms
from .models import *


class SessionForm(forms.ModelForm):
    class Meta:
        model = SessionExam
        fields = "__all__"
        exclude = ['created_at','updated_at','updated_by']

        widgets = {
            'code' : forms.TextInput(attrs={'class' : 'form-control'}),
            'label':forms.TextInput(attrs={'class' : 'form-control'}),
            'type_session':forms.Select(attrs={'class' : 'form-control'}),
            'date_debut':forms.DateInput(attrs={'class' : 'form-control','type' :'date'}),
            'date_fin':forms.DateInput(attrs={'class' : 'form-control','type' :'date'}),
        }