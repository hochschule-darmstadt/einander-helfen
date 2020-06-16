import Vue from 'vue';
import Vuex from 'vuex';
import DataService from '../utils/services/DataService';
import Location from '@/models/location';
import LocationService from '@/utils/services/LocationService';
import router from '@/router';
import Tag from '@/models/tag';
Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    searchProposals: [
      { header: 'Vorschläge' },
      { divider: true },
    ],
    radii: [
      {
        text: 'Überall',
        value: '',
      },
      {
        text: '5 km',
        value: '5km',
      },
      {
        text: '10 km',
        value: '10km',
      },
      {
        text: '25 km',
        value: '25km',
      },
      {
        text: '50 km',
        value: '50km',
      },
    ],
    posts: [],
    labels: [] as string[],
    synonyms: [] as string[],
    searchValues: [] as string[],
    locations: [] as Location[],
    locationSearchValue: '',
    radiusSearchValue: '',
    selectedLocation: '',
    selectedTag: '',
    page: 1 as number
  },
  mutations: {
    addSearchValue(state, value: string): void {
      state.searchValues.push(value);
    },
    initializeSearchProposals(state, tags: []): void {
      state.searchProposals = state.searchProposals.concat(tags);
    },
    removeSearchValue(state, value): void {
      state.searchValues.splice(state.searchValues.indexOf(value), 1);
    },
    setPosts(state, value): void {
      state.posts = value;
    },
    setLocations(state, value): void {
      state.locations = value;
    },
    setLocationSearchValue(state, value): void {
      state.locationSearchValue = value;
    },
    setRadiusSearchValue(state, value): void {
      state.radiusSearchValue = value;
    },
    setSelectedTag(state, value): void {
      state.selectedTag = value;
    },
    setSelectedLocation(state, value): void {
      state.selectedLocation = value;
    },
    clearSearchParams(state): void {
      state.searchValues = [];
      state.radiusSearchValue = '';
      state.selectedLocation = '';
    },
    setPage(state, value: number): void {
      state.page = value;
      router.replace({
        name: 'resultPage',
        query: {
          ...router.currentRoute.query,
          page: value.toString()
        }
      });
    }
  },
  actions: {
    initializeSearchProposals({ commit }, proposals: Tag[]): void {
      commit('initializeSearchProposals', proposals);
    },
    findPosts({ commit, state }): void {
      const location = LocationService.findByTitle(state.selectedLocation);
      const searchValues = state.searchValues;
      const radius = state.radii.find((r) => r.text === state.radiusSearchValue);
      DataService.findBySelection({
        searchValues,
        location,
        radius
      }).then((result) => commit('setPosts', result));
    },
    addSearchValue({ commit, dispatch }, searchValue): void {
      commit('addSearchValue', searchValue);
      dispatch('updateURIFromState');
      dispatch('findPosts');
    },
    addSearchValues({ commit, dispatch }, searchValues: string[]): void {
      searchValues.forEach((tag) => commit('addSearchValue', tag));
    },
    setResultPage({ commit }, value: number): void {
      commit('setPage', value);
    },
    removeSearchValue({ commit, dispatch }, value): void {
      commit('removeSearchValue', value);
      dispatch('updateURIFromState');
      dispatch('findPosts');
    },
    hydrateStateFromURIParams({ commit, dispatch }, queryParams): void {
      // Clear previous search parameters. The URI is our single source of truth!
      commit('clearSearchParams');
      if ('q' in queryParams) {
        dispatch('addSearchValues', queryParams.q.split(','));
      }
      if ('location' in queryParams) {
        dispatch('setSelectedLocation', queryParams.location);
      }
      if ('radius' in queryParams) {
        dispatch('setRadiusSearchValue', queryParams.radius);
      }
      if ('page' in queryParams) {
        commit('setPage', parseInt(queryParams.page, 10));
      }
      dispatch('findPosts');
    },
    updateURIFromState({ state }): void {
      router.replace({
        name: 'resultPage',
        query: {
          ...router.currentRoute.query,
          q: state.searchValues.join(','),
          city: state.selectedLocation,
          radius: state.radiusSearchValue,
          page: state.page.toString()
        }
      }).catch((err) => err);
    },
    findLocationByPlzOrName({ commit, state }): void {
      const newLocations = LocationService.findLocationByPlzOrName(state.locationSearchValue);
      commit('setLocations', newLocations);
    },
    setLocationSearchValue({ commit, dispatch }, locationSearchValue): void {
      commit('setLocationSearchValue', locationSearchValue);
    },
    setSelectedLocation({ commit, dispatch }, selectedLocation): void {
      commit('setSelectedLocation', selectedLocation);
      dispatch('findPosts');
    },
    setRadiusSearchValue({ commit, dispatch }, radiusSearchValue): void {
      commit('setRadiusSearchValue', radiusSearchValue);
    },
    setSelectedTag({ commit, dispatch }, selectedTag): void {
      commit('setSelectedTag', selectedTag);
    }
  },
  getters: {
    getLocations: (state) => {
      if (state.locations.length === 0) {
        return LocationService.findLocationByPlzOrName(state.locationSearchValue || state.selectedLocation);
      }
      return state.locations;
    }
  }
});

export default store;
