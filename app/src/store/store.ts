import Vue from 'vue';
import Vuex from 'vuex';
import DataService from '../utils/services/DataService';
import TagService from '../utils/services/TagService';
import Tag from '@/models/tag';
import router from '@/router';
Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    searchProposals: [
      { header: 'Vorschläge' },
      { divider: true },
    ],
    posts: [],
    labels: [] as string[],
    synonyms: [] as string[],
    searchValues: [] as string[],
    location: '',
    radius: '',
    page: 1 as number
  },
  mutations: {
    addSearchValue(state, value: string): void {
      state.searchValues.push(value);
    },
    addTag(state, tag): void {
      state.searchProposals.push(tag);
    },
    removeSearchValue(state, value): void {
      state.searchValues.splice(state.searchValues.indexOf(value), 1);
    },
    setLocation(state, value): void {
      state.location = value;
    },
    setRadius(state, value): void {
      state.radius = value;
    },
    setPosts(state, value): void {
      state.posts = value;
    },
    clearSearchParams(state): void {
      state.searchValues = [];
      state.location = '';
      state.radius = '';
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
      DataService.findBySelection({
        searchValues: state.searchValues,
        location: state.location,
        radius: state.radius
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
      if ('city' in queryParams) {
        commit('setLocation', queryParams.city);
      }
      if ('radius' in queryParams) {
        commit('setRadius', queryParams.radius);
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
          city: state.location,
          radius: state.radius,
          page: state.page.toString()
        }
      }).catch((err) => err);
    }
  }
});

export default store;
