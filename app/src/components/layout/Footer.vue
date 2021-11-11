<!-- The Footer contains links to other important pages of the website. -->

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
        { text: this.$t("home.footer.providerCap"), route: "/organizations" },
        { text: this.$t("home.footer.aboutUsCap"), route: "/about" },
        { text: this.$t("home.footer.impressumCap"), route: "/imprint" },
        { text: this.$t("home.footer.privacyPolicyCap"), route: "/privacy" },
      ],
    };
  },
});
</script>
