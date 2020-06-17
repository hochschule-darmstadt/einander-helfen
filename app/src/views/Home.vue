<template>
  <div class="home">
    <Toolbar />
    <VueSlickCarousel :dots="true" :infinite="true" :autoplay="true" :autoplaySpeed="30000" style="margin-top:4vh">
      :dots="true"
      :infinite="true"
      :autoplay="true"
      :autoplaySpeed="30000"
    >
      <picture>
        <source
          media="(max-width: 768px)"
          srcset="/images/header/1_phone.jpg"
        />
        <img src="/images/header/1.jpg" />
      </picture>
      <picture>
        <source
          media="(max-width: 768px)"
          srcset="/images/header/2_phone.jpg"
        />
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
              item-text="tag"
              autocomplete="off"
              :items="mySearchProposals"
              @input="addSearchTag"
              :search-input.sync="currentSearchValue"
            ></v-combobox>
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-col cols="12" md="6">
            <location-search-bar />
            >
          </v-col>

          <v-col cols="12" md="2">
            <radius />
            >
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
                  :to="{ name: 'resultPage', query: { q: tag.title } }"
                >
                  <v-img
                    class="white--text align-end mt-10"
                    height="300px"
                    :key="tag.title"
                    :src="tag.img"
                  >
                    <v-card>
                      <v-card-title
                        class="justify-center black--text"
                        v-html="tag.title"
                      ></v-card-title>
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
import {mapActions, mapState} from 'vuex';
import Vue from 'vue';
import Toolbar from '@/components/layout/Toolbar.vue';

import VueSlickCarousel from 'vue-slick-carousel';
import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css';
import 'vue-slick-carousel/dist/vue-slick-carousel.css';
import LocationSearchBar from '@/components/ui/LocationSearchBar.vue';
import Radius from '@/components/ui/Radius.vue';
import Tag from '@/models/tag';
import TagService from '../utils/services/TagService';
import SearchBar from '@/components/ui/SearchBar.vue';


export default Vue.extend({
  components: {
    SearchBar,
    VueSlickCarousel,
    LocationSearchBar,
    Radius,
    Toolbar
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
        title: 'Kommunikative',
        img: require('../../public/images/jugend.jpeg')
      },
      {
        title: 'Soziale',
        img: require('../../public/images/sozial.jpeg')
      }
    ],
    currentSearchValue: ''
  }),
   created(): void {
    // Initialize the searchProposals!
    this.initializeSearchProposals(TagService.getTags());
  },
  computed: {
    ...mapState(['searchProposals', 'selectedLocation', 'radiusSearchValue']),
        mySearchProposals(): string[] {
      if (!this.currentSearchValue || this.currentSearchValue.length < 2) {
        return [];
      }
      const searchTerm = this.currentSearchValue;
      const listOfMatchingTerms = this.matchSearchInput(searchTerm, this.searchProposals
        .filter((element) => 'label' in element));
      const rankedListOfOrderedTerms = this.rankTerms(searchTerm, listOfMatchingTerms);

      return rankedListOfOrderedTerms;
    }
  },
  methods: {
    ...mapActions(['initializeSearchProposals']),
    addSearchTag(tag: string): void {
      const tagName = tag.substr(0, tag.indexOf(' ('));

      this.$router.push({
        name: 'resultPage',
        query: {
          q: tagName,
          city: this.selectedLocation,
          radius: this.radiusSearchValue
        }
      });
    },
    matchSearchInput(searchTerm: string, proposals: Tag[]): string[] {
      const stringArray: string[] = [];
      searchTerm = searchTerm.toLowerCase();

      proposals.forEach((tag) => {
        if (tag.label.toLowerCase().match(searchTerm)) {
          stringArray.push(tag.label);
        } else {
          tag.synonyms.forEach((element) => {
            if (element.toLowerCase().match(searchTerm)) {
              stringArray.push(tag.label + ' (' + element + ')');
            }
          });
        }
      });
      return stringArray;
    },
    rankTerms(searchTerm: string, terms: string[]): string[] {
      return terms.map((term) => {
          // 2x on start; 1x on end, 0.5x in the middle
          const rank = term.toLowerCase().startsWith(searchTerm.toLowerCase())
            ? 2
            : this.isSuccessiveMatch(term.toLowerCase(),searchTerm.toLowerCase())
              ? 1
              : 0.5;
          return {
            label: term,
            rank
          };
        })
        .sort((a, b) => Math.sign(b.rank - a.rank))
        .map((obj) => obj.label);
    },
    isSuccessiveMatch(term: string, searchTerm: string): boolean
    {
      var isSuccessive: boolean = false;
      var sucArr = term.split(' ');
      sucArr.forEach((element) => {
        
        if(element.startsWith(searchTerm))
        {
          isSuccessive = true;
        }
      });
      if(sucArr.length < 2)
      {
        isSuccessive = false;
      } 
      return isSuccessive;
    }
  }
});
</script>

<style>
.v-input__slot {
  margin-bottom: 0;
}

img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>
