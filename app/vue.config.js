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
    plugins: [require("./build-env-plugin")],
  },
};
