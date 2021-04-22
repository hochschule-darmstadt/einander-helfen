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
          attachTo=".locationDiv"
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
import LocationSearchBar from "@/components/ui/LocationSearchBar.vue";
import Radius from "@/components/ui/Radius.vue";
import SearchBar from "@/components/ui/SearchBar.vue";
import SearchButton from "@/components/ui/SearchButton.vue";
import AreaSelect from "@/components/ui/AreaSelect.vue";

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
      radius: { text: "Überall", value: "" },
    };
  },
  mounted(): void {
    // TODO: load data from store

    this.$store.commit("clearSearchParams");
  },
  computed: {
    international(): boolean {
      return this.area === "international";
    },
    isFullwidth(): boolean {
      return this.fullwidth;
    },
  },
  methods: {
    executeSearch(): void {
      // add search value to tags
      if (this.searchValue) this.searchTags.push(this.searchValue);
      // update search parameter
      this.$store.commit("addSearchValue", this.searchValue);
      this.$store.commit("setInternational", this.international);
      this.$store.commit("setLocationSearchValue", this.locationSearchValue);
      this.$store.commit("setSelectedRadius", this.radius);
      // emit search event
      this.$emit("search");
      // update uri
      this.$store.commit("updateURIFromState");
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
      this.$store.commit("removeSearchValue", tag);
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
  /** TODO Umbruch zu mobile header */
}

@media (max-width: 959px) {
  .locationDiv {
    padding-bottom: 0px;
  }
  .searchCol {
    padding-top: 0px;
  }
}
@media (min-width: 960px) {
  .locationDiv,
  .searchCol {
    padding: 0px 12px;
    padding-top: 6px;
  }
}
</style>

<style lang="scss">
.searchbox .v-menu__content {
  z-index: 999 !important;
  display: inline-table;
}
</style>
