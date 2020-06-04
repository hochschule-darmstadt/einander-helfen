import Vue from 'vue';
import Vuex from 'vuex';
import DataService from '../utils/services/DataService';
import Advertisement from '../models/advertisement';
import router from '@/router';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    searchProposals: [
      {header: 'Vorschläge'},
      {divider: true},
      {tag: 'Macher/in'},
      {tag: 'Denker/in'},
      {tag: 'Jugendarbeit'}
    ],
    advertisements: [],
    searchValues: [] as string[],
    location: '',
    radius: '',
  },
  mutations: {
    addSearchValue(state, value: string): void {
      state.searchValues.push(value);
    },
    removeSearchValue(state, value): void {
      state.searchValues.splice(state.searchValues.indexOf(value), 1);
    },
    setAdvertisements(state, value): void {
      state.advertisements = value;
    }
  },
  actions: {
    findAdvertisements({ commit, state }): void {
      DataService.findBySelection({
        searchValues: state.searchValues,
        location: state.location,
        radius: state.radius
      }).then((result) => commit('setAdvertisements', result));
    },
    addSearchValue({ commit, dispatch }, searchValue): void {
      commit('addSearchValue', searchValue);
      dispatch('findAdvertisements');
    },
    addSearchValues({ commit, dispatch }, searchValues: string[]): void {
      searchValues.forEach((tag) => commit('addSearchValue', tag));
      dispatch('findAdvertisements');
    },
    removeSearchValue({ commit, dispatch }, value): void {
      commit('removeSearchValue', value);
      dispatch('findAdvertisements');
    },
    hydrateStateFromURIParams({ dispatch }, queryParams): void {
      if ('q' in queryParams) {
        dispatch('addSearchValues', queryParams.q.split(','));
      }
    }
  }
});

export default store;
