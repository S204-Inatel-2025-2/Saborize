describe('Saborize - Telas de Autenticação (Produção)', () => {

  const usuarioValido = {
    username: 'Joao1', 
    password: 'G7p!2xQ9'
  };

  beforeEach(() => {
    cy.on('uncaught:exception', () => false);
  });

  // =========================================
  // TESTES DA TELA DE LOGIN
  // =========================================
  context('Tela de Login', () => {
    
    beforeEach(() => {
      cy.visit('https://saborize-3.onrender.com/');
      cy.contains('.card a, .card button', 'Login').click();
      
      cy.url().should('include', '/login');
    });

    it('Deve exibir o formulário de login corretamente', () => {
      cy.get('h2, h1').invoke('text').should('match', /Login|Entrar|Acessar conta/i);
      
      cy.get('input[name="username"]').should('be.visible');
      cy.get('input[name="password"]').should('be.visible');
      
      cy.get('button[type="submit"]').invoke('text').should('match', /Entrar|Login|Acessar/i);
    });

    it('Deve validar credenciais inválidas (Caminho Infeliz)', () => {
      cy.get('input[name="username"]').type('UsuarioFalso123');
      cy.get('input[name="password"]').type('SenhaErrada');
      cy.get('button[type="submit"]').click();

      cy.contains(/inválidos|incorreta|encontrado|password|erro/i).should('be.visible');
    });

    it('Deve realizar Login com sucesso e redirecionar para a Home Logada', () => {
      cy.get('input[name="username"]').type(usuarioValido.username);
      cy.get('input[name="password"]').type(usuarioValido.password);
      cy.get('button[type="submit"]').click();

      cy.url().should('eq', 'https://saborize-3.onrender.com/');
      
      cy.contains('Minhas Receitas').should('be.visible');
      cy.contains('Logout').should('be.visible');
    });

    it('Deve ter um link para a página de Cadastro', () => {
      cy.contains('a', /Cadastre|Registrar|Criar/i) 
        .should('be.visible')
        .click();

      cy.url().should('match', /\/registrar|\/cadastro|\/register/); 
    });
  });

  // =========================================
  // TESTES DA TELA DE CADASTRO
  // =========================================
  context('Tela de Cadastro (Registro)', () => {

    beforeEach(() => {
      cy.visit('https://saborize-3.onrender.com/');
      cy.contains('.card a, .card button', 'Registrar').click();
      cy.url().should('match', /\/registrar|\/cadastro|\/register/);
    });

    it('Deve exibir o formulário de cadastro completo', () => {
      cy.get('input[name="username"]').should('be.visible');
      cy.get('input[name="email"]').should('be.visible');
      
      cy.get('input[type="password"]').should('have.length.at.least', 2); 
      
      cy.get('button[type="submit"]').should('be.visible');
    });

    it('Deve bloquear cadastro com senhas diferentes (Validação)', () => {
      const timestamp = Date.now();
      cy.get('input[name="username"]').type(`UserTeste${timestamp}`);
      cy.get('input[name="email"]').type(`teste${timestamp}@email.com`);
      
      cy.get('input[type="password"]').first().type('Senha123');
      cy.get('input[type="password"]').last().type('SenhaDiferente');
      
      cy.get('button[type="submit"]').click();

      // Verifica mensagem de erro
      cy.contains(/inválidos|incorreta|encontrado|password|erro/i).should('be.visible');
    });

    it('Deve ter um link para voltar ao Login', () => {

      cy.contains('a', 'Login') 
        .should('be.visible')
        .click();

      cy.url().should('include', '/login');
    });
  });

});