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
    :hide-no-data="true"
    :append-icon="shownLocations.length > 0 ? '$dropdown' : ''"
    v-model="locationSearchValue"
    @keyup.self="locationOnKeyUp"
    @keyup.enter="onEnter"
    @focus="clearOnFocus"
    @change="onInputChange"
  />
</template>

<script lang="ts">
import Vue from "vue";
import Location from "@/models/location";
import LocationService from "@/utils/services/LocationService";

export default Vue.extend({
  name: "LocationSearchBar",
  props: {
    value: {
      type: String,
      required: true,
    },
    international: {
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
      locationSearchValue: this.value,
    };
  },
  computed: {
    shownLocations(): Location[] {
      return this.international
        ? LocationService.findCountryByName(this.locationSearchValue)
        : LocationService.findLocationByPlzOrName(this.locationSearchValue);
    },
    hintText(): string {
      return this.international ? "Land" : "Ort oder PLZ";
    },
  },
  mounted(): void {
    this.locationSearchValue = this.value;
  },
  watch: {
    /** change selection on value change */
    value(): void {
      this.locationSearchValue = this.value;
    },
    international(): void {
      this.locationSearchValue = "";
    },
  },
  methods: {
    /**
     * used by the autocomplete component
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
          this.locationSearchValue = plz[0];
        } else {
          this.locationSearchValue = curValue;
        }
      }
    },
    clearOnFocus(evt): void {
      if (!evt.target.value) {
        this.locationSearchValue = "";
        this.$emit("input", this.locationSearchValue);
      }
    },
    onInputChange(): void {
      // reduce to only one word
      this.locationSearchValue = this.locationSearchValue.split(" ")[0];
      this.$emit("input", this.locationSearchValue);
    },
    onEnter(): void {
      this.$emit("input", this.locationSearchValue);
      this.$emit("enter");
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
