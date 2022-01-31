<!-- This Header contains the logo, the name of the website, some text and the burger menu.-->

<template>
  <v-app-bar class="header" flat height="100px" color="#00254f">
    <v-layout justify-space-between no-gutters color="#00254f">
      <v-row>
        <v-col class="logoCol">
          <v-app-bar-nav-icon width="80px" height="75px">
            <v-img
              width="80px"
              height="75px"
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Heart-hand-shake.svg/256px-Heart-hand-shake.svg.png"
            />
          </v-app-bar-nav-icon>
          <p class="headline pl-5 font-weight-light white--text">
            {{ $t("home.title") }}
          </p>
        </v-col>
        <v-col class="sloganCol">
          <span class="title font-weight-bold font-weight-light white--text">
            {{ $t("home.description") }}
          </span>
          <span class="subtitle font-weight-light white--text d-flex">
            <span class="mr-1">
              {{ $t("home.header.description1") }}
              {{ nationalCount.toLocaleString("de-DE") }}
              <span class="pl-1 pr-1">
                <img class="areImage" alt="Nationalflagge" :src="nationalImg" />
              </span>
              {{ $t("home.header.description2") }}
            </span>
            <span>
              {{ internationalCount.toLocaleString("de-DE") }}
              <span class="pl-1 pr-1">
                <img class="areImage" alt="Erdkugel" :src="internationalImg" />
              </span>
              {{ $t("home.header.description3") }}
            </span>
          </span>
        </v-col>
        <v-col class="menuCol">
          <MenuButton />
        </v-col>
      </v-row>
    </v-layout>
  </v-app-bar>
</template>

<script lang="ts">
import Vue from "vue";
import MenuButton from "@/components/layout/MenuButton.vue";
import PostService from "@/services/PostService";

export default Vue.extend({
  name: "MainHeader",
  components: {
    MenuButton,
  },
  data: function () {
    return {
      nationalCount: 0,
      nationalImg: require(`@/assets/images/area/${this.$i18n.locale}-Flag.png`),
      internationalCount: 0,
      internationalImg: require("@/assets/images/area/240px-Earth_icon_2.png"),
    };
  },
  async mounted() {
    // load internationalCount
    this.internationalCount = await PostService.countPosts(true);
    this.nationalCount = await PostService.countPosts(false);
  },
});
</script>

<style lang="scss" scoped>
.header {
  span {
    margin-bottom: unset;
  }
  span {
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  .logoCol {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  .sloganCol {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    flex-direction: column;
    flex-grow: 3;
    .subtitle > span {
      display: flex;
    }

    .areImage {
      border-radius: 50%;
      height: 17px;
      width: 17px;
    }
  }

  .menuCol {
    display: flex;
    justify-content: flex-end;
  }

  .menuCol ::v-deep .burgermenu {
    margin-top: unset;
  }

  @media (max-width: 766px) {
    .menuCol {
      flex-grow: 0;
    }
    .sloganCol {
      display: none !important;
    }
  }
  @media (min-width: 767px) and (max-width: 818px) {
    // give slogan more space because of long text
    .menuCol {
      flex-grow: 0;
    }
  }
  @media (max-width: 1144px) {
    .sloganCol .subtitle {
      flex-direction: column;
      align-items: center;
      > span {
        flex-shrink: 0;
      }
    }
  }
}
</style>
