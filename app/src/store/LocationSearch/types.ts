import Location from '@/models/location';

export interface LocationSearchState {
  locationSearchValue: string;
  selectedLocation: string;
  selectedLocationObject: Location|null;
  selectedRadius: string;
  alternateRadius: string;
}
