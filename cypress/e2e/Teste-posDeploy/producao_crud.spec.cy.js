describe('Saborize - CRUD Completo de Receitas (Em Produção)', () => {

  const baseUrl = 'https://saborize-3.onrender.com';
  const usuario = { username: 'Joao1', password: 'G7p!2xQ9' };

  beforeEach(() => {
    cy.on('uncaught:exception', () => false);

    cy.visit(`${baseUrl}/login`, { timeout: 120000 });


    cy.get('input[name="username"]', { timeout: 30000 }).should('be.visible').type(usuario.username);
    cy.get('input[name="password"]').should('be.visible').type(usuario.password);
    cy.get('button[type="submit"]').click();
    cy.get('h1', { timeout: 30000 }).should('contain.text', 'Bem-vindo');
  });

  it('Deve realizar o ciclo completo: CRIAR, LER, ATUALIZAR e DELETAR', () => {
    
    const timestamp = Date.now();
    const tituloReceita = `Prod Test ${timestamp}`; 
    const tituloAtualizado = `Prod Edit ${timestamp}`;
    
    // =================================================
    // 1. CREATE (Criar)
    // =================================================
    cy.log('--- PASSO 1: CRIAR ---');
    
    cy.visit(`${baseUrl}/receitas/criar/`); 

    cy.get('input[name="titulo"]')
      .should('be.visible')
      .and('not.be.disabled') 
      .type(tituloReceita);

    cy.get('textarea[name="descricao"]').type('Teste automatizado em produção.'); 
    cy.get('textarea[name="ingredientes"]').type('Dados reais, Teste real.');
    cy.get('textarea[name="passos"]').type('Validando deploy.'); 

    // Seleciona Tags (usando .first() por segurança)
    cy.get('label').contains('Doce').should('exist').first().click(); 
    cy.get('label').contains('Brasileira').should('exist').first().click();

    cy.get('button[type="submit"]').click();

    // =================================================
    // 2. READ (Verificar Criação)
    // =================================================
    cy.log('--- PASSO 2: VERIFICAR ---');
    
    cy.location('pathname', { timeout: 30000 }).should('eq', '/'); 
    
    cy.visit(`${baseUrl}/receitas/minhas/`);
    
    cy.contains(tituloReceita, { timeout: 20000 }).should('be.visible');

    // =================================================
    // 3. UPDATE (Atualizar)
    // =================================================
    cy.log('--- PASSO 3: EDITAR ---');

    cy.contains('.card', tituloReceita)
      .find('a[href*="/editar/"]')
      .click();

    // Verifica URL
    cy.url().should('include', '/editar/');

    // Edita título
    cy.get('input[name="titulo"]').clear().type(tituloAtualizado);
    
    // Edita tags
    cy.get('label').contains('Doce').first().click(); 
    cy.get('label').contains('Lanche').first().click();

    cy.get('button[type="submit"]').click(); 

    // =================================================
    // 4. READ (Verificar Atualização)
    // =================================================
    cy.log('--- PASSO 4: VERIFICAR EDIÇÃO ---');

    cy.visit(`${baseUrl}/receitas/minhas/`);
    
    cy.contains(tituloReceita).should('not.exist'); 
    cy.contains(tituloAtualizado).should('be.visible'); 

    // =================================================
    // 5. DELETE (Deletar)
    // =================================================
    cy.log('--- PASSO 5: DELETAR ---');

    cy.contains('.card', tituloAtualizado)
      .find('a[href*="/confirmar-deletar/"]') 
      .click();

    cy.get('button[type="submit"]').click(); 

    // =================================================
    // 6. VERIFICAÇÃO FINAL
    // =================================================
    cy.log('--- PASSO 6: FINALIZAR ---');
    
    cy.visit(`${baseUrl}/receitas/minhas/`);
    cy.contains(tituloAtualizado).should('not.exist'); 
  });

});