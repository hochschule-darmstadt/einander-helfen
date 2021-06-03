<template>
  <v-form class="searchbox" :class="{ fullwidth: isFullwidth }">
    <v-row justify="center" lg="2">
      <v-col class="searchCol" cols="12" :md="isFullwidth ? 12 : 6">
        <SearchBar
          tabindex="1"
          v-model="searchValue"
          :tags="searchValues"
          :enable-no-data-message="true"
          @click.native="onSearchClick"
          @enter="onSearchValueEnter"
          @remove="removeTag"
        />
      </v-col>

      <v-col class="locationDiv" cols="12" :md="isFullwidth ? 12 : 6">
        <div>
          <AreaSelect tabindex="2" v-model="internationalValue" :dark="dark" />
          <LocationSearchBar
            tabindex="3"
            :dark="dark"
            :isInternational="internationalValue"
            v-model="locationSearchValue"
            @enter="onLocationValueEnter"
            @click.native="onSearchClick"
          />
        </div>
        <div>
          <RadiusSelect
            tabindex="4"
            :dark="dark"
            :isInternational="internationalValue"
            v-model="radius"
            @input="onRadiusChanged"
            @enter="onRadiusChanged"
          />
          <SearchButton @click="executeSearch" tabindex="5" />
        </div>
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import Vue from "vue";
import LocationSearchBar from "@/components/search/LocationSearchBar.vue";
import RadiusSelect from "@/components/search/RadiusSelect.vue";
import SearchBar from "@/components/search/SearchBar.vue";
import SearchButton from "@/components/search/SearchButton.vue";
import AreaSelect from "@/components/search/AreaSelect.vue";
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";

/**
 * Emits @Search onSearch triggered event
 */
export default Vue.extend({
  name: "SearchComponent",
  components: {
    SearchBar,
    AreaSelect,
    LocationSearchBar,
    RadiusSelect,
    SearchButton,
  },
  props: {
    /**
     * define if the searchcomponent should be rendered smaller
     */
    small: {
      type: Boolean,
      default: false,
    },
    /**
     * define if the search should be executed by any value change
     */
    direktsearch: {
      type: Boolean,
      default: false,
    },
    dark: {
      type: Boolean,
      default: false,
    },
  },
  data: function () {
    return {
      searchValue: "",
      locationSearchValue: "",
      internationalValue: false,
      radius: "",
      oldValue: "",
    };
  },
  mounted() {
    // load internation value on startup else change it later by watcher
    this.internationalValue = this.isInternational;
  },
  watch: {
    // watch selectedRadius in store
    selectedRadius(value: string) {
      if (this.radius != value) this.radius = value;
    },
    // watch selectedLocation in store
    selectedLocation() {
      if (this.locationSearchValue != this.getLocationText())
        this.locationSearchValue = this.getLocationText();
    },
    // watch isInternational in store
    isInternational(value) {
      this.internationalValue = value;
    },
    internationalValue() {
      this.changeInternational();
    },
  },
  computed: {
    ...mapState("searchModule", [
      "searchValues",
      "selectedRadius",
      "selectedLocation",
      "isInternational",
    ]),
    isFullwidth(): boolean {
      return !this.small;
    },
  },
  methods: {
    ...mapGetters("searchModule", ["getLocationText"]),
    ...mapMutations("searchModule", [
      "setSelectedRadius",
      "setSelectedLocation",
      "addSearchValue",
      "removeSearchValue",
      "setInternational",
    ]),
    ...mapActions(["updateURIFromState"]),
    ...mapActions("postsModule", ["setSelectedPage"]),

    changeInternational(): void {
      // clear radius and location on international change
      this.radius = this.locationSearchValue = "";
      // set default radius in store
      this.setSelectedRadius();
      // unset location in stre
      this.setSelectedLocation();
      // update search parameter in store
      this.setInternational(this.internationalValue);
      // execute serach if directsearch is enabled
      if (this.direktsearch) {
        this.executeSearch();
      }
    },
    onSearchValueEnter(value: string): void {
      if (value != this.searchValue) this.searchValue = value;
      if (this.direktsearch || value == this.oldValue) {
        this.executeSearch();
      }
      this.oldValue = value;
    },
    onLocationValueEnter(value: string): void {
      if (value != this.locationSearchValue) this.locationSearchValue = value;
      if (this.direktsearch || value == this.oldValue) {
        this.executeSearch();
      }
      this.oldValue = value;
    },
    onRadiusChanged(value: string): void {
      if (value != this.radius) {
        this.radius = value;
      }
      // update state search parameter in store
      this.setSelectedRadius(this.radius);
      // execute serach if directsearch is enabled
      if (this.direktsearch) {
        this.executeSearch();
      }
    },
    executeSearch(): void {
      // update state search parameter in store
      this.addSearchValue(this.searchValue);
      this.setSelectedLocation(this.locationSearchValue);
      // reset the page to the default page
      this.setSelectedPage();
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
      // remove tag
      this.removeSearchValue(tag);
      // update uri
      this.updateURIFromState();
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
    display: flex;
    align-items: center;
    &:first-child {
      flex-grow: 1;
    }
    > div {
      margin-right: 8px;
    }
  }
}

@media (max-width: 599px) {
  .locationDiv {
    flex-direction: column;
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
  @media (min-width: 800px) {
    .radius_select {
      width: 200px;
    }
  }
}

.searchbox:not(.fullwidth) {
  @media (min-width: 960px) {
    .locationDiv,
    .searchCol {
      padding: 0px 12px;
      padding-top: 6px;
    }
  }
}
</style>
