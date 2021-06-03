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
import VueMatomo from "vue-matomo";

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
    debug: true,
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
  render: (h) => h(App),
}).$mount("#app");
