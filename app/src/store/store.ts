import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";
import router from "@/router";
import { searchModule, SearchState } from "./Search";
import { postsModule, PostsState } from "./Posts";
import DataService, { PaginatedResponse } from "@/services/DataService";
import Post from "@/models/post";
import radii from "@/resources/radii";

Vue.use(Vuex);

export interface RootState {
  searchModule: SearchState;
  postsModule: PostsState;
  radiusExtended: boolean;
  radiusExtendedFrom?: string;
}

const store: StoreOptions<RootState> = {
  modules: {
    searchModule,
    postsModule,
  },
  state: {
    radiusExtended: false,
    radiusExtendedFrom: undefined,
  } as RootState,
  getters: {},
  mutations: {},
  actions: {
    clearSearchParams({ commit }): void {
      commit("searchModule/clearSearchParams");
      commit("postsModule/clearPostParams");
    },
    /**
     * Sets state values from values of the current route
     */
    hydrateStateFromRoute({ commit, dispatch }): Promise<void> {
      const queryParams = router.currentRoute.query as any;
      const params = router.currentRoute.params;

      // Clear previous search parameters. The URI is our single source of truth!
      return dispatch("clearSearchParams").then(() => {
        const promises = new Array<Promise<any>>();
        if ("q" in queryParams && queryParams.q)
          promises.push(
            dispatch("searchModule/addSearchValues", queryParams.q.split(","))
          );
        if ("area" in queryParams && queryParams.area)
          commit(
            "searchModule/setInternational",
            queryParams.area.toLowerCase() === "international"
          );

        if ("location" in queryParams && queryParams.location)
          commit("searchModule/setSelectedLocation", queryParams.location);

        if ("radius" in queryParams && queryParams.radius)
          commit("searchModule/setSelectedRadius", queryParams.radius);

        if ("page" in queryParams && queryParams.page)
          promises.push(
            dispatch(
              "postsModule/setSelectedPage",
              parseInt(queryParams.page, 10)
            )
          );

        // wati that all properties are set
        return Promise.all(promises).then(() =>
          // load all posts for this properties
          dispatch("loadPosts").then((posts: Post[]) => {
            // set selected post if id is given
            if ("id" in params && params.id) {
              const post = posts.find((post) => post.id === params.id);
              dispatch("postsModule/setSelectedPost", post).then(() =>
                // to be sure that the param types are not overriden in the query
                dispatch("updateURIFromState")
              );
            }
          })
        );
      });
    },

    /**
     * Updates url parameter with currently values from the store
     */
    updateURIFromState({ state }): void {
      const query = {
        ...router.currentRoute.query,
        q: state.searchModule.searchValues.join(","),
        area: state.searchModule.isInternational ? "international" : "national",
        location: state.searchModule.selectedLocation
          ? state.searchModule.selectedLocation.title
          : "",
        radius: state.searchModule.selectedRadius,
        page: state.postsModule.selectedPage.toString(),
      };

      let path = "/posts";
      // is there a post currently open? => reflect it in the route
      if (state.postsModule.selectedPost)
        path += "/" + state.postsModule.selectedPost.id;

      // only change route if query parameter change from current query parameter
      if (
        JSON.stringify(query) !== JSON.stringify(router.currentRoute.query) ||
        router.currentRoute.path !== path
      )
        router.push({
          path,
          query,
        });
    },

    /**
     *  find posts from DataService by setted parameter
     */
    loadPosts({ state, commit }): Promise<Post[]> {
      return DataService.findBySelection({
        searchValues: state.searchModule.searchValues,
        location: state.searchModule.selectedLocation,
        radius: state.searchModule.selectedRadius,
        from: state.postsModule.resultsFrom,
        size: state.postsModule.resultSetSize,
        international: state.searchModule.isInternational,
      })
        .then((result: PaginatedResponse<Post>) => {
          state.postsModule.totalResultSize = result.meta.total;
          commit("postsModule/setPosts", result.data);
          return result.data;
        })
        .then((posts: Post[]) => {
          // there is a full list of posts
          if (posts.length) {
            state.radiusExtended = state.radiusExtendedFrom ? true : false;

            if (
              state.radiusExtendedFrom !== state.searchModule.selectedRadius &&
              !state.searchModule.selectedRadius
            )
              state.radiusExtended = false;

            return posts;
          }
          // if there are no posts in the list and // if a location and a radius is set
          else if (
            state.searchModule.selectedLocation &&
            state.searchModule.selectedRadius
          ) {
            const radiusValueBeforeExtend = state.searchModule.selectedRadius;
            // Wenn wir mit einem Radius um einen Ort suchen, den Radius vergr��ern und nochmal probieren!

            // find radius index of radii
            const currentRadiusIndex = radii.findIndex(
              (r) => r.value === radiusValueBeforeExtend
            );
            // find next bigger radii
            const nextBiggerRadiusValue =
              radii[(currentRadiusIndex + 1) % radii.length].value;

            // Wir wollen uns merken, dass wir den Radius ver�ndert haben, um den Nutzer dar�ber zu informieren.
            // Aber nur, wenn wir das nicht bereits gemacht haben um uns den Wert nicht zu �berschreiben.
            if (!state.radiusExtendedFrom)
              state.radiusExtendedFrom = radiusValueBeforeExtend;

            // update radius
            commit("searchModule/setSelectedRadius", nextBiggerRadiusValue);
            // and load posts again
            return this.dispatch("loadPosts");
          }
        });
    },
  },
};

export default new Vuex.Store<RootState>(store);
