import LocationService from '@/services/LocationService';
import {LocationSearchState} from '@/store/LocationSearch/types';
import {RootState} from '../types';
import {GetterTree} from 'vuex';

export const getters: GetterTree<LocationSearchState, RootState> = {
  getLocations: (state, gettersValue, rootState) => {
    const p = state.locationSearchValue || state.selectedLocation;
    if (rootState.international) {
        return LocationService.findCountryByName(p);
    } else {
        return LocationService.findLocationByPlzOrName(p);
    }
  }
};
