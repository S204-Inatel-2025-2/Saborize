describe('Saborize - Perfil do Usuário (Produção)', () => {

  const usuario = {
    username: 'Joao1',
    password: 'G7p!2xQ9',
    email: 'joaopedro@gmail.com' 
  };

  beforeEach(() => {
    cy.on('uncaught:exception', () => false);

    cy.visit('https://saborize-3.onrender.com/login', { timeout: 60000 });
    
    cy.get('input[name="username"]', { timeout: 30000 }).should('be.visible').type(usuario.username);
    cy.get('input[name="password"]').type(usuario.password);
    cy.get('button[type="submit"]').click();

    cy.get('h1', { timeout: 30000 }).should('contain.text', 'Bem-vindo');

    cy.get('nav').contains('Meu Perfil').click();
    
    cy.url().should('match', /\/perfil|\/profile|\/usuario/);
  });

  it('Deve exibir as informações básicas do perfil corretamente', () => {
    cy.contains(usuario.username).should('be.visible');
    
    cy.contains(`@${usuario.username}`).should('be.visible');

    cy.contains(usuario.email).should('be.visible');

    cy.get('img').should('exist'); 
  });

  it('Deve exibir as estatísticas zeradas (Receitas, Seguidores, Seguindo)', () => {
    cy.contains('Receitas').should('be.visible');
    cy.contains('Seguidores').should('be.visible');
    cy.contains('Seguindo').should('be.visible');

    cy.contains(/\b0\b/).should('be.visible'); 
  });

  it('Deve validar o botão de "Editar Perfil"', () => {
    cy.contains('button, a', 'Editar Perfil')
      .should('be.visible')
      .click();

    cy.url().should('include', '/editar');
    
    cy.go('back');
  });

});