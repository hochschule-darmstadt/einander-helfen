import {ActionTree} from 'vuex';
import {RadiusSearchState} from './types';
import {RootState} from '@/store/types';

export const actions: ActionTree<RadiusSearchState, RootState> = {
  setSelectedRadius({ commit, dispatch }, radiusSearchValue): void {
    commit('setSelectedRadius', radiusSearchValue);
  }
};
