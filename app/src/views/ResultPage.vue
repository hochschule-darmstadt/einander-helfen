<template>
  <div>
    <Header />

      <v-layout row wrap no-gutters>
        <!-- Map -->
        <v-flex xs12 md6 order-md2 v-if="postMapToggle === 'map'">
           <div class="map">
                <v-card tile height="70vh">
                    <div id="map" :style="{height: map.height, width: map.width}">
                        <v-btn v-if="currentPostId.length > 0" @click="postMapToggle = 'post'"
                               style="position: absolute; z-index: 9999; margin-right: 30px; margin-top: 20px; right: 0;"><v-icon>info</v-icon> Details
                        </v-btn>
                        <l-map ref="map" :center="map.center" :zoom="map.zoom">
                            <l-tile-layer :url="map.url" :attribution="map.attribution"></l-tile-layer>
                            <template v-for="post in posts">
                                <l-marker v-if="post.id === currentPostId" :icon="map.markerRed"
                                          :lat-lng="[post.geo_location.lat, post.geo_location.lon]"
                                          @click="openPost(post.id)">
                                    <l-tooltip>{{ post.title }}</l-tooltip>
                                </l-marker>
                                <l-marker v-else :icon="map.markerBlue"
                                          :lat-lng="[post.geo_location.lat, post.geo_location.lon]"
                                          @click="openPost(post.id)">
                                    <l-tooltip>{{ post.title }}</l-tooltip>
                                </l-marker>
                            </template>
                        </l-map>
                    </div>
                </v-card>
            </div>
        </v-flex>

        <!-- right side content-->
        <v-flex sm12 md6 order-md2 v-if="postMapToggle === 'post'" mb-5>
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
                selectedPost.title
              }}
            </v-list-item-content>
            <v-img
              style="margin-top:2%"
              max-width="80px"
              height="80px"
              contain
              :src="selectedPost.image"
            ></v-img>

            <v-btn style="margin-top:2%; background: #00254f" dark class="mr-3" text @click="openMap()">
              <v-icon>map</v-icon> Karte
            </v-btn>
          </v-list-item>

          <!--display content on the right side-->
          <v-card-text style="padding-left:5%; padding-right:5%">
            <v-row v-if="selectedPost.location">
             <v-flex md4 xs6>Einsatzort</v-flex>
             <v-flex md8 xs6 v-html="selectedPost.location"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="selectedPost.title">
             <v-flex md4 xs6 >Aufgabe</v-flex>
             <v-flex md8 xs6 v-html="selectedPost.task"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="selectedPost.contact">
              <v-flex md4 xs6>Ansprechpartner</v-flex>
              <v-flex md8 xs6 v-html="selectedPost.contact"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="selectedPost.organization">
              <v-flex md4 xs6>Organisation</v-flex>
              <v-flex md8 xs6 v-html="selectedPost.organization"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="selectedPost.target_group">
              <v-flex md4 xs6>Zielgruppe</v-flex>
              <v-flex md8 xs6 v-html="selectedPost.target_group"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="selectedPost.timing">
              <v-flex md4 xs6>Einstiegsdatum / Beginn</v-flex>
              <v-flex md8 xs6 v-html="selectedPost.timing"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="selectedPost.effort">
              <v-flex md4 xs6>Zeitaufwand</v-flex>
              <v-flex md8 xs6 v-html="selectedPost.effort"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="selectedPost.opportunities">
              <v-flex md4 xs6>Möglichkeiten</v-flex>
              <v-flex md8 xs6 v-html="selectedPost.opportunities"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="selectedPost.link">
              <v-flex md4 xs6>Quelle</v-flex>
              <v-flex md8 xs6><a :href="selectedPost.link" target="_blank">{{ selectedPost.source }}</a></v-flex>
            </v-row>
          </v-card-text>

          <v-card-actions>
            <v-flex md12 sm12>
              <v-container style="margin-bottom: 10px">
                <template
                  v-for="(category, i) in selectedPost.categories"
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
                  :href="selectedPost.link"
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
            <template v-for="post in postsOnCurrentPage">
              <v-card class="mb-3" :class="{ activeListItem: currentPostId === post.id }">
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
            <v-pagination @input="setPage($event)" :value="page" :length="numberOfPages" total-visible="7" color="#054C66"></v-pagination>
          </div>

  </div>


