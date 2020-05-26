<template>
  <div class="home">
    <VueSlickCarousel :dots="true" :infinite="true" :autoplay="true" :autoplaySpeed="5000">
        <picture>
          <source media="(max-width: 768px)" srcset="/images/header/1_phone.jpg">
          <img src="/images/header/1.jpg">
        </picture>
      <picture>
        <source media="(max-width: 768px)" srcset="/images/header/2_phone.jpg">
        <img src="/images/header/2.jpg">
      </picture>
      <picture>
        <source media="(max-width: 768px)" srcset="/images/header/3_phone.jpg">
        <img src="/images/header/3.jpg">
      </picture>
    </VueSlickCarousel>

    <v-container>
      <v-form class="mt-12 mb-12">
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-autocomplete
              filled
              rounded
              color="white"
              label="z.B. MacherIn"
              append-icon="search"
              item-text="title"
              :items="volunteerTags"
              v-model="selectedTag"
            ></v-autocomplete>
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-col cols="12" md="6">
            <v-autocomplete
              label="Standort"
              :items="volunteerCities"
              v-model="selectedCity"
              prepend-inner-icon="place"
            >Mein Standort</v-autocomplete>
          </v-col>

          <v-col cols="12" md="2">
            <v-autocomplete
              label="Umkreis"
              :items="volunteerRadius"
              v-model="selectedRadius"
            >Überall</v-autocomplete>
          </v-col>
        </v-row>
      </v-form>

      <v-row justify="center">
        <template v-for="tag in volunteerTags">
          <v-col cols="12" md="2" :key="tag.title">
            <v-hover v-slot:default="{ hover }">
              <v-card
                height="200px"
                class="mx-auto"
                :elevation="hover ? 12 : 2"
                :class="{ 'on-hover': hover }"
              >
                <v-img class="white--text align-end" height="200px" :key="tag.title" :src="tag.img">
                  <router-link
                    style="text-decoration: none; color: inherit;"
                    :to="{name: 'offers', params:{category: tag.title} }"
                  >
                    <v-card-title v-html="tag.title"></v-card-title>
                  </router-link>
                </v-img>
              </v-card>
            </v-hover>
          </v-col>
        </template>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
declare var require: any;
import Vue from 'vue';

import QueryBuilder from 'es-query-builder/dist';
import axios from 'axios';
import VueSlickCarousel from 'vue-slick-carousel';
import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css';
import 'vue-slick-carousel/dist/vue-slick-carousel.css';

export default Vue.extend({
  components: {
    VueSlickCarousel
  },

  data: () => ({
    volunteerTags: [
      {
        title: 'Macher/in',
        img: require('../../public/images/macherIN.jpeg')
      },
      {
        title: 'Denker/in',
        img: require('../../public/images/denkerIN.jpeg')
      },
      {
        title: 'Jugendarbeit',
        img: require('../../public/images/jugend.jpeg')
      },
      {
        title: 'Soziales',
        img: require('../../public/images/sozial.jpeg')
      }
    ],
    volunteerCities: [
      'Main Standort',
      'Darmstadt',
      'Frankfurt am Main',
      'Wiesbaden',
      'Mainz'
    ],
    volunteerRadius: ['Überall', '5 km', '10 km', '25 km', '50 km'],
    selectedTag: '',
    selectedCity: '',
    selectedRadius: ''
  }),

  created(): void {
    this.findArtworksByLabel('mona');
  },

  methods: {
    performQuery(query: QueryBuilder): void {
      axios.post('https://openartbrowser.org/api/de/_search', query.build()).then((result) => console.log(result));
    },

    findArtworksByLabel(label: string): void {
      const query = new QueryBuilder()
              .size(20)
              .sort()
              .mustMatch('type', 'artwork')
              .shouldMatch('label', `${label}`);
      this.performQuery(query);
    }
  }
});
</script>

<style scoped>
.v-card {
  transition: opacity 0.4s ease-in-out;
}

.v-card.on-hover {
  opacity: 0.7;
}

img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>
