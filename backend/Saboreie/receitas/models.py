from django.db import models
from autenticacao.models import User

class Receita(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receitas')
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
    publica = models.BooleanField(default=True, help_text="Receita visível no feed público")
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criada_em']
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'

    def __str__(self):
        return f"{self.titulo} - {self.user.username}"

    @property
    def total_comentarios(self):
        return self.comentarios.count()


class Comentario(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField(max_length=500)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return f"Comentário de {self.usuario.username} em {self.receita.titulo}"