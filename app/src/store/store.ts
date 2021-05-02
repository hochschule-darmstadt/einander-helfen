import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";
import router from "@/router";
import { searchModule, SearchState } from "./Search";
import { postsModule, PostsState } from "./Posts";
import DataService, { PaginatedResponse } from "@/utils/services/DataService";
import Post from "@/models/post";

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
      commit("searchModule/clearSearchParams"),
        commit("postsModule/setSelectedPost"),
        commit("postsModule/setSelectedPage")
    },
    /**
     * Sets state values from values of the current route 
     */
    hydrateStateFromRoute({ commit, dispatch }): Promise<any> {
      const queryParams = router.currentRoute.query as any;
      const params = router.currentRoute.params;

      // Clear previous search parameters. The URI is our single source of truth!
      return dispatch('clearSearchParams')
        .then(() => {
          if ('q' in queryParams && queryParams.q)
            commit('searchModule/addSearchValues', queryParams.q.split(','));

          if ('area' in queryParams && queryParams.area)
            commit('searchModule/setInternational', queryParams.area.toLowerCase() === 'international');

          if ('location' in queryParams && queryParams.location)
            commit('searchModule/setSelectedLocation', queryParams.location);

          if ('radius' in queryParams && queryParams.radius)
            commit('searchModule/setSelectedRadius', queryParams.radius);

          if ('page' in queryParams && queryParams.page)
            commit('postsModule/setSelectedPage', parseInt(queryParams.page, 10));

          // load posts for this params
          return dispatch("loadPosts")
            .then((posts: Post[]) => {
              // set selected post if id is given
              if ('id' in params && params.id) {
                const post = posts.find((post) => post.id === params.id);
                commit('postsModule/setSelectedPost', post);

                // to be sure that the param types are not overriden in the query
                dispatch("updateURIFromState");
              }
            });
          // TODO: add catch handler and show error
        });
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
      if (state.postsModule.selectedPost)
        path += "/" + state.postsModule.selectedPost.id;

      router.push({
        path,
        query
      })
        // TODO: show error message to user
        .catch((err) => console.debug(err));
    },
    /**
     *  find posts from DataService by setted parameter 
     */
    loadPosts({ state, commit }): Promise<Post[]> {
      return DataService.findBySelection({
        searchValues: state.searchModule.searchValues,
        location: state.searchModule.selectedLocation,
        radius: state.searchModule.selectedRadius.value,
        from: state.postsModule.resultsFrom,
        size: state.postsModule.resultSetSize,
        international: state.searchModule.international,
      }).then((result: PaginatedResponse<Post>) => {
        state.postsModule.totalResultSize = result.meta.total;
        commit("postsModule/setPosts", result.data);
        return result.data;
      });
      // TODO: add catch handler and show error
    },
  },
};

export default new Vuex.Store<RootState>(store);
