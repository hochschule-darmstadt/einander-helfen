<template>
  <v-form class="searchbox" :class="{ fullwidth: isFullwidth }">
    <v-row justify="center" lg="2">
      <v-col
        class="searchCol"
        cols="12"
        :md="isFullwidth ? 12 : 5"
        :lg="isFullwidth ? 12 : 6"
      >
        <SearchBar
          tabindex="1"
          v-model="searchValue"
          :tags="searchTags"
          :enable-no-data-message="true"
          @click.native="onSearchClick"
          @enter="executeSearch"
          @remove="removeTag"
        />
      </v-col>

      <v-col
        class="locationDiv"
        cols="12"
        :md="isFullwidth ? 12 : 7"
        :lg="isFullwidth ? 12 : 6"
      >
        <AreaSelect tabindex="2" v-model="area" :dark="dark" />
        <LocationSearchBar
          tabindex="3"
          :dark="dark"
          :international="international"
          v-model="locationSearchValue"
          @enter="executeSearch"
          @click.native="onSearchClick"
        />
        <Radius
          tabindex="4"
          :dark="dark"
          :international="international"
          v-model="radius"
          @enter="executeSearch"
        />
        <SearchButton @click="executeSearch" tabindex="5" />
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import Vue from "vue";
import LocationSearchBar from "@/components/search/LocationSearchBar.vue";
import Radius from "@/components/search/Radius.vue";
import SearchBar from "@/components/search/SearchBar.vue";
import SearchButton from "@/components/search/SearchButton.vue";
import AreaSelect from "@/components/search/AreaSelect.vue";
import { mapActions, mapGetters } from "vuex";

/**
 * Emits @Search onSearch triggered event
 */
export default Vue.extend({
  name: "SearchComponent",
  components: {
    SearchBar,
    AreaSelect,
    LocationSearchBar,
    Radius,
    SearchButton,
  },
  props: {
    fullwidth: {
      type: Boolean,
      default: true,
    },
    dark: {
      type: Boolean,
      default: false,
    },
  },
  data: function () {
    return {
      searchValue: "",
      searchTags: [] as string[],
      locationSearchValue: "",
      area: "germany",
      radius: "",
    };
  },
  mounted(): void {
    // load data from store
    this.area = this.getInternational ? "international" : "germany";
    this.radius = this.getRadius;
    this.searchTags = this.getSearchValues;
    this.locationSearchValue = this.getLocationText;
  },
  computed: {
    ...mapGetters("locationSearchModule", ["getRadius", "getLocationText"]),
    ...mapGetters("textSearchModule", ["getSearchValues"]),
    ...mapGetters(["getInternational"]),

    international(): boolean {
      return this.area === "international";
    },
    isFullwidth(): boolean {
      return this.fullwidth;
    },
  },
  methods: {
    ...mapActions("locationSearchModule", [
      "setSelectedRadius",
      "setSelectedLocation",
    ]),
    ...mapActions("textSearchModule", ["addSearchValue", "removeSearchValue"]),
    ...mapActions(["setInternational", "updateURIFromState"]),

    executeSearch(): void {
      // add search value to tags
      if (this.searchValue) this.searchTags.push(this.searchValue);
      // update search parameter in store
      this.addSearchValue(this.searchValue);
      this.setInternational(this.international);
      this.setSelectedLocation(this.locationSearchValue);
      this.setSelectedRadius(this.radius);
      // emit search event
      this.$emit("search");
      // update uri
      this.updateURIFromState();
      // clear search field
      this.searchValue = "";
    },
    onSearchClick(): void {
      const isSafari =
        navigator.vendor &&
        navigator.vendor.indexOf("Apple") > -1 &&
        navigator.userAgent &&
        navigator.userAgent.indexOf("CriOS") === -1 &&
        navigator.userAgent.indexOf("FxiOS") === -1;

      const focussearch = document.getElementById("searchCol");

      if (
        isSafari === false &&
        focussearch !== null &&
        window.matchMedia("(max-width: 420px)").matches
      ) {
        focussearch.scrollIntoView(true);
      }
    },
    removeTag(tag: string) {
      this.searchTags = this.searchTags.filter((item) => item != tag);
      this.removeSearchValue(tag);
    },
  },
});
</script>

<style lang="scss" scoped>
.searchbox {
  ::v-deep .v-input__slot {
    margin-bottom: 0;
  }
}

.locationDiv {
  display: flex;
  flex-direction: row;

  > div {
    margin-right: 8px;
  }
}

@media (max-width: 599px) {
  .locationDiv {
    flex-wrap: wrap;
  }
}

@media (max-width: 959px) {
  .locationDiv {
    padding-bottom: 0px;
  }
  .searchCol {
    padding-top: 0px;
  }
}

.searchbox.fullwidth {
  @media (max-width: 390px) {
    .radius_select {
      flex-basis: 0;
    }
  }
}

.searchbox:not(.fullwidth) {
  @media (max-width: 480px) {
    .radius_select {
      flex-basis: 0;
    }
  }

  @media (min-width: 960px) {
    .locationDiv,
    .searchCol {
      padding: 0px 12px;
      padding-top: 6px;
    }
  }
}
</style>

<style lang="scss">
.searchbox .v-menu__content {
  z-index: 1001 !important;
  display: inline-table;
  border-radius: 4px;
}
</style>
