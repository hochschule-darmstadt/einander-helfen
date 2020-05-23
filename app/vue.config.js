// vue.config.js
module.exports = {
    // options...
    devServer: {
        proxy: {
            '^/api': {
                    target: 'https://cai-einander-helfen.fbi.h-da.de/'
            }
        }
    }
};

