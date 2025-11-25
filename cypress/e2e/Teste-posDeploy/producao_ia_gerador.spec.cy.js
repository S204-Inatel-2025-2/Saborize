describe('Saborize - Gerador de Receitas com IA (Produção)', () => {

  const usuario = {
    username: 'Joao1',
    password: 'G7p!2xQ9'
  };

  beforeEach(() => {
    cy.on('uncaught:exception', () => false);

    cy.visit('https://saborize-3.onrender.com/login', { timeout: 60000 });

    cy.get('body').then(($body) => {
        if ($body.find('input[name="username"]').length > 0) {
            cy.get('input[name="username"]').type(usuario.username);
            cy.get('input[name="password"]').type(usuario.password);
            cy.get('button[type="submit"]').click();
        }
    });

    cy.get('h1', { timeout: 30000 }).should('contain.text', 'Bem-vindo');

    cy.visit('https://saborize-3.onrender.com/receitas/gerador-ia/'); 
  });

  it('Deve carregar a interface do Gerador corretamente', () => {
    cy.get('h1, h2').should('contain.text', 'Gerador de Receitas com IA');
    
    cy.contains('Tipo de Receita').should('be.visible');
    cy.contains('label', 'Brasileira').should('be.visible');
    cy.contains('label', 'Doce').should('be.visible');

    cy.contains('Tempo de Preparo').should('be.visible');
    cy.get('select').should('have.length.at.least', 2);

    cy.contains('Observações Especiais').should('be.visible');
    cy.get('textarea').should('be.visible').and('have.attr', 'placeholder', 'Ex.: sem glúten, vegano...');

    cy.contains('Sua receita aparecerá aqui após gerar.').should('be.visible');
  });

  it('Deve permitir selecionar opções no formulário (Checkboxes e Dropdowns)', () => {
    // 1. Marcar Checkboxes (Tipo de Receita)
    cy.contains('label', 'Apimentado').click();
    cy.contains('label', 'Cremoso').click();

    cy.get('select').first().select(1); 

    cy.get('select').last().select(1);
    
    cy.get('textarea').type('Quero uma receita com muito queijo!');
  });

  it('TESTE MOCK: Deve gerar uma receita simulada e exibir na tela', () => {
    
    const receitaFalsa = {
      titulo: "Macarrão com Queijo Mockado",
      conteudo: "Ingredientes: Macarrão, Queijo.\nModo de Preparo: Cozinhe e misture. (Gerado pelo Cypress)",
    };

    cy.intercept('POST', '**', {
      statusCode: 200,
      body: receitaFalsa, 
      delay: 1000 
    }).as('chamadaIA');

    cy.contains('label', 'Brasileira').click();
    
    cy.get('select').first().select(1); 
    cy.get('select').last().select(1);

    cy.get('textarea').type('Teste de Mock');

    cy.contains('button', 'Gerar Receita com IA').click();

    cy.wait('@chamadaIA');

    cy.contains('Sua receita aparecerá aqui após gerar.').should('not.exist');
    cy.contains('Macarrão com Queijo Mockado').should('be.visible');
    cy.contains('Gerado pelo Cypress').should('be.visible');
  });

});