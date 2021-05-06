import { Module } from "vuex";
import { RootState } from "../types";
import Tag from "@/models/tag";

export interface TextSearchState {
  labels: string[];
  synonyms: string[];
  searchValues: string[];
}

export const textSearchModule: Module<TextSearchState, RootState> = {
  namespaced: true,
  state: {
    labels: [] as string[],
    synonyms: [] as string[],
    searchValues: [] as string[],
  },
  getters: {
    getSearchValues(state): string[] {
      return state.searchValues;
    }
  },
  mutations: {
    addSearchValue(state, value: string): void {
      if (!state.searchValues.includes(value)) {
        state.searchValues.push(value);
      }
    },
    removeSearchValue(state, value: string): void {
      state.searchValues.splice(state.searchValues.indexOf(value), 1);
    },
  },
  actions: {
    addSearchValue({ commit }, searchValue: string): void {
      searchValue = searchValue.trim();
      if (searchValue) {
        commit("addSearchValue", searchValue);
      }
    },
    addSearchValues({ dispatch }, searchValues: string[]): void {
      searchValues.forEach((tag) => dispatch("addSearchValue", tag));
    },
    removeSearchValue({ commit }, value: string): void {
      commit("removeSearchValue", value);
    },
  },
};
