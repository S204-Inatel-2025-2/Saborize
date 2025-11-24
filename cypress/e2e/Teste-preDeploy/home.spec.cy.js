describe('Home Page - Saborize (Logado)', () => {

  beforeEach(() => {

    cy.visit('/login/');
    cy.get('input[name="username"]').type('Joao1'); 
    cy.get('input[name="password"]').type('G7p!2xQ9'); 
    cy.get('button[type="submit"]').click();
    cy.location('pathname').should('eq', '/');
  });

  it('Deve exibir todos os elementos de boas-vindas e botões de navegação', () => {
    cy.get('h1').should('contain.text', 'Bem-vindo ao Saborize!');
    cy.get('p').should('contain.text', 'Descubra e compartilhe receitas');
    cy.contains('a', 'Ver Feed de Receitas').should('be.visible');
    cy.contains('a', 'Criar Receita').should('be.visible');
    cy.contains('a', 'Minhas Receitas').should('be.visible');
    cy.get('.card').contains('a', 'Logout').should('be.visible');
  });

  it("Deve navegar para a página 'Criar Receita' ao clicar no botão", () => {
    cy.contains('a', 'Criar Receita').click();

    cy.location('pathname').should('eq', '/receitas/criar/'); 
  });
  
  it("Deve navegar para a página 'Ver Feed de Receitas'", () => {
     cy.contains('a', 'Ver Feed de Receitas').click();
     
     cy.location('pathname').should('eq', '/receitas/feed/'); 
  });

  it("Deve navegar para a página 'Minhas Receitas' ao clicar no botão", () => {
     cy.contains('a', 'Minhas Receitas').click();
     
     cy.location('pathname').should('eq', '/receitas/minhas/'); 
  });

  it("Deve deslogar o usuário e redirecionar para a página de login", () => {
    // Clica no botão "Logout" DENTRO do card branco
    cy.get('.card').contains('a', 'Logout').click();
    
    cy.location('pathname').should('eq', '/');
    
    cy.get('a[href="/login/"]').should('be.visible');
  });

});