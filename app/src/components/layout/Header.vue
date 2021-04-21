<template>
  <header>
    <v-layout
      id="header"
      row
      wrap
      align-center
      no-gutters
      style="padding: 12px; background: #00254f"
    >
      <div id="headerLeft">
        <v-btn
          id="headerLogo"
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
        <div id="searchBar">
          <search-bar
            ref="searchBar"
            @input="addSearchValueAndUpdate"
            :searchInput.sync="currentSearchValue"
            :enable-no-data-message="true"
          />
          <v-spacer></v-spacer>
          <v-chip-group
            active-class="primary-text"
            column
            style="margin-left: 10px; margin-right: 10px; margin-top: -20px"
          >
            <v-chip
              :key="tag"
              @click:close="removeSearchValueAndUpdate(tag)"
              close
              v-for="tag in searchValues"
              >{{ tag }}</v-chip
            >
          </v-chip-group>
        </div>
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              id="burgermenu_mobile"
              class="hidden-md-and-up"
              v-bind="attrs"
              v-on="on"
              dark
              icon
            >
              <v-icon>menu</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item
              v-for="(link, index) in links"
              :key="index"
              router
              :to="link.route"
            >
              <v-list-item-title>{{ link.text }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>

      <div id="headerRight">
        <div id="headerAreaLocation">
          <area-select
            id="areaSelect"
            ref="areaSelect"
            @change="switchArea"
            :dark="true"
          />
          <location-search-bar
            class="xs"
            @input="updateResults"
            id="headerLocation"
            ref="locationSearchBar"
            :dark="true"
          />
        </div>
        <div id="radiusSearchBtn">
          <radius
            @input="updateResults"
            id="headerRadius"
            ref="radius"
            :dark="true"
          />
          <search-button
            id="headerSearchButton"
            @click="updateSearchValueFromCurrentInputAndUpdateResults"
          />
        </div>
      </div>

      <v-col class="column menuCol hidden-sm-and-down">
        <div align="right">
          <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                id="burgermenu_web"
                class="hidden-sm-and-down"
                v-bind="attrs"
                v-on="on"
                dark
                icon
              >
                <v-icon>menu</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(link, index) in links"
                :key="index"
                router
                :to="link.route"
              >
                <v-list-item-title>{{ link.text }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </div>
      </v-col>
    </v-layout>
  </header>
</template>

<script lang="ts">
import Vue from "vue";
import {
  createNamespacedHelpers,
  mapActions as mapStateActions,
  mapGetters,
} from "vuex";
const { mapActions, mapState } = createNamespacedHelpers("textSearchModule");
import AreaSelect from "@/components/ui/AreaSelect.vue";
import LocationSearchBar from "@/components/ui/LocationSearchBar.vue";
import Radius from "@/components/ui/Radius.vue";
import SearchBar from "@/components/ui/SearchBar.vue";
import SearchButton from "@/components/ui/SearchButton.vue";

export default Vue.extend({
  components: {
    AreaSelect,
    LocationSearchBar,
    Radius,
    SearchBar,
    SearchButton,
  },
  data(): {
    links: any;
    currentSearchValue: string;
  } {
    return {
      links: [
        { text: "Home", route: "/" },
        { text: "Über uns", route: "/about" },
        { text: "Impressum", route: "/imprint" },
        { text: "Datenschutzerklärung", route: "/privacy" },
      ],
      currentSearchValue: "",
    };
  },
  methods: {
    ...mapActions(["addSearchValue", "removeSearchValue"]),
    ...mapStateActions([
      "updateURIFromState",
      "findPosts",
      "setPage",
      "setSelectedPost",
      "setInternational",
    ]),
    updateResults(): void {
      // After changing the query we want to begin on page 1
      this.setPage(1);
      // We also want to deselect the current selected post!
      this.setSelectedPost(null);
      this.findPosts();
    },
    addSearchValueAndUpdate(input): void {
      this.addSearchValue(input);
      this.$nextTick(() => {
        // @ts-ignore
        this.$refs.searchBar.clearInput();
      });
      this.updateResults();
    },
    removeSearchValueAndUpdate(element): void {
      this.removeSearchValue(element);
      this.updateResults();
    },
    updateSearchValueFromCurrentInputAndUpdateResults(): void {
      if (this.currentSearchValue) {
        this.addSearchValueAndUpdate(this.currentSearchValue);
      } else {
        this.updateResults();
      }
    },
    switchArea(): void {
      // @ts-ignore
      const areaSelect = this.$refs.areaSelect as AreaSelect;
      // @ts-ignore
      const areaSelection = (this.$refs.areaSelect as AreaSelect).selection;
      const international =
        areaSelection === areaSelect.items[0].title ? false : true;
      (this.$refs.locationSearchBar as any).setLocationSearchBar(international);
      (this.$refs.radius as any).disableRadius(international);
      (this.$refs.locationSearchBar as any).setSelectedLocation(null);

      if (international !== this.getInternational) {
        this.setInternational(international);
        this.updateResults();
      }
    },
  },
  computed: {
    ...mapState(["searchValues", "searchProposals"]),
    ...mapGetters(["getInternational"]),
  },
});
</script>

<style>
.v-menu__content {
  z-index: 9999 !important;
}

#searchBar {
  background: white;
  border-radius: 20px;
  margin-right: 2%;
  width: inherit;
}

#headerLeft {
  display: contents;
  width: 43%;
}

