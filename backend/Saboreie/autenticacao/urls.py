from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.paginaLogin, name="paginaLogin"),
    path('logout/', views.logoutUser, name="logout"),
    path('registrar/', views.registrarUser, name="registrarUser"),

    path('perfil/', views.perfil, name="perfil"),  # Perfil do usuário logado
    path('perfil/<int:user_id>/', views.perfil_publico, name="perfil_publico"),

    path('editar-perfil/', views.editar_perfil, name="editar_perfil"),

    path('', views.home, name="home"),
]
