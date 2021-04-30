import { Module } from "vuex";
import Post from "@/models/post";
import { RootState } from "../store";

export interface PostsState {
  posts: Post[]
  selectedPostId?: string;
  selectedPage: number
}

export const postsModule: Module<PostsState, RootState> = {
  namespaced: true,
  state: {
    posts: [] as Post[],
    selectedPostId: undefined,
    selectedPage: 0
  },
  getters: {
    getPosts(state): Post[] {
      return state.posts;
    },
    getSelectedPost(state): string | undefined {
      return state.selectedPostId;
    },
    getSelectedPostIndex(state): number {
      return state.posts.findIndex(
        (post) => post.id === state.selectedPostId
      );
    },
    getSelectedPage(state): number {
      return state.selectedPage;
    },
  },
  mutations: {
    setPosts(state, value: Post[]): void {
      state.posts = value;
    },
    setSelectedPostId(state, value: string | undefined): void {
      state.selectedPostId = value;

    },
    setSelectedPage(state, value: number): void {
      state.selectedPage = value;
    },
  },
  actions: {
  },
};
