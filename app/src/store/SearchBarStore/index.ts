import { Module } from 'vuex';
import { RootState } from '../types';
import { SearchBarState } from './types';
import { mutations } from './mutations';
import { actions } from './actions';

const state: SearchBarState = {
  searchProposals: [
    { header: 'Vorschläge' },
    { divider: true },
  ],
  labels: [] as string[],
  synonyms: [] as string[],
  searchValues: [] as string[],
  selectedTag: '',
};


const locationSearchModule: Module<SearchBarState, RootState> = {
  namespaced: true,
  state,
  mutations,
  actions
};

export default locationSearchModule;
