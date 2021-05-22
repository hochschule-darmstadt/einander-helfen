import { Module } from "vuex";
import Post from "@/models/post";
import { RootState } from "../store";

export interface PostsState {
  posts: Post[];
  selectedPostId?: string;
  selectedPage: number;
  hitsPerPage: number;
  resultSetSize: number;
  resultsFrom: number;
  totalResultSize: number;
}

export const postsModule: Module<PostsState, RootState> = {
  namespaced: true,
  state: {
    posts: [] as Post[],
    selectedPostId: undefined,
    selectedPage: 1,
    hitsPerPage: parseInt(process.env.VUE_APP_HITS_PER_PAGE, 10) || 10,
    resultSetSize: parseInt(process.env.VUE_APP_RESULT_SET_SIZE, 10) || 100,
    resultsFrom: 0,
    totalResultSize: 0,
  },
  getters: {
    getPosts(state): Post[] {
      return state.posts;
    },
    getSelectedPostId(state): string | undefined {
      return state.selectedPostId;
    },
    getSelectedPage(state): number {
      return state.selectedPage;
    },
    totalPages(state): number {
      return Math.ceil(state.totalResultSize / state.hitsPerPage);
    },
    postsOnCurrentPage(state): Post[] {
      return state.posts.slice(
        (state.selectedPage - 1) * state.hitsPerPage - state.resultsFrom,
        state.selectedPage * state.hitsPerPage - state.resultsFrom
      );
    },

    selectedPost(state): Post | undefined {
      if (!state.selectedPostId) return undefined;
      return state.posts.find((post) => post.id === state.selectedPostId);
    }
  },
  mutations: {
    clearPostParams(state): void {
      state.posts = [];
      state.selectedPostId = undefined;
      state.selectedPage = 1;
      state.resultsFrom = 0;
      state.totalResultSize = 0;
    },
    switchPageToSelectedPost(state): void {
      if (state.selectedPostId && state.posts) {
        // update page if nessecary
        const postIndex = state.posts.findIndex((post) => post.id === state.selectedPostId);

        if (postIndex > 0) {
          // if selectedPost is in posts set page to page of this selectedPost
          const pageOffset = state.resultsFrom / state.hitsPerPage + 1; // pages are 1 indexed
          const pageOnPost = Math.floor(postIndex / state.hitsPerPage) + pageOffset;
          if (state.selectedPage != pageOnPost)
            state.selectedPage = pageOnPost;
        } // else selectedPost not in posts => do nothing
      }
    },
  },
  actions: {
    setPosts({ state, commit }, posts: Post[]): void {
      state.posts = posts;
      commit("switchPageToSelectedPost");
    },
    setSelectedPostId({ state, commit }, postId: string | undefined = undefined): void {
      state.selectedPostId = postId;
      commit("switchPageToSelectedPost");
    },
    setSelectedPage({ state }, page = 1): void {
      const inChunk = (
        x: number,
        chunk: { min: number; max: number }
      ): boolean => x >= chunk.min && x <= chunk.max;

      // set page to minimal page if less
      if (page < 1) page = 1;

      if (page != state.selectedPage) {
        // Calculate the new from parameter to load the next resultSet chunk if necessary
        const currentPageIndex = (page - 1) * state.hitsPerPage; // Pages start at 1
        const currentLoadedChunk = {
          min: state.resultsFrom,
          max: state.resultsFrom + state.resultSetSize - 1, // Pages start at 1
        };
        if (!inChunk(currentPageIndex, currentLoadedChunk)) {
          // Calculate the needed offset
          // rounding off to the next multiple of our resultSetSize
          const from =
            currentPageIndex - (currentPageIndex % state.resultSetSize);
          state.resultsFrom = from;
        }

        state.selectedPage = page;
      }
    },
  },
};
