import {ActionTree} from 'vuex';
import {TextSearchState} from '@/store/TextSearch/types';
import {RootState} from '@/store/types';
import Tag from '@/models/tag';

export const actions: ActionTree<TextSearchState, RootState> = {
  initializeSearchProposals({ commit }, proposals: Tag[]): void {
    commit('initializeSearchProposals', proposals);
  },
  addSearchValue({ commit, dispatch }, searchValue): void {
    searchValue = searchValue.trim();
    if (searchValue) {
      commit('addSearchValue', searchValue);
    }
  },
  addSearchValues({ commit, dispatch }, searchValues: string[]): void {
    searchValues.forEach((tag) => dispatch('addSearchValue', tag));
  },
  removeSearchValue({ commit, dispatch }, value): void {
    commit('removeSearchValue', value);
  },
  setSelectedTag({ commit, dispatch }, selectedTag): void {
    commit('setSelectedTag', selectedTag);
  }
};
