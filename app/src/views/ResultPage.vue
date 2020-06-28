import * as Vue2Leaflet from "vue2-leaflet";
<template>
  <div>
    <Header />
    <v-snackbar v-model="showRadiusExtendedMessage" top="top">
        Zu Ihrer Suchanfrage mit einem Radius von {{radiusExtendedFrom}} haben wir keine Treffer gefunden.
        <template v-if="selectedRadius">
          Wir haben daher den Radius auf {{selectedRadius}} vergrößert.
        </template>
        <template v-else>
          Wir haben daher den Radius vergrößert, bis Ergebnisse gefunden wurden.
        </template>
    </v-snackbar>
      <v-layout row wrap no-gutters>
        <!-- Map -->
        <v-flex xs12 md6 order-md2 v-show="postMapToggle === 'map'">
           <div class="map">
                <v-card tile height="70vh">
                    <div id="map" :style="{height: map.height, width: map.width}">
                        <v-btn v-if="currentPostId.length > 0" @click="postMapToggle = 'post'"
                               style="position: absolute; z-index: 9999; margin-right: 30px; margin-top: 20px; right: 0;"><v-icon>info</v-icon> Details
                        </v-btn>
                        <l-map ref="map" :center="map.center" :zoom="map.zoom">
                            <l-tile-layer :url="map.url" :attribution="map.attribution"></l-tile-layer>
                            <v-marker-cluster>
                              <v-marker
                                      v-for="post in posts"
                                      :key="post.id"
                                      :icon="post.id === currentPostId ? map.markerRed: map.markerBlue"
                                      :lat-lng="[post.geo_location.lat, post.geo_location.lon]"
                                      @click="openPost(post.id)">
                                  <v-popup :content="post.title"></v-popup>
                              </v-marker>
                            </v-marker-cluster>
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
            <v-list-item-content style="margin-top:2%" class="headline">
              {{selectedPost.title}}
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
          <v-card-text style="padding:0 10px;">
            <v-simple-table class="no-border detail-table">
              <tbody>
              <tr v-if="selectedPost.location">
                <td>Einsatzort</td>
                <td v-html="selectedPost.location"></td>
              </tr>
              <tr class="pt-1" v-if="selectedPost.title">
                <td>Aufgabe</td>
                <td v-html="selectedPost.task"></td>
              </tr>
              <tr class="pt-1" v-if="selectedPost.contact">
                <td>Ansprechpartner</td>
                <td v-html="selectedPost.contact"></td>
              </tr>
              <tr class="pt-1" v-if="selectedPost.organization">
                <td>Organisation</td>
                <td v-html="selectedPost.organization"></td>
              </tr>
              <tr class="pt-1" v-if="selectedPost.target_group">
                <td>Zielgruppe</td>
                <td v-html="selectedPost.target_group"></td>
              </tr>
              <tr class="pt-1" v-if="selectedPost.timing">
                <td>Einstiegsdatum / Beginn</td>
                <td v-html="selectedPost.timing"></td>
              </tr>
              <tr class="pt-1" v-if="selectedPost.effort">
                <td>Zeitaufwand</td>
                <td v-html="selectedPost.effort"></td>
              </tr>
              <tr class="pt-1" v-if="selectedPost.opportunities">
                <td>Möglichkeiten</td>
                <td v-html="selectedPost.opportunities"></td>
              </tr>
              <tr class="pt-1" v-if="selectedPost.link">
                <td>Quelle</td>
                <td><a :href="selectedPost.link" target="_blank">{{ selectedPost.source }}</a></td>
              </tr>
              </tbody>
            </v-simple-table>
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
                    <v-list-item-title class="headline mb-1">
                      {{post.title}}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      {{post.location}} &mdash; {{post.task}}
                    </v-list-item-subtitle>
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
            <template v-if="!postsOnCurrentPage.length">
              <div class="text-center pt-12">
                <h3 class="font-weight-bold ">Es wurden keine Suchergebnisse zu Ihrer Suchanfrage gefunden.</h3>
              </div>
            </template>
          </div>
        </v-flex>

      </v-layout>
                       <!--pageination-->
          <div class="text-center" style="margin-top:2%; margin-bottom:1%">
            <v-pagination @input="setPage($event)" :value="page" :length="numberOfPages" total-visible="7" color="#054C66"></v-pagination>
            <span class="pl-2 mt-2 d-inline-block font-italic">{{totalResultSize}} Ergebnisse</span>
          </div>

  </div>


</template>

