<template>
  <div>
    <Header />
    <v-row ref="wrapper" no-gutters>
      <v-col cols="6">
        <div ref="wrapperPosts" style="height:75vh;overflow:auto">
          <template v-for="(advertisement, i) in visiblePages">
            <v-card class="mb-3" tile>
              <v-list-item three-line @click="openAdvertisement(i+(page-1)*perPage)">
                <v-list-item-content>
                  <v-list-item-title class="headline mb-1">{{
                    advertisement.title
                  }}</v-list-item-title>
                  <v-list-item-subtitle>{{
                    advertisement.task
                  }}</v-list-item-subtitle>
                </v-list-item-content>

                <v-img
                  max-width="80px"
                  height="80px"
                  contain
                  :src="advertisement.image"
                ></v-img>
              </v-list-item>
            </v-card>
          </template>
        </div>
        <!--pageination-->
        <div class="text-center" style="margin-top:2%">
          <v-pagination v-model="page" :length="numberOfPages" color="#054C66"></v-pagination>

        </div>
      </v-col>

      <!--map-->
      <v-col cols="6" v-if="!postIsOpen">
        <v-card tile height="75vh" style="position: absolute">
          <div id="map" :style="{height: map.height + 'px', width: map.width + 'px'}">
            <v-btn @click="closeMap()" style="position: absolute; z-index: 9999; margin-left: 50px; margin-top: 20px;">Details</v-btn>
            <l-map ref="map" :center="map.center" :zoom="map.zoom">
              <l-tile-layer :url="map.url" :attribution="map.attribution"></l-tile-layer>
              <template v-for="(advertisement, i) in posts">
                <l-marker v-if="i === currentPostId" :icon="map.markerRed" :lat-lng="[advertisement.lat, advertisement.lon]" @click="openAdvertisement(i)">
                  <l-tooltip>{{ advertisement.title }}</l-tooltip>
                </l-marker>
                <l-marker v-else :icon="map.markerBlue" :lat-lng="[advertisement.lat, advertisement.lon]" @click="openAdvertisement(i)">
                  <l-tooltip>{{ advertisement.title }}</l-tooltip>
                </l-marker>
              </template>
            </l-map>
          </div>
          <!--<v-img
            src="https://media.wired.com/photos/59269cd37034dc5f91bec0f1/master/pass/GoogleMapTA.jpg"
            height="100%"
            width="100%"
          ></v-img>-->
        </v-card>
      </v-col>
      <v-col cols="6" v-if="postIsOpen">
        <v-card
          tile
          height="75vh"
          width="50%"
          style="position: absolute;overflow:auto"
        >
          <v-list-item three-line>
            <v-btn class="mr-3" text @click="closeAdvertisement()">
              <v-icon>arrow_back</v-icon>
            </v-btn>
            <!--display title, subtitle and image on the left side-->
            <v-list-item-content style="margin-top:2%">
              <v-list-item-title class="headline mb-1">{{
                currentPost.title
              }}</v-list-item-title>
              <v-list-item-subtitle>{{
                currentPost.task
              }}</v-list-item-subtitle>
            </v-list-item-content>

            <v-img
              style="margin-top:2%"
              max-width="80px"
              height="80px"
              contain
              :src="currentPost.image"
            ></v-img>
          </v-list-item>

          <!--display content on the right side-->
          <v-card-text style="padding-left:5%; padding-right:5%">
            <v-row v-if="currentPost.location">
              <v-col cols="2">Einsatzort</v-col>
              <v-col cols="8" v-html="currentPost.location"></v-col>
            </v-row>
            <v-row v-if="currentPost.target_group">
              <v-col cols="2">Zielgruppe</v-col>
              <v-col
                cols="8"
                v-html="currentPost.target_group"
              ></v-col>
            </v-row>
            <v-row v-if="currentPost.timing">
              <v-col cols="2">Einstiegsdatum / Beginn</v-col>
              <v-col cols="8" v-html="currentPost.timing"></v-col>
            </v-row>
            <v-row v-if="currentPost.effort">
              <v-col cols="2">Zeitaufwand</v-col>
              <v-col cols="8" v-html="currentPost.effort"></v-col>
            </v-row>
            <v-row v-if="currentPost.opportunities">
              <v-col cols="2">Möglichkeiten</v-col>
              <v-col
                cols="8"
                v-html="currentPost.opportunities"
              ></v-col>
            </v-row>
            <v-row v-if="currentPost.organization">
              <v-col cols="2">Organisation</v-col>
              <v-col
                cols="8"
                v-html="currentPost.organization"
              ></v-col>
            </v-row>
            <v-row v-if="currentPost.contact">
              <v-col cols="2">Kontakt</v-col>
              <v-col cols="8" v-html="currentPost.contact"></v-col>
            </v-row>
          </v-card-text>

          <v-card-actions>
            <v-col>
              <v-container style="margin-bottom: 10px">
                <template
                  v-for="(category, i) in currentPost.categories"
                >
                  <v-chip :key="i" class="mr-2">{{ category }}</v-chip>
                </template>
              </v-container>
              <v-spacer></v-spacer>
              <v-container style="display:flex;justify-content:center;">
                <v-btn
                  class="my-2"
                  dark
                  large
                  color="#F29472"
                  :href="currentPost.link"
                  target="_blank"
                >
                  Zum Stellenangebot
                  <!--<v-icon dark>arrow_forward</v-icon>-->
                </v-btn>
              </v-container>
            </v-col>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<!-- test content -->
