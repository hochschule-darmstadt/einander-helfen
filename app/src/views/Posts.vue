<template>
  <div class="posts-page">
    <Header />
    <section class="sitecontent row">
      <MapButton v-if="smartphone" v-model="showMap" />

      <!-- right side content for desktop-->
      <v-flex class="map xs12 md6 order-md2">
        <!-- Map -->
        <MapCard
          v-show="showMap"
          :posts="posts"
          :activePost="selectedPost"
          @openPost="openPost"
        />
        <!-- detail card if not smartphone -->
        <PostCard
          v-if="!showMap && !smartphone"
          :post="selectedPost"
          @close="closePost"
          @openMap="openMap"
        />
      </v-flex>

      <!--left side content for desktop-->
      <v-flex class="list sm12 md6 order-md1">
        <!-- TODO: is this properlly working?! -->
        <div v-if="showRadiusExtendedMessage" class="text-center pt-12 pb-12">
          <h3 class="font-weight-bold">
            Zu Ihrer Suchanfrage mit einem Radius von
            {{ oldRadius }} haben wir keine Treffer gefunden.
            <template v-if="radius.value"
              >Folgende Ergebnisse werden in einem Umkreis von
              {{ radius }} gefunden.</template
            >
            <template v-else
              >Folgende Ergebnisse werden in einem Umkreis von mehr als 50 km
              gefunden.</template
            >
          </h3>
        </div>

        <PostListItem
          v-for="post in postsOnCurrentPage"
          :key="post.id"
          :post="post"
          :active="post.id == selectedPostId"
          :showDetail="smartphone"
          @click="selectedPostId === post.id ? closePost() : openPost(post)"
        />

        <div class="text-center pt-12" v-if="!posts.length">
          <h3 class="font-weight-bold">
            Es wurden keine Suchergebnisse zu Ihrer Suchanfrage gefunden.
          </h3>
        </div>
      </v-flex>
    </section>
    <PostPagination />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Header from "@/components/layout/Header.vue";
import PostCard from "@/components/posts/PostCard.vue";
import MapCard from "@/components/posts/MapCard.vue";
import PostListItem from "@/components/posts/PostListItem.vue";
import PostPagination from "@/components/posts/PostPagination.vue";
import MapButton from "@/components/posts/MapButton.vue";

import Radius from "@/models/radius";
import Post from "@/models/post";
import radii from "@/resources/radii";
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";

