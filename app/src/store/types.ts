import Post from '@/models/post';
import {TextSearchState} from '@/store/TextSearch/types';
import {LocationSearchState} from '@/store/LocationSearch/types';

export interface RootState {
  posts: Post[];
  page: number;
  textSearchModule: TextSearchState;
  locationSearchModule: LocationSearchState;
}
