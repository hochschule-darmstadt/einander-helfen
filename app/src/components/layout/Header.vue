<template>
  <v-header color="grey lighten-4" padless>
     <v-row no-gutters>
        <v-btn justify="left" style="margin:0 10px"
            v-for="(link, index) in links"
            :key="index"
            color="grey"
            text
            rounded
            class="my-2"
            router
            :to="link.route">
            {{ link.text }}
        </v-btn>

         <v-spacer></v-spacer>
        <v-col cols="4" md="4" style="background: #eee; border-radius: 20px; padding: 0px">
            <v-autocomplete
                style="margin-left: 10px; margin-right: 10px"
                append-icon="search"
                item-text="tag"
                :items="volunteerTags"
                v-model="searchResult"
                :search-input.sync="searchString"
                clearable
                @change="tagChange">
            </v-autocomplete>
            <v-chip-group column active-class="primary-text" style="margin-left: 10px; margin-right: 10px; margin-top: -20px">
                <v-chip v-for="tag in selectedTags" :key="tag" close @click:close="remove(tag)">
                    {{ tag }}
                </v-chip>
            </v-chip-group>
        </v-col>
         
        <v-col cols="2" md="2">
            <v-autocomplete
                    style="margin-left: 10px; margin-right: 10px;"
                label="Standort"
                :items="volunteerCities"
                v-model="selectedCity"
                prepend-inner-icon="place">
                Mein Standort
            </v-autocomplete>
        </v-col>

        <v-col  cols="1" md ="1">
            <v-autocomplete
                label="Umkreis"
                :items="volunteerRadius"
                v-model="selectedRadius">
                Überall
            </v-autocomplete>
        </v-col>
         <v-spacer></v-spacer>
     </v-row>
  </v-header>
</template>

<script>
export default {
  data: () => ({
    links: [
      { text: 'Logo', route: '/' },
    ],
      volunteerTags: [
          { header: 'Vorschläge' },
          { divider: true },
          { tag: 'Macher/in' },
          { tag: 'Denker/in' },
          { tag: 'Jugendarbeit' }
      ],
      volunteerCities: [
          'Main Standort',
          'Darmstadt',
          'Frankfurt am Main',
          'Wiesbaden',
          'Mainz'
      ],
      volunteerRadius: ['Überall', '5 km', '10 km', '25 km', '50 km'],
      selectedCity: '',
      selectedRadius: '',

      selectedTags: [],
      searchResult: null,
      searchString: ''
  }),
    methods: {
      remove(tag) {
          const index = this.selectedTags.indexOf(tag, 0);
          if (index >= 0) {
              this.selectedTags.splice(index, 1);
          }
        },
        tagChange(tag) {
          this.selectedTags.push(tag);
          this.$nextTick(() => {
              this.searchString = '';
              this.searchResult = null;
          });
        }
    }
};
</script>

<style scoped>
</style>
