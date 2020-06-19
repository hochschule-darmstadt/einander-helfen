import { MutationTree } from 'vuex';
import { SearchBarState } from './types';
import Tag from '@/models/tag';

export const mutations: MutationTree<SearchBarState> = {
  addSearchValue(state, value: string): void {
    state.searchValues.push(value);
  },
  initializeSearchProposals(state, tags: Tag[]): void {
    state.searchProposals = state.searchProposals.concat(tags);
  },
  removeSearchValue(state, value): void {
    state.searchValues.splice(state.searchValues.indexOf(value), 1);
  },
  setSelectedTag(state, value): void {
    state.selectedTag = value;
  },
};
