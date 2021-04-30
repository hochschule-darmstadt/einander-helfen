<template>
  <div>
    <Header />
    <PostsLoader @postsChange="onPostsChange" @extendRadius="onRadiusExtended">
      <template v-slot="{ allPosts, pagePosts }">
        <v-container class="sitecontent row wrap no-gutters">
          <MapButton v-if="smartphone" v-model="showMap" />

          <!-- right side content for desktop-->
          <v-flex class="map xs12 md6 order-md2">
            <!-- Map -->
            <MapCard
              v-show="showMap"
              :posts="allPosts"
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
            <div
              v-if="showRadiusExtendedMessage"
              class="text-center pt-12 pb-12"
            >
              <h3 class="font-weight-bold">
                Zu Ihrer Suchanfrage mit einem Radius von
                {{ oldRadius }} haben wir keine Treffer gefunden.
                <template v-if="radius.value"
                  >Folgende Ergebnisse werden in einem Umkreis von
                  {{ radius }} gefunden.</template
                >
                <template v-else
                  >Folgende Ergebnisse werden in einem Umkreis von mehr als 50
                  km gefunden.</template
                >
              </h3>
            </div>

            <PostListItem
              v-for="post in pagePosts"
              :key="post.id"
              :post="post"
              :active="post.id == selectedPost.id"
              :showDetail="smartphone"
              @click="currentPostId === post.id ? closePost() : openPost(post)"
            />

            <div class="text-center pt-12" v-if="!allPosts.length">
              <h3 class="font-weight-bold">
                Es wurden keine Suchergebnisse zu Ihrer Suchanfrage gefunden.
              </h3>
            </div>
          </v-flex>
        </v-container>
      </template>
    </PostsLoader>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Header from "@/components/layout/Header.vue";
import PostCard from "@/components/posts/PostCard.vue";
import MapCard from "@/components/posts/MapCard.vue";
import PostListItem from "@/components/posts/PostListItem.vue";
import PostsLoader from "@/components/posts/PostsLoader.vue";
import MapButton from "@/components/posts/MapButton.vue";

import Radius from "@/models/radius";
import Post from "@/models/post";
import { mapActions, mapMutations, mapState } from "vuex";

export default Vue.extend({
  name: "PostsView",
  components: {
    Header,
    MapButton,
    PostsLoader,
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
    ...mapState("postsModule", ["selectedPost"]),
  },
  mounted(): void {
    this.hydrateStateFromRoute().then(() => {
      // check if device is smartphone view
      if (window.matchMedia("(max-width: 960px)").matches) {
        this.showMap = false;
        this.smartphone = true;
      }
      // close map if a post is open
      if (this.selectedPost) this.showMap = false;

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
  },
  methods: {
    ...mapMutations("postsModule", ["setSelectedPostId"]),
    ...mapActions(["hydrateStateFromRoute"]),

    /** Open details for a post */
    openPost(post: Post): void {
      // close map to show detail page
      if (!this.smartphone) this.showMap = false;
      // set selected post
      this.setSelectedPostId(post.id);
    },
    /** Close current selected post  */
    closePost(): void {
      this.setSelectedPostId(undefined);
      if (!this.smartphone) {
        this.showMap = true;
      }
    },
    /** Show the map  */
    openMap(): void {
      this.showMap = true;
    },
    onPostsChange(posts: Post[]) {
      // Open post if list contains only one post.
      if (posts.length === 1) this.openPost(posts[0]);
      // there is a full list of posts
      else if (posts.length) {
        this.showRadiusExtendedMessage = this.radiusExtendedFrom ? true : false;
      }
      // else there are no posts in the list
    },
    onRadiusExtended(radii: Radius[]) {
      const oldRadius = radii[0];
      const newRadius = radii[1];

      // Wir wollen uns merken, dass wir den Radius verändert haben, um den Nutzer darüber zu informieren.
      // Aber nur, wenn wir das nicht bereits gemacht haben um uns den Wert nicht zu überschreiben.
      if (!this.radiusExtendedFrom) {
        this.radiusExtendedFrom = oldRadius;
      }
    },
    /** Resize handler for window Resize */
    onResize(): void {
      if (!this.smartphone && window.innerWidth <= 960) {
        this.smartphone = true;
        this.showMap = false;
      } else if (this.smartphone && window.innerWidth > 960) {
        this.smartphone = false;
        if (this.selectedPost === null) {
          this.showMap = true;
        }
      }
    },
  },
});
</script>
<style lang="scss" scoped>
.details {
  height: 75vh;
  overflow: auto;
}
</style>

<style>
@media (min-width: 960px) {
  .sitecontent {
    width: 960px;
    margin: auto;
    max-width: none;
    margin-top: 2%;
  }

  #postbox {
    margin-right: 2%;
  }
}

@media (min-width: 1100px) {
  .sitecontent {
    width: 1100px;
    margin: auto;
    margin-top: 2%;
  }

  #postbox {
    margin-right: 2%;
  }
}

@media (min-width: 1300px) {
  .sitecontent {
    width: 1300px;
    margin: auto;
    margin-top: 2%;
  }

  #postbox {
    margin-right: 2%;
  }
}

@media (min-width: 1618px) {
  .sitecontent {
    width: 1618px;
    margin-top: 2%;
  }

  #postbox {
    margin-right: 2%;
  }
}

@media (min-width: 1904px) {
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
