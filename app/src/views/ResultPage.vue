<template>
  <div>
    <Header />
    
      <v-layout row wrap no-gutters>
        <v-flex sm12 md6>
          <div style="height:70vh;overflow:auto; margin-bottom:5%">
            <template v-for="(advertisement, i) in visiblePages">
              <v-card class="mb-3">
                <v-list-item three-line @click="openAdvertisement(i)">
                  <v-list-item-content>
                    <v-list-item-title class="headline mb-1">{{
                      advertisement.title
                    }}</v-list-item-title>
                    <v-list-item-subtitle>{{
                      advertisement.task
                    }}</v-list-item-subtitle>
                  </v-list-item-content>

                  <v-img
                    max-width="80px"
                    height="80px"
                    contain
                    :src="advertisement.image"
                  ></v-img>
                </v-list-item>
              </v-card>
            </template>
          </div>
        </v-flex>
        
        <v-flex xs12 md6  v-if="!postIsOpen">
          <v-card tile height="70vh">
            <v-img
              src="https://media.wired.com/photos/59269cd37034dc5f91bec0f1/master/pass/GoogleMapTA.jpg"
              height="100%"
              width="100%"
            ></v-img>
          </v-card>
        </v-flex>
        
        <v-flex sm12 md6  v-if="postIsOpen">
          <v-card
            tile
            height="100%"
            width="100%"
          >
          <v-list-item three-line>
            <v-btn class="mr-3" text @click="closeAdvertisement()">
              <v-icon>arrow_back</v-icon>
            </v-btn>

            <!--display title, subtitle and image on the left side-->
            <v-list-item-content style="margin-top:2%" class="headline">{{
                currentPost.title
              }}
              <v-list-item-subtitle class="mt-1">{{
                currentPost.task
              }}</v-list-item-subtitle>
            </v-list-item-content>
            <v-img
              style="margin-top:2%"
              max-width="80px"
              height="80px"
              contain
              :src="currentPost.image"
            ></v-img>
          </v-list-item>

          <!--display content on the right side-->
          
          <v-card-text style="padding-left:5%; padding-right:5%">
            
            <v-row v-if="currentPost.location">
             <v-flex md4 xs6>Einsatzort</v-flex>
             <v-flex md8 xs6 v-html="currentPost.location"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.title">
             <v-flex md4 xs6 >Aufgabe</v-flex>
             <v-flex md8 xs6 v-html="currentPost.task"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.contact">
              <v-flex md4 xs6>Ansprechpartner</v-flex>
              <v-flex md8 xs6 v-html="currentPost.contact"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.organization">
              <v-flex md4 xs6>Organisation</v-flex>
              <v-flex md8 xs6 v-html="currentPost.organization"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.target_group">
              <v-flex md4 xs6>Zielgruppe</v-flex>
              <v-flex md8 xs6 v-html="currentPost.target_group"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.timing">
              <v-flex md4 xs6>Einstiegsdatum / Beginn</v-flex>
              <v-flex md8 xs6 v-html="currentPost.timing"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.effort">
              <v-flex md4 xs6>Zeitaufwand</v-flex>
              <v-flex md8 xs6 v-html="currentPost.effort"></v-flex>
            </v-row>
            <v-row class="pt-1" v-if="currentPost.opportunities">
              <v-flex md4 xs6>Möglichkeiten</v-flex>
              <v-flex md8 xs6 v-html="currentPost.opportunities"></v-flex>
            </v-row>


           
          </v-card-text>

          <v-card-actions>
            <v-flex md12 sm12>
              <v-container style="margin-bottom: 10px">
                <template
                  v-for="(category, i) in currentPost.categories"
                >
                  <v-chip :key="i" class="mr-2 mt-2">{{ category }}</v-chip>
                </template>
              </v-container>
              <v-spacer></v-spacer>
              <v-container style="display:flex;justify-content:center;">
                <v-btn
                  class="my-2"
                  dark
                  large
                  color="#054C66"
                  :href="currentPost.link"
                  target="_blank"
                >
                  Zum Stellenangebot
                  <!--<v-icon dark>arrow_forward</v-icon>-->
                </v-btn>
              </v-container>
            </v-flex>
          </v-card-actions>
        </v-card>

        
        </v-flex>
      <v-layout row wrap justify-center>
                 <!--pageination-->
          <div class="text-center" style="margin-top:2%; margin-bottom:1%">
            <v-pagination v-model="page" :length="numberOfPages" color="#054C66"></v-pagination>
          </div>
      </v-layout>
      </v-layout>
  </div>
</template>

<!-- test content -->
<script lang="ts">
import Header from '@/components/layout/Header.vue';
import Advertisement from '@/models/advertisement';

import Vue from 'vue';
import { mapActions, mapState } from 'vuex';

export default Vue.extend({
  components: { Header },
  data(): {
    postIsOpen: boolean;
    currentPostId: number;
    page: number;
    perPage: number;
  } {
    return {
      postIsOpen: false,
      currentPostId: 0,
      page: 1,
      perPage: 7,
    };
  },
  computed: {
    ...mapState(['posts']),
    visiblePages(): Advertisement[] {
      return this.posts.slice(
        (this.page - 1) * this.perPage,
        this.page * this.perPage
      );
    },
    currentPost(): Advertisement | null {
      return this.postIsOpen
        ? this.posts[this.currentPostId]
        : null;
    },
    numberOfPages(): number {
      return Math.ceil(this.posts.length / this.perPage);
    },
  },
  created(): void {
    this.hydrateStateFromURIParams(this.$route.query);
  },
  methods: {
    ...mapActions(['hydrateStateFromURIParams']),
    openAdvertisement(index: number): void {
      this.postIsOpen = true;
      this.currentPostId = index + ((this.page - 1) * this.perPage);
    },
    closeAdvertisement(): void {
      this.currentPostId = 0;
      this.postIsOpen = false;
    },
    numberOfPages(): number {
      return Math.ceil(this.posts.length / this.perPage);
    },
  },
});
</script>

<style scoped></style>
