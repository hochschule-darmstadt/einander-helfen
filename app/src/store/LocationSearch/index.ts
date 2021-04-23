import { Module } from "vuex";
import { RootState } from "../types";
import Location from "@/models/location";
import LocationService from "@/utils/services/LocationService";

export interface LocationSearchState {
  selectedLocation?: Location;
  selectedRadius?: string;
  alternateRadius?: string;
}

const locationSearchModule: Module<LocationSearchState, RootState> = {
  namespaced: true,
  state: {
    selectedLocation: undefined,
    selectedRadius: undefined,
    alternateRadius: undefined,
  },
  getters: {
    getLocationText(state): string {
      return state.selectedLocation ? state.selectedLocation.title : "";
    },
    getLocation(state): Location | undefined {
      return state.selectedLocation;
    },
    getRadius(state): string {
      return state.selectedRadius || "";
    },
  },
  mutations: {
    setSelectedLocation(state, value): void {
      state.selectedLocation = value;
    },
    setSelectedRadius(state, value): void {
      state.selectedRadius = value;
    },
    setAlternateRadius(state, value): void {
      state.alternateRadius = value;
    },
  },
  actions: {
    setLocationSearchValue({ commit }, locationSearchValue): void {
      commit("setLocationSearchValue", locationSearchValue);
    },
    setSelectedLocation({ commit, state }, selectedLocation): void {
      const selectedLocationObject = LocationService.findByTitle(selectedLocation)
        || {
        name: "",
        plz: "",
        title: "",
        state: "",
        lat: 0,
        lon: 0,
        rank: 0,
        country: selectedLocation,
      }

      state.selectedLocation = selectedLocationObject;
    },
    setSelectedRadius({ commit, dispatch }, radiusSearchValue): void {
      commit("setAlternateRadius", "");
      commit("setSelectedRadius", radiusSearchValue);
    },
    setAlternateRadius({ commit }, radiusSearchValue): void {
      commit("setAlternateRadius", radiusSearchValue);
    },
  },
};

export default locationSearchModule;
