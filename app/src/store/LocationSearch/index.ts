import { Module } from 'vuex';
import { RootState } from '../types';
import { LocationSearchState } from './types';
import { mutations } from './mutations';
import { actions } from './actions';
import { getters } from './getters';

const state: LocationSearchState = {
  locationSearchValue: '',
  selectedLocation: '',
  selectedRadius: '',
  alternateRadius: '',
};


const locationSearchModule: Module<LocationSearchState, RootState> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default locationSearchModule;
