<!-- The burger contains the navigation to every page of the website. -->

<template>
  <div class="menubutton">
    <v-menu offset-y fixed>
      <template v-slot:activator="{ on, attrs }">
        <v-btn v-bind="attrs" v-on="on" dark icon class="burgermenu">
          <v-icon class="menuicon">menu</v-icon>
        </v-btn>
      </template>
      <v-list class="pa-0">
        <template v-for="(link, index) in links">
          <v-list-item :key="link.text" router :to="link.route" color="#00254f">
            <v-list-item-icon>
              <v-icon v-if="link.icon" v-text="link.icon" />
            </v-list-item-icon>
            <v-list-item-title class="pr-2" v-text="link.text" />
          </v-list-item>
          <v-divider v-if="index < links.length - 1" :key="link.icon" />
        </template>
      </v-list>
    </v-menu>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

// icons can be found here: https://fonts.google.com/icons
//$t may look like an error, but it isn't
export default Vue.extend({
  name: "MenuButton",
  data: function () {
    return {
      links: [
        {
          text: this.$t("home.menu.home"),
          route: "/",
          icon: "home",
        },
        {
          text: this.$t("home.menu.provider"),
          route: "/organizations",
          icon: "groups",
        },
        { text: this.$t("home.menu.aboutUs"), route: "/about", icon: "group" },
        {
          text: this.$t("home.menu.impressum"),
          route: "/imprint",
          icon: "gavel",
        },
        {
          text: this.$t("home.menu.privacyPolicy"),
          route: "/privacy",
          icon: "privacy_tip",
        },
      ],
    };
  },
});
</script>

<style lang="scss" scoped>
.menubutton {
  display: flex;
  align-items: center;
  .menuicon {
    font-size: 32px;
  }
  /*Mobile Layout - Tablet Layout*/
  @media (min-width: 280px) and (max-width: 959px) {
    .burgermenu {
      margin-top: 19px;
      margin-right: 8px;

      .menuicon {
        font-size: 40px;
      }
    }
  }
}
</style>
