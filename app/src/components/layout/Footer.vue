<template>
  <v-footer color="#00254f" padless>
    <v-row justify="center" no-gutters>
      <v-btn
        v-for="(link, index) in links"
        :key="index"
        color="white"
        text
        rounded
        class="my-2"
        router
        :to="link.route"
      >
        {{ link.text }}
      </v-btn>
    </v-row>
  </v-footer>
</template>

<script>
import Vue from "vue";

export default Vue.extend({
  name: "Footer",
  data: function () {
    return {
      links: [
        { text: "Über uns", route: "/about" },
        { text: "Impressum", route: "/imprint" },
        { text: "Datenschutzerklärung", route: "/privacy" },
      ],
    };
  },
});
</script>
