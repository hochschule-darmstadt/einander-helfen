<template>
  <v-row justify="center">
            <v-autocomplete
              prepend-inner-icon="place"
              label="Standort"
              :filter="filterLocations"
              :items="getLocations()"
              :item-text="getItemText"
              item-value="plz"
              v-model="selectedLocation"
              style="margin-left: 10px; margin-right: 10px;"
              >
            </v-autocomplete>
  </v-row>
</template>

<script lang="ts">
import {mapActions, mapGetters, mapState} from 'vuex';
import Location from '@/models/location';

declare var require: any;
import Vue from 'vue';

import QueryBuilder from 'es-query-builder/dist';
import axios from 'axios';

export default Vue.extend({
    data(): {
    selectedLocation: string,
    selectedRadius: string,
    isSearching: boolean,
     } {
    return {
      isSearching: false,
      selectedLocation: '',
      selectedRadius: '',
    };
  },
  computed: {
    showLocations(): Location[] {
      return this.getLocations();
    }
  },
  watch: {
    selectedLocation(newValue, oldValue): void {
      if (newValue != '' && newValue != oldValue) {
        this.isSearching = false;
      }
      this.setLocationSearchValue(newValue); // newValue HAS to be a string
    },
    // Clear LocationSearchValue so that searching is not filtered to the currently selected zip-code
    isSearching(newValue, oldValue): void {
      if ((newValue == 'true' || newValue == '1') && newValue != oldValue) {
        this.setLocationSearchValue();
      }
    }
  },
  methods: {
    ...mapActions(['setLocationSearchValue']),
    ...mapGetters(['getLocations']),
    filterLocations(item: any, queryText: string, itemText: string): boolean {
      if (queryText) {
        this.isSearching = true;
        const search = (queryText + '').toLowerCase();
        const plz = item.plz + '';
        const name = (item.name + '').toLowerCase();
        const displayString = plz + ' '  + name;
        return name.indexOf(search) > -1 || plz.indexOf(search) > -1 || displayString.indexOf(search) > -1 || itemText.toLowerCase().indexOf(search) > -1;
      } else {
        return true;
      }
    },
    getItemText(item): string {
      return item.plz.toString() + ' ' + item.name.toString();
    }
  }
});
</script>
  
  

   

   