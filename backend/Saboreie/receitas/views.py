from django.shortcuts import render, redirect
from .forms import ReceitaForm as CriarReceita
from django.contrib import messages
from autenticacao.models import User
from django.contrib.auth.decorators import login_required
from .models import Receita
# Create your views here.

@login_required # Garante que o usuário esteja autenticado para acessar essa view
def criar_receita(request):
    form = CriarReceita() 
     # Se o método da requisição for POST, significa que o formulário foi enviado
    if request.method == 'POST':
        form = CriarReceita(request.POST)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.user = request.user  # Atribui o usuário logado à receita
            receita.save()  
            messages.success(request, 'Receita criada com sucesso!')
            return redirect('home') # Redireciona para a página inicial ou outra página desejada
    return render(request, 'receitas/criar_receita.html', {'form': form}) # Renderiza o formulário na página criar_receita.html

# cria um comando para listar todas as receitas de um user logado
@login_required
def listar_receitas(request):
    receitas = Receita.objects.filter(user=request.user)
    return render(request, 'receitas/listar_receitas.html', {'receitas': receitas})  # Renderiza a lista de receitas na página listar_receitas.html