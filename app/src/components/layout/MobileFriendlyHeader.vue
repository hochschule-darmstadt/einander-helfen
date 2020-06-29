<template>
  <header @focusin="focusIn" @focusout="focusOut" class="mobileHeader" :class="{menuOpen: isExpanded, fixed: fixed}">
    <v-layout row wrap justify-space-around align-center no-gutters style="padding: 2vh;">
      <v-btn
        class="d-none d-sm-flex justify-center mr-5"
        height="75px"
        width="80px"
        justify="left"
        rounded
        router
        depressed
        icon
      >
        <router-link to="/" exact>
          <v-img
            class="mt-1"
            width="80px"
            height="75px"
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Heart-hand-shake.svg/256px-Heart-hand-shake.svg.png"
          ></v-img>
        </router-link>
      </v-btn>

      <v-flex>
        <search-bar ref="searchBar"
                    @input="addSearchValueAndUpdate"
                    :searchInput.sync="currentSearchValue"
                    :enable-no-data-message="true"
        />
      </v-flex>

      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
                  v-bind="attrs"
                  v-on="on"
                  dark
                  style="margin-top: 1vh"
                  icon
          >
            <v-icon>more_vert</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item v-for="(link, index) in links" :key="index" router :to="link.route">
            <v-list-item-title>{{ link.text }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-flex xs12>
        <v-chip-group
                active-class="primary-text"
                column
                style="margin-left: 10px; margin-right: 10px"
        >
          <v-chip :key="tag" @click:close="removeSearchValueAndUpdate(tag)" close v-for="tag in searchValues">{{ tag }}</v-chip>
        </v-chip-group>
      </v-flex>

      <v-flex xs12 v-show="isExpanded">
        <location-search-bar @input="updateResults" :dark="true" />
      </v-flex>

      <v-flex xs12 v-show="isExpanded">
        <radius @input="updateResults" :dark="true" />
      </v-flex>



    </v-layout>
  </header>
</template>

<script lang="ts">
    import Vue from 'vue';
    import { createNamespacedHelpers, mapActions as mapStateActions } from 'vuex';
    const { mapActions, mapState } = createNamespacedHelpers('textSearchModule');
    import LocationSearchBar from '@/components/ui/LocationSearchBar.vue';
    import Radius from '@/components/ui/Radius.vue';
    import SearchBar from '@/components/ui/SearchBar.vue';
    import SearchButton from '@/components/ui/SearchButton.vue';

    export default Vue.extend({
  components: {
    LocationSearchBar,
    Radius,
    SearchBar,
    SearchButton
  },
  props: {
    fixed: {
      type: Boolean,
      default: false
    }
  },
  data(): {
    links: any;
    currentSearchValue: string;
    isExpanded: number;
  } {
    return {
      links: [
        { text: 'Home', route: '/' },
        { text: 'Über uns', route: '/about' },
        { text: 'Impressum', route: '/imprint' },
        { text: 'Datenschutzerklärung', route: '/privacy' }
      ],
      currentSearchValue: '',
      isExpanded: 0
    };
  },
  methods: {
    ...mapActions(['addSearchValue', 'removeSearchValue']),
    ...mapStateActions(['updateURIFromState', 'findPosts', 'setPage']),
    updateResults(): void {
        // After changing the query we want to begin on page 1
        this.setPage(1);
        this.findPosts();
    },
    addSearchValueAndUpdate(input): void {
      this.addSearchValue(input);
      this.$nextTick(() => {
        // @ts-ignore
        this.$refs.searchBar.clearInput();
      });
      this.updateResults();
    },
    removeSearchValueAndUpdate(element): void {
      this.removeSearchValue(element);
      this.updateResults();
    },
    updateSearchValueFromCurrentInputAndUpdateResults(): void {
      if (this.currentSearchValue) {
        this.addSearchValueAndUpdate(this.currentSearchValue);
      } else {
        this.updateResults();
      }
    },
    focusIn(): void {
      this.isExpanded++;
    },
    focusOut(): void {
      setTimeout(() => {
        this.isExpanded--;
      }, 100);
    }
  },
  computed: {
    ...mapState(['searchValues', 'searchProposals'])
  }
});
</script>

<style>
.v-menu__content {
  z-index: 9999 !important;
}
  .mobileHeader {
    width:100vw;
    top:0;
    z-index:9999;
    background-color: rgb(0, 37, 79);
    transition: background-color 0.3s ease-out;
  }
  .fixed {
    position:fixed;
    background-color:transparent;
  }
  .theme--dark.v-btn.v-btn--icon{
    color:#333;
  }
  .menuOpen{
    background-color:rgba(0,0,0,0.5);
  }
  .menuOpen .theme--dark.v-btn.v-btn--icon{
    color:#fff;
  }
</style>
