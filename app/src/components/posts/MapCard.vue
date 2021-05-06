<template>
  <v-card class="map" :style="{ height: map.height, width: map.width }" tile>
    <v-btn
      v-if="selectedPost != undefined"
      class="button-details"
      dark
      @click="openPost(selectedPost)"
    >
      <v-icon>info</v-icon> Details
    </v-btn>
    <LMap
      ref="map"
      :center="map.center"
      :zoom="map.zoom"
      :options="{ gestureHandling: true }"
    >
      <LTileLayer :url="map.url" :attribution="map.attribution" />
      <LMarckerCluster>
        <Lmarker
          v-for="post in postWithGeoLocation"
          :key="post.id"
          :icon="
            selectedPost && post.id === selectedPost.id
              ? map.markerRed
              : map.markerBlue
          "
          :lat-lng="[post.geo_location.lat, post.geo_location.lon]"
          @click="openPost(post)"
        >
          <LTooltip :content="post.title" />
        </Lmarker>
      </LMarckerCluster>
    </LMap>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import Post from "@/models/post";

// Map components
import L, { LatLngTuple } from "leaflet";
import { LMap, LTileLayer, LTooltip } from "vue2-leaflet";
import Vue2LeafletMarkerCluster from "vue2-leaflet-markercluster/Vue2LeafletMarkercluster.vue";
import * as Vue2Leaflet from "vue2-leaflet";
import { GestureHandling } from "leaflet-gesture-handling";

L.Map.addInitHook("addHandler", "gestureHandling", GestureHandling);

/**
 * Emits @openPost if single post is clickt
 */
export default Vue.extend({
  name: "MapCard",
  components: {
    LMap,
    LTileLayer,
    LTooltip,
    Lmarker: Vue2Leaflet.LMarker,
    LMarckerCluster: Vue2LeafletMarkerCluster,
  },
  props: {
    posts: {
      type: Array as () => Post[],
      required: true,
    },
    selectedPost: {
      type: Object as () => Post,
    },
  },
  data: function () {
    return {
      map: {
        url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attribution:
          '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        center: [51.5, 10.5],
        zoom: 12,
        width: "100%",
        height: "100%",
        markerBlue: L.icon({
          iconUrl: require("@/assets/images/marker/marker-icon.png"),
          iconSize: [25, 41],
        }),
        markerRed: L.icon({
          iconUrl: require("@/assets/images/marker/marker-icon-red.png"),
          iconSize: [25, 41],
        }),
      },
    };
  },
  computed: {
    /**
     * filter only posts that have a gea_location
     */
    postWithGeoLocation(): any {
      return this.posts.filter((post) => post.geo_location !== null);
    },
  },
  watch: {
    selectedPost() {
      this.rerenderMap();
    },
    posts() {
      this.rerenderMap();
    },
  },
  mounted(): void {
    this.rerenderMap();
  },
  methods: {
    rerenderMap(): void {
      this.$nextTick(() => {
        (this.$refs.map as LMap).mapObject.invalidateSize();
        this.$nextTick(() => {
          this.fitMapBounds();
          this.setMapLocation();
        });
      });
    },

    setMapLocation(): void {
      if (this.selectedPost) {
        const location = [
          this.selectedPost.geo_location.lat,
          this.selectedPost.geo_location.lon,
        ] as LatLngTuple;
        this.$nextTick(() => {
          (this.$refs.map as LMap).setCenter(location);
        });
      }
    },

    /**
     * Sets the viewpost of the map to all marks
     */
    fitMapBounds(): void {
      if (this.posts.length) {
        const markers = this.posts
          .filter((post) => post.geo_location !== null)
          .map(
            (post) =>
              [post.geo_location.lat, post.geo_location.lon] as LatLngTuple
          );
        (this.$refs.map as LMap).fitBounds(markers);
      }
    },

    openPost(post: Post): void {
      this.$emit("openPost", post);
    },
  },
});
</script>

<style>
/** load leaflet css */
@import "~leaflet/dist/leaflet.css";
@import "~leaflet.markercluster/dist/MarkerCluster.css";
@import "~leaflet.markercluster/dist/MarkerCluster.Default.css";
@import "~leaflet-gesture-handling/dist/leaflet-gesture-handling.css";
</style>

<style lang="scss" scoped>
.button-details {
  position: absolute;
  z-index: 500;
  margin-left: 50px;
  margin-top: 20px;
  background-color: rgb(5, 76, 102) !important;
}

.map ::v-deep a {
  color: #1976d2 !important;
  &:hover {
    color: #000 !important;
  }
}
@media only screen and (max-width: 960px) {
  .button-details {
    display: none;
  }
}
</style>

<style lang="scss">
/** global style */
.copyright,
.copy,
.cpy,
strong[class^="copyright"],
strong[class^="cpy"],
strong[class^="copy"] {
  clear: both;
  padding: 10px 0px;
  display: none;
}
</style>
