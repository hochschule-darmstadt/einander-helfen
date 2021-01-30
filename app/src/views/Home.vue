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

    <v-container id="container">
      <v-form>
        <v-row id="searchbox" justify="center" lg="2">
          <v-layout row justify-center no-gutters class="mt-8 mb-9">
            <v-flex>
              <v-form>
                <v-row>
                  <v-col id=searchCol cols="12">
                    <search-bar :searchInput.sync="currentSearchValue" id="search" :attachTo="'#search'" @click.native="focussearch" v-model="selectedInput" @enter="onSearchEnter" tabindex="1" />
                  </v-col>
                </v-row>

                <v-row class="flex-grow-1 ps-4" id="locationDiv">
                    <area-select id="areaSelect" ref="areaSelect" @change="switchArea" tabindex="2" />
                    <location-search-bar @click.native="focussearch" id="location" :attachTo="'#location'" ref="locationSearchBar" @enter="onLocationEnter" tabindex="3" />
                    <radius ref="radius" id="radius" @enter="onRadiusEnter" tabindex="4" />
                    <search-button id="searchButton" @click="executeSearch" tabindex="5" />
                </v-row>
              </v-form>
             </v-flex>
          </v-layout>
        </v-row>
      </v-form>

      <v-row justify="center" lg="3">
        <template v-for="tag in volunteerTags">
          <v-col md="3" xl="3" :key="tag.title">
            <v-hover v-slot:default="{ hover }">
              <v-card class="mx-auto" :elevation="hover ? 12 : 2" :class="{ 'on-hover': hover }">
                <router-link
                  style="text-decoration: none; color: inherit;"
                  :to="{ name: 'resultPage', query: { q: tag.to } }"
                >
                  <v-img
                    class="white--text align-end mt-10"
                    height="300px"
                    :key="tag.title"
                    :src="tag.img"
                  >
                    <v-card class="no-radius">
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
import { createNamespacedHelpers, mapActions } from 'vuex';
const { mapActions: mapTextSearchActions } = createNamespacedHelpers(
  'textSearchModule'
);
const { mapState: mapLocationSearchState } = createNamespacedHelpers(
  'locationSearchModule'
);


import Vue from 'vue';
import Toolbar from '@/components/layout/Toolbar.vue';

import VueSlickCarousel from 'vue-slick-carousel';
import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css';
import 'vue-slick-carousel/dist/vue-slick-carousel.css';
import LocationSearchBar from '@/components/ui/LocationSearchBar.vue';
import Radius from '@/components/ui/Radius.vue';
import SearchBar from '@/components/ui/SearchBar.vue';
import SearchButton from '@/components/ui/SearchButton.vue';
import AreaSelect from '../components/ui/AreaSelect.vue';

export default Vue.extend({
  components: {
    SearchBar,
    VueSlickCarousel,
    AreaSelect,
    LocationSearchBar,
    Radius,
    Toolbar,
    SearchButton
  },
  data(): {
    volunteerTags: { title: string; to: string; img: string }[];
    selectedInput: string;
    currentSearchValue: string;
  } {
    return {
      volunteerTags: [
        {
          title: 'Arbeit mit Kindern',
          to: 'Kinder',
          img: require('../../public/images/macherIN.jpeg')
        },
        {
          title: 'Arbeit mit Jugendlichen',
          to: 'Jugend',
          img: require('../../public/images/denkerIN.jpeg')
        },
        {
          title: 'Arbeit mit Senioren',
          to: 'Senioren',
          img: require('../../public/images/sozial.jpeg')
        },
        {
          title: 'Betreuung',
          to: 'Betreuung',
          img: require('../../public/images/jugend.jpeg')
        }
      ],
      selectedInput: '',
      currentSearchValue: ''
    };
  },
  created(): void {
    this.clearSearchParams();
    this.clearLocationSearchValue();
  },
  computed: {
    ...mapLocationSearchState(['selectedRadius', 'selectedLocation'])
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
    },
    clearLocationSearchValue(): void {
      this.$nextTick(() => {
        // @ts-ignore
        this.$refs.locationSearchBar.clearInput();
      });
    },
    onSearchEnter(): void {
      if (this.selectedInput) {
        this.executeSearch();
      }
    },
    onLocationEnter(): void {
      if (this.selectedLocation) {
        this.executeSearch();
      }
    },
    onRadiusEnter(): void {
      if (this.selectedRadius) {
       this.executeSearch();
      }
    },

    focussearch(): void {
      const isSafari = navigator.vendor && navigator.vendor.indexOf('Apple') > -1 &&
               navigator.userAgent &&
               navigator.userAgent.indexOf('CriOS') === -1 &&
               navigator.userAgent.indexOf('FxiOS') === -1;

      const focussearch = document.getElementById('searchCol');

      if (isSafari === false && focussearch !== null && window.matchMedia('(max-width: 420px)').matches) {
        focussearch.scrollIntoView(true);
      }
    },
    switchArea(): void {
      const areaSelect = (this.$refs.areaSelect as AreaSelect);
      const areaSelection = (this.$refs.areaSelect as AreaSelect).selection;
      const international = (areaSelection === areaSelect.items[0].title)? false : true;
      (this.$refs.locationSearchBar as any).setLocationSearchBar(international);
      (this.$refs.radius as any).disableRadius(international);
      (this.$refs.locationSearchBar as any).setSelectedLocation(null);
    }
  }
});
</script>

