<!-- This Header contains the logo, all components for searching and the burger menu. -->

<template>
  <header class="sticky_header" :class="{ expanded: expanded, fixed: fixed }">
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
  props: {
    fixed: {
      type: Boolean,
      default: false,
    },
  },
  data: function () {
    return {
      expanded: !this.fixed,
      scrollPosition: 0,
    };
  },
  watch: {
    fixed() {
      this.expanded = !this.fixed;
    },
  },
  mounted() {
    window.addEventListener("scroll", this.updateScroll);
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.updateScroll);
  },
  methods: {
    updateScroll() {
      const trashhold = 10; // px
      if (this.scrollPosition + trashhold < window.scrollY) {
        this.expanded = false;
        this.scrollPosition = window.scrollY;
      } else if (this.scrollPosition > window.scrollY) {
        this.scrollPosition = window.scrollY;
      }
    },
  },
});
</script>

<style lang="scss" scoped>
.sticky_header {
  padding: 12px;
  background: #00254f;
  width: 100%;

  &.fixed {
    position: fixed;
    top: 0;
    z-index: 1;
    & + section {
      position: relative;
      top: 100px;
    }
  }
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
    margin-top: -8px;
    margin-bottom: -8px;
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
// To move the next element after the header down if the header is sticky
.sticky_header.fixed + .container {
  padding-top: 200px !important;
}

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
