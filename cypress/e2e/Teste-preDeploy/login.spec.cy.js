describe('Funcionalidade de Login - Saborize', () => {
  it('Deve permitir o login com sucesso', () => {
    cy.visit('/login/');
    cy.get('input[name="username"]').type('Joao1');
    cy.get('input[name="password"]').type('G7p!2xQ9');
    cy.get('button[type="submit"]').click();
    cy.location('pathname').should('eq', '/');

    // 2. A mensagem de boas-vindas está visível e contém o texto esperado
    cy.get('h1').should('be.visible');
    cy.get('h1').should('contain.text', 'Bem-vindo ao Saborize!');

    // 3. O botão de "Sair" está visível
    cy.get('a[href="/logout/"]').should('be.visible');

    // 4. O botão de "Login" NÃO existe mais na página
    cy.get('a[href="/login/"]').should('not.exist');
  });
});