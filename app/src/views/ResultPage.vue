<template>
  <div>
    <Header />
      <v-container sitecontent row wrap no-gutters>
        <!-- Map -->
        <v-btn id="mapButton" class="mb-2 button-map-smartphone" dark @click="toggleMapVisibility()">
          <v-icon>map</v-icon> {{mapButtonText}}
        </v-btn>
        <v-flex xs12 md6 order-md2 class="map-smartphone" v-show="showMap">
           <div class="map">
              <v-card tile id="mapcard" class="map-heigth">
                  <div id="map" :style="{height: map.height, width: map.width}">
                    <v-btn v-if="currentPostId.length > 0" @click="toggleMapVisibility()"
                      class="button-details" dark><v-icon>info</v-icon> Details
                    </v-btn>
                    <l-map ref="map" :center="map.center" :zoom="map.zoom" :options="{gestureHandling: true}">
                      <l-tile-layer :url="map.url" :attribution="map.attribution"></l-tile-layer>
                      <v-marker-cluster>
                        <v-marker
                          v-for="post in postWithGeoLocation"
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
        <v-flex sm12 md6 order-md2 class="details" v-if="!showMap && !smartphone">
          <div>
          <v-card
            tile
            style="height:70vh; overflow:auto"
          >
          <v-list-item three-line>
            <v-tooltip top v-if="selectedPost.geo_location === null">
              <template v-slot:activator="{ on }">
                <div id="divWithDisabledButton" v-on="on" class="d-inline-block">
                 <v-btn id="disabledMapButton" :disabled="selectedPost.geo_location === null" dark class="mr-3" text>
                    <v-icon>map</v-icon> Karte
                  </v-btn>
                </div>
              </template>
              <span>Der Pin für dieses Angebot kann auf der Karte nicht angezeigt werden, da keine Geodaten hinterlegt sind.</span>
            </v-tooltip>
            
            <v-btn dark class="mr-3 button-map" text @click="openMap()" v-if="selectedPost.geo_location !== null">
              <v-icon>map</v-icon> Karte
            </v-btn>
     
            <!--display title, subtitle and image on the right side-->
            <v-list-item-content style="margin-top:2%" class="headline">
              {{selectedPost.title}}
            </v-list-item-content>
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
              <tr class="pt-1" v-if="selectedPost.prerequisites">
                <td>Anforderungen</td>
                <td v-html="selectedPost.prerequisites"></td>
              </tr>
              <tr class="pt-1" v-if="selectedPost.language_skills">
                <td>Sprachen</td>
                <td v-html="selectedPost.language_skills"></td>
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
        <v-flex sm12 md6 order-md1>
          <div id=postbox style="height:70vh; overflow:auto;">

            <div v-if="showRadiusExtendedMessage" class="text-center pt-12 pb-12">
              <h3 class="font-weight-bold">Zu Ihrer Suchanfrage mit einem Radius von {{radiusExtendedFrom}} haben wir keine Treffer gefunden.
                <template v-if="alternateRadius">Folgende Ergebnisse werden in einem Umkreis von {{alternateRadius}} gefunden.</template>
                <template v-else>Folgende Ergebnisse werden in einem Umkreis von mehr als 50 km gefunden.</template>
              </h3>
            </div>

            <v-card id="posttitlecard"
                    v-for="post in postsOnCurrentPage"
                    :key="post.id"
                    class="mb-3"
            >
                <v-list-item :ripple="false" three-line :class="{ activeListItem: currentPostId === post.id }" @click="currentPostId === post.id ? closePost() : openPost(post.id)">
                  <v-list-item-content>
                    <v-list-item-title class="headline mb-1" :class="{'full-text': currentPostId === post.id}">
                      {{post.title}}
                    </v-list-item-title>
                    <v-list-item-subtitle :set="distance = postDistance(post)" :class="{ 'post-subtitle-hidden': currentPostId === post.id, 'post-subtitle': currentPostId !== post.id  }">
                      <strong>
                        <span v-if="post.post_struct.location.country === 'Deutschland'">{{post.post_struct.location.zipcode}}</span>
                        <span> {{post.post_struct.location.city}}</span>
                        <span v-if="post.post_struct.location.country !== 'Deutschland'">{{post.post_struct.location.country}}</span>
                        <em v-if="distance && post.post_struct.location.country === 'Deutschland'"> (in {{distance}})</em>
                      </strong> &mdash;
                      <span v-html="post.task"/>
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-card ref="detailsSmartphone"  class="details-smartphone" :class="{ 'details-smartphone-visible' : currentPostId === post.id, 'details-smartphone-hidden' : currentPostId !== post.id }">
                  <v-card-text>
                    <div v-if="post.location">
                      <h3>Einsatzort</h3>
                      <p v-html="post.location"></p>
                    </div>
                    <div v-if="post.task">
                      <h3>Aufgabe</h3>
                      <p v-html="post.task"></p>
                    </div>
                    <div v-if="post.contact">
                      <h3>Ansprechpartner</h3>
                      <p v-html="post.contact"></p>
                    </div>
                    <div v-if="post.organization">
                      <h3>Organisation</h3>
                      <p v-html="post.organization"></p>
                    </div>
                    <div v-if="post.target_group">
                      <h3>Zielgruppe</h3>
                      <p v-html="post.target_group"></p>
                    </div>
                    <div v-if="post.timing">
                      <h3>Einstiegsdatum / Beginn</h3>
                      <p v-html="post.timing"></p>
                    </div>
                    <div v-if="post.effort">
                      <h3>Zeitaufwand</h3>
                      <p v-html="post.effort"></p>
                    </div>
                    <div v-if="post.opportunities">
                      <h3>Möglichkeiten</h3>
                      <p v-html="post.opportunities"></p>
                    </div>
                    <div v-if="post.prerequisites">
                      <h3>Anforderungen</h3>
                      <p v-html="post.prerequisites"></p>
                    </div>
                    <div v-if="post.language_skills">
                      <h3>Sprachen</h3>
                      <p v-html="post.language_skills"></p>
                    </div>
                    <div v-if="post.link">
                      <h3>Quelle</h3>
                      <p>
                        <a :href="post.link" target="_blank">{{
                        post.source
                        }}</a>
                      </p>
                    </div>
                  </v-card-text>
                  <v-card-actions>
                    <v-flex md12 sm12>
                      <v-container style="margin-bottom: 10px">
                        <template
                          v-for="(category, i) in post.categories"
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
                          :href="post.link"
                          target="_blank"
                        >
                          Zum Angebot
                        </v-btn>
                      </v-container>
                    </v-flex>
                  </v-card-actions>
                </v-card>
              </v-card>
            <div class="text-center pt-12" v-if="!postsOnCurrentPage.length">
              <h3 class="font-weight-bold ">Es wurden keine Suchergebnisse zu Ihrer Suchanfrage gefunden.</h3>
            </div>
          </div>
        </v-flex>
        
      </v-container>
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
            mapButtonText: string;
            showMap: boolean;
            smartphone: boolean;
            radiusExtendedFrom: '';
            showRadiusExtendedMessage: boolean;
        } {
            return {
                mapButtonText: 'Karte anzeigen',
                showMap: true,
                smartphone: false,
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
            ...mapState(['posts', 'page', 'resultsFrom', 'selectedPost', 'totalResultSize', 'hitsPerPage']),
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
            },
            postWithGeoLocation(): any {
              return this.posts.filter((post) => post.geo_location !== null);
            }
        },
        created(): void {
            this.hydrateStateFromRoute(this.$route).then(() => {
              if (window.matchMedia('(max-width: 960px)').matches) {
                this.showMap = false;
                this.smartphone = true;
              }
              if (this.postIsOpen) {
                this.showMap = false;
              }
              window.addEventListener('resize', this.onResize);
            });
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
                if (!this.smartphone) {
                  this.showMap = false;
                }
                const postIndex = this.posts.findIndex((post) => post.id === id);
                this.setSelectedPost(this.posts[postIndex]);
                this.setPage(this.pageOfCurrentPost);
                this.setMapLocation();
            },
            openMap(): void {
                this.showMap = true;
                this.setMapLocation();
            },
            setMapLocation(): void {
              if (!this.showMap) {
                return;
              }
              const currentPost = this.selectedPost as Post;
              const location = [currentPost.geo_location.lat, currentPost.geo_location.lon] as LatLngTuple;
              this.rerenderMap();
              this.$nextTick(() => {
                  (this.$refs.map as LMap).setCenter(location);
              });
            },
            closePost(): void {
                this.setSelectedPost(null);
                if (!this.smartphone) {
                  this.showMap = true;
                }
                this.rerenderMap();
                this.$nextTick(() => {
                  this.fitMapBounds(this.posts);
                });
            },
            fitMapBounds(posts: Post[]): void {
              if (!this.showMap) {
                return;
              }
              const markers = posts.filter((post) => post.geo_location !== null )
                .map((post) => [post.geo_location.lat, post.geo_location.lon] as LatLngTuple);
              (this.$refs.map as LMap).fitBounds(markers);
            },
            rerenderMap(): void {
              if (!this.showMap) {
                return;
              }
              this.$nextTick(() => {
                (this.$refs.map as LMap).mapObject.invalidateSize();
              });
            },
            toggleMapVisibility(): void {
              this.showMap = !this.showMap;
              this.mapButtonText = (this.showMap) ? 'Karte ausblenden' : 'Karte anzeigen';
              this.$nextTick(() => {
                if (this.showMap) {
                  if (this.selectedPost !== null) {
                    this.setMapLocation();
                  } else {
                    this.rerenderMap();
                  }
                }
              });
            },
            postDistance(post: Post): string {
              if (!this.selectedLocationObject || !post.geo_location) {
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
            },
            onResize(): void {
              if (!this.smartphone && window.innerWidth <= 960 ) {
                this.smartphone = true;
                this.showMap = false;
                this.mapButtonText = 'Karte anzeigen';
              } else if (this.smartphone && window.innerWidth > 960) {
                this.smartphone = false;
                if (this.selectedPost === null) {
                  this.showMap = true;
                }
              }
            }
        }
    });
