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
  private baseUrl = searchURI;

  public findBySelection(params: SearchParameters): Promise<PaginatedResponse<Post>> {

    const builder = BuilderFactory()
      .from(params.from)
      .size(params.size)

      .andQuery("bool", (builder) => {
        params.searchValues
          .map((value) => value + "*")
          .map((value) =>
            builder.orQuery("query_string",
              {
                query: value,
                fields: ["title", "categories", "task"]
              },
            )
          )
        return builder;
      })

    const complete_builder = params.international ?
      this.findInternationalBySelection(builder, params.location) :
      this.findNationalBySelection(builder, params.location, params.radius);

    return this.performQuery<Post>(complete_builder);
  }


  public findById(id: string): Promise<Post | undefined> {
    const builder = BuilderFactory()
      .query('term', "_id", id);

    return axios
      .post(this.baseUrl, builder.build())
      .then(({ data }) => {
        if (!data.hits.hits.length) return undefined;
        const entity = data.hits.hits.pop();
        return {
          id: entity._id,
          ...entity._source,
        } as Post;
      });
  }

  private findNationalBySelection(
    builder: Bodybuilder,
    location: Location | undefined,
    radius: string | undefined
  ): Bodybuilder {
    if (location) {
      builder = builder.sort([{
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
      }]);
    }

    if (location && radius) {
      builder = builder.filter("bool", "geo_distance",
        {
          distance: radius,
          geo_location: {
            lat: location.lat,
            lon: location.lon,
          },
        },
      );
    }

    // only national posts
    builder = builder.notQuery("term", "categories", "international");
    return builder;
  }

  private findInternationalBySelection(
    builder: Bodybuilder,
    location: Location | undefined
  ): Bodybuilder {
    // only international posts (default)
    builder = builder.andQuery("term", "categories", "international");

    if (location) {
      if (location.country && location.country !== "Deutschland") {
        builder = builder.andQuery("match", "post_struct.location.country", location.country);
      }
    }
    return builder;
  }

  private performQuery<T>(query: Bodybuilder): Promise<PaginatedResponse<T>> {
    return axios
      .post(this.baseUrl, query.build())
      .then(({ data }) => {
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
      })
  }
}

const serviceInstance = new PostService();

export default serviceInstance;
