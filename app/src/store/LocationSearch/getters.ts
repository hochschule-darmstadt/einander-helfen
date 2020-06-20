import LocationService from '@/utils/services/LocationService';
import {LocationSearchState} from '@/store/LocationSearch/types';
import {RootState} from '../types';
import {GetterTree} from 'vuex';

export const getters: GetterTree<LocationSearchState, RootState> = {
  getLocations: (state) => {
    const p = state.locationSearchValue || state.selectedLocation;
    return LocationService
      .findLocationByPlzOrName(p);
  }
};
