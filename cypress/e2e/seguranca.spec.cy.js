describe('Testes de Segurança - Acesso Deslogado', () => {


const urlsProtegidas = [
    '/receitas/criar/',    
    '/receitas/minhas/',  
    '/receitas/feed/'
  ];
  urlsProtegidas.forEach((url) => {
    
    it(`Deve redirecionar para o Login ao tentar acessar "${url}" sem estar logado`, () => {
      

      cy.visit(url);

      cy.location('pathname').should('eq', '/login/');
      
      cy.get('button[type="submit"]').should('be.visible');
    });

  });

});