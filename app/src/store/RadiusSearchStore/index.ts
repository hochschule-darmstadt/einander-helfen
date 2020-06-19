import { Module } from 'vuex';
import { RootState } from '../types';
import { RadiusSearchState } from './types';
import { mutations } from './mutations';
import { actions } from './actions';

const state: RadiusSearchState = {
  selectedRadius: '',
};


const locationSearchModule: Module<RadiusSearchState, RootState> = {
  namespaced: true,
  state,
  mutations,
  actions
};

export default locationSearchModule;
