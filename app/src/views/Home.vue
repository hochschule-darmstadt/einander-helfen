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
  data: function () {
    return {
      volunteerTags: [
        {
          title: "Arbeit mit Kindern",
          to: "Kinder",
          img: require("@/assets/images/macherIN.jpeg"),
        },
        {
          title: "Arbeit mit Jugendlichen",
          to: "Jugend",
          img: require("@/assets/images/denkerIN.jpeg"),
        },
        {
          title: "Arbeit mit Senioren",
          to: "Senioren",
          img: require("@/assets/images/sozial.jpeg"),
        },
        {
          title: "Betreuung",
          to: "Betreuung",
          img: require("@/assets/images/jugend.jpeg"),
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
