import Post from "@/models/post";
import { TextSearchState } from "@/store/TextSearch";
import { LocationSearchState } from "@/store/LocationSearch/types";

export interface RootState {
  posts: Post[];
  selectedPost: Post | null;
  page: number;
  textSearchModule: TextSearchState;
  locationSearchModule: LocationSearchState;
  totalResultSize: number;
  resultSetSize: number;
  resultsFrom: number;
  hitsPerPage: number;
  international: boolean;
}
