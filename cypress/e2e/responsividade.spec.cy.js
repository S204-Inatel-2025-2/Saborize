describe('Testes de Responsividade e Layout (Mobile vs Desktop)', () => {

  beforeEach(() => {
    cy.visit('/'); 
  });


  it('Deve exibir o layout padrão em telas de Desktop (1280px)', () => {
    cy.viewport(1280, 720);

    cy.get('.navbar-collapse').should('be.visible');

    cy.get('.navbar-toggler').should('not.be.visible');

    cy.contains('a', 'Login').should('be.visible');
  });

  it('Deve exibir o layout mobile em um iPhone X', () => {
    cy.viewport('iphone-x');

    cy.get('.navbar-toggler').should('be.visible');

    cy.contains('a', 'Login').should('not.be.visible');

    cy.get('.navbar-toggler').click();

    // 5. VERIFICAÇÃO: Agora os links devem aparecer
    cy.contains('a', 'Login').should('be.visible');
  });

});