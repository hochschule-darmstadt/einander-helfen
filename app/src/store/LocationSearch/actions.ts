import {ActionTree} from 'vuex';
import {LocationSearchState} from './types';
import {RootState} from '@/store/types';

export const actions: ActionTree<LocationSearchState, RootState> = {
  setLocationSearchValue({ commit, dispatch }, locationSearchValue): void {
    commit('setLocationSearchValue', locationSearchValue);
  },
  setSelectedLocation({ commit, dispatch }, selectedLocation): void {
    commit('setSelectedLocation', selectedLocation);
    dispatch('findPosts', {}, {root: true});
  },
  setSelectedRadius({ commit, dispatch }, radiusSearchValue): void {
    commit('setSelectedRadius', radiusSearchValue);
  }
};
