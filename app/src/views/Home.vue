<!-- The page 'Home' and the entry point when visiting einander-helfen.org. It show a slide show of pictures, the SearchComponent and 4 examples of tags to search. -->

<template>
  <div class="home">
    <Header />
    <Carousel />

    <section class="container">
      <SearchComponent class="searchcomponent" />

      <ImageCards v-if="postLoaded" :cards="volunteerTags" />
    </section>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Header from "@/components/layout/MainHeader.vue";
import Carousel from "@/components/layout/Carousel.vue";
import SearchComponent from "@/components/search/SearchComponent.vue";
import { mapActions } from "vuex";
import PostService, { SearchParameters } from "@/services/PostService";
import Post from "@/models/post";
import ImageCards from "@/components/layout/ImageCards.vue";
import { Card } from "@/components/layout/ImageCard.vue";

export default Vue.extend({
  name: "HomeView",
  components: {
    Carousel,
    Header,
    SearchComponent,
    ImageCards,
  },
  watch: {
    title: {
      immediate: true,
      handler() {
        document.title = "Einander Helfen";
      },
    },
  },
  data: function () {
    return {
      postLoaded: false,
      volunteerTags: [
        {
          title: "FSJ",
          search: ["Freiwilliges Soziales Jahr", "Kinder"],
          img: require("../../public/images/categories/macherIN.jpeg"),
          post: undefined,
        },
        {
          title: "FÖJ",
          search: ["Freiwilliges Ökologisches Jahr", "Kinder"],
          img: require("../../public/images/categories/denkerIN.jpeg"),
          post: undefined,
        },
        {
          title: "Ehrenamt",
          search: ["Ehrenamt", "Senioren"],
          img: require("../../public/images/categories/sozial.jpeg"),
          post: undefined,
        },
        {
          title: "Freiwilligenarbeit",
          search: ["Freiwilligenarbeit", "Kinder"],
          img: require("../../public/images/categories/jugend.jpeg"),
          post: undefined,
        },
      ] as Card[],
    };
  },
  created() {
    // clear search params on home load
    this.clearSearchParams();
    this.loadPosts();
  },
  methods: {
    ...mapActions(["clearSearchParams"]),
    async getPost(searchValue: string[]): Promise<Post> {
      const searchParams: SearchParameters = {
        searchValues: searchValue,
        from: 1,
        size: 10,
        international: false,
      };
      const PaginatedPosts = await PostService.findPosts(searchParams);
      let randomId = Math.random() * 10;
      while (PaginatedPosts.data[Math.floor(randomId)].task == null) {
        randomId = Math.random() * 10;
      }
      return PaginatedPosts.data[Math.floor(randomId)];
    },
    async loadPosts(): Promise<void> {
      this.postLoaded = false;
      const postsWithIndexPromise = this.volunteerTags.map(
        async (volunteerTag, index) => {
          const post = await this.getPost(volunteerTag.search);
          return {
            index,
            post,
          };
        }
      );
      const postsWithIndex = await Promise.all(postsWithIndexPromise);

      postsWithIndex.forEach((postWithIndex) => {
        this.volunteerTags[postWithIndex.index].post = postWithIndex.post;
      });
      this.postLoaded = true;
    },
  },
});
</script>

<style lang="scss" scoped>
.searchcomponent {
  margin: 3em 0;
}
</style>
