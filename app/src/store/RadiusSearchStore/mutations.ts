import { MutationTree } from 'vuex';
import { RadiusSearchState } from './types';

export const mutations: MutationTree<RadiusSearchState> = {
  setSelectedRadius(state, value): void {
    state.selectedRadius = value;
  },
};
