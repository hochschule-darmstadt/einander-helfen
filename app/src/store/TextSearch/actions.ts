import {ActionTree} from 'vuex';
import {TextSearchState} from '@/store/TextSearch/types';
import {RootState} from '@/store/types';
import Tag from '@/models/tag';

export const actions: ActionTree<TextSearchState, RootState> = {
  initializeSearchProposals({ commit }, proposals: Tag[]): void {
    commit('initializeSearchProposals', proposals);
  },
  addSearchValue({ commit, dispatch }, searchValue): void {
    commit('addSearchValue', searchValue);
    dispatch('updateURIFromState', {}, {root: true});
    dispatch('findPosts', {}, {root: true});
  },
  addSearchValues({ commit, dispatch }, searchValues: string[]): void {
    searchValues.forEach((tag) => commit('addSearchValue', tag));
  },
  removeSearchValue({ commit, dispatch }, value): void {
    commit('removeSearchValue', value);
    dispatch('updateURIFromState', {}, {root: true});
    dispatch('findPosts', {}, {root: true});
  },
  setSelectedTag({ commit, dispatch }, selectedTag): void {
    commit('setSelectedTag', selectedTag);
  }
};
