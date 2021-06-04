<!-- Part of the SearchComponent to select a location for the search. It's possible to select a city or postalcode for national searches or a county for international searchers -->

<template>
  <v-autocomplete
    class="location_search"
    prepend-inner-icon="place"
    item-text="title"
    item-value="title"
    auto-select-first
    :label="hintText"
    :filter="filterLocations"
    :items="shownLocations"
    :dark="dark"
    :attach="attachTo"
    :hide-no-data="true"
    :append-icon="shownLocations.length > 0 ? '$dropdown' : ''"
    v-model="location"
    @keyup.self="locationOnKeyUp"
    @keyup.enter="onEnter"
    @focus="onFocus"
    @change="onInputChange"
  />
</template>

<script lang="ts">
import Vue from "vue";
import Location from "@/models/location";
import LocationService from "@/services/LocationService";

export default Vue.extend({
  name: "LocationSearchBar",
  props: {
    value: {
      type: String,
      required: true,
    },
    isInternational: {
      type: Boolean,
      default: true,
    },
    dark: {
      type: Boolean,
      default: false,
    },
    attachTo: {
      type: String,
      default: "",
    },
  },
  data: function () {
    return {
      location: this.value as string | undefined,
      searchValue: "",
    };
  },
  computed: {
    shownLocations(): Location[] {
      const q = this.searchValue || this.location || "";
      return this.isInternational
        ? LocationService.findCountryByName(q)
        : LocationService.findLocationByPlzOrName(q);
    },
    hintText(): string {
      return this.isInternational ? "Land" : "Ort oder PLZ";
    },
  },
  mounted(): void {
    this.location = this.value;
  },
  watch: {
    /** change selection on value change */
    value(): void {
      this.$nextTick(() => {
        this.location = this.searchValue = this.value;
      });
    },
    isInternational(): void {
      this.searchValue = "";
      this.location = "";
    },
  },
  methods: {
    /**
     * Filter all locations based on the user input to give proposals instead of giving the full location item list.
     * The postcode and location name are taken into account.
     *
     * @param {any} item: The current location item to check if it matches the user input.
     * @param {string} querText: The user input.
     * @param {string} itemText: The text value of the item.
     * @return {boolean}:  If the checked item should be display in the proposal list.
     */
    filterLocations(item: any, queryText: string, itemText: string): boolean {
      if (queryText) {
        const search = queryText.toLowerCase();

        const name = item.name.toLowerCase();
        let plz = "";
        let displayString = name;
        if (item.plz) {
          plz = item.plz;
          displayString = plz + " " + displayString;
        }
        return (
          name.includes(search) ||
          plz.includes(search) ||
          displayString.includes(search) ||
          itemText.toLowerCase().includes(search)
        );
      } else return true;
    },
    /**
     * This event is triggert after every new input key. It will update the valie of the LocationSearchBar
     * and if the whole input was deleted it will immediately start a search.
     */
    locationOnKeyUp(evt): void {
      const handleDesktop =
        evt.code.startsWith("Key") ||
        evt.code.startsWith("Digit") ||
        evt.code === "Backspace";
      const handleMobile =
        Number.isInteger(evt.key) ||
        evt.key.match(/[a-z]/i) ||
        evt.key === "Backspace";
      if (handleDesktop || handleMobile) {
        const curValue = evt.target.value;
        const plz = curValue.match(/^\d+/);
        if (plz) {
          this.searchValue = plz[0];
        } else {
          this.searchValue = curValue;
          // emit event by clearing field
          if (!curValue) {
            this.location = "";
            this.$emit("input", this.location);
          }
        }
      }
    },
    /**
     * Clear search value on focus.
     */
    onFocus(evt): void {
      if (!evt.target.value) {
        this.searchValue = "";
      }
    },
    /**
     * Reduce to only one word.
     */
    onInputChange(): void {
      this.searchValue = this.searchValue.split(" ")[0];
      this.$emit("input", this.location);
    },
    onEnter(): void {
      this.searchValue = this.location || "";
      this.$emit("enter", this.location);
    },
  },
});
</script>

<style lang="scss" scoped>
.location_search {
  .v-menu__content {
    z-index: 9999 !important;
  }

  .v-text-field {
    padding-right: 5px;
  }
}

@media (min-width: 280px) and (max-width: 305px) {
  .location_search {
    max-width: 77vw;

    .v-input__slot {
      margin-left: 2px;
    }

    .v-text-field {
      padding-right: 0px !important;
    }
  }
}

@media (min-width: 305px) and (max-width: 342px) {
  #location_search {
    max-width: 79.5vw;

    .v-input__slot {
      margin-left: 2px;
    }

    .v-text-field {
      padding-right: 0px !important;
    }
  }
}

@media (min-width: 315px) and (max-width: 382px) {
  #headerLocation .v-autocomplete__content.v-menu__content {
    max-height: 225px !important;
    overflow-y: scroll;
    overflow-x: hidden;
  }
}

@media (min-width: 342px) and (max-width: 383px) {
  #location_search {
    max-width: 98vw;

    .v-autocomplete__content.v-menu__content {
      max-height: 225px !important;
      overflow-y: scroll;
      overflow-x: hidden;
    }
  }
}

@media (min-width: 383px) {
  #location_search {
    max-width: 98vw;

    .v-input__slot {
      margin-left: 2px;
    }
  }
}

@media (min-width: 410px) {
  #location_search {
    max-width: 98vw;

    .v-input__slot {
      margin-left: 2px;
    }
  }
}

@media (min-width: 535px) {
  #location_search {
    width: auto;
    max-width: none;

    .v-text-field {
      padding-right: 0px;
    }
  }
}
</style>
