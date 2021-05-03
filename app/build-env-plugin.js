const webpack = require('webpack');

module.exports = new webpack.DefinePlugin({
    searchURI: process.env.NODE_ENV === 'production'
        ? JSON.stringify('/api/_search/')
        : JSON.stringify('https://cai-einander-helfen-staging.fbi.h-da.de/api/_search/')
});
