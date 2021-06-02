<template>
  <div class="home">
    <Header />
    <Carousel />

    <v-container class="container">
      <SearchComponent class="searchcomponent" />

      <ImageCard :cols="12" :cards="volunteerTags" />
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Header from "@/components/layout/MainHeader.vue";
import Carousel from "@/components/layout/Carousel.vue";
import ImageCard, { Card } from "@/components/layout/ImageCard.vue";
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

.container {
  margin: auto;
}

@media (min-width: 800px) {
  .container {
    max-width: 1450px;
  }
}

@media (min-width: 960px) {
  .container {
    width: 960px;
    max-width: none;
  }
}

@media (min-width: 1100px) {
  .container {
    width: 1100px;
  }
}

@media (min-width: 1300px) {
  .container {
    width: 1300px;
  }
}

@media (min-width: 1618px) {
  .container {
    width: 1618px;
  }
}

@media (min-width: 1904px) {
  .container {
    width: 85%;
  }
}
</style>
