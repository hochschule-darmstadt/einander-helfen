<template>
  <div class="menubutton">
    <v-menu offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn v-bind="attrs" v-on="on" dark icon class="burgermenu">
          <v-icon>menu</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          v-for="(link, index) in links"
          :key="index"
          router
          :to="link.route"
        >
          <v-list-item-title>{{ link.text }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "MenuButton",
  data: function () {
    return {
      links: [
        { text: "Home", route: "/" },
        { text: "Organisationen", route: "/companies" },
        { text: "Über uns", route: "/about" },
        { text: "Impressum", route: "/imprint" },
        { text: "Datenschutzerklärung", route: "/privacy" },
      ],
    };
  },
});
</script>

<style lang="scss" scoped>
.menubutton {
  display: flex;
  align-items: center;
}

/*Mobile Layout*/
@media (min-width: 280px) and (max-width: 599px) {
  .burgermenu {
    margin-top: 19px;
    margin-right: 8px;
  }
}

@media (min-width: 600px) and (max-width: 765px) {
  .burgermenu {
    margin-top: 19px;
  }
}

/*Tablet Layout*/
@media (min-width: 600px) and (max-width: 959px) {
  .burgermenu {
    margin-top: 19.5px;
    margin-right: 8px;
  }
}
</style>
