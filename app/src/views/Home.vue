<template>
  <div class="home">
    <Toolbar />
    <VueSlickCarousel :dots="true" :infinite="true" :autoplay="true" :autoplaySpeed="30000">
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
        <source
          media="(max-width: 768px)"
          srcset="/images/header/3_phone.jpg"
        />
        <img src="/images/header/3.jpg" />
      </picture>
    </VueSlickCarousel>

    <v-container>
      <v-form>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-layout
              row
              justify-center
              no-gutters
              class="mt-8 mb-9 "
            >
              <v-flex >
                <v-form>
                  <v-row>
                    <v-col cols="12">
                      <search-bar
                        :searchInput.sync="currentSearchValue"
                        v-model="selectedInput"
                      />
                    </v-col>
                  </v-row>

                  <v-row>
                    <v-col cols="12" md="6">
                      <location-search-bar />
                    </v-col>

                    <v-col cols="8" sm="9" md="4">
                      <radius />
                    </v-col>
                    <v-col cols="4" sm="3" md="2" class="d-flex flex-row-reverse py-1 pr-1">
                      <search-button @click="executeSearch" />
                    </v-col>
                  </v-row>
                </v-form>
              </v-flex>
            </v-layout>
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
                    <v-card class="no-radius">
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
import { createNamespacedHelpers, mapActions} from 'vuex';
const { mapActions: mapTextSearchActions } = createNamespacedHelpers('textSearchModule');

import Vue from 'vue';
import Toolbar from '@/components/layout/Toolbar.vue';

import VueSlickCarousel from 'vue-slick-carousel';
import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css';
import 'vue-slick-carousel/dist/vue-slick-carousel.css';
import LocationSearchBar from '@/components/ui/LocationSearchBar.vue';
import Radius from '@/components/ui/Radius.vue';
import SearchBar from '@/components/ui/SearchBar.vue';
import SearchButton from '@/components/ui/SearchButton.vue';

export default Vue.extend({
  components: {
    SearchBar,
    VueSlickCarousel,
    LocationSearchBar,
    Radius,
    Toolbar,
    SearchButton
  },
  data(): {
    volunteerTags: Array<{ title: string; img: string }>
    selectedInput: string,
    currentSearchValue: string
  } {
    return {
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
      selectedInput: '',
      currentSearchValue: ''
    };
  },
  created(): void {
    this.clearSearchParams();
  },
  methods: {
    ...mapTextSearchActions(['addSearchValue']),
    ...mapActions(['updateURIFromState', 'clearSearchParams']),
    executeSearch(): void {
      if (this.selectedInput) {
        this.addSearchValue(this.selectedInput);
      } else if (this.currentSearchValue) {
        this.addSearchValue(this.currentSearchValue);
      }
      this.updateURIFromState();
    }
  }
});
</script>

<style>
.v-input__slot {
  margin-bottom: 0;
}

.no-radius {
  border-radius: 0!important;
}

img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>
