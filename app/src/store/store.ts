/**
 * This store contains methods to find and load posts matching the search.
 */

import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";
import router from "@/router";
import { searchModule, SearchState } from "./Search";
import { postsModule, PostsState } from "./Posts";
import PostService, { PaginatedResponse } from "@/services/PostService";
import Post from "@/models/post";
import radii from "@/assets/resources/radii";

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
    findPosts({ commit, state }): Promise<Post[]> {
      const location = state.searchModule.selectedLocation;
      const searchValues = state.searchModule.searchValues;
      const radius = state.searchModule.selectedRadius;

      const from = state.postsModule.resultsFrom;
      const size = state.postsModule.resultSetSize;
      const international = state.searchModule.isInternational;

      return new Promise((resolve) => {
        PostService.findPosts({
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
    /**
     * Sets state values from values of the current route
     */
    hydrateStateFromRoute({ commit, dispatch }): Promise<any> {
      const queryParams = router.currentRoute.query as any;
      const params = router.currentRoute.params;

      // Clear previous search parameters. The URI is our single source of truth!
      return dispatch("clearSearchParams").then(() => {
        const promises = new Array<Promise<any>>();
        // get query string
        if ("q" in queryParams && queryParams.q)
          promises.push(
            dispatch("searchModule/addSearchValues", queryParams.q.split(","))
          );
        // get area value
        if ("area" in queryParams && queryParams.area)
          commit(
            "searchModule/setInternational",
            queryParams.area.toLowerCase() === "international"
          );

        // get location value
        if ("location" in queryParams && queryParams.location)
          commit("searchModule/setSelectedLocation", queryParams.location);

        // get radius value
        if ("radius" in queryParams && queryParams.radius)
          commit("searchModule/setSelectedRadius", queryParams.radius);

        // get page value
        if ("page" in queryParams && queryParams.page)
          promises.push(
            dispatch(
              "postsModule/setSelectedPage",
              parseInt(queryParams.page, 10)
            )
          );

        // get selected post id value
        if ("id" in params && params.id)
          promises.push(dispatch("postsModule/setSelectedPostId", params.id));

        // wati that all properties are set
        return Promise.all(promises);
      });
    },

    /**
     * Updates url parameter with current values from the store
     */
    updateURIFromState({ state, getters }): void {
      const query = {
        ...router.currentRoute.query,
        q: state.searchModule.searchValues.join(","),
        area: state.searchModule.isInternational ? "international" : "national",
        location: getters["searchModule/getLocationText"],
        radius: state.searchModule.selectedRadius,
        page: state.postsModule.selectedPage.toString(),
      };

      let path = "/posts";
      // is there a post currently open? => reflect it in the route
      if (state.postsModule.selectedPostId)
        path += "/" + state.postsModule.selectedPostId;

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
     *  Load a post from DataService by given id.
     */
    loadPost(context, id: string): Promise<Post | undefined> {
      return PostService.findById(id).then((post) => post);
    },

    /**
     *  Load posts from DataService by setted parameter.
     */
    loadPosts({ state, dispatch, commit }): Promise<Post[]> {
      // clear extended properties
      if (!state.radiusExtended) state.radiusExtendedFrom = undefined;
      else state.radiusExtended = false;

      return PostService.findPosts({
        searchValues: state.searchModule.searchValues,
        location: state.searchModule.selectedLocation,
        radius: state.searchModule.selectedRadius,
        from: state.postsModule.resultsFrom,
        size: state.postsModule.resultSetSize,
        international: state.searchModule.isInternational,
      })
        .then((result: PaginatedResponse<Post>) => {
          state.postsModule.totalResultSize = result.meta.total;
          return dispatch("postsModule/setPosts", result.data).then(
            () => result.data
          );
        })
        .then((posts: Post[]) => {
          // there is a full list of posts
          if (posts.length) {
            // set Open post if list contains only one post.
            if (posts.length === 1)
              dispatch("postsModule/setSelectedPostId", posts[0].id);

            return posts;
          }
          // if there are no posts in the list and // if a location and a radius is set
          else if (
            state.searchModule.selectedLocation &&
            state.searchModule.selectedRadius
          ) {
            const radiusValueBeforeExtend = state.searchModule.selectedRadius;
            // Wenn wir mit einem Radius um einen Ort suchen, den Radius vergroeßern und nochmal probieren!

            // find radius index of radii
            const currentRadiusIndex = radii.findIndex(
              (r) => r.value === radiusValueBeforeExtend
            );
            // find next bigger radii
            const nextBiggerRadiusValue =
              radii[(currentRadiusIndex + 1) % radii.length].value;

            // We want to notice whether the radius changed to inform the user
            // but only if we did not already do so in order to not overwrite the value.
            const extendFrom =
              state.radiusExtendedFrom || radiusValueBeforeExtend;

            // update radius
            commit("searchModule/setSelectedRadius", nextBiggerRadiusValue);
            // load posts again
            return this.dispatch("loadPosts").then((posts) => {
              // set extended properties after new posts are loaded
              state.radiusExtended = true;
              state.radiusExtendedFrom = extendFrom;

              return posts;
            });
          }
        });
    },
  },
};

export default new Vuex.Store<RootState>(store);
