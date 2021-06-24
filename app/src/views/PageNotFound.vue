<!-- The 'Page not found' page that is shown on 404 errors. -->

<template>
  <div class="pageNotFound">
    <Header />
    <section class="container pt-6 text-center fill-height">
      <img src="/images/robot.png" class="mb-6" :width="width" />
      <h1>Seite konnte nicht gefunden werden</h1>
      <p class="mt-3 mb-8">
        Es tut uns Leid. Die von Ihnen gesuchte Seite existiert nicht (mehr).
        Bitte stellen Sie sicher, dass die URL korrekt ist oder kehren Sie zur
        Startseite zurück.
      </p>
      <v-btn href="/" class="btn-dark" dark>
        <v-icon class="mr-3">home</v-icon>
        Zurück zur Startseite
      </v-btn>
    </section>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Header from "@/components/layout/SearchHeader.vue";

export default Vue.extend({
  name: "PageNotFound",
  components: {
    Header,
  },
  computed: {
    width() {
      switch (this.$vuetify.breakpoint.name) {
        case "xs":
          return "100";
        case "sm":
          return "150";
        case "md":
          return "250";
        default:
          return "300";
      }
    },
  },
});
</script>

<style lang="scss" scoped>
.pageNotFound {
  display: flex;
  align-content: stretch;
  flex-direction: column;
  height: 100%;
}

.container {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
</style>
