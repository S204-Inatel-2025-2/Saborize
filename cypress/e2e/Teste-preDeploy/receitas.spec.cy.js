describe('Funcionalidade de CRUD Completo de Receitas (com Tags)', () => {

  // --- PREPARAÇÃO ---
  beforeEach(() => {
    // Garante que estamos logados antes de cada teste
    cy.visit('/login/');
    cy.get('input[name="username"]').type('Joao1'); 
    cy.get('input[name="password"]').type('G7p!2xQ9'); 
    cy.get('button[type="submit"]').click();
    cy.location('pathname').should('eq', '/'); // Garante que o login funcionou
  });

  // --- O GRANDE TESTE "TUDO JUNTO" ---
  it('Deve permitir CRIAR com Tags, LER, ATUALIZAR e DELETAR uma receita', () => {
    
    // --- Variáveis de Teste ---
    const timestamp = Date.now();
    const tituloReceita = `Bolo Teste ${timestamp}`;
    const tituloAtualizado = `Bolo EDITADO ${timestamp}`;
    
    // --- 1. CREATE (Criar com Tags) ---
    cy.log('--- INICIANDO: PARTE 1: CREATE ---');
    cy.visit('/receitas/criar/'); 

    // Preenche os campos de texto
    cy.get('input[name="titulo"]').type(tituloReceita);
    cy.get('textarea[name="descricao"]').type('Bolo delicioso de teste com tags.'); 
    cy.get('textarea[name="ingredientes"]').type('Farinha, Ovos, Leite.');
    cy.get('textarea[name="passos"]').type('Misture tudo.'); 

    // Seleciona algumas Tags (Checkbox)
    // Usamos .first() para garantir que clicamos apenas no primeiro, caso existam duplicados
    cy.contains('label', 'Doce').first().click(); 
    cy.contains('label', 'Brasileira').first().click();

    cy.get('button[type="submit"]').click();

    
    // --- 2. READ (Verificar Criação) ---
    cy.log('--- INICIANDO: PARTE 2: READ ---');
    
    // Verifica se voltou para a Home
    cy.location('pathname').should('eq', '/'); 
    
    // CORREÇÃO: Usa .first() para clicar no primeiro botão "Minhas Receitas" que encontrar
    cy.get('a[href="/receitas/minhas/"]').first().click();
    
    cy.location('pathname').should('eq', '/receitas/minhas/');
    
    // Verifica se a receita aparece na lista
    cy.contains(tituloReceita).should('be.visible');

    
    // --- 3. UPDATE (Atualizar) ---
    cy.log('--- INICIANDO: PARTE 3: UPDATE ---');

    // Entra na receita (Encontra o card pelo título e clica no botão "Ver Receita Completa" dentro dele)
    cy.contains('.card', tituloReceita)
      .find('a:contains("Ver Receita Completa")')
      .click();

    // Clica em Editar
    cy.contains('a', 'Editar').click(); 

    // Verifica se foi para a edição
    cy.location('pathname').should('include', '/editar/');

    // Altera o título
    cy.get('input[name="titulo"]')
      .clear()
      .type(tituloAtualizado);
    
    // Altera as tags (Desmarca Doce e marca Lanche)
    cy.contains('label', 'Doce').first().click(); 
    cy.contains('label', 'Lanche').first().click();

    cy.get('button[type="submit"]').click(); 

    
    // --- 4. READ (Verificar Atualização) ---
    cy.log('--- INICIANDO: PARTE 4: READ APÓS UPDATE ---');

    // Volta para a lista e verifica o novo nome
    // CORREÇÃO: Adicionado .first() aqui também por segurança
    cy.visit('/'); // Volta pra home para garantir o fluxo
    cy.get('a[href="/receitas/minhas/"]').first().click();
    
    cy.contains(tituloReceita).should('not.exist'); // Nome antigo sumiu
    cy.contains(tituloAtualizado).should('be.visible'); // Nome novo apareceu

    
    // --- 5. DELETE (Deletar) ---
    cy.log('--- INICIANDO: PARTE 5: DELETE ---');

    // Entra na receita atualizada
    cy.contains('.card', tituloAtualizado)
      .find('a:contains("Ver Receita Completa")')
      .click();

    // Clica em Deletar/Excluir
    cy.contains('button', 'Deletar').click(); 

    // (Se houver confirmação JS, descomente a linha abaixo): 
    // cy.on('window:confirm', () => true);

    
    // --- 6. VERIFICAÇÃO FINAL ---
    cy.log('--- INICIANDO: PARTE 6: VERIFICAÇÃO FINAL ---');
    
    // Garante que sumiu da lista
    cy.visit('/receitas/minhas/');
    cy.contains(tituloAtualizado).should('not.exist'); 
  });

});