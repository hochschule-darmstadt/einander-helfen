<template>
    <header>
        <v-row
                no-gutters
                style="padding: 1vh">
            <v-btn
                    :key="index"
                    :to="link.route"
                    class="my-2"
                    color="grey"
                    justify="left"
                    rounded
                    router
                    text
                    style="margin-top: 1vh"
                    v-for="(link, index) in links">
                {{ link.text }}
            </v-btn>

            <v-spacer></v-spacer>
            <v-col
                    cols="4"
                    md="4"
                    style="background: #eee; border-radius: 20px">
                <v-autocomplete
                        :items="volunteerProposals"
                        :search-input.sync="searchString"
                        @change="tagChange"
                        append-icon="search"
                        clearable
                        item-text="tag"
                        style="margin-left: 10px; margin-right: 10px"
                        v-model="searchResult">
                </v-autocomplete>
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
                        :items="volunteerRadius"
                        label="Umkreis"
                        v-model="selectedRadius">
                    Überall
                </v-autocomplete>
            </v-col>
            <v-spacer></v-spacer>

            <v-btn
                    style="margin-top: 1vh"
                    icon>
                <v-icon>more_vert</v-icon>
            </v-btn>
        </v-row>
    </header>
</template>

<script lang="ts">
    import Vue from 'vue';

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
                    {text: 'Logo', route: '/'},
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
                this.$nextTick(() => {
                    this.searchString = '';
                    this.searchResult = null;
                });
            }
        }
    });
</script>

<style scoped>
</style>
