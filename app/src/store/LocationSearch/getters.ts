import LocationService from '@/utils/services/LocationService';
import {LocationSearchState} from '@/store/LocationSearch/types';
import {RootState} from '../types';
import {GetterTree} from 'vuex';

export const getters: GetterTree<LocationSearchState, RootState> = {
  getLocations: (state, getters, RootState) => {
    const p = state.locationSearchValue || state.selectedLocation;
    if (RootState.international)
        return LocationService.findCountryByName(p)
    else
        return LocationService.findLocationByPlzOrName(p)
  }
};