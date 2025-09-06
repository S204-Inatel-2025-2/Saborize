from django.db import models
from autenticacao.models import User

class Receita(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    descricao = models.TextField( 
        help_text="Descreva a receita em detalhes, incluindo ingredientes e modo de preparo."
    )
    ingredientes = models.TextField(
        help_text="Liste os ingredientes necessários para a receita."
    )
    passos = models.TextField(
        help_text="Descreva os passos para preparar a receita."
    )

    criada_em = models.DateTimeField(auto_now_add=True) # Data e hora em que a receita foi criada













# Create your models here.

