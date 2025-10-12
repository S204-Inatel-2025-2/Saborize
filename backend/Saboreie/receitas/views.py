from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json

from .forms import ReceitaForm as CriarReceita
from .models import Receita, Comentario
from autenticacao.models import User


@login_required
def criar_receita(request):
    form = CriarReceita() 
    if request.method == 'POST':
        form = CriarReceita(request.POST)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.user = request.user
            receita.save()  
            messages.success(request, 'Receita criada com sucesso!')
            return redirect('home')
    return render(request, 'receitas/criar_receita.html', {'form': form})


@login_required
def listar_receitas(request):
    receitas = Receita.objects.filter(user=request.user)
    return render(request, 'receitas/listar_receitas.html', {'receitas': receitas})


def ver_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    comentarios = receita.comentarios.all()
    
    context = {
        'receita': receita,
        'comentarios': comentarios,
        'total_comentarios': comentarios.count()
    }
    
    return render(request, 'receitas/receita_simples.html', context)


def fazer_comentario(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    comentarios = receita.comentarios.all()
    
    context = {
        'receita': receita,
        'comentarios': comentarios,
        'total_comentarios': comentarios.count()
    }
    
    return render(request, 'receitas/comentarios.html', context)


def comentarios_receita(request, receita_id):
    """
    View simples para mostrar uma receita com seus comentários
    """
    receita = get_object_or_404(Receita, id=receita_id)
    comentarios = receita.comentarios.all()
    
    context = {
        'receita': receita,
        'comentarios': comentarios,
        'total_comentarios': comentarios.count()
    }
    
    return render(request, 'receitas/receita_simples.html', context)


#aq fica a parte dos comentarios

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def criar_comentario(request, receita_id):
    try:
        receita = get_object_or_404(Receita, id=receita_id)
        
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            texto = data.get('texto', '').strip()
        else:
            texto = request.POST.get('texto', '').strip()
        
        if not texto:
            return JsonResponse({
                'success': False,
                'error': 'Texto do comentário é obrigatório'
            }, status=400)
        
        if len(texto) > 500:
            return JsonResponse({
                'success': False,
                'error': 'Comentário muito longo (máximo 500 caracteres)'
            }, status=400)
        
        comentario = Comentario.objects.create(
            receita=receita,
            usuario=request.user,
            texto=texto
        )
        
        return JsonResponse({
            'success': True,
            'comentario': {
                'id': comentario.id,
                'texto': comentario.texto,
                'usuario': comentario.usuario.username,
                'criado_em': comentario.criado_em.isoformat(),
                'pode_editar': True
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Erro interno do servidor'
        }, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
@login_required
def editar_comentario(request, comentario_id):
    try:
        comentario = get_object_or_404(Comentario, id=comentario_id)
        
        # Verifica se o usuário pode editar (apenas o autor)
        if comentario.usuario != request.user:
            return JsonResponse({
                'success': False,
                'error': 'Você não tem permissão para editar este comentário'
            }, status=403)
        
        data = json.loads(request.body)
        novo_texto = data.get('texto', '').strip()
        
        if not novo_texto:
            return JsonResponse({
                'success': False,
                'error': 'Texto do comentário é obrigatório'
            }, status=400)
        
        if len(novo_texto) > 500:
            return JsonResponse({
                'success': False,
                'error': 'Comentário muito longo (máximo 500 caracteres)'
            }, status=400)
        
        comentario.texto = novo_texto
        comentario.save()
        
        return JsonResponse({
            'success': True,
            'comentario': {
                'id': comentario.id,
                'texto': comentario.texto,
                'usuario': comentario.usuario.username,
                'criado_em': comentario.criado_em.isoformat(),
                'atualizado_em': comentario.atualizado_em.isoformat(),
                'editado': True
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Erro interno do servidor'
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
@login_required
def deletar_comentario(request, comentario_id):
    try:
        comentario = get_object_or_404(Comentario, id=comentario_id)
        
        # Verifica se o usuário pode deletar (autor do comentário ou autor da receita)
        if comentario.usuario != request.user and comentario.receita.user != request.user:
            return JsonResponse({
                'success': False,
                'error': 'Você não tem permissão para deletar este comentário'
            }, status=403)
        
        comentario.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Comentário deletado com sucesso'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Erro interno do servidor'
        }, status=500)


@require_http_methods(["GET"])
def listar_comentarios(request, receita_id):
    try:
        receita = get_object_or_404(Receita, id=receita_id)
        comentarios = receita.comentarios.all()
        
        comentarios_data = []
        for comentario in comentarios:
            pode_editar = request.user.is_authenticated and (
                comentario.usuario == request.user or receita.user == request.user
            )
            
            comentarios_data.append({
                'id': comentario.id,
                'texto': comentario.texto,
                'usuario': comentario.usuario.username,
                'criado_em': comentario.criado_em.isoformat(),
                'atualizado_em': comentario.atualizado_em.isoformat() if comentario.atualizado_em != comentario.criado_em else None,
                'pode_editar': pode_editar,
                'editado': comentario.atualizado_em != comentario.criado_em
            })
        
        return JsonResponse({
            'success': True,
            'comentarios': comentarios_data,
            'total': len(comentarios_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Erro interno do servidor'
        }, status=500)