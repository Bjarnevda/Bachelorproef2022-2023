const { v4: uuidv4 } = require("uuid"); // Importeer uuidv4 van uuid

// Maak een lege object aan ==> dit is een object waarin we de classname en de hash gaan opslaan
const classToHashMap = {};

// Maak een functie aan die de classname en de hash gaat opslaan in het object, en de hash gaat returnen
const hashOnlyIdent = (context, _, localName) => {
  // Check of de classname al een hash heeft, zo niet, genereer een nieuwe hash en sla deze op in het object
  if (!classToHashMap[localName]) {
    classToHashMap[localName] = `_${uuidv4().replace(/-/g, "")}`;
  }

  // Return de opgeslagen hash voor de classname
  return classToHashMap[localName];
};

module.exports = {
  webpack: (config, { dev }) => {
    config.module.rules.forEach((rule) => {
      if (rule.oneOf && Array.isArray(rule.oneOf)) {
        rule.oneOf.forEach((oneOfRule) => {
          if (
            oneOfRule.test &&
            oneOfRule.test.toString() === /\.module\.css$/.toString()
          ) {
            oneOfRule.use.forEach((loader) => {
              if (
                loader.loader &&
                loader.loader.includes("css-loader") &&
                !loader.loader.includes("postcss-loader")
              ) {
                if (!loader.options.modules) {
                  loader.options.modules = {};
                }
                loader.options.modules.getLocalIdent = hashOnlyIdent;
                loader.options.esModule = false; // Disable caching
              }
            });
          }
        });
      }
    });

    return config;
  },
};
