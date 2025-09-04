from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def paginaLogin(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    
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

def home(request):
    return render(request, 'home.html')