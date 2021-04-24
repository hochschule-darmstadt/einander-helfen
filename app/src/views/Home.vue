<template>
  <div class="home">
    <Toolbar />
    <Carousel />

    <v-container class="container">
      <SearchComponent class="searchcomponent" :fullwidth="true" />

      <v-row justify="center" lg="3">
        <v-col md="3" xl="3" v-for="tag in volunteerTags" :key="tag.title">
          <v-hover v-slot:default="{ hover }">
            <v-card
              class="mx-auto"
              :elevation="hover ? 12 : 2"
              :class="{ 'on-hover': hover }"
            >
              <router-link
                style="text-decoration: none; color: inherit"
                :to="{ name: 'posts', query: { q: tag.to } }"
              >
                <v-img
                  class="white--text align-end mt-10"
                  height="300px"
                  :key="tag.title"
                  :src="tag.img"
                >
                  <v-card class="no-radius">
                    <v-card-title
                      class="justify-center black--text"
                      v-html="tag.title"
                    />
                  </v-card>
                </v-img>
              </router-link>
            </v-card>
          </v-hover>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Toolbar from "@/components/layout/Toolbar.vue";
import Carousel from "@/components/layout/Carousel.vue";
import SearchComponent from "@/components/search/SearchComponent.vue";
import { mapActions } from "vuex";

export default Vue.extend({
  components: {
    Carousel,
    Toolbar,
    SearchComponent,
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
      ] as { title: string; to: string; img: string }[],
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
