<template>
  <div class="posts-page" v-if="isInitialised">
    <Header />
    <section class="sitecontent row">
      <MapButton v-if="smartphone" v-model="showMap" />

      <!-- right side content for desktop-->
      <v-flex class="map xs12 md6 order-md2">
        <!-- Map -->
        <MapCard
          :show="!smartphone || showMap"
          :posts="posts"
          :selectedPost="selectedPost"
          @openPost="togglePostDetails"
        />
        <!-- detail card if not smartphone -->
        <PostCard
          v-if="!smartphone && !isLoading"
          class="map-overlay"
          :show="!showMap"
          :post="selectedPost"
          @close="togglePostDetails"
          @openMap="openMap"
        />
        <v-skeleton-loader
          v-if="showMap && isLoading"
          height="100%"
          width="100%"
          type="image"
          light
          class="map-overlay map-loader"
        />
      </v-flex>

      <!--left side content for desktop-->
      <v-flex class="list sm12 md6 order-md1">
        <template v-if="isLoading">
          <PostListItemSkeleton v-for="i in 3" :key="i" />
        </template>
        <template v-else>
          <template v-if="radiusExtended">
            <div class="text-center pt-12 pb-12">
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
          </template>

          <PostListItem
            v-for="post in postsOnCurrentPage"
            :key="post.id"
            :post="post"
            :active="post.id == selectedPostId"
            :showDetail="smartphone"
            :location="selectedLocation"
            @click="
              togglePostDetails(selectedPostId === post.id ? undefined : post)
            "
          />

          <template v-if="!posts.length">
            <div class="text-center pt-12">
              <h3 class="font-weight-bold">
                Es wurden keine Suchergebnisse zu Ihrer Suchanfrage gefunden.
              </h3>
            </div>
          </template>
        </template>
      </v-flex>
    </section>
    <PostPagination />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Header from "@/components/layout/SearchHeader.vue";
import PostCard from "@/components/posts/PostCard.vue";
import MapCard from "@/components/posts/MapCard.vue";
import PostListItem from "@/components/posts/PostListItem.vue";
import PostListItemSkeleton from "@/components/posts/PostListItemSkeleton.vue";
import PostPagination from "@/components/posts/PostPagination.vue";
import MapButton from "@/components/posts/MapButton.vue";

import Post from "@/models/post";
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";

export default Vue.extend({
  name: "PostsView",
  components: {
    Header,
    MapButton,
    PostPagination,
    PostCard,
    MapCard,
    PostListItem,
    PostListItemSkeleton,
  },
  data: function () {
    return {
      showMap: true,
      smartphone: false,
      isLoading: true,
      isInitialised: false,
    };
  },
  computed: {
    ...mapState("postsModule", ["selectedPostId", "posts", "resultsFrom"]),
    ...mapGetters("postsModule", ["postsOnCurrentPage", "selectedPost"]),
    ...mapState(["radiusExtended", "radiusExtendedFrom"]),
    ...mapState("searchModule", [
      "selectedLocation",
      "selectedRadius",
      "searchValues",
      "isInternational",
    ]),
  },
  mounted(): void {
    // get params from route
    this.hydrateStateFromRoute()
      .then(() => {
        this.isInitialised = true;
        this.isLoading = true;
        // load posts by updated state parameter
        return this.loadPosts()
          .then(() => this.togglePostDetails(this.selectedPost))
          .finally(() => (this.isLoading = false));
      })
      // set properties
      .then(() => {
        // check if device is smartphone view
        if (window.matchMedia("(max-width: 959px)").matches) {
          this.showMap = false;
          this.smartphone = true;
        }
        // close map if a post is open
        if (this.selectedPost) {
          this.showMap = false;
        }

        // set resize event handler
        window.addEventListener("resize", this.onWindowResize);
      })
      // do stuff after parameters are loaded from route
      .then(() => {
        // add watcher to fire load event if search parameter have changed
        this.$watch(
          // watch all parameters which are used to find posts
          () => (
            this.searchValues,
            this.isInternational,
            this.selectedLocation,
            this.selectedRadius,
            // and to be sure that a different value is returned every time
            Date.now()
          ),
          () => {
            this.isLoading = true;
            // clear selected post
            this.togglePostDetails();
            // clear total result
            this.resetTotalResults();
            // and execute loadPosts
            this.loadPosts().finally(() => (this.isLoading = false));
          }
        );
        // results from is changes if the page is changed a new junk must be laoded
        this.$watch(
          () => (this.resultsFrom, Date.now()),
          () => {
            this.isLoading = true;
            // clear selected post
            this.togglePostDetails();
            // and execute loadPosts
            this.loadPosts().finally(() => (this.isLoading = false));
          }
        );
      });
  },
  beforeDestroy(): void {
    // remove event handler
    window.removeEventListener("resize", this.onWindowResize);
  },
  methods: {
    ...mapMutations("searchModule", ["setSelectedRadius"]),
    ...mapMutations("postsModule", ["resetTotalResults"]),
    ...mapActions("postsModule", ["setSelectedPostId"]),
    ...mapActions([
      "hydrateStateFromRoute",
      "updateURIFromState",
      "loadPosts",
      "loadPost",
    ]),
    /** Opens a post if a post is given, else clear the selected post */
    togglePostDetails(post: Post | undefined = undefined): void {
      // close map to show detail page if not smartphone
      if (post && !this.smartphone) this.showMap = false;
      // show map if not smartphone
      if (!post && !this.smartphone) this.showMap = true;
      // set selected post id or set undefined in store
      const id = post ? post.id : undefined;
      this.setSelectedPostId(id).then(() =>
        // update uri
        this.updateURIFromState()
      );
    },
    /** Show the map  */
    openMap(): void {
      this.showMap = true;
    },
    /** Resize handler for window Resize */
    onWindowResize(): void {
      // swtich to smartphone view
      if (!this.smartphone && window.innerWidth < 960) {
        this.smartphone = true;
        this.showMap = false;
      }
      // switch to desktop view
      else if (this.smartphone && window.innerWidth >= 960) {
        this.smartphone = false;
        if (!this.selectedPost) {
          this.showMap = true;
        }
      }
    },
  },
});
</script>

<style lang="scss" scoped>
@media screen and (max-width: 959px) {
  .map {
    overflow: hidden;
  }
}
@media screen and (min-width: 960px) {
  .posts-page {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: space-between;
  }
  .map,
  .map-loader v-deep .v-skeleton-loader__image,
  .list {
    // full height minus header, footer and pagination height
    height: calc(100vh - 325px);
  }

  .list {
    overflow-y: auto;
    margin-right: 1%;
    flex-basis: 49%;
    padding-right: 3px;
    padding-left: 3px;
  }

  .map {
    position: relative;

    .map-overlay {
      z-index: 1000;
      position: absolute;
      top: 0;
    }
  }
  .map-loader {
    background-color: white;
    &::v-deep > div {
      height: 100% !important;
    }
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
