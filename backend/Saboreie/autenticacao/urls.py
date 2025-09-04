from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.paginaLogin, name="paginaLogin"),
    path('logout/', views.logoutUser, name="logout"),
    path('registrar/', views.registrarUser, name="registrarUser"),
    path('', views.home, name="home"),
]
