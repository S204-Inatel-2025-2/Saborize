describe('Funcionalidade de CRUD Completo de Receitas (com Tags)', () => {

  beforeEach(() => {
    cy.visit('/login/');
    cy.get('input[name="username"]').type('Joao1'); 
    cy.get('input[name="password"]').type('G7p!2xQ9'); 
    cy.get('button[type="submit"]').click();
    cy.location('pathname').should('eq', '/'); 
  });

  it('Deve permitir CRIAR com Tags, LER, ATUALIZAR e DELETAR uma receita', () => {
    
    const timestamp = Date.now();
    const tituloReceita = `Bolo Teste ${timestamp}`;
    const tituloAtualizado = `Bolo EDITADO ${timestamp}`;
    
    // --- 1. CREATE (Criar) ---
    cy.log('--- INICIANDO: PARTE 1: CREATE ---');
    cy.visit('/receitas/criar/'); 

    cy.get('input[name="titulo"]').type(tituloReceita);
    cy.get('textarea[name="descricao"]').type('Bolo delicioso de teste.'); 
    cy.get('textarea[name="ingredientes"]').type('Farinha, Ovos, Leite.');
    cy.get('textarea[name="passos"]').type('Misture tudo.'); 

    // Seleciona Tags (usando .first() para evitar erro)
    cy.contains('label', 'Doce').first().click(); 
    cy.contains('label', 'Brasileira').first().click();

    cy.get('button[type="submit"]').click();

    
    // --- 2. READ (Verificar Criação) ---
    cy.log('--- INICIANDO: PARTE 2: READ ---');
    
    cy.location('pathname').should('eq', '/'); 
    cy.get('a[href="/receitas/minhas/"]').first().click();
    cy.location('pathname').should('eq', '/receitas/minhas/');
    
    // Verifica se a receita aparece na lista
    cy.contains(tituloReceita).should('be.visible');

    
    // --- 3. UPDATE (Atualizar) ---
    cy.log('--- INICIANDO: PARTE 3: UPDATE ---');

    // AJUSTE: Clica no botão de EDITAR direto no card (baseado no href da sua imagem)
    // Procura o card com o título, e dentro dele busca o link que contém "/editar/"
    cy.contains('.card', tituloReceita)
      .find('a[href*="/editar/"]')
      .click();

    // Verifica se foi para a edição
    cy.location('pathname').should('include', '/editar/');

    // Edita título e salva
    cy.get('input[name="titulo"]').clear().type(tituloAtualizado);
    cy.get('button[type="submit"]').click(); 

    
    // --- 4. READ (Verificar Atualização) ---
    cy.log('--- INICIANDO: PARTE 4: READ APÓS UPDATE ---');

    // Volta para a lista (se não tiver voltado automático)
    cy.visit('/receitas/minhas/'); // Garante que estamos na lista
    
    cy.contains(tituloReceita).should('not.exist'); 
    cy.contains(tituloAtualizado).should('be.visible'); 

    
    // --- 5. DELETE (Deletar) ---
    cy.log('--- INICIANDO: PARTE 5: DELETE ---');

    // AJUSTE: Clica no botão de DELETAR direto no card (baseado no href da sua imagem)
    // Procura o card ATUALIZADO, e dentro dele busca o link que contém "/confirmar-deletar/"
    cy.contains('.card', tituloAtualizado)
      .find('a[href*="/confirmar-deletar/"]')
      .click();

    // A URL sugere que fomos para uma página de confirmação.
    // Precisamos confirmar a exclusão clicando no botão final (geralmente um submit vermelho)
    cy.get('button[type="submit"]').click(); 


    // --- 6. VERIFICAÇÃO FINAL ---
    cy.log('--- INICIANDO: PARTE 6: VERIFICAÇÃO FINAL ---');
    
    cy.visit('/receitas/minhas/');
    cy.contains(tituloAtualizado).should('not.exist'); 
  });

});