</script>

<style>
  @import "~leaflet/dist/leaflet.css";
  @import "~leaflet.markercluster/dist/MarkerCluster.css";
  @import "~leaflet.markercluster/dist/MarkerCluster.Default.css";
  @import "~leaflet-gesture-handling/dist/leaflet-gesture-handling.css";

  .copyright, .copy, .cpy, strong[class^="copyright"], strong[class^="cpy"], strong[class^="copy"] {
    clear: both;
    padding: 10px 0px;
    display: none;
  }
  .activeListItem {
    background-color: #c4e0ff !important;
  }
  .no-border tr:not(:last-child) td:not(.v-data-table__mobile-row) {
    border: 0 !important;
  }
  .detail-table table {
    border-spacing: 0 20px !important;
  }
  .detail-table td {
    height:unset !important;
  }
  .detail-table tr:hover {
    background: unset !important;
  }
  .detail-table tr td {
    vertical-align: top;
  }
  #divWithDisabledButton {
    padding-top: 21px;
    align-self: flex-start;
  }
  #disabledMapButton {
    margin-left: 35px;
    background-color: #e0e0e0;
    color: rgb(174, 168, 168) !important;
  }
  #disabledMapButton .v-icon {
    color: rgb(174, 168, 168) !important;
  }
  .button-map {
    margin-top: 21px;
    margin-left: 35px;
    background-color: rgb(5, 76, 102);
    align-self: flex-start;
  }
  .button-smartphone {
    display: none;
  }
  .button-map-smartphone {
    display: none;
  }
  .button-close {
    align-self: flex-start;
  }
  .button-close-smartphone {
    position: absolute;
    right: 0;
  }
  .button-details {
    position: absolute;
    z-index: 9999;
    margin-left: 50px;
    margin-top: 20px;
    background-color: rgb(5, 76, 102) !important;
  }
  .details-smartphone {
    display: none;
  }
  .post-subtitle {
    display: -webkit-box !important;
  }
  .map-heigth {
    height: 70vh;
  }

  html, body {
    overflow-x: hidden;
  }

  @media only screen and (max-width: 960px) {
    .map-heigth {
      height: 60vh;
    }
    .map-smartphone {
      margin-bottom: 12px;
    }
    .button-map-smartphone {
      display: block;
      width: 100%;
      background-color: rgb(5, 76, 102) !important;
    }
    .details {
      display: none;
    }
    .details-smartphone {
      display: block;
      overflow: hidden;
    }
    .details-smartphone-visible {
      max-height: 10000px;
      transition: max-height 0.4s ease;
    }
    .details-smartphone-hidden {
      max-height: 0;
      transition: max-height 0.4s ease;
    }
    .details-smartphone p,
    .details-smartphone h3{
      color: rgba(0,0,0,.87)!important;
    }
    .button-details {
      display: none;
    }
    .v-application .headline {
      font-size: 1.3rem !important;
    }
    .full-text {
      white-space: normal;
    }
    .post-subtitle-hidden {
      max-height: 0;
      opacity: 0;
      position: absolute;
    }
    .post-subtitle {
      max-height: 40px;
      opacity: 1;
      transition: all 0.4s 0.2s;
    }
  }
  @media only screen and (max-width: 500px) {
    .button-map, .button-close {
      display: none;
    }
    .button-smartphone {
      display: block;
    }
  }

  @media (max-width: 480px){
    .card {
      max-width: 75vh
    }
  }

  @media (min-width:960px){
    .sitecontent {
      width: 960px;
      margin: auto;
      max-width: none;
      margin-top: 2%;
    }

    #postbox {
      margin-right: 2%;
    }

    .list-item {
      margin-top:5%; 
      margin-right: 1px;
    }
    }

    @media (min-width: 1100px){
    .sitecontent {
      width: 1100px;
      margin: auto;
      margin-top: 2%;
    }

    #postbox {
      margin-right: 2%;
    }
  }

  @media (min-width: 1300px){
    .sitecontent {
      width: 1300px;
      margin: auto;
      margin-top: 2%; 
    }

    #postbox {
      margin-right: 2%;
    }
  }

  @media (min-width: 1618px){
    .sitecontent {
      width: 1618px;
      margin-top: 2%; 
    }

    #postbox {
      margin-right: 2%;
    }
}

  @media (min-width: 1904px){
    .sitecontent {
      width: 85%;
      margin: auto;
      margin-top: 2%; 
    }

    #postbox {
      margin-right: 2%;
    }
  }
</style>
