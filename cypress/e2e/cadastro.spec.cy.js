// Descreve a suíte de testes para a funcionalidade de Cadastro
describe('Funcionalidade de Cadastro de Usuário - Saborize', () => {

  // --- Teste de Sucesso ("Caminho Feliz") ---
  it('Deve permitir que um novo usuário se cadastre com sucesso', () => {
    cy.visit('/registrar/');
    const timestamp = Date.now();
    cy.get('input[name="username"]').type(`usuario${timestamp}`);
    cy.get('input[name="email"]').type(`usuario${timestamp}@teste.com`); 
    cy.get('input[name="password1"]').type('G7p!2xQ9');
    cy.get('input[name="password2"]').type('G7p!2xQ9');
    cy.get('button[type="submit"]').click();
    cy.location('pathname').should('eq', '/');
  });

  // --- Teste de Falha ("Caminho Infeliz") ---
  it('Deve exibir uma mensagem de erro se as senhas não conferirem', () => {
    cy.visit('/registrar/');

    cy.get('input[name="username"]').type('usuarioErro');         
    cy.get('input[name="email"]').type('usuario.erro@teste.com');  
    cy.get('input[name="password1"]').type('G7p!2xQ9');            
    cy.get('input[name="password2"]').type('senhaDIFERENTE456');  

    cy.get('button[type="submit"]').click();

    // A VERIFICAÇÃO da mensagem de erro
    cy.get('.text-danger').should('be.visible');
    cy.get('.text-danger').should('contain.text', "The two password fields didn’t match");
  });
});