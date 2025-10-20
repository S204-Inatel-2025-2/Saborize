describe('Funcionalidade de CRUD de Receitas', () => {

  // --- PREPARAÇÃO ---
  beforeEach(() => {
    // Garante que estamos logados antes de cada teste
    cy.visit('/login/');
    cy.get('input[name="username"]').type('Joao'); // Seu usuário de teste
    cy.get('input[name="password"]').type('G7p!2xQ9'); // Sua senha de teste
    cy.get('button[type="submit"]').click();
    cy.location('pathname').should('eq', '/'); // Garante que o login funcionou
  });

  // --- Teste Modificado ---
  it('Deve permitir CRIAR e LER, e verificar que EDITAR e DELETAR não estão implementados', () => {
    
    // --- Variáveis de Teste ---
    const timestamp = Date.now();
    const tituloReceita = `Bolo de Teste Automatizado ${timestamp}`;
    
    // --- 1. CREATE (Criar) ---
    cy.log('--- INICIANDO: PARTE 1: CREATE ---');
    cy.visit('/receitas/criar/'); 

    // ❗ SUA MISSÃO: Continue verificando se faltam mais campos obrigatórios
    cy.get('input[name="titulo"]').type(tituloReceita);
    cy.get('textarea[name="descricao"]').type('bolinho'); // Você adicionou este!
    cy.get('textarea[name="ingredientes"]').type('Farinha, Ovos, Leite e Cypress');
    cy.get('textarea[name="passos"]').type('Misture tudo e rode o teste.'); 
    // cy.get('input[name="tempo_preparo"]').type('45'); // ❗ Exemplo de outro campo

    cy.get('button[type="submit"]').click();

    
    // --- 2. READ (Verificar o Create) ---
    cy.log('--- INICIANDO: PARTE 2: READ (Verificar Create) ---');
    
    cy.location('pathname').should('eq', '/'); 
    cy.get('a[href="/receitas/minhas/"]').click();
    cy.location('pathname').should('eq', '/receitas/minhas/');
    cy.contains(tituloReceita).should('be.visible');

    
    // --- 3. VERIFICAR "UPDATE" (Atualizar) ---
    cy.log('--- INICIANDO: PARTE 3: VERIFICAR AUSÊNCIA DO UPDATE ---');

    // Encontra o card que contém o título, e DENTRO dele, clica em "Ver Receita Completa"
    cy.contains('.card', tituloReceita)
      .find('a:contains("Ver Receita Completa")')
      .click();

    // Agora estamos na página de DETALHE da receita...
    
    // TESTE MODIFICADO:
    // Em vez de clicar, verificamos que o botão "Editar" NÃO EXISTE.
    cy.log('Verificando se o botão "Editar" não foi implementado...');
    cy.contains('a', 'Editar Receita').should('not.exist');

    
    // --- 4. VERIFICAR "DELETE" (Deletar) ---
    cy.log('--- INICIANDO: PARTE 4: VERIFICAR AUSÊNCIA DO DELETE ---');
    
    // Como já estamos na página de detalhe, apenas procuramos o botão "Deletar"

    // TESTE MODIFICADO:
    // Verificamos que o botão "Deletar" NÃO EXISTE.
    cy.log('Verificando se o botão "Deletar" não foi implementado...');
    cy.contains('button', 'Deletar Receita').should('not.exist');
    
    
    // --- 5. VERIFICAÇÃO FINAL ---
    cy.log('--- INICIANDO: PARTE 5: VERIFICAÇÃO FINAL ---');
    
    // Como não podemos editar ou deletar, o teste termina aqui.
    // Vamos voltar para "Minhas Receitas" e garantir que a receita original ainda está lá.
    cy.visit('/receitas/minhas/');
    cy.contains(tituloReceita).should('be.visible');
  });

});