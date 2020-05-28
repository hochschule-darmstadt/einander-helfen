<template>
  <div class="home">
    <v-img dark max-height="250px" :src="require('../../public/images/senior-mother_crop.jpg')"></v-img>

    <!--SearchBar-Container-->
    <v-container>
      <v-form class="mt-12 mb-12">
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-combobox
              filled
              rounded
              color="white"
              label="z.B. MacherIn"
              append-icon="search"
              item-text="title"
              :items="volunteerTags"
              v-model="selectedTag"
            ></v-combobox>
          </v-col>
        </v-row>
        <!--cities-->
        <v-row justify="center">
          <v-col cols="12" md="6">
            <v-autocomplete
              label="Standort"
              :items="volunteerCities"
              v-model="selectedCity"
              prepend-inner-icon="place"
            >Mein Standort</v-autocomplete>
          </v-col>
          <!--Radius-Contaienr-->
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
                    :to="{name: 'resultPage', params:{category: tag.title} }"
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
import {mapActions} from 'vuex';

declare var require: any;
import Vue from 'vue';

import QueryBuilder from 'es-query-builder/dist';
import axios from 'axios';

export default Vue.extend({
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
    selectedRadius: '',
    dummyData: null
  }),
  watch: {
    selectedTag(newValue, oldValue): void {
      this.setSearchValue(newValue);
      this.$router.push('/resultPage');
    }
  },
  methods: {
    ...mapActions([
      'setSearchValue'
    ])
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
</style>
