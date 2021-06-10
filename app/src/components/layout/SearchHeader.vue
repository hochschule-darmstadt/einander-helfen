<template>
  <header class="header_layout">
    <v-btn
      class="d-none d-sm-flex justify-center mr-4"
      height="70px"
      width="80px"
      justify="left"
      rounded
      router
      depressed
      icon
    >
      <router-link to="/" exact>
        <v-img
          class="mt-1"
          width="80px"
          height="75px"
          src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Heart-hand-shake.svg/256px-Heart-hand-shake.svg.png"
        />
      </router-link>
    </v-btn>

    <SearchComponent class="search_bar" dark direktsearch small />

    <MenuButton />
  </header>
</template>

<script lang="ts">
import Vue from "vue";
import SearchComponent from "@/components/search/SearchComponent.vue";
import MenuButton from "@/components/layout/MenuButton.vue";

export default Vue.extend({
  name: "SearchHeader",
  components: {
    SearchComponent,
    MenuButton,
  },
  methods: {},
});
</script>

<style lang="scss" scoped>
.header_layout {
  padding: 12px;
  background: #00254f;
  display: flex;
  flex-direction: row;
  width: 100%;

  .search_bar {
    flex-grow: 1;
    margin-right: 30px;
  }
}
</style>

<style lang="scss">
/** global style */

// some hacks for optimal use of space in header
// only needed if the search component is used in this header
@media screen and (max-width: 599px) {
  .header_layout {
    .locationDiv {
      padding-top: 0px;
      & > div {
        width: calc(100% + 80px);
      }
    }
  }
}
@media screen and (max-width: 959px) {
  .header_layout {
    .menubutton {
      max-height: 50px;
    }
  }
}
</style>
