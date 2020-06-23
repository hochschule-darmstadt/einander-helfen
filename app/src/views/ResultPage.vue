<template>
  <div>
    <Header />

      <v-layout row wrap no-gutters>
        <!-- Map -->
        <v-flex xs12 md6 order-md2 v-if="!postIsOpen">
           <div class="map" v-if="!postIsOpen">
                <v-card tile height="70vh">
                    <div id="map" :style="{height: map.height, width: map.width}">
                        <v-btn v-if="currentPostId !== ''" @click="postIsOpen = true"
                               style="position: absolute; right; z-index: 9999; margin-right: 30px; margin-top: 20px; right: 0;"><v-icon>info</v-icon> Details
                        </v-btn>
                        <l-map ref="map" :center="map.center" :zoom="map.zoom">
                            <l-tile-layer :url="map.url" :attribution="map.attribution"></l-tile-layer>
                            <template v-for="post in posts">
                                <l-marker v-if="post.id === currentPostId" :icon="map.markerRed"
                                          :lat-lng="[post.geo_location.lat, post.geo_location.lon]"
                                          @click="openPost(post.i)">
                                    <l-tooltip>{{ post.title }}</l-tooltip>
                                </l-marker>
                                <l-marker v-else :icon="map.markerBlue"
                                          :lat-lng="[post.geo_location.lat, post.geo_location.lon]"
                                          @click="openPost(post.i)">
                                    <l-tooltip>{{ post.title }}</l-tooltip>
                                </l-marker>
                            </template>
                        </l-map>
                    </div>
                </v-card>
            </div>
        </v-flex>

        <!-- right side content-->
        <v-flex sm12 md6 order-md2 v-if="postIsOpen" mb-5>
          <div>
          <v-card
            tile
            style="height:70vh ;overflow:auto"
          >
          <v-list-item three-line>
            <!--
              This functionality may be added later. This button allows to deselect the current post and load all markers on the map.

            <v-btn class="mr-3" text @click="closePost()">
              <v-icon>arrow_back</v-icon>
            </v-btn> -->

            <!--display title, subtitle and image on the right side-->
            <v-list-item-content style="margin-top:2%" class="headline">{{
                currentPost.title
              }}
            </v-list-item-content>
            <v-img
              style="margin-top:2%"
              max-width="80px"
              height="80px"
              contain
              :src="currentPost.image"
            ></v-img>

            <v-btn style="margin-top:2%; background: #00254f" dark class="mr-3" text @click="openMap()">
              <v-icon>map</v-icon> Karte
            </v-btn>
          </v-list-item>

          <!--display content on the right side-->
          <v-card-text style="padding-left:5%; padding-right:5%">
            <v-row v-if="currentPost.location">
             <v-flex md4 xs6>Einsatzort</v-flex>
             <v-flex md8 xs6 v-html="currentPost.location"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.title">
             <v-flex md4 xs6 >Aufgabe</v-flex>
             <v-flex md8 xs6 v-html="currentPost.task"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.contact">
              <v-flex md4 xs6>Ansprechpartner</v-flex>
              <v-flex md8 xs6 v-html="currentPost.contact"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.organization">
              <v-flex md4 xs6>Organisation</v-flex>
              <v-flex md8 xs6 v-html="currentPost.organization"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.target_group">
              <v-flex md4 xs6>Zielgruppe</v-flex>
              <v-flex md8 xs6 v-html="currentPost.target_group"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.timing">
              <v-flex md4 xs6>Einstiegsdatum / Beginn</v-flex>
              <v-flex md8 xs6 v-html="currentPost.timing"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.effort">
              <v-flex md4 xs6>Zeitaufwand</v-flex>
              <v-flex md8 xs6 v-html="currentPost.effort"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.opportunities">
              <v-flex md4 xs6>Möglichkeiten</v-flex>
              <v-flex md8 xs6 v-html="currentPost.opportunities"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.link">
              <v-flex md4 xs6>Quelle</v-flex>
              <v-flex md8 xs6><a :href="currentPost.link" target="_blank">{{ currentPost.source }}</a></v-flex>
            </v-row>
          </v-card-text>

          <v-card-actions>
            <v-flex md12 sm12>
              <v-container style="margin-bottom: 10px">
                <template
                  v-for="(category, i) in currentPost.categories"
                >
                  <v-chip :key="i" class="mr-2 mt-2">{{ category }}</v-chip>
                </template>
              </v-container>
              <v-spacer></v-spacer>
              <v-container style="display:flex;justify-content:center;">
                <v-btn
                  class="my-2"
                  dark
                  large
                  color="#054C66"
                  :href="currentPost.link"
                  target="_blank"
                >
                  Zum Angebot
                </v-btn>
              </v-container>
            </v-flex>
          </v-card-actions>
        </v-card>
          </div>
        </v-flex>

        <!--left side content-->
        <v-flex sm12 md6 order-md1 >
          <div style="height:70vh ;overflow:auto">
            <template v-for="post in visiblePages">
              <v-card class="mb-3">
                <v-list-item three-line @click="openPost(post.id)">
                  <v-list-item-content>
                    <v-list-item-title class="headline mb-1">{{
                      post.title
                    }}</v-list-item-title>
                    <v-list-item-subtitle>{{
                      post.task
                    }}</v-list-item-subtitle>
                  </v-list-item-content>

                  <v-img
                    max-width="80px"
                    height="80px"
                    contain
                    :src="post.image"
                  ></v-img>
                </v-list-item>
              </v-card>
            </template>
          </div>
        </v-flex>

      </v-layout>
                       <!--pageination-->
          <div class="text-center" style="margin-top:2%; margin-bottom:1%">
            <v-pagination @input="setResultPage($event)" :value="page" :length="numberOfPages" total-visible="7" color="#054C66"></v-pagination>
          </div>

  </div>


