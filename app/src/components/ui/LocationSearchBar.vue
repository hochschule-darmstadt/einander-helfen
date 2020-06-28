<template>
  <v-row justify="center">
            <v-autocomplete
              prepend-inner-icon="place"
              label="Standort"
              :filter="filterLocations"
              :items="showLocations"
              item-text="title"
              item-value="title"
              v-bind:value="selectedLocation"
              @input="newSelectedLocation = $event"
              style="margin-left: 10px; margin-right: 10px;"
              v-on:keyup.self="locationOnKeyUp"
              auto-select-first
              v-on:keyup.enter="emitInput"
              :dark="dark"
              >
            </v-autocomplete>
  </v-row>

</template>

<script lang="ts">
  import { createNamespacedHelpers } from 'vuex';
  import Location from '@/models/location';

  const { mapState, mapActions, mapGetters } = createNamespacedHelpers('locationSearchModule');
  import Vue from 'vue';

  export default Vue.extend({
    props: {
      dark: {
        type: Boolean,
        default: false
      },
    },
      data(): {
        newSelectedLocation: string,
        isSearching: boolean
      } {
        return {
          isSearching: false,
          newSelectedLocation: ''
        };
      },
      computed: {
        ...mapState(['selectedLocation']),
        showLocations(): Location[] {
          return this.getLocations();
        }
      },
      watch: {
        newSelectedLocation(newValue, oldValue): void {
          if (newValue !== '' && newValue !== oldValue) {
            this.isSearching = false; //
          }
          if (newValue) {
            this.setLocationSearchValue(newValue.split(' ')[0]);
          } else {
            this.setLocationSearchValue(''); // newValue HAS to be a string
          }
          this.setSelectedLocation(newValue);
          this.emitInput(newValue);
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
            const search = queryText.toLowerCase();
            const plz = item.plz;
            const name = item.name.toLowerCase();
            const displayString = plz + ' '  + name;
            return name.includes(search) ||
                plz.includes(search) ||
                displayString.includes(search) ||
                itemText.toLowerCase().includes(search);
          } else {
            return true;
          }
        },
        locationOnKeyUp(evt): void {
          const handleDesktop = evt.code.startsWith('Key') || evt.code.startsWith('Digit') || evt.code === 'Backspace';
          const handleMobile = Number.isInteger(evt.key) || evt.key.match(/[a-z]/i) || evt.key === 'Backspace';
          if (handleDesktop || handleMobile) {
            const curValue = evt.target.value;
            const plz = curValue.match(/^\d+/);
            if (plz) {
              this.setLocationSearchValue(plz[0]);
            } else {
              this.setLocationSearchValue(curValue);
              if (!curValue) {
                this.setSelectedLocation('');
              }
            }
          }
        },
        emitInput(data: string = ''): void {
            if (!data) {
                data = this.selectedLocation;
            }
            this.$emit('input', data);
        },
      },
    }
  );
</script>





