import Vue from "vue";
import App from "@/App.vue";
import router from "@/router";
import store from "@/store/store";

import Vuetify from "vuetify";
import VueMatomo from "vue-matomo";
import VueMeta from "vue-meta";

// import vuetify css
import "vuetify/dist/vuetify.min.css";

// import matierial design icons
import "material-design-icons-iconfont/dist/material-design-icons.css";

// import global css
import "@/assets/styles/style.scss";

// @ts-ignore
import de from "vuetify/es5/locale/de.js";

import i18n from "./i18n";

Vue.config.productionTip = false;

Vue.use(Vuetify);
Vue.use(VueMeta);

const vuetify = new Vuetify({
  lang: {
    locales: { de },
    current: "de",
  },
  icons: {
    iconfont: "mdiSvg",
  },
});

function statisticsEnabled() {
  return (
    process.env.VUE_APP_ENABLE_STATISTICS === "true" ||
    process.env.VUE_APP_ENABLE_STATISTICS === "True" ||
    process.env.VUE_APP_ENABLE_STATISTICS === "1"
  );
}

if (statisticsEnabled()) {
  Vue.use(VueMatomo, {
    host: "https://einander-helfen.org/api/analytics",
    siteId: 1,
    trackerFileName: "matomo",
    router: router,
    enableLinkTracking: true,
    requireConsent: false,
    trackInitialView: true,
    disableCookies: true,
    enableHeartBeatTimer: false,
    heartBeatTimerInterval: 0,
    debug: false,
    userId: undefined,
    cookieDomain: undefined,
    domains: undefined,
    preInitActions: [],
  });
}

new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: (h) => h(App),
}).$mount("#app");
