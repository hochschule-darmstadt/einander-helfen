<template>
    <header>
        <v-row
                no-gutters
                style="padding: 1vh; background: #00254f">
            <v-btn
                    :key="index"
                    :to="link.route"
                    height="75px"
                    width="80px"
                    justify="left"
                    rounded
                    router
                    v-for="(link, index) in links"
                    depressed
                    icon
                >{{ link.text }}  <v-img class="mt-1" width=80px height=75px src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Heart-hand-shake.svg/256px-Heart-hand-shake.svg.png"></v-img>
         </v-btn>
            <v-spacer></v-spacer>
            <v-col
                    cols="4"
                    md="4"
                    style="background: white; border-radius: 20px">
                <v-combobox
                        :items="volunteerProposals"
                        :search-input.sync="searchString"
                        @change="tagChange"
                        append-icon="search"
                        clearable
                        item-text="tag"
                        style="margin-left: 10px; margin-right: 10px"
                        v-bind:value="searchValue">
                </v-combobox>
                <v-chip-group
                        active-class="primary-text"
                        column
                        style="margin-left: 10px; margin-right: 10px; margin-top: -20px">
                    <v-chip
                            :key="tag"
                            @click:close="remove(tag)"
                            close
                            v-for="tag in selectedTags">
                        {{ tag }}
                    </v-chip>
                </v-chip-group>
            </v-col>

            <v-col
                    cols="2"
                    md="2">
                <v-autocomplete
                        dark
                        :items="volunteerCities"
                        label="Standort"
                        prepend-inner-icon="place"
                        style="margin-left: 10px; margin-right: 10px;"
                        v-model="selectedCity">
                    Mein Standort
                </v-autocomplete>
            </v-col>

            <v-col cols="1" md="1">
                <v-autocomplete
                        dark
                        :items="volunteerRadius"
                        label="Umkreis"
                        v-model="selectedRadius">
                    Überall
                </v-autocomplete>
            </v-col>
            <v-spacer></v-spacer>

            <v-btn
                    dark
                    style="margin-top: 1vh"
                    icon>
                <v-icon>more_vert</v-icon>
            </v-btn>
        </v-row>
    </header>
</template>

<script lang="ts">
    import Vue from 'vue';
    import {mapActions, mapState} from 'vuex';
    export default Vue.extend({
        data(): {
            links: any,
            volunteerProposals: any,
            volunteerTags: string[],
            volunteerCities: string[],
            volunteerRadius: string[],
            selectedCity: string,
            selectedRadius: string,
            selectedTags: string[],
            searchResult: null,
            searchString: string
        } {
            return {
                links: [
                    {text: '', route: '/'},
                ],
                volunteerProposals: [
                    {header: 'Vorschläge'},
                    {divider: true},
                    {tag: 'Macher/in'},
                    {tag: 'Denker/in'},
                    {tag: 'Jugendarbeit'}
                ],
                // TODO volunteerTags are currently not in use:
                // volunteerTags need to be implemented in the search of the main search field.
                // But they should not be displayed if the main search field is empty.
                // - volunteerProposals: display if main search field contains 0 characters.
                // - volunteerTags: display if main search field contains at least 1 character.
                volunteerTags: [
                    'Macher/in',
                    'Denker/in',
                    'Jugendarbeit',
                    'Kunst',
                    'Einkaufen'
                ],
                volunteerCities: [
                    'Main Standort',
                    'Darmstadt',
                    'Frankfurt am Main',
                    'Wiesbaden',
                    'Mainz'
                ],
                volunteerRadius: [
                    'Überall',
                    '5 km',
                    '10 km',
                    '25 km',
                    '50 km'
                ],
                selectedCity: '',
                selectedRadius: '',
                selectedTags: [],
                searchResult: null,
                searchString: ''
            };
        },
        methods: {
          ...mapActions([
            'setSearchValue'
          ]),
            remove(tag: string): void {
                const index = this.selectedTags.indexOf(tag, 0);
                if (index >= 0) {
                    this.selectedTags.splice(index, 1);
                }
                if (this.selectedTags.length === 0) {
                    // TODO should this be implemented?
                    // if no tags are selected go back to the home page.
                }
            },
            tagChange(tag: string): void {
                this.selectedTags.push(tag);
                this.setSearchValue(tag);
                this.$nextTick(() => {
                    this.searchString = '';
                });
            }
        },
      computed: {
        ...mapState([
          'searchValue'
        ])
      },
    });
</script>

<style scoped>
</style>