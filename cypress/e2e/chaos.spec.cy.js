const gremlins = require('gremlins.js');

describe('Testes de Monkey (Chaos Testing) com Gremlins.js', () => {


  beforeEach(() => {
    cy.visit('/login/');
    cy.get('input[name="username"]').type('Joao'); 
    cy.get('input[name="password"]').type('G7p!2xQ9');
    cy.get('button[type="submit"]').click();
    cy.location('pathname').should('eq', '/'); 
  });


  function unleashGremlins(duration) {
    cy.window().then((win) => {
    
      const horde = gremlins.createHorde({
          window: win, 
          strategies: [
              gremlins.strategies.allTogether({ 
                  nb: 1000, 
                  delay: 50, 
              })
          ],
          species: [
              gremlins.species.clicker(),
              gremlins.species.toucher(),
              gremlins.species.formFiller(),
              gremlins.species.scroller(),
              gremlins.species.typer()
          ]
      });

      horde.unleash();

      setTimeout(() => {
          horde.stop();
      }, duration);
    });
  }

  it('Deve sobreviver a um ataque de Gremlins na Home Page', () => {
    cy.log('--- Logado. Soltando os Gremlins na Home Page! ---');

    unleashGremlins(10000);

    cy.wait(10000);

    cy.log('Ataque concluído. Verificando se a Home sobreviveu...');
    cy.get('h1').should('be.visible');
  });

  it('Deve sobreviver a um ataque de Gremlins na página "Criar Receita"', () => {
    cy.log('--- Navegando para Criar Receita... ---');
    cy.visit('/receitas/criar/'); 

    cy.log('--- Soltando os Gremlins no formulário de Criar Receita! ---');

    unleashGremlins(15000);

    cy.wait(15000);

    cy.log('Ataque concluído. Verificando se a página de Criar Receita sobreviveu...');
    cy.get('button[type="submit"]').should('be.visible');
  });

});