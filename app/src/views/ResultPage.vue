<template>
  <div>
    <Header />
      <v-layout row wrap no-gutters>
        <!-- Map -->
        <v-flex xs12 md6 order-md2 v-show="postMapToggle === 'map'">
           <div class="map">
                <v-card tile height="70vh">
                    <div id="map" :style="{height: map.height, width: map.width}">
                        <v-btn v-if="currentPostId.length > 0" @click="postMapToggle = 'post'"
                               class="button-details" dark><v-icon>info</v-icon> Details
                        </v-btn>
                        <l-map ref="map" :center="map.center" :zoom="map.zoom" :options="{gestureHandling: true}">
                            <l-tile-layer :url="map.url" :attribution="map.attribution"></l-tile-layer>
                            <v-marker-cluster>
                              <v-marker
                                      v-for="post in posts"
                                      :key="post.id"
                                      :icon="post.id === currentPostId ? map.markerRed: map.markerBlue"
                                      :lat-lng="[post.geo_location.lat, post.geo_location.lon]"
                                      @click="openPost(post.id)">
                                  <l-tooltip :content="post.title"></l-tooltip>
                              </v-marker>
                            </v-marker-cluster>
                        </l-map>
                    </div>
                </v-card>
            </div>
        </v-flex>

        <!-- right side content-->
        <v-flex sm12 md6 order-md2 v-if="postMapToggle === 'post'">
          <div>
          <v-card
            tile
            style="height:70vh ;overflow:auto"
          >
          <div class="container-buttons-smartphone">
            <v-btn dark class="mr-3 button-smartphone button-map-smartphone" text @click="openMap()">
              <v-icon>map</v-icon> Karte
            </v-btn>
            <v-btn class="button-close button-smartphone button-close-smartphone" icon @click="closePost()">
              <v-icon>close</v-icon>
            </v-btn>
          </div>
          <v-list-item three-line>
            <v-btn dark class="mr-3 button-map" text @click="openMap()">
              <v-icon>map</v-icon> Karte
            </v-btn>

            <!--display title, subtitle and image on the right side-->
            <v-list-item-content style="margin-top:2%" class="headline">
              {{selectedPost.title}}
            </v-list-item-content>
            <div>
            <v-img
              style="margin-top:2%"
              max-width="80px"
              height="80px"
              contain
              :src="selectedPost.image"
            ></v-img></div>

            <v-btn class="button-close" icon @click="closePost()">
              <v-icon>close</v-icon>
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
              <tr class="pt-1 hide-copyright" v-if="selectedPost.title">
                <strong>You suck</strong>
                <td>Aufgabe</td>
                <td v-html="selectedPost.task"></td>
              </tr>
              <tr class="pt-1" v-if="selectedPost.contact">
                <td>Ansprechpartner</td>
                <td v-html="selectedPost.contact"></td>
              </tr>
              <tr class="pt-1 hide-copyright" v-if="selectedPost.organization">
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


            <div v-if="showRadiusExtendedMessage" class="text-center pt-12 pb-12">
              <h3 class="font-weight-bold">Zu Ihrer Suchanfrage mit einem Radius von {{radiusExtendedFrom}} haben wir keine Treffer gefunden.
                <template v-if="alternateRadius">Folgende Ergebnisse werden in einem Umkreis von {{alternateRadius}} gefunden.</template>
                <template v-else>Folgende Ergebnisse werden in einem Umkreis von mehr als 50 km gefunden.</template>
              </h3>
            </div>



            <v-card
                    v-for="post in postsOnCurrentPage"
                    :key="post.id"
                    class="mb-3"
                    :class="{ activeListItem: currentPostId === post.id }"
            >
                <v-list-item three-line @click="currentPostId === post.id ? closePost() : openPost(post.id)">
                  <v-list-item-content>
                    <v-list-item-title class="headline mb-1">
                      {{post.title}}
                    </v-list-item-title>
                    <v-list-item-subtitle :set="distance = postDistance(post)">
                      <strong>{{post.location}} <em v-if="distance">(in {{distance}})</em></strong> &mdash; {{post.task}}
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


              <div class="text-center pt-12" v-if="!postsOnCurrentPage.length">
                <h3 class="font-weight-bold ">Es wurden keine Suchergebnisse zu Ihrer Suchanfrage gefunden.</h3>
              </div>
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
    import { GestureHandling } from 'leaflet-gesture-handling';
    import radii from '@/resources/radii';

    L.Map.addInitHook('addHandler', 'gestureHandling', GestureHandling);

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
            ...mapLocationState(['selectedLocation', 'selectedLocationObject', 'selectedRadius', 'alternateRadius']),
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
                  this.fitMapBounds(val);

                  if (this.radiusExtendedFrom) {
                    this.showRadiusExtendedMessage = true;
                  }

                } else {
                  // Unsere Suche hat keine Ergebnisse geliefert.
                  if (this.selectedLocation && (this.selectedRadius || this.alternateRadius)) {
                    const myRadius = this.alternateRadius
                      ? this.alternateRadius
                      : this.selectedRadius;

                    // Wenn wir mit einem Radius um einen Ort suchen, den Radius vergrößern und nochmal probieren!
                    const currentRadiusIndex = radii.findIndex((r) => r.value === myRadius);
                    const nextBiggerRadius = radii[(currentRadiusIndex + 1) % radii.length];
                    // Wir wollen uns merken, dass wir den Radius verändert haben, um den Nutzer darüber zu informieren.
                    // Aber nur, wenn wir das nicht bereits gemacht haben um uns den Wert nicht zu überschreiben.
                    if (!this.radiusExtendedFrom) {
                      this.radiusExtendedFrom = this.selectedRadius;
                    }
                    this.setAlternateRadius(nextBiggerRadius.value);
                    this.findPosts();
                  }
                }
            },
            selectedPost(value): void {
              if (value === null) {
                this.closePost();
              }
              this.updateURIFromState();
            },
            page(value): void {
                this.setPage(value);
            },
            resultsFrom(newValue, oldValue): void {
              if (oldValue !== newValue) {
                this.findPosts();
              }
            },
            alternateRadius(newValue, oldValue): void {
              if (oldValue !== newValue && !newValue) {
                this.showRadiusExtendedMessage = false;
                this.radiusExtendedFrom = '';
              }
            }
        },
        methods: {
            ...mapActions(['hydrateStateFromRoute', 'updateURIFromState', 'setSelectedPost', 'setPage', 'findPosts']),
            ...mapLocationActions(['setSelectedRadius', 'setAlternateRadius']),
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
            closePost(): void {
                this.setSelectedPost(null);
                this.postMapToggle = 'map';

                this.fitMapBounds(this.posts);
            },
            fitMapBounds(posts: Post[]): void {
                const markers = posts.map((post) => [post.geo_location.lat, post.geo_location.lon] as LatLngTuple);
                (this.$refs.map as LMap).fitBounds(markers);
            },
            rerenderMap(): void {
              this.$nextTick(() => {
                (this.$refs.map as LMap).mapObject.invalidateSize();
              });
            },
            postDistance(post: Post): string {
              if (!this.selectedLocationObject) {
                return '';
              }

              const distance = this.haversineDistance([post.geo_location.lat, post.geo_location.lon],
                [this.selectedLocationObject.lat, this.selectedLocationObject.lon]);

              if (distance) {
                return Math.round(distance) + ' km';
              } else {
                return '';
              }

            },
            haversineDistance([lat1, lon1], [lat2, lon2]): number {
              const toRadian = (angle) => (Math.PI / 180) * angle;
              const distance = (a, b) => (Math.PI / 180) * (a - b);
              const RADIUS_OF_EARTH_IN_KM = 6371;

              const dLat = distance(lat2, lat1);
              const dLon = distance(lon2, lon1);

              lat1 = toRadian(lat1);
              lat2 = toRadian(lat2);

              // Haversine Formula
              const h =
                Math.pow(Math.sin(dLat / 2), 2) +
                Math.pow(Math.sin(dLon / 2), 2) * Math.cos(lat1) * Math.cos(lat2);
              const c = 2 * Math.asin(Math.sqrt(h));

              return RADIUS_OF_EARTH_IN_KM * c;
            }
        }
    });
</script>

<style>
  @import "~leaflet/dist/leaflet.css";
  @import "~leaflet.markercluster/dist/MarkerCluster.css";
  @import "~leaflet.markercluster/dist/MarkerCluster.Default.css";
  @import "~leaflet-gesture-handling/dist/leaflet-gesture-handling.css";

    .hide-copyright strong{
      display:none;
    }
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
   .button-map {
     margin-top: 30px;
     background-color: rgb(5, 76, 102);
     align-self: flex-start;
   }
   .button-smartphone {
     display: none;
   }
   .button-map-smartphone {
     background-color: rgb(5, 76, 102);
   }
   .button-close-smartphone {
     position: absolute;
     right: 0;
   }
   .container-buttons-smartphone {
     display: none;
     position: relative;
     justify-content: center;
     margin-top: 5px;
   }
   .button-details {
     position: absolute;
     z-index: 9999;
     margin-left: 50px;
     margin-top: 20px;
     background-color: rgb(5, 76, 102) !important;
   }
   .button-close {
     align-self: flex-start;
   }
   @media only screen and (max-width: 500px) {
    .button-map, .button-close {
      display: none;
    }
    .button-smartphone {
      display: block;
    }
    .container-buttons-smartphone {
      display: flex;
    }

   }

</style>
