import Vue from 'vue';
import Vuex, {StoreOptions} from 'vuex';
import DataService, {PaginatedResponse} from '../utils/services/DataService';
import LocationService from '@/utils/services/LocationService';
import router from '@/router';
import Post from '@/models/post';
import textSearchModule from './TextSearch';
import locationSearchModule from './LocationSearch';
import {RootState} from './types';
Vue.use(Vuex);

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
    hitsPerPage: 10 // must be a divider of resultSetSize, or the chunk loading gets complexer
  } as RootState,
  mutations: {

    clearSearchParams(state): void {
      state.textSearchModule.searchValues = [];
      state.locationSearchModule.selectedRadius = '';
      state.locationSearchModule.selectedLocation = '';
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
    setSelectedPost(state, value: Post|null): void {
      state.selectedPost = value;
    },
    setPage(state, value: number): void {
      state.page = value;
    }
  },
  actions: {
    clearSearchParams({commit}): void {
      commit('clearSearchParams');
    },
    findPosts({ commit, state }): Promise<Post[]> {
      const location = LocationService.findByTitle(state.locationSearchModule.selectedLocation);
      const searchValues = state.textSearchModule.searchValues;
      const radius = state.locationSearchModule.selectedRadius;

      const from = state.resultsFrom;
      const size = state.resultSetSize;

      return new Promise((resolve) => {
        DataService.findBySelection({
          searchValues,
          location,
          radius,
          from,
          size
        }).then((result: PaginatedResponse<Post>) => {
          commit('setTotalResultSize', result.meta.total);
          commit('setPosts', result.data);
          resolve(result.data);
        });
      });

    },
    setPage({ commit, dispatch, state }, page: number): void {
        if (page < 1) {
          page = 1;
        }
        // Calculate the new from parameter to load the next resultSet chunk if necessary
        const currentPageIndex = (page - 1) * state.hitsPerPage; // these hu-mons start counting their pages at 1...
        const currentLoadedChunk = {
          min: state.resultsFrom,
          max: state.resultsFrom + state.resultSetSize - 1 // again with these hu-mons and their count beginning at 1...
        };
        if (! inChunk(currentPageIndex, currentLoadedChunk)) {
          // Calculate the needed offset
          // rounding off to the next multiple of our resultSetSize
          const from = currentPageIndex - (currentPageIndex % state.resultSetSize);
          commit('setResultsFrom', from);
        }

        commit('setPage', page);
        dispatch('updateURIFromState');
    },
    setSelectedPost({ commit }, value: Post|null): void {
      commit('setSelectedPost', value);
    },
    hydrateStateFromRoute({ commit, dispatch }, route): void {
      const queryParams = route.query;
      const params = route.params;

      // Clear previous search parameters. The URI is our single source of truth!
      commit('clearSearchParams');
      if ('q' in queryParams && queryParams.q) {
        dispatch('textSearchModule/addSearchValues', queryParams.q.split(','));
      }
      if ('location' in queryParams && queryParams.location) {
        commit('locationSearchModule/setSelectedLocation', queryParams.location);
      }
      if ('radius' in queryParams && queryParams.radius) {
        commit('locationSearchModule/setSelectedRadius', queryParams.radius);
      }
      if ('page' in queryParams && queryParams.page) {
        commit('setPage', parseInt(queryParams.page, 10));
      }
      dispatch('findPosts').then((posts: Post[]) => {
        if ('id' in params && params.id) {
          const selectedPost = posts.find((post) => post.id === params.id);
          if (selectedPost) {
            commit('setSelectedPost', selectedPost);
          }
        }
      });
    },
    updateURIFromState({ state }): void {
      const query = {
        ...router.currentRoute.query,
        q: state.textSearchModule.searchValues.join(','),
        location: state.locationSearchModule.selectedLocation,
        radius: state.locationSearchModule.selectedRadius,
        page: state.page.toString()
      };

      let path  = '/posts';
      // is there a post currently open? => reflect it in the route
      if (state.selectedPost) {
        path += '/' + state.selectedPost.id;
      }

      router.push({
        path,
        query
      }).catch((err) => err);
    },
  },
  getters: {
    postsOnCurrentPage(state): Post[] {
      return state.posts.slice(
        ((state.page - 1) * state.hitsPerPage) - state.resultsFrom,
        (state.page * state.hitsPerPage) - state.resultsFrom
      );
    },
    numberOfPages(state): number {
      return Math.ceil(state.totalResultSize / state.hitsPerPage);
    },
    pageOfCurrentPost(state): number|null {
      const postIndex = state.posts.findIndex((post) => state.selectedPost && post.id === state.selectedPost.id);
      if (postIndex < 0) {
        return null;
      }
      const pageOffset = state.resultsFrom / state.hitsPerPage + 1; // pages are 1 indexed...
      return Math.floor(postIndex / state.hitsPerPage) + pageOffset;
    }
  }
};

function inChunk(x: number, chunk: {min: number, max: number}): boolean {
  return x >= chunk.min && x <= chunk.max;
}

export default new Vuex.Store<RootState>(store);
