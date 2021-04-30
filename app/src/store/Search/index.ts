import { Module } from "vuex";
import Tag from "@/models/tag";
import Location from "@/models/location";
import LocationService from "@/utils/services/LocationService";
import Radius from "@/models/radius";
import { RootState } from "../store";
import radii from "@/resources/radii";

export interface SearchState {
  tags: Tag[]
  searchValues: string[];
  selectedLocation?: Location;
  selectedRadius: Radius;
  international: boolean,
}

export const searchModule: Module<SearchState, RootState> = {
  namespaced: true,
  state: {
    tags: [] as Tag[],
    searchValues: [] as string[],
    selectedLocation: undefined,
    selectedRadius: radii[0],
    international: false,
  },
  getters: {
    getLocationText(state): string {
      return state.selectedLocation ? state.selectedLocation.title : "";
    },
    getLocation(state): Location | undefined {
      return state.selectedLocation;
    },
    getRadius(state): Radius | undefined {
      return state.selectedRadius;
    },
    getSearchValues(state): string[] {
      return state.searchValues;
    },
    getInternational(state): boolean {
      return state.international;
    },
  },
  mutations: {
    setTags(state, value: Tag[]): void {
      state.tags = value;
    },
    setSelectedLocation(state, value: Location | undefined): void {
      state.selectedLocation = value;
    },
    setSelectedRadius(state, value: Radius): void {
      state.selectedRadius = value;
    },
    addSearchValue(state, value: string): void {
      if (value && !state.searchValues.includes(value))
        state.searchValues.push(value);
    },
    removeSearchValue(state, value: string): void {
      state.searchValues.splice(state.searchValues.indexOf(value), 1);
    },
    setInternational(state, value: boolean): void {
      state.international = value;
    },
    clearSearchParams(state): void {
      state.searchValues = [];
      state.selectedRadius = radii[0];
      state.selectedLocation = undefined;
    },
  },
  actions: {
    addSearchValue({ commit }, searchValue: string): void {
      searchValue = searchValue.trim();
      commit("addSearchValue", searchValue);
    },
    addSearchValues({ dispatch }, searchValues: string[]): void {
      searchValues.forEach((val) => dispatch("addSearchValue", val));
    },
    removeSearchValue({ commit }, value: string): void {
      commit("removeSearchValue", value);
    },
    setSelectedLocation({ state }, location: string): void {
      const locationObject = LocationService.findByTitle(location)
        || {
        name: "",
        plz: "",
        title: "",
        state: "",
        lat: 0,
        lon: 0,
        rank: 0,
        country: location,
      }

      state.selectedLocation = locationObject;
    },
    setSelectedRadius({ commit }, radiusSearchValue): void {
      commit("setSelectedRadius", radiusSearchValue);
    },
    setInternational({ commit }, international: boolean): void {
      commit("setInternational", international);
    },
    clearSearchParams({ commit }): void {
      commit("clearSearchParams");
    },
  },
};
