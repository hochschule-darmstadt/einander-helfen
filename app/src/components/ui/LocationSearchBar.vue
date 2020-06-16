<template>
  <v-row justify="center">
            <v-autocomplete
              prepend-inner-icon="place"
              label="Standort"
              :filter="filterLocations"
              :items="showLocations"
              item-text="title"
              item-value="title"
              v-model="selectedLocation"
              style="margin-left: 10px; margin-right: 10px;"
              v-on:keyup.self="locationOnKeyUp"
              auto-select-first
              v-on:keyup.enter="routeToResultPage"
              >
            </v-autocomplete>
  </v-row>

</template>

<script lang="ts">
  import {mapActions, mapGetters, mapState} from 'vuex';
  import Location from '../../models/location';

  declare var require: any;
  import Vue from 'vue';

  import QueryBuilder from 'es-query-builder/dist';
  import axios from 'axios';

  export default Vue.extend(
    {
      data(): {
        selectedLocation: string,
        isSearching: boolean,
      } {
        return {
          isSearching: false,
          selectedLocation: this.$store.state.selectedLocation || '',
        };
      },
      computed: {
        showLocations(): Location[] {
          const locations: Location[] = this.getLocations();
          const filteredLocations: any = locations.map((location) => {
            const title = location.plz + ' ' + location.name;
            return Object.assign({}, location, {title});
          });
          console.log(filteredLocations);
          return filteredLocations;
        }
      },
      watch: {
        selectedLocation(newValue, oldValue): void {
          if (newValue !== '' && newValue !== oldValue) {
            this.isSearching = false; //
          }
          if (newValue) {
            this.setLocationSearchValue(newValue.split(' ')[0]);
          } else {
            this.setLocationSearchValue(''); // newValue HAS to be a string
          }
          this.setSelectedLocation(newValue);
          if (this.$route.name === 'resultPage') {
            this.$router.push({
              name: 'resultPage',
              query: {
                q: this.$route.query.q,
                location: newValue,
                radius: this.$route.query.radius
              }
            });
          } /*else {
          }*/

        },
        // Clear LocationSearchValue so that searching is not filtered to the currently selected zip-code
        isSearching(newValue, oldValue): void {
          if ((newValue === 'true' || newValue === '1') && newValue !== oldValue) {
            this.setLocationSearchValue();
          }
        }
      },
      methods: {
        ...mapActions(['setLocationSearchValue', 'setSelectedLocation']),
        ...mapGetters(['getLocations']),
        filterLocations(item: any, queryText: string, itemText: string): boolean {
          if (queryText) {
            this.isSearching = true;
            const search = (queryText + '').toLowerCase();
            const plz = item.plz + '';
            const name = (item.name + '').toLowerCase();
            const displayString = plz + ' '  + name;
            return name.indexOf(search) > -1 ||
                plz.indexOf(search) > -1 ||
                displayString.indexOf(search) > -1 ||
                itemText.toLowerCase().indexOf(search) > -1;
          } else {
            return true;
          }
        },
        getItemText(item): string {
          return item.plz.toString() + ' ' + item.name.toString();
        },
        getItemValue(item): any {
          return item.plz;
        },
        locationOnKeyUp(evt): void {
          if (evt.code.startsWith('Key') || evt.code.startsWith('Digit') || evt.code === 'Backspace') {
            const curValue = evt.target.value;
            const plz = curValue.match(/^\d+/);
            if (plz) {
              this.setLocationSearchValue(plz[0]);
            } else {
              this.setLocationSearchValue(curValue);
            }
          }
        },
        routeToResultPage(evt): void {
          this.$router.push({
              name: 'resultPage',
              query: {
                q: this.$store.state.selectedTag,
                location: this.selectedLocation,
                radius: this.$store.state.radiusSearchValue
              }
            });
        },
      },
    }
  );
</script>
  
  

   

   