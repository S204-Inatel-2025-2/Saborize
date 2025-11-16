from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.template.context_processors import csrf
import json

from .forms import ReceitaForm as CriarReceita
from .models import Receita, Comentario, Avaliacao, Seguidor
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
def editar_receita(request, receita_id):
    """
    View para editar uma receita (apenas o próprio autor pode editar)
    """
    receita = get_object_or_404(Receita, id=receita_id, user=request.user)
    
    if request.method == 'POST':
        form = CriarReceita(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receita atualizada com sucesso!')
            return redirect('listar_receitas')
    else:
        form = CriarReceita(instance=receita)
    
    context = {
        'form': form,
        'receita': receita,
        'editing': True
    }
    return render(request, 'receitas/criar_receita.html', context)


@login_required
@require_http_methods(["POST"])
def deletar_receita(request, receita_id):
    """
    View para deletar uma receita (apenas o próprio autor pode deletar)
    """
    receita = get_object_or_404(Receita, id=receita_id, user=request.user)
    
    titulo = receita.titulo
    receita.delete()
    
    messages.success(request, f'Receita "{titulo}" foi deletada com sucesso!')
    return redirect('listar_receitas')


@login_required
def confirmar_deletar_receita(request, receita_id):
    """
    View para mostrar página de confirmação antes de deletar
    """
    receita = get_object_or_404(Receita, id=receita_id, user=request.user)
    return render(request, 'receitas/confirmar_deletar.html', {'receita': receita})


@login_required
def listar_receitas(request):
    receitas = Receita.objects.filter(user=request.user).prefetch_related('avaliacoes__usuario', 'comentarios').order_by('-criada_em')
    return render(request, 'receitas/listar_receitas.html', {'receitas': receitas})


def ver_receita(request, receita_id):
    receita = get_object_or_404(Receita.objects.prefetch_related('avaliacoes__usuario', 'comentarios'), id=receita_id)
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
    
    # Adicionar token CSRF ao context
    context.update(csrf(request))
    
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


# =============================================================================
# SISTEMA DE AVALIAÇÕES
# =============================================================================

@login_required
@require_http_methods(["POST"])
def avaliar_receita(request, receita_id):
    """
    API para avaliar uma receita (1-5 estrelas)
    """
    try:
        receita = get_object_or_404(Receita, id=receita_id)
        
        # Parse do JSON
        data = json.loads(request.body)
        nota = data.get('nota')
        
        # Validação
        if not nota or not isinstance(nota, int) or nota < 1 or nota > 5:
            return JsonResponse({
                'success': False,
                'error': 'Nota deve ser um número inteiro entre 1 e 5'
            }, status=400)
        
        # Não permitir autoavaliação
        if receita.user == request.user:
            return JsonResponse({
                'success': False,
                'error': 'Você não pode avaliar sua própria receita'
            }, status=400)
        
        # Criar ou atualizar avaliação
        avaliacao, created = Avaliacao.objects.update_or_create(
            receita=receita,
            usuario=request.user,
            defaults={'nota': nota}
        )
        
        action = 'criada' if created else 'atualizada'
        
        return JsonResponse({
            'success': True,
            'message': f'Avaliação {action} com sucesso!',
            'avaliacao': {
                'nota': avaliacao.nota,
                'created': created
            },
            'receita_stats': {
                'total_avaliacoes': receita.total_avaliacoes,
                'media_avaliacoes': receita.media_avaliacoes
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Dados JSON inválidos'
        }, status=400)
    except Exception as e:
        import traceback
        print(f"Erro ao avaliar receita: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def listar_avaliacoes(request, receita_id):
    """
    API para listar todas as avaliações de uma receita
    """
    try:
        receita = get_object_or_404(Receita, id=receita_id)
        avaliacoes = receita.avaliacoes.all()
        
        # Verifica se o usuário atual já avaliou
        user_avaliacao = None
        if request.user.is_authenticated:
            try:
                user_avaliacao = avaliacoes.get(usuario=request.user)
            except Avaliacao.DoesNotExist:
                pass
        
        avaliacoes_list = []
        for avaliacao in avaliacoes:
            avaliacoes_list.append({
                'id': avaliacao.id,
                'usuario': avaliacao.usuario.username,
                'nota': avaliacao.nota,
                'criada_em': avaliacao.criada_em.strftime('%d/%m/%Y %H:%M'),
                'atualizada_em': avaliacao.atualizada_em.strftime('%d/%m/%Y %H:%M') if avaliacao.atualizada_em != avaliacao.criada_em else None
            })
        
        return JsonResponse({
            'success': True,
            'receita': {
                'id': receita.id,
                'titulo': receita.titulo,
                'total_avaliacoes': receita.total_avaliacoes,
                'media_avaliacoes': receita.media_avaliacoes
            },
            'avaliacoes': avaliacoes_list,
            'user_avaliacao': {
                'nota': user_avaliacao.nota if user_avaliacao else None,
                'criada_em': user_avaliacao.criada_em.strftime('%d/%m/%Y %H:%M') if user_avaliacao else None
            } if request.user.is_authenticated else None
        })
        
    except Exception as e:
        import traceback
        print(f"Erro ao listar avaliações: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["DELETE"])
def remover_avaliacao(request, receita_id):
    """
    API para remover a avaliação do usuário de uma receita
    """
    try:
        receita = get_object_or_404(Receita, id=receita_id)
        
        try:
            avaliacao = Avaliacao.objects.get(receita=receita, usuario=request.user)
            avaliacao.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Avaliação removida com sucesso!',
                'receita_stats': {
                    'total_avaliacoes': receita.total_avaliacoes,
                    'media_avaliacoes': receita.media_avaliacoes
                }
            })
            
        except Avaliacao.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Você não avaliou esta receita'
            }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Erro interno do servidor'
        }, status=500)


