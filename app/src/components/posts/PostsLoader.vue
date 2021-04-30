<template>
  <div class="posts-loader">
    <!-- slot with posts from current page -->
    <slot :pagePosts="postsOnCurrentPage" :allPosts="posts" />
    <!--pageination-->
    <div class="pagination-container text-center">
      <v-pagination
        v-model="page"
        :length="numberOfPages"
        total-visible="7"
        color="#054C66"
      />
      <span class="pl-2 mt-2 d-inline-block font-italic">
        {{ totalResultSize }} Ergebnisse
      </span>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Post from "@/models/post";
import DataService, { PaginatedResponse } from "@/utils/services/DataService";
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";
import radii from "@/resources/radii";
/**
 * Emits @pageChange if page change
 * Emits @postsChange if posts on current page change
 * Emits @extendRadius if no posts are found with the current radius
 * Defaul Slot props :posts -> posts on current page change
 */
export default Vue.extend({
  name: "PostsLoader",
  data: function () {
    return {
      page: 0,
      hitsPerPage: process.env.VUE_APP_HITS_PER_PAGE || 10,
      resultSetSize: process.env.VUE_APP_RESULT_SET_SIZE || 100,
      resultsFrom: 0,
      totalResultSize: 0,
    };
  },
  computed: {
    ...mapState("searchModule", [
      "selectedLocation",
      "selectedRadius",
      "searchValues",
      "international",
    ]),
    ...mapState("postsModule", ["selectedPost", "posts"]),

    numberOfPages(): number {
      return Math.ceil(this.totalResultSize / this.hitsPerPage);
    },
    postsOnCurrentPage(): Post[] {
      const posts = this.posts.slice(
        (this.page - 1) * this.hitsPerPage - this.resultsFrom,
        this.page * this.hitsPerPage - this.resultsFrom
      );
      // emits posts of current page
      this.$emit("posts", posts);
      return posts;
    },
  },
  watch: {
    /** watch page change */
    page(page: number) {
      if (page < 1) {
        page = 1;
      }
      // Calculate the new from parameter to load the next resultSet chunk if necessary
      const currentPageIndex = (page - 1) * this.hitsPerPage; // these hu-mons start counting their pages at 1...
      const currentLoadedChunk = {
        min: this.resultsFrom,
        max: this.resultsFrom + this.resultSetSize - 1, // again with these hu-mons and their count beginning at 1...
      };
      if (!this.inChunk(currentPageIndex, currentLoadedChunk)) {
        // Calculate the needed offset
        // rounding off to the next multiple of our resultSetSize
        const from = currentPageIndex - (currentPageIndex % this.resultSetSize);
        this.resultsFrom = from;
      }

      this.$emit("page", page);
      this.setSelectedPage(page);
      this.updateURIFromState();
    },
    /** watch selected post change */
    selectedPost(selectedPost: Post) {
      if (selectedPost) {
        const postIndex = this.getSelectedPostIndex();
        if (postIndex > 0) {
          // if selectedPost is in posts set page to page of this selectedPost
          const pageOffset = this.resultsFrom / this.hitsPerPage + 1; // pages are 1 indexed...
          const pageOnPost =
            Math.floor(postIndex / this.hitsPerPage) + pageOffset;
          this.page = pageOnPost;
        } // else selectedPost not in posts => do nothing
      }
    },
  },
  mounted() {
    // Set page from uri from store
    this.page = this.getSelectedPage();

    // watch all parameters which are used to find posts
    // and execute findPosts if a parameter change
    this.$watch(
      () => (
        this.searchValues,
        this.international,
        this.selectedLocation,
        this.selectedRadius,
        this.resultsFrom,
        // and to be sure that a different value is returned every time
        Date.now()
      ),
      () => this.loadPosts()
    );

    // initial posts loading
    this.loadPosts();
  },
  methods: {
    ...mapGetters("postsModule", ["getSelectedPostIndex", "getSelectedPage"]),
    ...mapMutations("searchModule", ["setRadius"]),
    ...mapMutations("postsModule", ["setSelectedPage", "setPosts"]),
    ...mapActions(["updateURIFromState"]),

    inChunk(x: number, chunk: { min: number; max: number }): boolean {
      return x >= chunk.min && x <= chunk.max;
    },

    /** find posts from DataService by setted parameter */
    loadPosts(): Promise<Post[]> {
      return DataService.findBySelection({
        searchValues: this.searchValues,
        location: this.selectedLocation,
        radius: this.selectedRadius.value,
        from: this.resultsFrom,
        size: this.resultSetSize,
        international: this.international,
      }).then((result: PaginatedResponse<Post>) => {
        this.totalResultSize = result.meta.total;
        this.setPosts(result.data);
        return result.data;
      });
      // TODO: add catch handler and show error
    },
    /** If the list of posts is emtpy, increase the radius an search again. */
    extendRadius() {
      // if there are no posts in the list
      if (!this.posts.length) {
        // if a location and a radius is set
        if (this.selectedLocation && this.selectedRadius) {
          const radiusBeforeExtend = this.selectedRadius;
          // Wenn wir mit einem Radius um einen Ort suchen, den Radius vergrößern und nochmal probieren!

          // const myRadius = this.alternateRadius
          //   ? this.alternateRadius
          //   : this.selectedRadius;

          // find radius index of radii
          const currentRadiusIndex = radii.findIndex(
            (r) => r.value === radiusBeforeExtend.value
          );
          // find next bigger radii
          const nextBiggerRadius =
            radii[(currentRadiusIndex + 1) % radii.length];

          this.$emit("extendRadius", [radiusBeforeExtend, nextBiggerRadius]);
          // // Wir wollen uns merken, dass wir den Radius verändert haben, um den Nutzer darüber zu informieren.
          // // Aber nur, wenn wir das nicht bereits gemacht haben um uns den Wert nicht zu überschreiben.
          // if (!this.radiusExtendedFrom) {
          //   this.radiusExtendedFrom = this.selectedRadius;
          // }
          // update radius -> new search is triggered
          this.setRadius(nextBiggerRadius.value);
        }
      }
    },
  },
});
</script>

<style lang="scss" scoped>
.pagination-container {
  margin-top: 2%;
  margin-bottom: 1%;
}
</style>
