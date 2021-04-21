<template>
  <v-form class="searchbox mt-8 mb-9">
    <v-row justify="center" lg="2">
      <v-col class="searchCol" cols="12">
        <SearchBar
          attachTo=".searchCol"
          tabindex="1"
          v-model="searchValue"
          :tags="searchTags"
          :enable-no-data-message="true"
          @click.native="onSearchBarClick"
          @enter="executeSearch"
          @remove="removeTag"
        />
      </v-col>

      <v-col cols="12" class="locationDiv">
        <AreaSelect attachTo=".locationDiv" v-model="area" tabindex="2" />
        <LocationSearchBar
          attachTo=".locationDiv"
          tabindex="3"
          :international="international"
          v-model="locationSearchValue"
          @enter="executeSearch"
          @click.native="focussearch"
        />
        <Radius
          tabindex="4"
          :international="international"
          v-model="radius"
          @enter="onRadiusEnter"
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

export default Vue.extend({
  name: "SearchComponent",
  components: {
    SearchBar,
    AreaSelect,
    LocationSearchBar,
    Radius,
    SearchButton,
  },
  data: function () {
    return {
      searchValue: "",
      searchTags: [] as string[],
      locationSearchValue: "",
      area: "germany",
      radius: null,
    };
  },
  mounted(): void {
    this.$store.commit("clearSearchParams");
  },
  computed: {
    international(): boolean {
      return this.area === "international";
    },
  },
  methods: {
    executeSearch(): void {
      // update search parameter
      this.$store.commit("addSearchValue", this.searchValue);
      this.$store.commit("setInternational", this.international);
      this.$store.commit("setLocationSearchValue", this.locationSearchValue);
      this.$store.commit("setSelectedRadius", this.radius);
      // todo radius
      // update uri
      this.$store.commit("updateURIFromState");
    },
    onSearchBarClick(): void {
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
      this.$store.commit("removeSearchValue", tag);
    },
  },
});
</script>

<style lang="scss">
.v-input__slot {
  margin-bottom: 0;
}

img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.slick-arrow {
  display: none !important ;
  visibility: hidden;
}

#searchButton {
  margin-right: 0 !important;
}

#searchbox {
  padding-left: 12px;
  padding-right: 12px;
}

#container {
  margin: auto;
}

#locationDiv {
  padding-left: 12px !important;
  padding-right: 12px !important;
}

@media (min-width: 800px) {
  #container {
    max-width: 1450px;
  }
}

@media (min-width: 960px) {
  #container {
    width: 960px;
    max-width: none;
  }
}

@media (min-width: 1100px) {
  #container {
    width: 1100px;
  }
}

@media (min-width: 1300px) {
  #container {
    width: 1300px;
  }
}

@media (min-width: 1618px) {
  #container {
    width: 1618px;
  }
}

@media (min-width: 1904px) {
  #container {
    width: 85%;
  }
}
</style>
