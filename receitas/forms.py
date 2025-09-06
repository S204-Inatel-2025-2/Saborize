#serve para criar formulários para o modelo Receita
from .models import Receita
from django.forms import ModelForm 


class ReceitaForm(ModelForm):
    class Meta: #
        model = Receita
        fields = ['titulo', 'descricao', 'ingredientes', 'passos']

        