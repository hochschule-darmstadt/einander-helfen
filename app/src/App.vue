<template>
  <v-app>
    <v-main style="background: #00254f0c">
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
  components: {
    Footer,
    // Toolbar,
  },
});
</script>



<style lang="scss">
/** global style */

html,
body {
  overflow-x: hidden;
}

.v-menu__content {
  z-index: 1001 !important;
  display: inline-table;
  border-radius: 4px;
}

.btn-dark {
  background-color: rgb(5, 76, 102) !important;
}
</style>

