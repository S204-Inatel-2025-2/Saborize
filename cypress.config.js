const { defineConfig } = require("cypress");

module.exports = defineConfig({
 
  reporter: 'cypress-mochawesome-reporter',
  reporterOptions: {
    charts: true, 
    reportPageTitle: 'Saborize - Relatório de Testes', 
    embeddedScreenshots: true, 
    inlineAssets: true,
  },

  e2e: {
    baseUrl: 'http://127.0.0.1:8000',
    setupNodeEvents(on, config) {
      
      require('cypress-mochawesome-reporter/plugin')(on);

    },
  },
});