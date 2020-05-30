<template>
  <div>
    <div v-for="tag in volunteerTags">{tag}</div>
    <Header />
    <v-row no-gutters>
      <v-col cols="6">
        <div style="height:75vh;overflow:auto">
          <template v-for="(advertisement, i) in visiblePages">
            <v-card class="mb-3" tile>
              <v-list-item three-line @click="openAdvertisement(i)">
                <v-list-item-content>
                  <v-list-item-title class="headline mb-1">{{advertisement.title}}</v-list-item-title>
                  <v-list-item-subtitle>{{advertisement.task}}</v-list-item-subtitle>
                </v-list-item-content>

                <v-img max-width="80px" height="80px" contain :src="advertisement.image"></v-img>
              </v-list-item>
            </v-card>
          </template>
        </div>
        <!--pageination-->
        <div class="text-center" style="margin-top:2%">
          <v-pagination v-model="page" :length="numberOfPages"></v-pagination>
        </div>
      </v-col>

      <v-col cols="6" v-if="!advertisementIsOpen">
        <v-card tile height="75vh" style="position: absolute">
          <v-img
            src="https://media.wired.com/photos/59269cd37034dc5f91bec0f1/master/pass/GoogleMapTA.jpg"
            height="100%"
            width="100%"
          ></v-img>
        </v-card>
      </v-col>
      <v-col cols="6" v-if="advertisementIsOpen">
        <v-card tile height="75vh" width="50%" style="position: absolute;overflow:auto">
          <v-list-item three-line>
            <v-btn class="mr-3" text @click="closeAdvertisement()">
              <v-icon>arrow_back</v-icon>
            </v-btn>
            <!--display title, subtitle and image on the left side-->
            <v-list-item-content style="margin-top:2%">
              <v-list-item-title class="headline mb-1">{{currentAdvertisement.title}}</v-list-item-title>
              <v-list-item-subtitle>{{currentAdvertisement.task}}</v-list-item-subtitle>
            </v-list-item-content>

            <v-img
              style="margin-top:2%"
              max-width="80px"
              height="80px"
              contain
              :src="currentAdvertisement.image"
            ></v-img>
          </v-list-item>

          <!--display content on the right side-->
          <v-card-text style="padding-left:5%; padding-right:5%">
            <v-row v-if="currentAdvertisement.location">
              <v-col cols="2">Einsatzort</v-col>
              <v-col cols="8" v-html="currentAdvertisement.location"></v-col>
            </v-row>
            <v-row v-if="currentAdvertisement.target_group">
              <v-col cols="2">Zielgruppe</v-col>
              <v-col cols="8" v-html="currentAdvertisement.target_group"></v-col>
            </v-row>
            <v-row v-if="currentAdvertisement.timing">
              <v-col cols="2">Einstiegsdatum / Beginn</v-col>
              <v-col cols="8" v-html="currentAdvertisement.timing"></v-col>
            </v-row>
            <v-row v-if="currentAdvertisement.effort">
              <v-col cols="2">Zeitaufwand</v-col>
              <v-col cols="8" v-html="currentAdvertisement.effort"></v-col>
            </v-row>
            <v-row v-if="currentAdvertisement.opportunities">
              <v-col cols="2">Möglichkeiten</v-col>
              <v-col cols="8" v-html="currentAdvertisement.opportunities"></v-col>
            </v-row>
            <v-row v-if="currentAdvertisement.organization">
              <v-col cols="2">Organisation</v-col>
              <v-col cols="8" v-html="currentAdvertisement.organization"></v-col>
            </v-row>
            <v-row v-if="currentAdvertisement.contact">
              <v-col cols="2">Kontakt</v-col>
              <v-col cols="8" v-html="currentAdvertisement.contact"></v-col>
            </v-row>
          </v-card-text>

          <v-card-actions>
            <v-col>
              <v-container style="margin-bottom: 10px">
                <template v-for="(category, i) in currentAdvertisement.categories">
                  <v-chip :key="i" class="mr-2">{{ category }}</v-chip>
                </template>
              </v-container>
              <v-spacer></v-spacer>
              <v-container style="display:flex;justify-content:center;">
                <v-btn
                  class="my-2"
                  dark
                  large
                  color="#F29472"
                  :href="currentAdvertisement.link"
                  target="_blank"
                >
                  Zum Stellenangebot
                  <!--<v-icon dark>arrow_forward</v-icon>-->
                </v-btn>
              </v-container>
            </v-col>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>



<!-- test content -->
<script lang="ts">
import Header from '@/components/layout/Header.vue';
import Advertisement from '../models/advertisement';
import DataService from '../utils/services/DataService';

import Vue from 'vue';
import { mapState } from 'vuex';

export default Vue.extend({
  components: { Header },
  data(): {
    advertisementIsOpen: boolean;
    currentAdvertisementId: number;
    page: number;
    perPage: number;
  } {
    return {
      advertisementIsOpen: true,
      currentAdvertisementId: 0,
      page: 1,
      perPage: 7
    };
  },
  computed: {
    visiblePages(): Advertisement[] {
      return this.advertisements.slice(
        (this.page - 1) * this.perPage,
        this.page * this.perPage
      );
    },
    currentAdvertisement(): Advertisement | null {
      return this.advertisementIsOpen
        ? this.advertisements[this.currentAdvertisementId]
        : null;
    },
    numberOfPages(): number {
      return Math.ceil(this.advertisements.length / this.perPage);
    },
    ...mapState(['advertisements'])
  },
  created(): void {
    // TODO ?
  },
  methods: {
    openAdvertisement(index: number): void {
      this.advertisementIsOpen = true;
      this.currentAdvertisementId = index;
    },
    numberOfPages(): number {
      return Math.ceil(this.advertisements.length / this.perPage);
    }
  }
});
</script>

<style scoped>
</style>