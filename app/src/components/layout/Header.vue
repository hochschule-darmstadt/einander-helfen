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

            <v-flex xs10 sm8 md6 style="background: white; border-radius: 20px; margin-right:2%">
                <search-bar @input="addSearchValue"/>
                <v-spacer></v-spacer>
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

            <v-flex xs12 sm5 md3>
                 <location-search-bar :dark="true"/>
            </v-flex>

            <v-flex xs12 sm4 md1>
                <radius :dark="true" />
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
    import { createNamespacedHelpers } from 'vuex';
    const { mapActions, mapState } = createNamespacedHelpers('searchBarModule');
    import LocationSearchBar from '@/components/ui/LocationSearchBar.vue';
    import Radius from '@/components/ui/Radius.vue';
    import SearchBar from '@/components/ui/SearchBar.vue';

    export default Vue.extend({
        components: {
            LocationSearchBar,
            Radius,
            SearchBar
        },
        data(): {
            links: any,
        } {
            return {
                links: [
                    {text: 'Home', route: '/'},
                    { text: 'Über uns', route: '/about' },
                    { text: 'Impressum', route: '/imprint' },
                    { text: 'Datenschutzerklärung', route: '/privacy' }
                ],
            };
        },
        methods: {
          ...mapActions([
              'addSearchValue',
              'removeSearchValue'
          ]),
            remove(tag: string): void {
                this.removeSearchValue(tag);
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
