import Vue from "vue";
import App from "@/App.vue";
import router from "@/router";
import store from "@/store/store";

import Vuetify from "vuetify";
import "material-design-icons-iconfont/dist/material-design-icons.css";

// @ts-ignore
import de from "vuetify/es5/locale/de.js";
import "vuetify/dist/vuetify.min.css";

import "material-design-icons-iconfont/dist/material-design-icons.css";

Vue.config.productionTip = false;

Vue.use(Vuetify);

const vuetify = new Vuetify({
  lang: {
    locales: { de },
    current: "de",
  },
  icons: {
    iconfont: "mdiSvg",
  },
});

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
