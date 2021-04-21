<template>
  <v-app>
    <Header />
    <v-content style="background: #00254f0c">
      <router-view></router-view>
    </v-content>
    <Footer />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
// import Toolbar from "@/components/layout/Toolbar.vue";
import Footer from "@/components/layout/Footer.vue";

export default Vue.extend({
  components: {
    Footer,
    // Toolbar,
  },
});
</script>
