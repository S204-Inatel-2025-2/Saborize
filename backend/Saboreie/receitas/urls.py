from django.urls import path
from . import views
 
urlpatterns = [
   path ('listar_receitas/', views.listar_receitas, name='listar_receitas'), # URL para listar as receitas do usuário logado
   path('criar_receita/', views.criar_receita, name='criar_receita'), # URL para criar uma nova receita
]