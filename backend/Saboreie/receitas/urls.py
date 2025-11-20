from django.urls import path
from receitas.views import listar_tags
from . import views
 
urlpatterns = [
    # URLs principais das receitas (requer login)
    path('minhas/', views.listar_receitas, name='listar_receitas'),
    path('criar/', views.criar_receita, name='criar_receita'),
    path('editar/<int:receita_id>/', views.editar_receita, name='editar_receita'),
    path('deletar/<int:receita_id>/', views.deletar_receita, name='deletar_receita'),
    path('confirmar-deletar/<int:receita_id>/', views.confirmar_deletar_receita, name='confirmar_deletar_receita'),
    
    # URLs para visualizar receita e comentários (requer login)
    path('ver/<int:receita_id>/', views.ver_receita, name='ver_receita'),
    path('comentar/<int:receita_id>/', views.fazer_comentario, name='fazer_comentario'),
    
    # Feed público (acessível para todos)
    path('feed/', views.feed_receitas, name='feed_receitas'),
    path('feed/ver/<int:receita_id>/', views.ver_receita_feed, name='ver_receita_feed'),
    
    # APIs para comentários (URLs mais organizadas)
    path('api/comentarios/<int:receita_id>/', views.listar_comentarios, name='listar_comentarios'),
    path('api/comentario/criar/<int:receita_id>/', views.criar_comentario, name='api_criar_comentario'),
    path('api/comentario/editar/<int:comentario_id>/', views.editar_comentario, name='api_editar_comentario'),
    path('api/comentario/deletar/<int:comentario_id>/', views.deletar_comentario, name='api_deletar_comentario'),
    
    # APIs para avaliações (requer login para avaliar)
    path('api/avaliacoes/<int:receita_id>/', views.listar_avaliacoes, name='listar_avaliacoes'),
    path('api/avaliacao/criar/<int:receita_id>/', views.avaliar_receita, name='api_avaliar_receita'),
    path('api/avaliacao/remover/<int:receita_id>/', views.remover_avaliacao, name='api_remover_avaliacao'),
    
    # API do feed (acessível para todos)
    path('api/feed/', views.api_feed_receitas, name='api_feed_receitas'),
    
    # Sistema de seguir usuários (requer login)
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('seguidos/', views.feed_seguidos, name='feed_seguidos'),
    path('api/seguir/<int:user_id>/', views.seguir_usuario, name='seguir_usuario'),
    path('api/parar-seguir/<int:user_id>/', views.parar_de_seguir, name='parar_de_seguir'),

    # Gerador de receitas com IA (requer login)
    path('gerador-ia/', views.gerador_receitas_ai, name='gerador_receitas_ai'),

    # listar todas as tags
     path("tags/", listar_tags, name="listar_tags"),
]