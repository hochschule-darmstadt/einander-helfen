<template>
    <header>
        <v-layout row wrap justify-space-around
                no-gutters
                style="padding: 1vh; background: #00254f">
            <v-btn class="d-none d-sm-flex justify-center mr-5"
                    
                    height="75px"
                    width="80px"
                    justify="left"
                    rounded
                    router
                    
                    depressed
                    icon
                > <router-link to="/" exact><v-img class="mt-1" width=80px height=75px src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Heart-hand-shake.svg/256px-Heart-hand-shake.svg.png"></v-img>
        </router-link>
         </v-btn>
           
            <v-flex
                    md6 sm8
                    style="background: white; border-radius: 20px; margin-right:2%">
                <v-combobox
                        :items="searchProposals"
                        :search-input.sync="searchString"
                        @input="tagAdded"
                        append-icon="search"
                        clearable
                        item-text="tag"
                        style="margin-left: 10px; margin-right: 10px">
                </v-combobox>
                <v-chip-group
                        active-class="primary-text"
                        column
                        style="margin-left: 10px; margin-right: 10px; margin-top: -20px">
                    <v-chip
                            :key="tag"
                            @click:close="remove(tag)"
                            close
                            v-for="tag in searchValues">
                        {{ tag }}
                    </v-chip>
                </v-chip-group>
            </v-flex>

             <v-menu offset-y>
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                            class="hidden-md-and-up"
                            v-bind="attrs"
                            v-on="on"
                            dark
                            style="margin-top: 1vh"
                            icon
                            >
                            <v-icon>more_vert</v-icon>
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

            <v-flex md3 sm5>
                 <location-search-bar/>
            </v-flex>

            <v-flex md1 sm4>
                <radius />
            </v-flex>
            
            <v-menu offset-y>
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                            class="hidden-sm-and-down"
                            v-bind="attrs"
                            v-on="on"
                            dark
                            style="margin-top: 1vh"
                            icon
                            >
                            <v-icon>more_vert</v-icon>
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
        </v-layout>
    </header>
</template>

<script lang="ts">
    import Vue from 'vue';
    import {mapActions, mapState} from 'vuex';
    import LocationSearchBar from '@/components/ui/LocationSearchBar.vue';
    import Radius from '@/components/ui/Radius.vue';

    export default Vue.extend({
        components: {
            LocationSearchBar,
            Radius
        },
        data(): {
            links: any,
            volunteerTags: string[],
            selectedTags: string[],
            searchResult: null,
            searchString: string
        } {
            return {
                links: [
                    {text: 'Home', route: '/'},
                    { text: 'Über uns', route: '/about' },
                    { text: 'Impressum', route: '/imprint' },
                    { text: 'Datenschutzerklärung', route: '/privacy' }
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
                selectedTags: [],
                searchResult: null,
                searchString: ''
            };
        },
        methods: {
          ...mapActions([
              'addSearchValue',
              'removeSearchValue'
          ]),
            remove(tag: string): void {
                this.removeSearchValue(tag);
            },
            tagAdded(tag: string): void {
                if (tag.length) {
                    this.addSearchValue(tag);
                    this.searchString = '';
                }
                this.$router.push({
                    name: 'resultPage',
                    query: {
                        ...this.$route.query,
                        q: this.selectedTags
                    }
                });
            }
        },
      computed: {
        ...mapState([
            'searchValues',
            'searchProposals'
        ])
      },
    });
</script>

<style>
  .v-menu__content{
    z-index:9999 !important;
  }
</style>
