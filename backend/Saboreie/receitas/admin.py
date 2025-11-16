from django.contrib import admin
from .models import Receita, Comentario, Avaliacao, Seguidor


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'user', 'publica', 'criada_em', 'total_comentarios', 'total_avaliacoes', 'media_avaliacoes']
    list_filter = ['publica', 'criada_em', 'user', 'tags']  # ← agora pode filtrar receitas por tag no admin
    search_fields = ['titulo', 'descricao', 'ingredientes']
    readonly_fields = ['criada_em', 'atualizada_em']
    list_editable = ['publica']

    # 👇 MOSTRAR CAMPO DE TAGS NO ADMIN
    filter_horizontal = ('tags',)

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'titulo', 'publica', 'tags')  # ← tags adicionadas aqui
        }),
        ('Conteúdo', {
            'fields': ('descricao', 'ingredientes', 'passos')
        }),
        ('Datas', {
            'fields': ('criada_em', 'atualizada_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['receita', 'usuario', 'texto_resumo', 'criado_em']
    list_filter = ['criado_em', 'receita__user']
    search_fields = ['texto', 'usuario__username', 'receita__titulo']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    def texto_resumo(self, obj):
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_resumo.short_description = 'Texto'


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['receita', 'usuario', 'nota', 'criada_em']
    list_filter = ['nota', 'criada_em', 'receita__user']
    search_fields = ['usuario__username', 'receita__titulo']
    readonly_fields = ['criada_em', 'atualizada_em']
    
    fieldsets = (
        ('Avaliação', {
            'fields': ('receita', 'usuario', 'nota')
        }),
        ('Datas', {
            'fields': ('criada_em', 'atualizada_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Seguidor)
class SeguidorAdmin(admin.ModelAdmin):
    list_display = ['seguidor', 'seguido', 'criado_em']
    list_filter = ['criado_em']
    search_fields = ['seguidor__username', 'seguido__username']
    readonly_fields = ['criado_em']
    
    fieldsets = (
        ('Relacionamento', {
            'fields': ('seguidor', 'seguido')
        }),
        ('Data', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )