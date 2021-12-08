<!-- The page 'Home' and the entry point when visiting einander-helfen.org. It show a slide show of pictures, the SearchComponent and 4 examples of tags to search. -->

<template>
  <div class="home">
    <Header />
    <Carousel />

    <section class="container">
      <SearchComponent class="searchcomponent" />

      <ImageCard :cards="volunteerTags" />
    </section>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Header from "@/components/layout/MainHeader.vue";
import Carousel from "@/components/layout/Carousel.vue";
import ImageCard, { Card } from "@/components/layout/ImageCards.vue";
import SearchComponent from "@/components/search/SearchComponent.vue";
import { mapActions } from "vuex";

export default Vue.extend({
  name: "HomeView",
  components: {
    Carousel,
    Header,
    SearchComponent,
    ImageCard,
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
      volunteerTags: [
        {
          title: "Arbeit mit Kindern",
          to: "Kinder",
          imgBasePath: "/images/categories/macherIN",
        },
        {
          title: "Arbeit mit Jugendlichen",
          to: "Jugend",
          imgBasePath: "/images/categories/denkerIN",
        },
        {
          title: "Arbeit mit Senioren",
          to: "Senioren",
          imgBasePath: "/images/categories/sozial",
        },
        {
          title: "Betreuung",
          to: "Betreuung",
          imgBasePath: "/images/categories/jugend",
        },
      ] as Card[],
    };
  },
  created() {
    // clear search params on home load
    this.clearSearchParams();
  },
  methods: {
    ...mapActions(["clearSearchParams"]),
  },
});
</script>

<style lang="scss" scoped>
.searchcomponent {
  margin: 3em 0;
}
</style>