<!-- test content -->
<script lang="ts">
    import Header from '@/components/layout/Header.vue';
    import Post from '@/models/post';
    import Vue from 'vue';
    import {mapActions, mapState, mapGetters, createNamespacedHelpers} from 'vuex';
    const {mapState: mapLocationState, mapActions: mapLocationActions} = createNamespacedHelpers('locationSearchModule');
    const {mapState: mapSearchState} = createNamespacedHelpers('textSearchModule');

    import L, {LatLngTuple} from 'leaflet';
    import {LMap, LTileLayer, LMarker, LTooltip} from 'vue2-leaflet';
    import Vue2LeafletMarkerCluster from 'vue2-leaflet-markercluster/Vue2LeafletMarkercluster.vue';
    import * as Vue2Leaflet from 'vue2-leaflet';
    import radii from '@/resources/radii';

    export default Vue.extend({
        components: {Header, LMap, LTileLayer, LMarker, LTooltip,
          'v-marker': Vue2Leaflet.LMarker,
          'v-popup': Vue2Leaflet.LPopup,
          'v-marker-cluster': Vue2LeafletMarkerCluster
        },
        data(): {
            map: any;
            postMapToggle: 'post' | 'map';
            radiusExtendedFrom: '';
            showRadiusExtendedMessage: boolean;
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
                },
                radiusExtendedFrom: '',
                showRadiusExtendedMessage: false
            };
        },
        computed: {
            ...mapState(['posts', 'page', 'resultsFrom', 'selectedPost', 'totalResultSize']),
            ...mapGetters(['postsOnCurrentPage', 'numberOfPages', 'pageOfCurrentPost']),
            ...mapLocationState(['selectedLocation', 'selectedRadius']),
            ...mapSearchState(['searchValues']),
            currentPostId(): string {
                return this.selectedPost
                    ? this.selectedPost.id
                    : '';
            },
            postIsOpen(): boolean {
                return !!this.selectedPost;
            }
        },
        created(): void {
            this.hydrateStateFromRoute(this.$route);
        },
        mounted(): void {
          this.rerenderMap();
        },
        watch: {
          /**
           * Beobachtet die aktuell geladenen Posts.
           * Wenn nur ein Post vorhanden ist, diesen direkt öffnen.
           * Wenn überhaupt Posts vorhanden sind, den Viewport der Karte auf alle Marker setzen.
           * Wenn keine Posts da sind, ggf. den Radius vergrößern und erneut suchen.
           *
           * @param val Post[]
           */
            posts(val: Post[]): void {
                if (val.length === 1) {
                    this.openPost(val[0].id);
                }
                if (val.length) {
                  const markers = val.map((post) => [post.geo_location.lat, post.geo_location.lon] as LatLngTuple);
                  (this.$refs.map as LMap).fitBounds(markers);

                  if (this.radiusExtendedFrom) {
                    this.showRadiusExtendedMessage = true;
                  }

                } else {
                  // Unsere Suche hat keine Ergebnisse geliefert.
                  if (this.selectedLocation && this.selectedRadius) {
                    // Wenn wir mit einem Radius um einen Ort suchen, den Radius vergrößern und nochmal probieren!
                    const currentRadiusIndex = radii.findIndex((r) => r.value === this.selectedRadius);
                    const nextBiggerRadius = radii[(currentRadiusIndex + 1) % (radii.length - 1)];
                    // Wir wollen uns merken, dass wir den Radius verändert haben, um den Nutzer darüber zu informieren.
                    // Aber nur, wenn wir das nicht bereits gemacht haben um uns den Wert nicht zu überschreiben.
                    if (!this.radiusExtendedFrom) {
                      this.radiusExtendedFrom = this.selectedRadius;
                    }
                    this.setSelectedRadius(nextBiggerRadius.value);
                    this.updateURIFromState();
                    this.findPosts();
                  }
                }
            },
            showRadiusExtendedMessage(newValue, oldValue): void {
              // After the message closed we can remove this knowlage.
              if (newValue !== oldValue && !newValue) {
                this.radiusExtendedFrom = '';
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
                        const postIndex = this.posts.findIndex((post) => post.id === id);
                        this.setSelectedPost(this.posts[postIndex]);
                        this.setPage(this.pageOfCurrentPost);
            },
            openMap(): void {
                const currentPost = this.selectedPost as Post;
                const location = [currentPost.geo_location.lat, currentPost.geo_location.lon] as LatLngTuple;
                this.postMapToggle = 'map';
                this.rerenderMap();
                this.$nextTick(() => {
                    (this.$refs.map as LMap).setCenter(location);
                });
            },
            rerenderMap(): void {
              this.$nextTick(() => {
                (this.$refs.map as LMap).mapObject.invalidateSize();
              });
            }
        }
    });
</script>

<style>
  @import "~leaflet/dist/leaflet.css";
  @import "~leaflet.markercluster/dist/MarkerCluster.css";
  @import "~leaflet.markercluster/dist/MarkerCluster.Default.css";

   .activeListItem {
     background-color: #c4e0ff !important;
   }
   .no-border tr:not(:last-child) td:not(.v-data-table__mobile-row) {
    border: 0 !important;
   }
   .detail-table tr:hover {
    background: unset !important;
   }
   .detail-table tr {
     margin-bottom: 10px;
   }
   .detail-table tr td {
     vertical-align: top;
     padding-bottom: 25px;
   }

</style>
