import { Module } from "vuex";
import Tag from "@/models/tag";
import Location from "@/models/location";
import LocationService from "@/services/LocationService";
import { RootState } from "../store";
import { getDefaultRadius } from "@/resources/radii";

export interface SearchState {
  tags: Tag[]
  searchValues: string[];
  selectedLocation?: Location;
  selectedRadius: string;
  isInternational: boolean,
}

export const searchModule: Module<SearchState, RootState> = {
  namespaced: true,
  state: {
    tags: [] as Tag[],
    searchValues: [] as string[],
    selectedLocation: undefined,
    selectedRadius: "",
    isInternational: false,
  },
  getters: {
    getLocationText(state): string {
      return state.selectedLocation ? state.selectedLocation.title : "";
    },
    getLocation(state): Location | undefined {
      return state.selectedLocation;
    },
    getRadius(state): string {
      return state.selectedRadius;
    },
    getSearchValues(state): string[] {
      return state.searchValues;
    },
    isInternational(state): boolean {
      return state.isInternational;
    },
  },
  mutations: {
    setTags(state, value: Tag[]): void {
      state.tags = value;
    },
    setSelectedLocation(state, location: string): void {
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
    setSelectedRadius(state, value: string): void {
      state.selectedRadius = value;
    },
    addSearchValue(state, value: string): void {
      value = value.trim();
      if (value && !state.searchValues.includes(value))
        state.searchValues.push(value);
    },
    removeSearchValue(state, value: string): void {
      state.searchValues.splice(state.searchValues.indexOf(value), 1);
    },
    setInternational(state, value: boolean): void {
      if (state.isInternational != value)
        state.selectedRadius = getDefaultRadius().value;
      state.isInternational = value;
    },
    clearSearchParams(state): void {
      state.searchValues = [];
      state.selectedRadius = getDefaultRadius().value;
      state.selectedLocation = undefined;
    },
  },
  actions: {
    addSearchValues({ commit }, searchValues: string[]): void {
      searchValues.forEach((val) => commit("addSearchValue", val));
    },
  },
};
