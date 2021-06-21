<!-- This Header contains the logo, all components for searching and the burger menu. -->

<template>
  <header class="header" :class="{ expanded: expanded }">
    <div class="header_layout">
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

      <SearchComponent
        class="search_bar"
        dark
        direktsearch
        small
        :expanded="expanded"
      />

      <MenuButton />
    </div>
    <div class="expantion_area d-sm-none" @click="expanded = !expanded">
      <v-icon class="icon" large>expand_more</v-icon>
    </div>
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
  data: function () {
    return {
      expanded: false,
    };
  },
});
</script>

<style lang="scss" scoped>
.header {
  padding: 12px 12px 0 12px;
  background: #00254f;
  width: 100%;
  // TODO: add transition

  .header_layout {
    display: flex;
    flex-direction: row;
    width: 100%;

    .search_bar {
      flex-grow: 1;
      margin-right: 30px;
    }
  }

  .expantion_area {
    text-align: center;
    width: 100%;
    margin-top: -5px;
    .icon {
      color: white;
    }
  }

  @media screen and (max-width: 600px) {
    $radius: 17px;
    border-bottom-left-radius: $radius;
    border-bottom-right-radius: $radius;

    &.expanded .expantion_area .icon {
      transform: rotate(180deg);
    }
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
