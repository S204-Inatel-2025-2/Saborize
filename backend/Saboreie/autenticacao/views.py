from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, TagsReceita
from django.contrib.auth import authenticate, login, logout
from .forms import CriacaoUser, PerfilForm


# Create your views here.

def paginaLogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get("password")
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username ou senha está incorreta')
        
    return render(request, 'autenticacao/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def registrarUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CriacaoUser()
    if request.method =="POST":
        form = CriacaoUser(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Conta criada')
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'autenticacao/registrar_user.html', {'form':form})
    return render(request, 'autenticacao/registrar_user.html', {'form':form})

def home(request):
    return render(request, 'home.html')

@login_required
def perfil(request, username=None):
    """View para visualizar perfil de usuário"""
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    # Pega as últimas receitas do usuário
    receitas_recentes = user.receitas.filter(publica=True)[:6]
    
    context = {
        'perfil_usuario': user,
        'receitas_recentes': receitas_recentes,
        'is_own_profile': user == request.user,
    }
    
    return render(request, 'autenticacao/perfil.html', context)

@login_required
def editar_perfil(request):
    """View para editar perfil do usuário logado"""
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PerfilForm(instance=request.user)
    
    context = {
        'form': form,
        'tags_receitas': TagsReceita.objects.all()
    }
    
    return render(request, 'autenticacao/editar_perfil.html', context)