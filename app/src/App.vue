<template>
  <v-app>
    <v-main style="background: #00254f0c">
      <router-view></router-view>
    </v-main>
    <Footer />
    <ScrollTopButton />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
// import Toolbar from "@/components/layout/Toolbar.vue";
import Footer from "@/components/layout/Footer.vue";
import ScrollTopButton from "@/components/layout/ScrollTopButton.vue";

export default Vue.extend({
  name: "App",
  components: {
    Footer,
    ScrollTopButton,
    // Toolbar,
  },
});
</script>

<style lang="scss">
/** global style */
.v-menu__content {
  z-index: 1001 !important;
  border-radius: 4px !important;
}
</style>
