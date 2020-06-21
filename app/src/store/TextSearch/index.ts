import { Module } from 'vuex';
import { RootState } from '../types';
import { TextSearchState } from './types';
import { mutations } from './mutations';
import { actions } from './actions';

const state: TextSearchState = {
  searchProposals: [
    { header: 'Vorschläge' },
    { divider: true },
  ],
  labels: [] as string[],
  synonyms: [] as string[],
  searchValues: [] as string[],
  selectedTag: '',
};


const locationSearchModule: Module<TextSearchState, RootState> = {
  namespaced: true,
  state,
  mutations,
  actions
};

export default locationSearchModule;
