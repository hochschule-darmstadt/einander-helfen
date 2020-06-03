<template>
  <div class="home">
    <Toolbar />
    <VueSlickCarousel :dots="true" :infinite="true" :autoplay="true" :autoplaySpeed="30000">
      <picture>
        <source media="(max-width: 768px)" srcset="/images/header/1_phone.jpg" />
        <img src="/images/header/1.jpg" />
      </picture>
      <picture>
        <source media="(max-width: 768px)" srcset="/images/header/2_phone.jpg" />
        <img src="/images/header/2.jpg" />
      </picture>
      <picture>
        <source media="(max-width: 768px)" srcset="/images/header/3_phone.jpg" />
        <img src="/images/header/3.jpg" />
      </picture>
    </VueSlickCarousel>

    <v-container>
      <v-form class="mt-12 mb-12">
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-combobox
              style="background: white"
              rounded
              color="white"
              label="z.B. Macher/in"
              append-icon="search"
              item-text="title"
              autocomplete="off"
              :items="volunteerTitle"
              v-model="selectedTag"
              return-object
            ></v-combobox>
            <div class="panel-footer" v-if="objectArray"></div>
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
                class="mx-auto"
                :elevation="hover ? 12 : 2"
                :class="{ 'on-hover': hover }"
              >
                  <router-link
                    style="text-decoration: none; color: inherit;"
                    :to="{name: 'resultPage', params:{category: tag.title} }"
                  >
                    <v-img class="white--text align-end mt-10" height="300px" :key="tag.title" :src="tag.img">
                      <v-card >
                    <v-card-title class="justify-center black--text" v-html="tag.title"></v-card-title>
                      </v-card>                
                   </v-img>
                 </router-link>
              </v-card>
            </v-hover>
          </v-col>
        </template>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { mapActions } from 'vuex';

declare var require: any;
import Vue from 'vue';
import Toolbar from '@/components/layout/Toolbar.vue';

import QueryBuilder from 'es-query-builder/dist';
import axios from 'axios';
import VueSlickCarousel from 'vue-slick-carousel';
import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css';
import 'vue-slick-carousel/dist/vue-slick-carousel.css';
import Advertisement from '../models/advertisement';
import { DataService } from '../utils/services/DataService';

export default Vue.extend({
  components: {
    VueSlickCarousel,
    Toolbar
  },


  data: () => ({
    volunteerTitle: [] as string[],
    // objectArray: [] as Advertisement[],
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
        title: 'Kommunikative',
        img: require('../../public/images/jugend.jpeg')
      },
      {
        title: 'Soziale',
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
    selectedRadius: '',
  }),
  watch: {
    selectedTag(newValue, oldValue): void {
      this.$router.push({
        name: 'resultPage',
        query: {
          q: newValue,
          city: this.selectedCity,
          radius: this.selectedRadius
        }
      });
    }
  },
  created(): void {
    this.extractTitle(this.volunteerTags);
  },
  methods: {
    extractTitle(volunteerTags): void {
      volunteerTags.forEach((elem) => {
        this.volunteerTitle.push(elem.title);
      });
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
