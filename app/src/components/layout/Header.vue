<template>
  <header>
    <v-layout row wrap justify-space-around align-center no-gutters style="padding: 2vh; background: #00254f">
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

      <v-flex xs10 sm8 md6 style="background: white; border-radius: 20px; margin-right:2%">
        <search-bar ref="searchBar"
                    @input="addSearchValueAndUpdate"
                    :searchInput.sync="currentSearchValue"
                    :enable-no-data-message="true"
        />
        <v-spacer></v-spacer>
        <v-chip-group
          active-class="primary-text"
          column
          style="margin-left: 10px; margin-right: 10px; margin-top: -20px"
        >
          <v-chip :key="tag" @click:close="removeSearchValueAndUpdate(tag)" close v-for="tag in searchValues">{{ tag }}</v-chip>
        </v-chip-group>
      </v-flex>

      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            class="hidden-md-and-up"
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

      <v-flex xs12 sm5 md2>
        <location-search-bar @input="updateResults" :dark="true" />
      </v-flex>

      <v-flex xs12 sm4 md1>
        <radius @input="updateResults" :dark="true" />
      </v-flex>

      <v-flex xs12 sm4 md1>
        <search-button @click="updateSearchValueFromCurrentInputAndUpdateResults" />
      </v-flex>

      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            class="hidden-sm-and-down"
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
  data(): {
    links: any;
    currentSearchValue: string;
  } {
    return {
      links: [
        { text: 'Home', route: '/' },
        { text: 'Über uns', route: '/about' },
        { text: 'Impressum', route: '/imprint' },
        { text: 'Datenschutzerklärung', route: '/privacy' }
      ],
      currentSearchValue: ''
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
</style>
