module.exports = [];

const { v4: uuidv4 } = require("uuid");

// Create an object to store unique hashes for each classname
const classToHashMap = {};

const hashOnlyIdent = (context, _, localName) => {
  // Check if the classname already has a hash, if not, generate a new hash and store it
  if (!classToHashMap[localName]) {
    classToHashMap[localName] = `_${uuidv4().replace(/-/g, "")}`;
  }

  // Return the stored hash for the classname
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

/*const { v4: uuidv4 } = require("uuid");

const generatedHash = uuidv4().replace(/-/g, "");

const classToHashMap = {};

const hashOnlyIdent = (context, _, localName) => {
  // Check if the classname already has a hash, if not, generate a new hash and store it
  if (!classToHashMap[localName]) {
    classToHashMap[localName] = `_${uuidv4().replace(/-/g, "")}`;
  }

  // Return the stored hash for the classname
  return classToHashMap[localName];
};

module.exports = {
  webpack(config, { dev }) {
    const rules = config.module.rules
      .find((rule) => typeof rule.oneOf === "object")
      .oneOf.filter((rule) => Array.isArray(rule.use));

    if (!dev) {
      rules.forEach((rule) => {
        rule.use.forEach((moduleLoader) => {
          if (
            moduleLoader.loader &&
            moduleLoader.loader.includes("css-loader") &&
            !moduleLoader.loader.includes("postcss-loader")
          ) {
            if (!moduleLoader.options.modules) {
              moduleLoader.options.modules = {};
            }
            moduleLoader.options.modules.getLocalIdent = hashOnlyIdent;
            moduleLoader.options.esModule = false; // Disable caching
          }
        });
      });
    }

    return config;
  },
};
*/
