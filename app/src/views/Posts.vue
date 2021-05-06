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
        <div v-if="radiusExtended" class="text-center pt-12 pb-12">
          <h3 class="font-weight-bold">
            Zu Ihrer Suchanfrage mit einem Radius von
            {{ radiusExtendedFrom }} haben wir keine Treffer gefunden.
            <template v-if="selectedRadius">
              Folgende Ergebnisse werden in einem Umkreis von
              {{ selectedRadius }} gefunden.
            </template>
            <template v-else>
              Folgende Ergebnisse werden in einem Umkreis von mehr als 50 km
              gefunden.
            </template>
          </h3>
        </div>

        <PostListItem
          v-for="post in postsOnCurrentPage"
          :key="post.id"
          :post="post"
          :active="post.id == selectedPostId"
          :showDetail="smartphone"
          :location="selectedLocation"
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

import Post from "@/models/post";
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";
import radii from "@/resources/radii";

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
    };
  },
  computed: {
    ...mapState("postsModule", ["selectedPost", "posts", "resultsFrom"]),
    ...mapGetters("postsModule", ["postsOnCurrentPage", "selectedPostId"]),
    ...mapState(["radiusExtended", "radiusExtendedFrom"]),
    ...mapState("searchModule", [
      "selectedLocation",
      "selectedRadius",
      "searchValues",
      "international",
    ]),
    ...mapGetters("searchModule", []),
  },
  created(): void {
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
  watch: {},
  methods: {
    ...mapMutations("searchModule", ["setSelectedRadius"]),
    ...mapActions("postsModule", ["setSelectedPost"]),
    ...mapActions(["hydrateStateFromRoute", "updateURIFromState", "loadPosts"]),

    /** Open details for a post */
    openPost(post: Post): void {
      // close map to show detail page
      if (!this.smartphone) this.showMap = false;
      // set selected post
      this.setSelectedPost(post).then(() =>
        // update uri with post
        this.updateURIFromState()
      );
    },
    /** Close current selected post  */
    closePost(): void {
      // show map on smartphone
      if (!this.smartphone) this.showMap = true;
      // remove selected post
      this.setSelectedPost(undefined).then(() =>
        // update uri without post
        this.updateURIFromState()
      );
    },
    /** Show the map  */
    openMap(): void {
      // TODO: Details Button is not shown -  map is not focusing on the item
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
    // full height minus header, footer and pagination height
    height: calc(100vh - 340px);
  }

  .list {
    overflow-y: auto;
    margin-right: 1%;
    flex-basis: 49%;
    padding-right: 3px;
    padding-left: 3px;
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
    padding: 0 5px;
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
