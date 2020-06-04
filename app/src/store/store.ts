import Vue from 'vue';
import Vuex from 'vuex';
import Location from '@/models/location';
import LocationService from '@/utils/services/LocationService';

Vue.use(Vuex);

const store = new Vuex.Store({
   state: {
       locations: [] as Location[],
       locationSearchValue: '',
       radiusSearchValue: ''
   },
   mutations: {
       setLocations(state, value): void {
           state.locations = value;
       },
       setLocationSearchValue(state, value): void {
           state.locationSearchValue = value;
       },
       setRadiusSearchValue(state, value): void {
           state.radiusSearchValue = value;
       }
   },
   actions: {
       findLocationByPlzOrName({ commit, state }): void {
           const newLocations = LocationService.findLocationByPlzOrName(state.locationSearchValue);
           commit('setLocations', newLocations);
           console.log(state.locations);
       },
       setLocationSearchValue({ commit, dispatch }, locationSearchValue): void {
           commit('setLocationSearchValue', locationSearchValue);
           dispatch('findLocationByPlzOrName');
       },
       setRadiusSearchValue({ commit, dispatch }, radiusSearchValue): void {
           commit('setRadiusSearchValue', radiusSearchValue);
       }
   },
   getters: {
       getLocations: (state) => {
           if (state.locations.length === 0) {
               return LocationService.findLocationByPlzOrName(state.locationSearchValue);
           }
           return state.locations;
       }
   }
});

export default store;
