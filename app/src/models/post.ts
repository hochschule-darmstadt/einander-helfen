interface Post {
  id: string;
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
  geo_location: {
    lat: number;
    lon: number;
  };
}

export {Post};
export default Post;
