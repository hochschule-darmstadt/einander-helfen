import { Module } from "vuex";
import Post from "@/models/post";
import { RootState } from "../store";

export interface PostsState {
  // post stuff
  posts: Post[];
  selectedPost?: Post;
  // page stuff
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
    selectedPost: undefined,
    selectedPage: 1,
    hitsPerPage: process.env.VUE_APP_HITS_PER_PAGE || 10,
    resultSetSize: process.env.VUE_APP_RESULT_SET_SIZE || 100,
    resultsFrom: 0,
    totalResultSize: 0,
  },
  getters: {
    getPosts(state): Post[] {
      return state.posts;
    },
    getSelectedPost(state): Post | undefined {
      return state.selectedPost;
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
    selectedPostId(state): string | undefined {
      return state.selectedPost ? state.selectedPost.id : undefined;
    },
  },
  mutations: {
    clearPostParams(state): void {
      state.posts = [];
      state.selectedPost = undefined;
      state.selectedPage = 1;
      state.resultsFrom = 0;
      state.totalResultSize = 0;
    },
    setPosts(state, posts: Post[]): void {
      // set Open post if list contains only one post.
      if (posts.length === 1) state.selectedPost = posts[0];
      state.posts = posts;
    },
  },
  actions: {
    setSelectedPost({ state }, post: Post | undefined = undefined): void {
      const selectedPostIndex = state.posts.findIndex(
        (post) => state.selectedPost && post.id === state.selectedPost.id
      );

      // set post
      state.selectedPost = post;
      if (post) {
        // update page if nessecary
        const postIndex = selectedPostIndex;
        if (postIndex > 0) {
          // if selectedPost is in posts set page to page of this selectedPost
          const pageOffset = state.resultsFrom / state.hitsPerPage + 1; // pages are 1 indexed...
          const pageOnPost =
            Math.floor(postIndex / state.hitsPerPage) + pageOffset;
          state.selectedPage = pageOnPost;
        } // else selectedPost not in posts => do nothing
      }
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
          state.resultsFrom = from;
        }

        state.selectedPage = page;
      }
    },
  },
};
