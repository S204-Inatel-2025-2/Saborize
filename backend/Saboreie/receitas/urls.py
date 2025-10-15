from django.urls import path
from . import views
 
urlpatterns = [
    # URLs principais das receitas (requer login)
    path('minhas/', views.listar_receitas, name='listar_receitas'),
    path('criar/', views.criar_receita, name='criar_receita'),
    
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
    
    # API do feed (acessível para todos)
    path('api/feed/', views.api_feed_receitas, name='api_feed_receitas'),
]