#headerRight {
  display: inherit;
  width: 40%;
}

#headerAreaLocation {
  display: flex;
}

/*Mobile Layout*/
@media (min-width: 280px) and (max-width: 599px) {
  #header {
    display: block;
  }

  #headerLeft {
    width: 100%;
    margin-bottom: 20px;
    display: flex;
  }

  #headerRight {
    width: 100%;
    display: block;
  }

  #searchBar {
    margin-right: 30px;
  }

  #headerLocation {
    margin-left: -10px;
    margin-right: -10px !important;
  }

  #radiusSearchBtn {
    display: flex;
  }

  #headerRadius {
    margin-left: 0px !important;
  }

  #headerSearchButton {
    margin-right: 0px !important;
  }

  #burgermenu_mobile {
    display: flex;
    margin-top: 19px;
    margin-right: 8px;
  }
}

/*Tablet Layout*/
@media (min-width: 600px) and (max-width: 959px) {
  #header {
    display: block;
  }

  #headerLeft {
    width: 100%;
    margin-bottom: 20px;
    display: flex;
  }

  #headerRight {
    width: 100%;
    display: flex;
  }

  #headerAreaLocation {
    margin-left: 95px;
    width: 70%;
  }

  #headerLocation {
    margin-left: -9px;
    margin-right: 0;
  }

  #searchBar {
    margin-right: 30px;
  }

  #headerRadius {
    margin-left: 0px !important;
  }

  #radiusSearchBtn {
    display: flex;
  }

  #headerSearchButton {
    margin-right: 73px !important;
  }

  #burgermenu_mobile {
    display: flex;
    margin-top: 19.5px;
    margin-right: 8px;
  }
}

@media (min-width: 600px) and (max-width: 765px) {
  #burgermenu_mobile {
    margin-top: 19px;
  }
}

/*Web Layout*/
@media (min-width: 960px) {
  #header {
    display: flex;
  }

  #headerLeft {
    display: contents;
  }

  #headerRight {
    display: inherit;
  }

  #radiusSearchBtn {
    display: flex;
  }

  #headerSearchButton {
    margin-right: 0px !important;
  }

  #headerAreaLocation {
    width: 100%;
  }

  #headerLocation {
    margin-left: 0px;
  }
}

@media (min-width: 960px) and (max-width: 1099px) {
  #headerLeft {
    width: 38.5%;
  }

  #headerRight {
    width: 44%;
  }

  #searchBar {
    margin-right: 1.2%;
  }
}

@media (min-width: 1100px) {
  #headerLeft {
    width: 41%;
  }

  #headerRight {
    width: 43.5%;
  }

  #searchBar {
    margin-right: 1.2%;
  }
}

@media (min-width: 1300px) {
  #headerLeft {
    width: 42.5%;
  }

  #headerRight {
    width: 42.5%;
  }

  #searchBar {
    margin-right: 1.2%;
  }
}

@media (min-width: 1618px) {
  #headerLeft {
    width: 43%;
  }

  #headerRight {
    width: 44.5%;
  }

  #searchBar {
    margin-right: 1.5%;
  }
}

@media (min-width: 1904px) {
  #headerLeft {
    width: 45%;
  }

  #headerRight {
    width: 42.5%;
  }

  #searchBar {
    margin-right: 1.5%;
  }
}

@media (min-width: 3000px) {
  #headerLeft {
    width: 46.5%;
  }

  #headerRight {
    width: 42%;
  }

  #searchBar {
    margin-right: 1.5%;
  }
}

@media (min-width: 4000px) {
  #headerLeft {
    width: 47%;
  }

  #headerRight {
    width: 41.5%;
  }

  #searchBar {
    margin-right: 1.5%;
  }
}

@media (min-width: 315px) and (max-width: 382px) {
  #headerLocation .v-autocomplete__content.v-menu__content {
    max-height: 225px !important;
    overflow-y: scroll;
    overflow-x: hidden;
  }
}

#headerLocation .v-autocomplete__content.v-menu__content {
  top: auto !important;
  left: auto !important;
  margin-top: 33px;
}
</style>

<style scoped>
@media (min-width: 960px) {
  #areaSelect {
    margin-right: 0;
  }
}
</style>
