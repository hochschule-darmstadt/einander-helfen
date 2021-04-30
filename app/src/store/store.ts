import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";
import router from "@/router";
import { searchModule, SearchState } from "./Search";
import { postsModule, PostsState } from "./Posts";

Vue.use(Vuex);

export interface RootState {
  searchModule: SearchState;
  postsModule: PostsState;
}

const store: StoreOptions<RootState> = {
  modules: {
    searchModule,
    postsModule,
  },
  state: {
  } as RootState,
  getters: {
  },
  mutations: {
  },
  actions: {
    clearSearchParams({ commit }): void {
      commit("searchModule/clearSearchParams");
      commit("postsModule/setSelectedPostId", undefined);
    },
    /**
     * Sets state values from values of the current route 
     * @param param0 
     * @param route 
     * @returns 
     */
    hydrateStateFromRoute({ commit, dispatch }): void {
      const queryParams = router.currentRoute.query as any;
      const params = router.currentRoute.params;

      // Clear previous search parameters. The URI is our single source of truth!
      dispatch('clearSearchParams');
      if ('q' in queryParams && queryParams.q) {
        commit('searchModule/addSearchValues', queryParams.q.split(','));
      }
      if ('area' in queryParams && queryParams.area) {
        commit('searchModule/setInternational', queryParams.area.toLowerCase() === 'international');
      }
      if ('location' in queryParams && queryParams.location) {
        commit('searchModule/setSelectedLocation', queryParams.location);
      }
      if ('radius' in queryParams && queryParams.radius) {
        commit('searchModule/setSelectedRadius', queryParams.radius);
      }
      if ('page' in queryParams && queryParams.page) {
        commit('postsModule/setSelectedPage', parseInt(queryParams.page, 10));
      }
      if ('id' in params && params.id) {
        commit('postsModule/setSelectedPostId', params.id);
      }
    },
    /**
     * Updates url parameter with currently values from the store
     */
    updateURIFromState({ state }): void {
      const query = {
        ...router.currentRoute.query,
        q: state.searchModule.searchValues.join(","),
        area: state.searchModule.international ? "international" : "national",
        location: state.searchModule.selectedLocation ? state.searchModule.selectedLocation.title : "",
        radius: state.searchModule.selectedRadius ? state.searchModule.selectedRadius.value : "",
        page: state.postsModule.selectedPage.toString(),
      };

      let path = "/posts";
      // is there a post currently open? => reflect it in the route
      if (state.postsModule.selectedPostId)
        path += "/" + state.postsModule.selectedPostId;

      router.push({
        path,
        query
      })
        .catch((err) => console.debug(err));
    },
  },
};

export default new Vuex.Store<RootState>(store);
