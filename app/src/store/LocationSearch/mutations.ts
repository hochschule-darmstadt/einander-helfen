import { MutationTree } from 'vuex';
import { LocationSearchState } from './types';

export const mutations: MutationTree<LocationSearchState> = {
  setSelectedLocation(state, value): void {
    state.selectedLocation = value;
  },
  setSelectedLocationObject(state, value): void {
    state.selectedLocationObject = value;
  },
  setLocationSearchValue(state, value): void {
    state.locationSearchValue = value;
  },
  setSelectedRadius(state, value): void {
    state.selectedRadius = value;
  },
  setAlternateRadius(state, value): void {
    state.alternateRadius = value;
  },
};
