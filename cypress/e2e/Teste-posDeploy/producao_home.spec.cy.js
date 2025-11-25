describe('Saborize - Home Page Logada (Produção)', () => {

  const usuario = {
    username: 'Joao1',
    password: 'G7p!2xQ9'
  };

  beforeEach(() => {
    cy.on('uncaught:exception', () => false);

    cy.visit('https://saborize-3.onrender.com/login', { timeout: 60000 });
    
    cy.get('input[name="username"]').should('be.visible').type(usuario.username);
    cy.get('input[name="password"]').should('be.visible').type(usuario.password);
    cy.get('button[type="submit"]').click();

    cy.get('h1', { timeout: 30000 }).should('contain.text', 'Bem-vindo');
    cy.url().should('match', /saborize-3\.onrender\.com\/?$/);
  });

  it('Deve exibir os elementos principais da Dashboard', () => {
    cy.get('h1').should('contain.text', 'Bem-vindo ao Saborize!');
    cy.get('nav').should('be.visible');
    cy.contains('SABORIZE').should('be.visible');
  });

  it('Deve exibir e validar os links da Barra de Navegação (Topo)', () => {
    const linksNavbar = [
      'Criar Receita',
      'Feed',
      'Seguindo',
      'Descobrir Usuários',
      'Gerador IA',
      'Minhas Receitas',
      'Meu Perfil',
      'Logout'
    ];

    linksNavbar.forEach(link => {
      cy.get('nav').contains(link).should('be.visible');
    });

    // Verifica ícones (i ou svg)
    cy.get('nav').find('i, svg').should('exist');
  });

  it('Deve navegar corretamente pelos botões do Card Central', () => {

    cy.contains('.card a, .card button', 'Ver Feed de Receitas').first().click();
    cy.url().should('include', '/feed');
    cy.go('back');
    cy.get('h1', { timeout: 10000 }).should('contain.text', 'Bem-vindo'); 

    // 2. Criar
    cy.contains('.card a, .card button', 'Criar Receita').first().click();
    cy.url().should('include', '/criar');
    cy.go('back');
    cy.get('h1', { timeout: 10000 }).should('contain.text', 'Bem-vindo');

    // 3. Minhas Receitas
    cy.contains('.card a, .card button', 'Minhas Receitas').first().click();
    cy.url().should('include', '/minhas');
    cy.go('back');
    cy.get('h1', { timeout: 10000 }).should('contain.text', 'Bem-vindo');

    // 4. Perfil
    cy.contains('.card a, .card button', 'Meu Perfil').first().click();
    cy.url().should('include', '/perfil');
    cy.go('back');
  });


});