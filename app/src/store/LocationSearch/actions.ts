import { ActionTree } from "vuex";
import { LocationSearchState } from "./types";
import { RootState } from "@/store/types";
import LocationService from "@/utils/services/LocationService";

export const actions: ActionTree<LocationSearchState, RootState> = {
  setLocationSearchValue({ commit }, locationSearchValue): void {
    commit("setLocationSearchValue", locationSearchValue);
  },
  setSelectedLocation({ commit }, selectedLocation): void {
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
  setSelectedRadius({ commit }, radiusSearchValue): void {
    commit("setAlternateRadius", "");
    commit("setSelectedRadius", radiusSearchValue);
  },
  setAlternateRadius({ commit }, radiusSearchValue): void {
    commit("setAlternateRadius", radiusSearchValue);
  },
};
