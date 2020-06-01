import Vue from 'vue';
import Vuex from 'vuex';
import DataService from '../utils/services/DataService';
import Advertisement from '../models/advertisement';
import router from '@/router';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    advertisements: [],
    searchValue: '',
    location: '',
    radius: '',
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
    findAdvertisementsByTitle({ commit, state }): void {
      DataService.findByCategories(state.searchValue)
        .then((result) => commit('setAdvertisements', result));
    },
    setSearchValue({ commit, dispatch }, searchValue): void {
      commit('setSearchValue', searchValue);
      dispatch('findAdvertisementsByTitle');
    }
  }
});

export default store;
