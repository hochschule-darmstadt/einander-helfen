<template>
  <v-app class="app">
    <v-main class="main">
      <router-view></router-view>
    </v-main>
    <Footer />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
// import Toolbar from "@/components/layout/Toolbar.vue";
import Footer from "@/components/layout/Footer.vue";

export default Vue.extend({
  name: 'App',

  components: {
    Footer,
    // Toolbar,
  },
});
</script>

<style lang="scss" scoped>
.app {
  background: #00254f0c !important;
}
</style>

<style lang="scss">
/** global style */
@media screen and (min-width: 960px) {
  html,
  body {
    overflow: hidden !important;
    max-height: 100vh;
  }
}

.v-menu__content {
  z-index: 1001 !important;
  border-radius: 4px !important;
}

.btn-dark {
  background-color: rgb(5, 76, 102) !important;
}
</style>