# =============================================================================
# SISTEMA DE SEGUIR USUÁRIOS
# =============================================================================

@login_required
@require_http_methods(["POST"])
def seguir_usuario(request, user_id):
    """
    API para seguir um usuário
    """
    try:
        usuario_a_seguir = get_object_or_404(User, id=user_id)
        
        # Não permitir seguir a si mesmo
        if usuario_a_seguir == request.user:
            return JsonResponse({
                'success': False,
                'error': 'Você não pode seguir a si mesmo'
            }, status=400)
        
        # Criar ou verificar se já segue
        seguidor, created = Seguidor.objects.get_or_create(
            seguidor=request.user,
            seguido=usuario_a_seguir
        )
        
        if created:
            return JsonResponse({
                'success': True,
                'message': f'Você agora está seguindo {usuario_a_seguir.username}!',
                'action': 'seguindo'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': f'Você já está seguindo {usuario_a_seguir.username}'
            }, status=400)
            
    except Exception as e:
        import traceback
        print(f"Erro ao seguir usuário: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["POST"])
def parar_de_seguir(request, user_id):
    """
    API para parar de seguir um usuário
    """
    try:
        usuario_seguido = get_object_or_404(User, id=user_id)
        
        try:
            seguidor = Seguidor.objects.get(
                seguidor=request.user,
                seguido=usuario_seguido
            )
            seguidor.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Você parou de seguir {usuario_seguido.username}',
                'action': 'nao_seguindo'
            })
            
        except Seguidor.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Você não está seguindo {usuario_seguido.username}'
            }, status=404)
        
    except Exception as e:
        import traceback
        print(f"Erro ao parar de seguir usuário: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        }, status=500)


@login_required
def feed_seguidos(request):
    """
    Feed de receitas apenas dos usuários que o usuário atual segue
    """
    # Buscar IDs dos usuários que o usuário atual segue
    usuarios_seguidos_ids = Seguidor.objects.filter(
        seguidor=request.user
    ).values_list('seguido_id', flat=True)
    
    # Buscar receitas públicas apenas dos usuários seguidos
    receitas = Receita.objects.filter(
        user_id__in=usuarios_seguidos_ids,
        publica=True
    ).select_related('user').prefetch_related(
        'avaliacoes', 'comentarios'
    ).order_by('-criada_em')
    
    # Buscar informações dos usuários seguidos para o template
    usuarios_seguidos = User.objects.filter(id__in=usuarios_seguidos_ids)
    
    context = {
        'receitas': receitas,
        'usuarios_seguidos': usuarios_seguidos,
        'total_seguindo': len(usuarios_seguidos_ids)
    }
    
    return render(request, 'receitas/feed_seguidos.html', context)


@login_required  
def listar_usuarios(request):
    """
    Lista todos os usuários para poder seguir
    """
    from django.db import models
    
    # Buscar usuários que o usuário atual já segue
    usuarios_seguindo_ids = Seguidor.objects.filter(
        seguidor=request.user
    ).values_list('seguido_id', flat=True)
    
    # Buscar todos os usuários exceto o próprio usuário
    usuarios = User.objects.exclude(id=request.user.id).annotate(
        total_receitas=models.Count('receitas', filter=models.Q(receitas__publica=True)),
        total_seguidores=models.Count('seguidores')
    ).order_by('-total_receitas')
    
    # Adicionar informação se já está seguindo cada usuário
    for usuario in usuarios:
        usuario.ja_seguindo = usuario.id in usuarios_seguindo_ids
    
    context = {
        'usuarios': usuarios,
        'total_seguindo': len(usuarios_seguindo_ids)
    }
    
    return render(request, 'receitas/listar_usuarios.html', context)