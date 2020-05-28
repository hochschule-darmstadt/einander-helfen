import Vue from 'vue';
import Vuex from 'vuex';
import DataService from '../utils/services/DataService';
import Advertisement from '../models/advertisement';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    advertisements: [],
    searchValue: '',
    location: '',
    radius: ''
  },
  mutations: {
    setSearchValue(state, value): void {
      state.searchValue = value;
    },
    setAdvertisements(state, value): void {
      state.advertisements = value;
    }
  },
  actions: {
    findAdvertisements({commit, state}): void {
      DataService.findByTitle(state.searchValue)
        .then((result) => commit('setAdvertisements', result));
    },
    setSearchValue({commit, dispatch}, searchValue): void {
      commit('setSearchValue', searchValue);
      dispatch('findAdvertisements');
    }
  }
});

export default store;
