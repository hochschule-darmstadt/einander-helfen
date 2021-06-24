<!-- Root of the whole application. It defines the template of the website and contains global styles -->

<template>
  <v-app class="app">
    <v-main class="main">
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

<style lang="scss" scoped></style>
