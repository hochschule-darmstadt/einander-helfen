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
                <search-bar
                  @input="addSearchValue"
                />
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
            </v-col>

             <v-col
                cols="2"
                md="2">
                <location-search-bar />
            </v-col>

            <v-col
                cols="1"
                md="1">
                <radius />
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
                    {text: '', route: '/'},
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