<script lang="ts">
import Header from '@/components/layout/Header.vue';
import Advertisement from '@/models/advertisement';

import Vue from 'vue';
import { mapActions, mapState } from 'vuex';

import L from 'leaflet';
import { LMap, LTileLayer, LMarker , LTooltip, LIcon} from 'vue2-leaflet';
import 'leaflet/dist/leaflet.css';

export default Vue.extend({
  components: { Header, LMap, LTileLayer, LMarker, LTooltip },
  data(): {
    postIsOpen: boolean;
    currentPostId: number;
    page: number;
    perPage: number;
    map: any;
  } {
    return {
      postIsOpen: false,
      currentPostId: 0,
      page: 1,
      perPage: 7,
      map: {
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        center: [51.5000, 10.5000],
        zoom: 6,
        width: 700,
        height: 700,
        markerBlue: L.icon({
          iconUrl: '/images/marker/marker-icon.png',
          iconRetinaUrl: '/images/marker/marker-icon-2x.png'
        }),
        markerRed: L.icon({
          iconUrl: '/images/marker/marker-icon-red.png',
          iconRetinaUrl: '/images/marker/marker-icon-2x-red.png'
        })
      }
    };
  },
  computed: {
    ...mapState(['posts']),
    visiblePages(): Advertisement[] {
      return this.posts.slice(
        (this.page - 1) * this.perPage,
        this.page * this.perPage
      );
    },
    currentPost(): Advertisement | null {
      return this.postIsOpen
        ? this.posts[this.currentPostId]
        : null;
    },
    numberOfPages(): number {
      return Math.ceil(this.posts.length / this.perPage);
    }
  },
  created(): void {
    this.hydrateStateFromURIParams(this.$route.query);
    window.addEventListener('resize', this.resize);
  },
  mounted(): void {
    this.map.height = (this.$refs.wrapperPosts as HTMLElement).clientHeight;
    const wrapperWidth = (this.$refs.wrapper as HTMLElement).clientWidth;
    const wrapperPostsWidth = (this.$refs.wrapperPosts as HTMLElement).clientWidth;
    this.map.width = wrapperWidth - wrapperPostsWidth;
  },
  destroyed(): void {
    window.removeEventListener('resize', this.resize);
  },
  watch: {
    posts(val: Advertisement[], oldVal: Advertisement[]): void {
        if (val.length === 1) {
          this.openAdvertisement(0);
        }
    }
  },
  methods: {
    ...mapActions(['hydrateStateFromURIParams']),
    openAdvertisement(index: number): void {
      this.postIsOpen = true;
      this.currentPostId = index;
    },
    closeAdvertisement(): void {
      this.postIsOpen = false;
    },
    numberOfPages(): number {
      return Math.ceil(this.posts.length / this.perPage);
    },
    closeMap(): void {
      this.postIsOpen = true;
    },
    resize(e: UIEvent): void {
      this.map.height = (this.$refs.wrapperPosts as HTMLElement).clientHeight;
      const wrapperWidth = (this.$refs.wrapper as HTMLElement).clientWidth;
      const wrapperPostsWidth = (this.$refs.wrapperPosts as HTMLElement).clientWidth;
      this.map.width = wrapperWidth - wrapperPostsWidth;
    }
  }
});
</script>

<style scoped></style>
