import Vue from 'vue';
import Vuex, {StoreOptions} from 'vuex';
import DataService from '../utils/services/DataService';
import LocationService from '@/utils/services/LocationService';
import router from '@/router';
import Post from '@/models/post';
import textSearchModule from './TextSearch';
import locationSearchModule from './LocationSearch';
import {RootState} from './types';
Vue.use(Vuex);

const store: StoreOptions<RootState> = {
  modules: {
    textSearchModule,
    locationSearchModule,
  },
  state: {
    posts: [] as Post[],
    page: 1 as number
  } as RootState,
  mutations: {

    clearSearchParams(state): void {
      state.textSearchModule.searchValues = [];
      state.locationSearchModule.selectedRadius = '';
      state.locationSearchModule.selectedLocation = '';
    },

    setPosts(state, value): void {
      state.posts = value;
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

    findPosts({ commit, state }): void {
      const location = LocationService.findByTitle(state.locationSearchModule.selectedLocation);
      const searchValues = state.textSearchModule.searchValues;
      const radius = state.locationSearchModule.selectedRadius;
      DataService.findBySelection({
        searchValues,
        location,
        radius
      }).then((result) => commit('setPosts', result));
    },
    setResultPage({ commit }, value: number): void {
      commit('setPage', value);
    },
    hydrateStateFromURIParams({ commit, dispatch }, queryParams): void {
      // Clear previous search parameters. The URI is our single source of truth!
      commit('clearSearchParams');
      if ('q' in queryParams) {
        dispatch('textSearchModule/addSearchValues', queryParams.q.split(','));
      }
      if ('location' in queryParams) {
        dispatch('locationSearchModule/setSelectedLocation', queryParams.location);
      }
      if ('radius' in queryParams) {
        dispatch('locationSearchModule/setSelectedRadius', queryParams.radius);
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
          q: state.textSearchModule.searchValues.join(','),
          location: state.locationSearchModule.selectedLocation,
          radius: state.locationSearchModule.selectedRadius,
          page: state.page.toString()
        }
      }).catch((err) => err);
    },
  },
};

export default new Vuex.Store<RootState>(store);
