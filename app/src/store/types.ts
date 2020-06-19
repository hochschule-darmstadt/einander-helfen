import Post from '@/models/post';
import {SearchBarState} from '@/store/SearchBarStore/types';
import {RadiusSearchState} from '@/store/RadiusSearchStore/types';
import {LocationSearchState} from '@/store/LocationSearchStore/types';

export interface RootState {
  posts: Post[];
  page: number;
  searchBarModule: SearchBarState;
  radiusSearchModule: RadiusSearchState;
  locationSearchModule: LocationSearchState;
}
