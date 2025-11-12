from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import os

# Create your models here.

class TagsReceita(models.Model):
    """Modelo para tags de tipos de receitas"""
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.CharField(max_length=200, blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Tag de Receita'
        verbose_name_plural = 'Tags de Receitas'
    
    def __str__(self):
        return self.nome


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biografia")
    foto_perfil = models.ImageField(upload_to='perfil/', default='perfil/default.jpg', blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    tags_favoritas = models.ManyToManyField(
        TagsReceita, 
        blank=True, 
        related_name='usuarios_favoritos',
        verbose_name="Tipos de receitas favoritas"
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Redimensionar a imagem de perfil se ela for muito grande
        if self.foto_perfil and hasattr(self.foto_perfil, 'path'):
            try:
                img = Image.open(self.foto_perfil.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.foto_perfil.path)
            except Exception:
                pass  # Se houver erro ao redimensionar, apenas continue
    
    @property
    def total_seguidores(self):
        """Retorna o número de seguidores"""
        return self.seguidores.count()
    
    @property 
    def total_seguindo(self):
        """Retorna o número de usuários que este usuário segue"""
        return self.seguindo.count()
        
    @property
    def total_receitas(self):
        """Retorna o número total de receitas do usuário"""
        return self.receitas.count()
    
    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"