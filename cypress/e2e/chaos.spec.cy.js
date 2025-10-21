// Importa a biblioteca gremlins.js usando require
const gremlins = require('gremlins.js');

describe('Testes de Monkey (Chaos Testing) com Gremlins.js', () => {

  // --- PREPARAÇÃO ---
  beforeEach(() => {
    // Faz o login antes de cada teste para acessar as páginas internas
    cy.visit('/login/');
    cy.get('input[name="username"]').type('Joao'); // Seu usuário de teste
    cy.get('input[name="password"]').type('G7p!2xQ9'); // Sua senha de teste
    cy.get('button[type="submit"]').click();
    cy.location('pathname').should('eq', '/'); // Garante que o login funcionou
  });

  // Função CORRIGIDA para "soltar" os Gremlins na janela do navegador
  function unleashGremlins(duration) {
    cy.window().then((win) => {
      // Cria a "horda" de gremlins dentro da janela da sua aplicação
      const horde = gremlins.createHorde({
          window: win, // Especifica a janela da aplicação
          strategies: [
              gremlins.strategies.allTogether({ // Usa a estratégia allTogether
                  nb: 1000, // Número de ataques (pode ajustar)
                  delay: 50, // Milissegundos entre ataques (pode ajustar)
              })
          ],
          // Quais gremlins usar (pode adicionar/remover conforme necessário)
          species: [
              gremlins.species.clicker(),
              gremlins.species.toucher(),
              gremlins.species.formFiller(),
              gremlins.species.scroller(),
              gremlins.species.typer()
          ]
      });

      // Inicia o ataque!
      horde.unleash();

      // Para o ataque após a duração definida
      setTimeout(() => {
          horde.stop();
      }, duration);
    });
  }

  it('Deve sobreviver a um ataque de Gremlins na Home Page', () => {
    cy.log('--- Logado. Soltando os Gremlins na Home Page! ---');

    // Solta os gremlins por 10 segundos (10000 milissegundos)
    // Se a aplicação "quebrar" (lançar um erro JS), o Cypress falhará este teste.
    unleashGremlins(10000);

    // Damos um tempo para os gremlins terminarem e a aplicação se recuperar
    cy.wait(10000);

    // --- VERIFICAÇÃO FINAL ---
    // Apenas verificamos se a página ainda está carregada
    cy.log('Ataque concluído. Verificando se a Home sobreviveu...');
    cy.get('h1').should('be.visible');
  });

  it('Deve sobreviver a um ataque de Gremlins na página "Criar Receita"', () => {
    cy.log('--- Navegando para Criar Receita... ---');
    cy.visit('/receitas/criar/'); // Use a URL correta

    cy.log('--- Soltando os Gremlins no formulário de Criar Receita! ---');

    // Solta os gremlins por 15 segundos (15000 milissegundos)
    unleashGremlins(15000);

    // Damos um tempo para os gremlins terminarem
    cy.wait(15000);

    // --- VERIFICAÇÃO FINAL ---
    // Apenas verificamos se a página ainda está carregada
    cy.log('Ataque concluído. Verificando se a página de Criar Receita sobreviveu...');
    cy.get('button[type="submit"]').should('be.visible');
  });

  // (Opcional) Adicione mais testes 'it' para outras páginas complexas
  // Ex: Página "Minhas Receitas", Página de Detalhe de uma Receita, etc.

});