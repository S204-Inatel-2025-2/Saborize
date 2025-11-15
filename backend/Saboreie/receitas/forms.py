from django import forms
from .models import Receita


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['titulo', 'descricao', 'ingredientes', 'passos', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }