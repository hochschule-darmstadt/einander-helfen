import Tag from '@/models/tag';

export interface SearchBarState {
  searchProposals: Array<{header: string}|{divider: boolean}|Tag>;
  labels: string[];
  synonyms: string[];
  searchValues: string[];
  selectedTag: string;
}
