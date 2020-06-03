interface Advertisement {
  title: string;
  categories: string[];
  location: string;
  task: string;
  target_group: string;
  timing: string;
  effort: string;
  opportunities: string;
  organization: string;
  contact: string;
  link: string;
  image: string;
  map_address: [];
  lat: number;
  lon: number;
}

export {Advertisement};
export default Advertisement;
