from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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

    @property
    def total_avaliacoes(self):
        return self.avaliacoes.count()

    @property
    def media_avaliacoes(self):
        """Calcula a média simples das avaliações"""
        avaliacoes = self.avaliacoes.all()
        if not avaliacoes:
            return 0
        return round(sum([av.nota for av in avaliacoes]) / len(avaliacoes), 1)


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


class Avaliacao(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Nota de 1 a 5 estrelas"
    )
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('receita', 'usuario')  # Um usuário só pode avaliar uma receita uma vez
        ordering = ['-criada_em']
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    def __str__(self):
        return f"{self.usuario.username} avaliou {self.receita.titulo} com {self.nota} estrelas"