# 🍴 Saborize

**Saborize** é uma rede social gastronômica onde cada usuário pode compartilhar suas próprias receitas, descobrir novos sabores e até criar pratos únicos com a ajuda da inteligência artificial.  

---

## 🧭 Sumário
- [Descrição do Projeto](#descrição-do-projeto)
- [Objetivos](#objetivos)
- [Arquitetura e Tecnologias](#arquitetura-e-tecnologias)
- [Funcionalidades Principais](#funcionalidades-principais)
- [Testes Executados](#testes-executados)
- [Instalação e Execução](#instalação-e-execução)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Melhorias Futuras](#melhorias-futuras)
- [Equipe de Desenvolvimento](#equipe-de-desenvolvimento)

---

## 📘 Descrição do Projeto

O **Saborize** é uma plataforma social voltada para a culinária.  
Cada usuário pode:
- Criar e publicar receitas com descrição, ingredientes e modo de preparo;  
- Seguir outros perfis e visualizar um *feed* personalizado de receitas;  
- Explorar novos pratos recomendados por meio de recursos de IA (em desenvolvimento).  

---

## 🎯 Objetivos

- Promover o compartilhamento de receitas de forma interativa.  
- Facilitar a descoberta de técnicas culinárias.  
- Oferecer um espaço digital colaborativo para usuários interessados em gastrônomia.  
- Implementar recursos de **inteligência artificial** para sugerir receitas personalizadas com base em dados fornecidos pelo usuário.

---

## 🧱 Arquitetura e Tecnologias

| Camada | Tecnologia | Descrição |
|--------|-------------|-----------|
| **Backend** | Django | Framework web em Python, responsável pela lógica do sistema. |
| **Frontend** | Bootstrap | Framework CSS para estabelecer uma interface responsiva. |
| **Testes** | Cypress | Ferramenta para testes automatizados end-to-end. |
| **Banco de Dados** | SQLite | Armazena dados de usuários, receitas e interações. |

---

## 🧩 Funcionalidades Principais

- 👤 **Cadastro e login de usuários**  
- 📖 **Criação, edição e exclusão de receitas**  
- ❤️ **Curtir e comentar receitas**  
- 👥 **Seguir outros usuários**  
- 📰 **Feed personalizado com receitas de quem o usuário segue**  
- 👤 **Sistema de perfil de usuário com tags de receitas favoritas**
- 🤖 **Geração de receitas via IA** (Em desenvolvimento)

---

## 🧩 Testes executados
Os testes são realizados com o **Cypress**, garantindo o funcionamento das principais funcionalidades do sistema.  
Exemplos de testes realizados:

- Login, logout e cadastro de usuários;
- Criação, edição e exclusão de receitas;
- Verificação e interação dos elementos visuais no frontend.

---

## ⚙️ Instalação e Execução

### 🔹 1. Criar ambiente virtual e instalar dependências
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 🔹 2. Instalar Django
```
pip install django
```

### 🔹 3. Instalar Bootstrap
```
npm install bootstrap
```

### 🔹 4. Rodar o projeto Django
```
python manage.py runserver
```

### 🔹 5. Instalar Cypress
```
npm install cypress --save-dev
```

### 🔹 6. Rodar Cypress
```
npx cypress open
```
---

### 📁 Estrutura de Pastas

```
saboreie/
├── autenticacao/
│   ├── __pycache__/
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── receitas/
│   ├── __pycache__/
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── Saboreie/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   └── home.html
│
├── db.sqlite3
└── manage.py
```

---

## 🚀 Melhorias Futuras

- 🧠 **Integração com API de Inteligência Artificial para criação automática de receitas**
- 📸 **Upload de fotos na criação de receitas**
- 🏷️ **Incluir tags para categorização das receitas**
- 🔔 **Implementar o sistema de notificação das interações entre os usuários** 
- 🦾 **Realizar os testes das novas funcionalidades implementadas** 

---

## 👨‍💻 Equipe de Desenvolvimento

| **Nome**                                        | **Função**                                    |
| ----------------------------------------------- | --------------------------------------------- |
| 💾 **Lucca Marcondes Madeira**                  | Desenvolvedor **Backend**                     |
| 💾 **Gustavo Macedo Silva**                     | Desenvolvedor **Backend**                     |
| 🎨 **Dérick Siécola Villela** | Desenvolvedor **Frontend** / **Documentação** |
| 🎨 **José Carlos Rebouças**                     | Desenvolvedor **Frontend**                    |
| 🔍 **João Pedro Moreira**                       | **QA / Testes**                               |