</template>

<!-- test content -->
<script lang="ts">
    import Header from '@/components/layout/Header.vue';
    import Post from '@/models/post';
    import Vue from 'vue';
    import {mapActions, mapState, createNamespacedHelpers} from 'vuex';
    const {mapState: mapLocationState, mapActions: mapLocationActions} = createNamespacedHelpers('locationSearchModule');
    const {mapState: mapSearchState} = createNamespacedHelpers('textSearchModule');

    import L, {LatLngTuple} from 'leaflet';
    import {LMap, LTileLayer, LMarker, LTooltip} from 'vue2-leaflet';
    import 'leaflet/dist/leaflet.css';
    import radii from '@/resources/radii';

    export default Vue.extend({
        components: {Header, LMap, LTileLayer, LMarker, LTooltip},
        data(): {
            map: any;
            postMapToggle: 'post' | 'map';
        } {
            return {
                postMapToggle: 'map',
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
            ...mapState(['posts', 'page', 'resultsFrom', 'totalResultSize',
                         'hitsPerPage', 'selectedPost']),
            ...mapLocationState(['selectedLocation', 'selectedRadius']),
            ...mapSearchState(['searchValues']),
            currentPostId(): string {
                return this.selectedPost
                    ? this.selectedPost.id
                    : '';
            },
            postIsOpen(): boolean {
                return !!this.selectedPost;
            },
            postsOnCurrentPage(): Post[] {
                return this.posts.slice(
                  ((this.page - 1) * this.hitsPerPage) - this.resultsFrom,
                  (this.page * this.hitsPerPage) - this.resultsFrom
                );
            },
            numberOfPages(): number {
                return Math.ceil(this.totalResultSize / this.hitsPerPage);
            }
        },
        created(): void {
            this.hydrateStateFromRoute(this.$route);
        },
        watch: {
            posts(val: Post[]): void {
                if (val.length === 1) {
                    this.openPost(val[0].id);
                }
                if (val.length) {
                  const markers = val.map((post) => [post.geo_location.lat, post.geo_location.lon] as LatLngTuple);
                  (this.$refs.map as LMap).fitBounds(markers);
                } else {
                  // Unsere Suche hat keine Ergebnisse geliefert.
                  if (this.selectedLocation && this.selectedRadius) {
                    // Wenn wir mit einem Radius um einen Ort suchen, den Radius vergrößern und nochmal probieren!
                    const currentRadiusIndex = radii.findIndex((r) => r.value === this.selectedRadius);
                    const nextBiggerRadius = radii[currentRadiusIndex + 1 % radii.length];
                    this.setSelectedRadius(nextBiggerRadius.value);
                    this.updateURIFromState();
                    this.findPosts();
                  }
                }
            },
            selectedPost(): void {
                this.updateURIFromState();
            },
            page(value): void {
                this.setPage(value);
            },
            resultsFrom(oldValue, newValue): void {
              if (oldValue !== newValue) {
                this.findPosts();
              }
            }
        },
        methods: {
            ...mapActions(['hydrateStateFromRoute', 'updateURIFromState', 'setSelectedPost', 'setPage', 'findPosts']),
            ...mapLocationActions(['setSelectedRadius']),
            openPost(id: string): void {
                        this.postMapToggle = 'post';
                        this.setSelectedPost(this.posts.find((post) => post.id === id));
            },
            openMap(): void {
                const currentPost = this.selectedPost as Post;
                const location = [currentPost.geo_location.lat, currentPost.geo_location.lon] as LatLngTuple;
                this.postMapToggle = 'map';
                this.$nextTick(() => {
                    (this.$refs.map as LMap).setCenter(location);
                });
            }
        }
    });
</script>

<style scoped>
   .activeListItem {
     background-color: #c4e0ff;
   }
</style>
