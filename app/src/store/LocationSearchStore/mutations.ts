import { MutationTree } from 'vuex';
import { LocationSearchState } from './types';

export const mutations: MutationTree<LocationSearchState> = {
  setSelectedLocation(state, value): void {
    state.selectedLocation = value;
  },
  setLocationSearchValue(state, value): void {
    state.locationSearchValue = value;
  },
};
