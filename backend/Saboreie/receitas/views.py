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


@login_required
def fazer_comentario(request, receita_id):
    """
    View para a página de fazer comentário em uma receita (requer login)
    """
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


# ================================
# SISTEMA DE FEED PÚBLICO
# ================================

def feed_receitas(request):
    """
    Feed público de receitas - acessível para todos (logados e não logados)
    """
    from django.core.paginator import Paginator
    from django.db.models import Q
    
    # Buscar receitas públicas
    receitas = Receita.objects.filter(publica=True).select_related('user').prefetch_related('comentarios')
    
    # Filtros de busca
    busca = request.GET.get('busca', '').strip()
    ordenacao = request.GET.get('ordem', 'recentes')  # recentes, populares
    
    if busca:
        receitas = receitas.filter(
            Q(titulo__icontains=busca) | 
            Q(descricao__icontains=busca) |
            Q(ingredientes__icontains=busca)
        )
    
    # Aplicar ordenação
    if ordenacao == 'populares':
        # Ordenar por quantidade de comentários
        receitas = receitas.order_by('-comentarios__criado_em').distinct()
    else:  # recentes (padrão)
        receitas = receitas.order_by('-criada_em')
    
    # Paginação
    paginator = Paginator(receitas, 10)  # 10 receitas por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'receitas': page_obj,
        'busca': busca,
        'ordenacao': ordenacao,
        'total_receitas': paginator.count,
        'opcoes_ordenacao': [
            ('recentes', 'Mais Recentes'),
            ('populares', 'Mais Populares'),
        ]
    }
    
    return render(request, 'receitas/feed.html', context)


def ver_receita_feed(request, receita_id):
    """
    View para ver receita individual do feed (acessível para todos)
    """
    receita = get_object_or_404(Receita, id=receita_id, publica=True)
    comentarios = receita.comentarios.all()
    
    context = {
        'receita': receita,
        'comentarios': comentarios,
        'total_comentarios': comentarios.count(),
        'from_feed': True  # Flag para indicar que veio do feed
    }
    
    return render(request, 'receitas/receita_feed.html', context)


@require_http_methods(["GET"])
def api_feed_receitas(request):
    """
    API REST para obter feed de receitas (acessível para todos)
    """
    from django.core.paginator import Paginator
    from django.db.models import Q
    
    try:
        # Parâmetros da API
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 10)), 50)  # Máximo 50 por página
        busca = request.GET.get('busca', '').strip()
        ordenacao = request.GET.get('ordem', 'recentes')
        
        # Buscar receitas públicas
        receitas = Receita.objects.filter(publica=True).select_related('user')
        
        # Filtro de busca
        if busca:
            receitas = receitas.filter(
                Q(titulo__icontains=busca) | 
                Q(descricao__icontains=busca) |
                Q(ingredientes__icontains=busca)
            )
        
        # Ordenação
        if ordenacao == 'populares':
            receitas = receitas.order_by('-comentarios__criado_em').distinct()
        else:  # recentes
            receitas = receitas.order_by('-criada_em')
        
        # Paginação
        paginator = Paginator(receitas, limit)
        page_obj = paginator.get_page(page)
        
        # Serializar dados
        receitas_data = []
        for receita in page_obj:
            receitas_data.append({
                'id': receita.id,
                'titulo': receita.titulo,
                'descricao': receita.descricao[:200] + '...' if len(receita.descricao) > 200 else receita.descricao,
                'criada_em': receita.criada_em.isoformat(),
                'autor': {
                    'id': receita.user.id,
                    'username': receita.user.username
                },
                'total_comentarios': receita.total_comentarios,
                'urls': {
                    'detalhes': f'/receitas/feed/ver/{receita.id}/',
                    'api_comentarios': f'/receitas/api/comentarios/{receita.id}/',
                }
            })
        
        return JsonResponse({
            'success': True,
            'receitas': receitas_data,
            'paginacao': {
                'page_atual': page_obj.number,
                'total_paginas': paginator.num_pages,
                'total_receitas': paginator.count,
                'tem_anterior': page_obj.has_previous(),
                'tem_proximo': page_obj.has_next(),
                'proxima_pagina': page_obj.next_page_number() if page_obj.has_next() else None,
                'pagina_anterior': page_obj.previous_page_number() if page_obj.has_previous() else None
            },
            'filtros': {
                'busca': busca,
                'ordenacao': ordenacao,
                'user_authenticated': request.user.is_authenticated
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Erro interno do servidor'
        }, status=500)