// TODO: add isLoading state
export default Vue.extend({
  name: "PostsView",
  components: {
    Header,
    MapButton,
    PostPagination,
    PostCard,
    MapCard,
    PostListItem,
  },
  data: function () {
    return {
      showMap: true,
      smartphone: false,
      radiusExtendedFrom: undefined as Radius | undefined,
      showRadiusExtendedMessage: false,
    };
  },
  computed: {
    ...mapState("postsModule", ["selectedPost", "posts", "resultsFrom"]),
    ...mapGetters("postsModule", ["postsOnCurrentPage", "selectedPostId"]),
    ...mapState("searchModule", [
      "selectedLocation",
      "selectedRadius",
      "searchValues",
      "international",
    ]),
  },
  mounted(): void {
    // get params from route query and execute findPosts
    this.hydrateStateFromRoute()
      .then(() => {
        // check if device is smartphone view
        if (window.matchMedia("(max-width: 960px)").matches) {
          this.showMap = false;
          this.smartphone = true;
        }
        // close map if a post is open
        if (this.selectedPost) {
          this.showMap = false;
        }
      })
      .then(() => {
        this.$watch(
          // watch all parameters which are used to find posts
          () => (
            this.searchValues,
            this.international,
            this.selectedLocation,
            this.selectedRadius,
            this.resultsFrom,
            // and to be sure that a different value is returned every time
            Date.now()
          ),
          // and execute findPosts if a parameter change
          () => this.loadPosts()
        );

        // set resize event handler
        window.addEventListener("resize", this.onResize);
      });
  },
  beforeDestroy(): void {
    // remove event handler
    window.removeEventListener("resize", this.onResize);
  },
  watch: {
    radiusExtendedFrom(newValue, oldValue): void {
      if (oldValue !== newValue && !newValue)
        this.showRadiusExtendedMessage = false;
    },

    /** If the list of posts is emtpy, increase the radius an search again. */
    posts(posts: Post[]): void {
      // there is a full list of posts
      if (posts.length) {
        this.showRadiusExtendedMessage = this.radiusExtendedFrom ? true : false;
      }
      // if there are no posts in the list
      else {
        // if a location and a radius is set
        if (this.selectedLocation && this.selectedRadius) {
          const radiusBeforeExtend = this.selectedRadius;
          // Wenn wir mit einem Radius um einen Ort suchen, den Radius vergrößern und nochmal probieren!

          // find radius index of radii
          const currentRadiusIndex = radii.findIndex(
            (r) => r.value === radiusBeforeExtend.value
          );
          // find next bigger radii
          const nextBiggerRadius =
            radii[(currentRadiusIndex + 1) % radii.length];

          // Wir wollen uns merken, dass wir den Radius verändert haben, um den Nutzer darüber zu informieren.
          // Aber nur, wenn wir das nicht bereits gemacht haben um uns den Wert nicht zu überschreiben.
          if (!this.radiusExtendedFrom) {
            this.radiusExtendedFrom = radiusBeforeExtend;
          }

          // update radius -> new search is triggered
          this.setRadius(nextBiggerRadius);
        }
      }
    },
  },
  methods: {
    ...mapMutations("searchModule", ["setRadius"]),
    ...mapMutations("postsModule", ["setSelectedPost"]),
    ...mapActions(["hydrateStateFromRoute", "updateURIFromState", "loadPosts"]),

    /** Open details for a post */
    openPost(post: Post): void {
      // close map to show detail page
      if (!this.smartphone) this.showMap = false;
      // set selected post
      this.setSelectedPost(post);
      // update uri with post
      this.$nextTick(() => this.updateURIFromState());
    },
    /** Close current selected post  */
    closePost(): void {
      // show map on smartphone
      if (!this.smartphone) this.showMap = true;
      // remove selected post
      this.setSelectedPost(undefined);
      // update uri without post
      this.$nextTick(() => this.updateURIFromState());
    },
    /** Show the map  */
    openMap(): void {
      this.showMap = true;
    },

    /** Resize handler for window Resize */
    onResize(): void {
      // swtich to smartphone view
      if (!this.smartphone && window.innerWidth <= 960) {
        this.smartphone = true;
        this.showMap = false;
      }
      // switch to desktop view
      else if (this.smartphone && window.innerWidth > 960) {
        this.smartphone = false;
        if (!this.selectedPost) this.showMap = true;
      }
    },
  },
});
</script>

<style lang="scss" scoped>
@media (min-width: 960px) {
  .posts-page {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: space-between;
  }
  .map,
  .list {
    height: calc(100vh - 345px);
  }

  .list {
    overflow-y: auto;
    margin-right: 1%;
    flex-basis: 49%;
    padding-right: 3px;
  }
}
.sitecontent {
  @media (max-width: 959px) {
    width: 100%;
    padding: 12px;
    margin-right: auto;
    margin-left: auto;
  }
  @media (min-width: 960px) {
    width: 960px;
    margin: auto;
    max-width: none;
    margin-top: 2%;
  }
  @media (min-width: 1100px) {
    width: 1100px;
    margin: auto;
    margin-top: 2%;
  }
  @media (min-width: 1300px) {
    width: 1300px;
    margin: auto;
    margin-top: 2%;
  }
  @media (min-width: 1618px) {
    width: 1618px;
    margin-top: 2%;
  }
  @media (min-width: 1904px) {
    width: 85%;
    margin: auto;
    margin-top: 2%;
  }
}
</style>
