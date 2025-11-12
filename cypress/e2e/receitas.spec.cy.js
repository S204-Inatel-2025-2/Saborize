describe('Funcionalidade de CRUD de Receitas', () => {

beforeEach(() => {
    cy.visit('/login/');
    cy.get('input[name="username"]').type('Joao'); 
    cy.get('input[name="password"]').type('G7p!2xQ9'); 
    cy.get('button[type="submit"]').click();
    cy.location('pathname').should('eq', '/'); 
  });

  it('Deve permitir CRIAR e LER, e verificar que EDITAR e DELETAR não estão implementados', () => {
    
    const timestamp = Date.now();
    const tituloReceita = `Bolo de Teste Automatizado ${timestamp}`;
    
    // --- 1. CREATE (Criar) ---
    cy.log('--- INICIANDO: PARTE 1: CREATE ---');
    cy.visit('/receitas/criar/'); 

    cy.get('input[name="titulo"]').type(tituloReceita);
    cy.get('textarea[name="descricao"]').type('bolinho'); 
    cy.get('textarea[name="ingredientes"]').type('Farinha, Ovos, Leite e Cypress');
    cy.get('textarea[name="passos"]').type('Misture tudo e rode o teste.'); 

    cy.get('button[type="submit"]').click();

    
    // --- 2. READ (Verificar o Create) ---
    cy.log('--- INICIANDO: PARTE 2: READ (Verificar Create) ---');
    
    cy.location('pathname').should('eq', '/'); 
    cy.get('a[href="/receitas/minhas/"]').click();
    cy.location('pathname').should('eq', '/receitas/minhas/');
    cy.contains(tituloReceita).should('be.visible');

    
    // --- 3. VERIFICAR "UPDATE" (Atualizar) ---
    cy.log('--- INICIANDO: PARTE 3: VERIFICAR AUSÊNCIA DO UPDATE ---');

    cy.contains('.card', tituloReceita)
      .find('a:contains("Ver Receita Completa")')
      .click();

 
    cy.log('Verificando se o botão "Editar" não foi implementado...');
    cy.contains('a', 'Editar Receita').should('not.exist');

    
    // --- 4. VERIFICAR "DELETE" (Deletar) ---
    cy.log('--- INICIANDO: PARTE 4: VERIFICAR AUSÊNCIA DO DELETE ---');
    

    cy.log('Verificando se o botão "Deletar" não foi implementado...');
    cy.contains('button', 'Deletar Receita').should('not.exist');
    
    
    // --- 5. VERIFICAÇÃO FINAL ---
    cy.log('--- INICIANDO: PARTE 5: VERIFICAÇÃO FINAL ---');
    
    cy.visit('/receitas/minhas/');
    cy.contains(tituloReceita).should('be.visible');
  });

});