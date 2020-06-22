import Tag from '@/models/tag';

export interface TextSearchState {
  searchProposals: Array<{header: string}|{divider: boolean}|Tag>;
  labels: string[];
  synonyms: string[];
  searchValues: string[];
  selectedTag: string;
}
