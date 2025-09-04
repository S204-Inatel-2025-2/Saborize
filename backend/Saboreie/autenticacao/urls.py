from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.paginaLogin, name="paginaLogin"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
]
