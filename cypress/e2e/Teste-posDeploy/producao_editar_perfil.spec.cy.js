describe('Saborize - Editar Perfil Completo (Produção)', () => {

  const usuario = {
    username: 'Joao1',
    password: 'G7p!2xQ9'
  };

  const dadosPerfil = {
    nome: 'Joao',
    sobrenome: 'Pedro',
    bio: 'Apenas um teste boy com foto nova!',
    telefone: '35999999999',
    cidade: 'Santa Rita',
    estado: 'MG',
    dataNascimento: '2001-12-07', 
    apiKey: 'sk-teste-123456'
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
    cy.visit('https://saborize-3.onrender.com/editar-perfil/');
  });

  it('Deve preencher dados pessoais, FOTO, tags e API Key, e validar persistência', () => {
    cy.log('--- Preenchendo Informações Pessoais ---');


    cy.get('input[name="first_name"], #id_first_name').clear().type(dadosPerfil.nome);
    cy.get('input[name="last_name"], #id_last_name').clear().type(dadosPerfil.sobrenome);

    cy.get('textarea[name="bio"], #id_bio').clear().type(dadosPerfil.bio);

    cy.get('input[name="telefone"], #id_telefone').clear().type(dadosPerfil.telefone);

    cy.get('input[name="data_nascimento"], #id_data_nascimento').clear().type(dadosPerfil.dataNascimento);

    cy.get('input[name="cidade"], #id_cidade').clear().type(dadosPerfil.cidade);
    cy.get('input[name="estado"], #id_estado').clear().type(dadosPerfil.estado);

    
    cy.log('--- Fazendo Upload da Foto ---');

    cy.get('input[type="file"]').selectFile('cypress/fixtures/perfil.jpg', { force: true });

    cy.log('--- Selecionando Tags ---');
    cy.contains('label', 'Brasileira').should('be.visible').first().click();
    cy.contains('label', 'Fácil').should('be.visible').first().click();


    cy.log('--- Preenchendo API Key ---');
    cy.get('input[name="openai_api_key"], #id_openai_api_key').clear().type(dadosPerfil.apiKey);

    cy.log('--- Salvando Perfil ---');
    cy.get('button[type="submit"]').click();

    cy.visit('https://saborize-3.onrender.com/editar-perfil/');

    cy.log('--- Validando se os dados ficaram salvos ---');

    // Valida Textos
    cy.get('input[name="first_name"], #id_first_name').should('have.value', dadosPerfil.nome);
    cy.get('input[name="last_name"], #id_last_name').should('have.value', dadosPerfil.sobrenome);
    cy.get('textarea[name="bio"], #id_bio').should('have.value', dadosPerfil.bio);
    cy.get('input[name="telefone"], #id_telefone').should('have.value', dadosPerfil.telefone);
    cy.get('input[name="cidade"], #id_cidade').should('have.value', dadosPerfil.cidade);
    cy.get('input[name="data_nascimento"], #id_data_nascimento').should('have.value', dadosPerfil.dataNascimento);
    
  });

});