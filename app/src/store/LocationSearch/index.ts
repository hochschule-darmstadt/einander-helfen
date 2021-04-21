import { Module } from "vuex";
import { RootState } from "../types";
import Location from "@/models/location";
import LocationService from "@/utils/services/LocationService";


export interface LocationSearchState {
  locationSearchValue: string;
  selectedLocation: string;
  selectedLocationObject: Location | null;
  selectedRadius: string;
  alternateRadius: string;
}

const locationSearchModule: Module<LocationSearchState, RootState> = {
  namespaced: true,
  state: {
    locationSearchValue: "",
    selectedLocation: "",
    selectedLocationObject: null,
    selectedRadius: "",
    alternateRadius: "",
  },
  getters: {
  },
  mutations: {
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
  },
  actions: {
    setLocationSearchValue({ commit, dispatch }, locationSearchValue): void {
      commit("setLocationSearchValue", locationSearchValue);
    },
    setSelectedLocation({ commit, dispatch, state }, selectedLocation): void {
      let selectedLocationObject = selectedLocation
        ? LocationService.findByTitle(selectedLocation)
        : null;
      if (selectedLocationObject === undefined) {
        selectedLocationObject = {
          name: "",
          plz: "",
          title: "",
          state: "",
          lat: 0,
          lon: 0,
          rank: 0,
          country: selectedLocation,
        };
      }
      if (selectedLocationObject === undefined) {
        selectedLocationObject = null;
      }

      commit("setSelectedLocation", selectedLocation);
      commit("setSelectedLocationObject", selectedLocationObject);
    },
    setSelectedRadius({ commit, dispatch }, radiusSearchValue): void {
      commit("setAlternateRadius", "");
      commit("setSelectedRadius", radiusSearchValue);
    },
    setAlternateRadius({ commit }, radiusSearchValue): void {
      commit("setAlternateRadius", radiusSearchValue);
    },
  }

};

export default locationSearchModule;
