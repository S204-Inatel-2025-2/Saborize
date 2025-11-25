describe('Saborize - Home Page: Funcionalidades (IA e Logout)', () => {

  const usuario = { username: 'Joao1', password: 'G7p!2xQ9' };

  beforeEach(() => {
    cy.on('uncaught:exception', () => false)
    cy.visit('https://saborize-3.onrender.com/login', { timeout: 120000, failOnStatusCode: false });
    cy.wait(2000);
    
    cy.get('input[name="username"]', { timeout: 30000 }).should('be.visible').type(usuario.username);
    cy.get('input[name="password"]').type(usuario.password);
    cy.get('button[type="submit"]').click();

    // Trava de segurança
    cy.get('h1', { timeout: 60000 }).should('contain.text', 'Bem-vindo');
  });

  it('Deve testar o botão "Gerador IA" na navbar', () => {
    cy.get('nav').contains('Gerador IA').click();

    cy.url({ timeout: 30000 }).should('include', 'gerador-ia');
    
    cy.get('body').invoke('text').should('match', /IA|Gerador/i);
  });

  it('Deve realizar Logout com sucesso', () => {
    cy.contains('Logout').should('be.visible').first().click();

    cy.url({ timeout: 30000 }).should('match', /\/login|saborize-3\.onrender\.com\/?$/);

    cy.contains('a', /Login|Entrar/i, { timeout: 20000 }).should('be.visible');
  });

});