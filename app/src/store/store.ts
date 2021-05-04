import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";
import DataService, { PaginatedResponse } from "../services/DataService";
import router from "@/router";
import Post from "@/models/post";
import { textSearchModule } from "./TextSearch";
import locationSearchModule from "./LocationSearch";
import { RootState } from "./types";

Vue.use(Vuex);

/** TODO: remove unnessesary module splitting, maybe just one searchmodule and one page module */
const store: StoreOptions<RootState> = {
  modules: {
    textSearchModule,
    locationSearchModule,
  },
  state: {
    posts: [] as Post[],
    selectedPost: null,
    page: 1 as number,
    resultSetSize: 100,
    totalResultSize: 0,
    resultsFrom: 0,
    hitsPerPage: 10, // must be a divider of resultSetSize, or the chunk loading gets complexer
    international: false,
  } as RootState,
  getters: {
    postsOnCurrentPage(state): Post[] {
      return state.posts.slice(
        (state.page - 1) * state.hitsPerPage - state.resultsFrom,
        state.page * state.hitsPerPage - state.resultsFrom
      );
    },
    numberOfPages(state): number {
      return Math.ceil(state.totalResultSize / state.hitsPerPage);
    },
    pageOfCurrentPost(state): number | null {
      const postIndex = state.posts.findIndex(
        (post) => state.selectedPost && post.id === state.selectedPost.id
      );
      if (postIndex < 0) {
        return null;
      }
      const pageOffset = state.resultsFrom / state.hitsPerPage + 1; // pages are 1 indexed...
      return Math.floor(postIndex / state.hitsPerPage) + pageOffset;
    },
    getInternational(state): boolean {
      return state.international;
    },
  },
  mutations: {
    clearSearchParams(state): void {
      state.textSearchModule.searchValues = [];
      state.locationSearchModule.selectedRadius = undefined;
      state.locationSearchModule.selectedLocation = undefined;
      state.page = 1;
      state.selectedPost = null;
    },
    setResultsFrom(state, value: number): void {
      state.resultsFrom = value;
    },
    setTotalResultSize(state, value: number): void {
      state.totalResultSize = value;
    },
    setPosts(state, value): void {
      state.posts = value;
    },
    setSelectedPost(state, value: Post | null): void {
      state.selectedPost = value;
    },
    setPage(state, value: number): void {
      state.page = value;
    },
    setInternational(state, value: boolean): void {
      state.international = value;
    },
  },
  actions: {
    clearSearchParams({ commit }): void {
      commit("clearSearchParams");
    },
    findPosts({ commit, state }): Promise<Post[]> {
      const location = state.locationSearchModule.selectedLocation;
      const searchValues = state.textSearchModule.searchValues;
      const radius =
        state.locationSearchModule.alternateRadius ||
        state.locationSearchModule.selectedRadius;

      const from = state.resultsFrom;
      const size = state.resultSetSize;
      const international = state.international;

      return new Promise((resolve) => {
        DataService.findBySelection({
          searchValues,
          location,
          radius,
          from,
          size,
          international,
        }).then((result: PaginatedResponse<Post>) => {
          commit("setTotalResultSize", result.meta.total);
          commit("setPosts", result.data);
          resolve(result.data);
        });
      });
    },
    setPage({ commit, dispatch, state, getters }, page: number): void {
      if (page < 1) {
        page = 1;
      }
      // Calculate the new from parameter to load the next resultSet chunk if necessary
      const currentPageIndex = (page - 1) * state.hitsPerPage; // these hu-mons start counting their pages at 1...
      const currentLoadedChunk = {
        min: state.resultsFrom,
        max: state.resultsFrom + state.resultSetSize - 1, // again with these hu-mons and their count beginning at 1...
      };
      if (!inChunk(currentPageIndex, currentLoadedChunk)) {
        // Calculate the needed offset
        // rounding off to the next multiple of our resultSetSize
        const from =
          currentPageIndex - (currentPageIndex % state.resultSetSize);
        commit("setResultsFrom", from);
      }

      commit("setPage", page);
      dispatch("updateURIFromState");
    },
    setInternational({ commit }, international: boolean): void {
      commit("setInternational", international);
    },
    setSelectedPost({ commit }, value: Post | null): void {
      commit("setSelectedPost", value);
    },
    /**
     * Sets state values from values of the current route 
     * @param param0 
     * @param route 
     * @returns 
     */
    hydrateStateFromRoute({ commit, dispatch }): Promise<any> {
      const queryParams = router.currentRoute.query as any;
      const params = router.currentRoute.params;

      // Clear previous search parameters. The URI is our single source of truth!
      commit("clearSearchParams");
      if ("q" in queryParams && queryParams.q) {
        dispatch("textSearchModule/addSearchValues", queryParams.q.split(","));
      }
      if ("area" in queryParams && queryParams.area) {
        dispatch(
          "setInternational",
          queryParams.area.toLowerCase() === "international"
        );
      }
      if ("location" in queryParams && queryParams.location) {
        dispatch(
          "locationSearchModule/setSelectedLocation",
          queryParams.location
        );
      }
      if ("radius" in queryParams && queryParams.radius) {
        dispatch("locationSearchModule/setSelectedRadius", queryParams.radius);
      }
      if ("page" in queryParams && queryParams.page) {
        dispatch("setPage", parseInt(queryParams.page, 10));
      }
      return dispatch("findPosts").then((posts: Post[]) => {
        if ("id" in params && params.id) {
          const selectedPost = posts.find((post) => post.id === params.id);
          if (selectedPost) {
            dispatch("setSelectedPost", selectedPost);
          }
        }
      });
    },
    /**
     * Updates url parameter with currently values from the store
     */
    updateURIFromState({ state }): void {
      const query = {
        ...router.currentRoute.query,
        q: state.textSearchModule.searchValues.join(","),
        area: state.international ? "international" : "national",
        location: state.locationSearchModule.selectedLocation ? state.locationSearchModule.selectedLocation.title : "",
        radius: state.locationSearchModule.selectedRadius,
        page: state.page.toString(),
      };

      let path = "/posts";
      // is there a post currently open? => reflect it in the route
      if (state.selectedPost) {
        path += "/" + state.selectedPost.id;
      }

      router
        .push({
          path,
          query,
        })
        .catch((err) => err);
    },
  },
};

function inChunk(x: number, chunk: { min: number; max: number }): boolean {
  return x >= chunk.min && x <= chunk.max;
}

export default new Vuex.Store<RootState>(store);
