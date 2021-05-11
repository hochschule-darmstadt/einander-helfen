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
          @enter="paramChanged"
          @remove="removeTag"
        />
      </v-col>

      <v-col class="locationDiv" cols="12" :md="isFullwidth ? 12 : 6">
        <div>
          <AreaSelect tabindex="2" v-model="internationalValue" :dark="dark" />
          <LocationSearchBar
            tabindex="3"
            :dark="dark"
            :isInternational="isInternational"
            v-model="locationSearchValue"
            @enter="paramChanged"
            @click.native="onSearchClick"
          />
        </div>
        <div>
          <RadiusSelect
            tabindex="4"
            :dark="dark"
            :isInternational="isInternational"
            v-model="radius"
            @input="paramChanged"
            @enter="paramChanged"
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
      secondSearch: false,
    };
  },
  mounted(): void {
    this.$nextTick(() =>
      // set watcher after data initialisation
      this.$watch(
        // watch these parameters to detect change
        () => (
          // this.radius,
          this.internationalValue,
          // and to be sure that a different value is returned every time
          Date.now()
        ),
        // and execute paramChanged if a parameter change
        () => {
          this.paramChanged();
        }
      )
    );
  },
  watch: {
    // watch selectedRadius in store
    selectedRadius(value: string) {
      if (this.radius != value) this.radius = value;
    },
    // watch selectedLocation in store
    selectedLocation() {
      if (this.locationSearchValue != this.getLocationText())
        this.locationSearchValue = this.getLocationText() || "";
    },
    isInternational(value) {
      this.internationalValue = value;
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

    paramChanged(): void {
      if (this.direktsearch || this.secondSearch) this.executeSearch();
      else this.secondSearch = true;
    },
    executeSearch(): void {
      // update search parameter in store
      this.addSearchValue(this.searchValue);
      this.setSelectedLocation(this.locationSearchValue);
      this.setSelectedRadius(this.radius);
      this.setInternational(this.internationalValue);
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