<style>
#location .v-autocomplete__content.v-menu__content{ 
  top: auto !important;
  left: auto !important;
  margin-top: 50px;
}

.v-input__slot {
  margin-bottom: 0;
}

.no-radius {
  border-radius: 0 !important;
}

img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.slick-arrow {
  display: none !important ;
  visibility: hidden;
}

#searchButton {
  margin-right: 0 !important;
}

#searchbox {
  padding-left: 12px;
  padding-right: 12px;
}

#container{
  margin: auto;
}

#locationDiv {
  padding-left: 12px !important;
  padding-right: 12px !important;
}


@media (min-width: 280px) and (max-width: 310px) {
  #location {
    max-width: 75vw;
  }

  #radius{
    margin-left: 0 !important;
    width: 60%;
  }

  #location .v-input__slot {
    margin-left: 2px;
  }
  
  #location .v-text-field {
    padding-right: 0px !important;
}
}


@media (min-width: 310px) and (max-width: 344px) {
  #location {
    max-width: 77vw;
  }

  #radius{
    margin-left: 0 !important;
    width: 60%;
  }

  #location .v-input__slot {
    margin-left: 2px;
  }
  
  #location .v-text-field {
    padding-right: 0px !important;
}

}


@media (min-width: 344px) and (max-width: 383px) {
  #location {
    max-width: 98vw;
  }

  #radius {
    margin-left: 0 !important;
    width: 70%;
  }

  #location .v-autocomplete__content.v-menu__content { 
    max-height: 225px !important;
    overflow-y: scroll;
    overflow-x: hidden;
  }

}

#location .v-text-field {
  padding-right: 5px;
}


@media (min-width: 383px) {
  #location {
    max-width: 98vw;
  }

  #location .v-input__slot {
    margin-left: 2px;
  }

  #radius {
    margin-left: 0 !important;
    max-width: 72.5vw;
  } 
}

@media (min-width: 535px) {
  #location {
    width: auto;
    max-width: none;
  }

  #radius {
    max-width: 20%;
    min-width: none;
    margin-left: 10px !important;
  }

  #location .v-text-field {
    padding-right: 0px;
  }
}

@media (min-width: 613px) {
  #radius {
    width: 200px;
  }
}

@media (min-width: 800px) {
  #container {
    max-width:1450px;
  }
}

@media (min-width: 960px) {
  #container {
    width: 960px;
    max-width: none;
  }
}

@media (min-width: 1100px) {
  #container {
    width: 1100px;
  }
}

@media (min-width: 1300px) {
  #container {
    width: 1300px;
  }
}

@media (min-width: 1618px) {
  #container {
    width: 1618px;
  }
}

@media (min-width: 1904px) {
  #container {
    width: 85%;
  }
}


</style>