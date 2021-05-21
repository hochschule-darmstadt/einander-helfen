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
          <div class="pl-5 headline font-weight-light white--text">
            einander-helfen.org
          </div>
        </v-col>
        <v-col class="sloganCol">
          <div
            class="font-weight-bold pl-5 mt-5 title font-weight-light white--text"
          >
            Das schnelle Suchportal für Freiwilligenarbeit
          </div>
        </v-col>
        <v-col class="menuCol">
          <MenuButton />
        </v-col>
      </v-row>
    </v-layout>
  </v-app-bar>
</template>

<script>
import Vue from "vue";
import MenuButton from "@/components/layout/MenuButton.vue";

export default Vue.extend({
  name: "HeaderHome",
  components: {
    MenuButton,
  },
  data: function () {
    return {};
  },
});
</script>


<style lang="scss" scoped>
.header {
  .logoCol {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  .sloganCol {
    display: flex;
    justify-content: center;
    text-align: center;
    flex-grow: 2;
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
}
</style>
