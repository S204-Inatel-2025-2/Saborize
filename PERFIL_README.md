# Sistema de Perfil de Usuário - Saborize

## 📋 Funcionalidades Implementadas

### 🔧 Backend Completo

#### 1. **Modelo de Usuário Estendido** (`autenticacao/models.py`)
- **Informações Pessoais:**
  - Biografia (500 caracteres)
  - Telefone
  - Data de nascimento
  - Cidade e Estado
  - Datas de criação e atualização

- **Foto de Perfil:**
  - Upload de imagens para pasta `media/perfil/`
  - Redimensionamento automático (300x300px) usando Pillow
  - Imagem padrão quando não há upload

- **Tags Favoritas:**
  - Sistema de tags para tipos de receitas preferidas
  - Relacionamento many-to-many com `TagsReceita`

- **Estatísticas do Perfil:**
  - Contador de receitas
  - Contador de seguidores
  - Contador de usuários seguindo

#### 2. **Modelo de Tags** (`autenticacao/models.py`)
- Sistema de categorização de tipos de receita
- 20 tags pré-criadas (doce, salgado, vegana, italiana, etc.)
- Interface administrativa para gerenciar tags

#### 3. **Formulários** (`autenticacao/forms.py`)
- `PerfilForm`: Formulário completo para edição de perfil
- Validação de email único
- Widgets Bootstrap estilizados
- Suporte a upload de arquivos

#### 4. **Views** (`autenticacao/views.py`)
- `perfil(username=None)`: Visualização de perfil (próprio ou de outros)
- `editar_perfil()`: Edição completa do perfil
- Proteção com `@login_required`
- Mensagens de feedback para o usuário

#### 5. **URLs** (`autenticacao/urls.py`)
```python
path('perfil/', views.perfil, name="perfil")
path('perfil/<str:username>/', views.perfil, name="perfil_usuario")
path('editar-perfil/', views.editar_perfil, name="editar_perfil")
```

#### 6. **Configurações** (`settings.py`)
- Configuração de arquivos de mídia (`MEDIA_URL`, `MEDIA_ROOT`)
- Servir arquivos estáticos em desenvolvimento

#### 7. **Admin Interface** (`autenticacao/admin.py`)
- Interface personalizada para gerenciar usuários
- Gestão de tags de receitas
- Filtros e campos de busca

### 🎨 Templates Responsivos

#### 1. **Página de Perfil** (`autenticacao/perfil.html`)
**Seções principais:**
- **Header do Perfil:**
  - Foto de perfil circular (150x150px)
  - Nome completo ou username
  - Biografia
  - Estatísticas (receitas, seguidores, seguindo)
  - Botão "Editar Perfil" (perfil próprio)

- **Informações Detalhadas:**
  - Localização (cidade/estado)
  - Email, telefone, data nascimento (apenas perfil próprio)
  - Tags favoritas com badges coloridas

- **Grade de Receitas:**
  - Últimas 6 receitas do usuário
  - Cards estilizados com avaliações
  - Link para ver todas as receitas
  - Estado vazio com call-to-action

#### 2. **Página de Edição** (`autenticacao/editar_perfil.html`)
**Funcionalidades:**
- Preview da foto atual
- Formulário organizado em seções
- Upload de nova foto
- Seleção múltipla de tags favoritas
- Informações de privacidade
- Validação e mensagens de erro
- Botões de ação (salvar/cancelar)

### 📱 Design Responsivo
- Layout Bootstrap 5
- Tema consistente (preto/amarelo)
- Cards com sombras e bordas arredondadas
- Ícones Bootstrap Icons
- Responsivo para mobile/desktop

### 🗄️ Banco de Dados

#### Migrações Criadas:
```
autenticacao/migrations/0002_tagsreceita_user_atualizado_em_user_bio_user_cidade_and_more.py
```

#### Tags Pré-criadas (20 tipos):
- doce, salgado, vegana, vegetariana, fitness
- brasileira, italiana, japonesa, mexicana, árabe, francesa
- fast food, bebidas, low carb, sem glúten
- massa, churrasco, frutos do mar
- café da manhã, lanche

### 🔐 Segurança e Validação
- Verificação de propriedade do perfil
- Validação de email único
- Upload seguro de imagens
- Redimensionamento automático para performance
- Proteção CSRF nos formulários

### 🚀 Como Testar

1. **Executar o servidor:**
   ```bash
   cd backend/Saboreie
   python manage.py runserver
   ```

2. **Acessar URLs:**
   - `/perfil/` - Meu perfil
   - `/perfil/username/` - Perfil de outro usuário
   - `/editar-perfil/` - Editar meu perfil
   - `/admin/` - Gerenciar tags (admin:admin123)

3. **Funcionalidades para testar:**
   - Criar/editar perfil completo
   - Upload de foto de perfil
   - Seleção de tags favoritas
   - Visualização de perfis de outros usuários
   - Responsividade mobile

### 📁 Estrutura de Arquivos
```
backend/Saboreie/
├── autenticacao/
│   ├── models.py          # User e TagsReceita
│   ├── forms.py           # PerfilForm
│   ├── views.py           # perfil, editar_perfil
│   ├── urls.py            # URLs do perfil
│   ├── admin.py           # Interface admin
│   └── templates/autenticacao/
│       ├── perfil.html
│       └── editar_perfil.html
├── media/
│   └── perfil/            # Fotos de perfil
└── Saboreie/
    ├── settings.py        # Configuração de mídia
    └── urls.py            # URLs principais
```

### 🎯 Próximos Passos Sugeridos
1. Sistema de seguir/deixar de seguir usuários
2. Feed personalizado com base em tags favoritas
3. Notificações de atividades
4. Histórico de receitas visualizadas
5. Sistema de conquistas/badges
6. Chat entre usuários

### 📋 Dependências Adicionais
- **Pillow**: Para manipulação de imagens
- **Django**: Framework principal
- **Bootstrap 5**: Framework CSS
- **Bootstrap Icons**: Ícones