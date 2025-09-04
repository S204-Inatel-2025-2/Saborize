from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login, logout
from .forms import CriacaoUser


# Create your views here.

def paginaLogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get("senha")
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Usuario não existe')
            
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