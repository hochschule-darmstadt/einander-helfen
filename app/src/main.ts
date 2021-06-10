import Vue from "vue";
import App from "@/App.vue";
import router from "@/router";
import store from "@/store/store";

// import vuetify
import Vuetify from "vuetify";

// import global css
import "@/assets/styles/style.scss";


// @ts-ignore
import de from "vuetify/es5/locale/de.js";

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