</template>

<!-- test content -->
<script lang="ts">
    import Header from '@/components/layout/Header.vue';
    import Post from '@/models/post';
    import Vue from 'vue';
    import {mapActions, mapState} from 'vuex';

    import L, {LatLngTuple} from 'leaflet';
    import {LMap, LTileLayer, LMarker, LTooltip, LIcon} from 'vue2-leaflet';
    import 'leaflet/dist/leaflet.css';

    export default Vue.extend({
        components: {Header, LMap, LTileLayer, LMarker, LTooltip},
        data(): {
            postIsOpen: boolean;
            currentPostId: string;
            perPage: number;
            map: any;
        } {
            return {
                postIsOpen: false,
                currentPostId: '',
                perPage: 15,
                map: {
                    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
                    center: [51.5000, 10.5000],
                    zoom: 12,
                    width: '100%',
                    height: '100%',
                    markerBlue: L.icon({
                        iconUrl: require('../../public/images/marker/marker-icon.png'),
                        iconSize: [25, 41]
                    }),
                    markerRed: L.icon({
                        iconUrl: require('../../public/images/marker/marker-icon-red.png'),
                        iconSize: [25, 41]
                    })
                }
            };
        },
        computed: {
            ...mapState(['posts', 'page', 'selectedLocation', 'radiusSearchValue']),
            visiblePages(): Post[] {
                return this.posts.slice(
                    (this.page - 1) * this.perPage,
                    this.page * this.perPage
                );
            },
            currentPost(): Post | null {
                return this.postIsOpen
                    ? this.posts.find((post) => post.id === this.currentPostId)
                    : null;
            },
            numberOfPages(): number {
                return Math.ceil(this.posts.length / this.perPage);
            }
        },
        created(): void {
            this.hydrateStateFromURIParams(this.$route.query);
        },
        watch: {
            posts(val: Post[], oldVal: Post[]): void {
                if (val.length === 1) {
                    this.openPost(val[0].id);
                }
                if (val.length) {
                  const markers = val.map((post) => [post.geo_location.lat, post.geo_location.lon] as LatLngTuple);
                  (this.$refs.map as LMap).fitBounds(markers);
                }
            },
            radiusSearchValue(): void {
                this.findPosts();
            },
            selectedLocation(): void {
                this.findPosts();
            },
            page(value): void {
                this.setResultPage(value);
            }
        },
        methods: {
            ...mapActions(['hydrateStateFromURIParams', 'setResultPage', 'findPosts']),
            openPost(id: string): void {
                        this.postIsOpen = true;
                        this.currentPostId = id;
                    },
            closePost(): void {
                this.currentPostId = '';
                this.postIsOpen = false;
                if (this.posts.length) {
                  const markers = this.posts.map((post) => [post.geo_location.lat, post.geo_location.lon] as LatLngTuple);
                  this.$nextTick(() => {
                    (this.$refs.map as LMap).fitBounds(markers);
                  });
                }
            },
            openMap(): void {
                const currentPost = this.currentPost as Post;
                const location = [currentPost.geo_location.lat, currentPost.geo_location.lon] as LatLngTuple;
                this.postIsOpen = false;
                this.$nextTick(() => {
                    (this.$refs.map as LMap).setCenter(location);
                });
            }
        }
    });
</script>

<style scoped>
    .grid {
        width: 100%;
        display: grid;
        grid-template-columns: 50% 50%;
        grid-template-areas: "posts detail";
    }

    .map,
    .detail {
        grid-area: detail;
        height: 75vh;
    }

    .posts {
        grid-area: posts;
        height: 75vh;
        overflow: auto
    }

    @media (max-width: 500px) {
        .grid {
            grid-template-columns: 100%;
            grid-row-gap: 10px;
            grid-template-areas: "detail" "posts";
        }

        .posts {
            height: auto;
        }
    }
</style>
