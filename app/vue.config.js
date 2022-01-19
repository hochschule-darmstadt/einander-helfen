module.exports = {
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.csv$/,
          loader: "csv-loader",
          options: {
            dynamicTyping: false,
            header: true,
            skipEmptyLines: true,
          },
        },
      ],
    },
  },

  pluginOptions: {
    i18n: {
      locale: "de",
      fallbackLocale: "de",
      localeDir: "locales",
      enableInSFC: true,
      includeLocales: false,
      enableBridge: true,
    },
  },
};
