/**
 * This service provides the methods to find posts in the database.
 */

import axios from "axios";
import Location from "@/models/location";
import Post from "@/models/post";
import BuilderFactory, { Bodybuilder } from "bodybuilder";

export interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    size: number;
  };
}

export interface SearchParameters {
  searchValues: string[];
  location?: Location;
  radius?: string;
  from: number;
  size: number;
  international: boolean;
}

class PostService {
  private baseUrl = process.env.VUE_APP_SEARCH_URI;

  /**
   * Return a paginated list of posts fitting to the @SearchParameters
   *
   * @param params @SearchParameters
   * @return {Promise<PaginatedResponse<Post>>}: The found posts
   */
  public findPosts(params: SearchParameters): Promise<PaginatedResponse<Post>> {
    let builder = BuilderFactory()
      .rawOption("track_total_hits", true)
      .from(params.from)
      .size(params.size)
      .andQuery("bool", (builder) => {
        params.searchValues
          .map((value) => value + "*")
          .map((value) =>
            builder.orQuery("query_string", {
              query: value,
              fields: ["title", "categories", "task"],
            })
          );
        return builder;
      });

    builder = params.international
      ? this.addInternationalFilter(builder, params.location)
      : this.addNationalFilter(builder, params.location, params.radius);

    return this.performPostsQuery<Post>(builder);
  }

  /**
   * Find a post by its ID.
   *
   * @param {string} id: The ID of the post to find.
   * @return {Promise<Post | undefined>}: The matching Post or undefined if no Post was found.
   */
  public findById(id: string): Promise<Post | undefined> {
    const builder = BuilderFactory().query("term", "_id", id);

    return axios.post(this.baseUrl, builder.build()).then(({ data }) => {
      if (!data.hits.hits.length) return undefined;
      const entity = data.hits.hits.pop();
      return {
        id: entity._id,
        ...entity._source,
      } as Post;
    });
  }

  /**
   * Return the number of national or international posts
   *
   * @param {boolean} international: true if international posts are wanted. False if national posts are wanted.
   * @return {Promise<number>}: The number of existing posts
   */
  public countPosts(international: boolean): Promise<number> {
    let builder = BuilderFactory().rawOption("track_total_hits", true);

    builder = international
      ? this.addInternationalFilter(builder)
      : this.addNationalFilter(builder);

    return this.performCountQuery(builder);
  }

  /**
   * Add a filter to only retrieve national posts.
   *
   * @param {Bodybuilder} builder: Builder for elastic search queries to add the filter to.
   * @param {Location} location: Location of the search.
   * @param {string} radius: Radius of the search.
   * @return {Bodybuilder}: The @Bodybuilder with the new filter.
   */
  private addNationalFilter(
    builder: Bodybuilder,
    location: Location | undefined = undefined,
    radius: string | undefined = undefined
  ): Bodybuilder {
    // only national posts
    builder = builder.notQuery("term", "categories", "international");

    if (location) {
      builder = builder.sort([
        {
          _geo_distance: {
            geo_location: {
              lat: location.lat,
              lon: location.lon,
            },
            order: "asc",
            unit: "km",
            mode: "min",
            distance_type: "arc",
            ignore_unmapped: true,
          },
        },
      ]);
    }

    if (location && radius) {
      builder = builder.filter("geo_distance", {
        distance: radius,
        geo_location: {
          lat: location.lat,
          lon: location.lon,
        },
      });
    }

    return builder;
  }

  /**
   * Add a filter to only retrieve international posts.
   *
   * @param {Bodybuilder} builder: Builder for elastic search queries to add the filter to.
   * @param {Location} location: Location of the search.
   * @return {Bodybuilder}: The @Bodybuilder with the new filter.
   */
  private addInternationalFilter(
    builder: Bodybuilder,
    location: Location | undefined = undefined
  ): Bodybuilder {
    // only international posts (default)
    builder = builder.andQuery("term", "categories", "international");

    if (location) {
      if (location.country && location.country !== "Deutschland") {
        builder = builder.andQuery(
          "match",
          "post_struct.location.country.keyword",
          location.country
        );
      }
    }

    return builder;
  }

  private performPostsQuery<T>(
    query: Bodybuilder
  ): Promise<PaginatedResponse<T>> {
    return axios.post(this.baseUrl, query.build()).then(({ data }) => {
      const entities: T[] = data.hits.hits.map((elem: any) => {
        return {
          id: elem._id,
          ...elem._source,
        };
      });

      const response: PaginatedResponse<T> = {
        data: entities,
        meta: {
          total: data.hits.total.value,
          size: entities.length,
        },
      };
      return response;
    });
  }

  private performCountQuery(query: Bodybuilder): Promise<number> {
    return axios
      .post(this.baseUrl + "posts/?filter_path=hits.total", query.build())
      .then(({ data }) => {
        const count: number = data.hits.total.value;
        return count;
      });
  }
}

const postServiceInstance = new PostService();

export default postServiceInstance;
