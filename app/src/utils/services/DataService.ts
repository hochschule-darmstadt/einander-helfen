import axios from 'axios';
import QueryBuilder from 'es-query-builder';
import Location from '@/models/location';
import Post from '@/models/post';

export interface PaginatedResponse<T> {
    data: T[];
    meta: {
        total: number;
        size: number;
    };
}

export interface SearchParameters {
    searchValues: string[];
    location: Location|undefined;
    radius: string;
    from: number;
    size: number;
}

class DataService {
    private baseUrl = searchURI;

    public findBySelection(params: SearchParameters): Promise<PaginatedResponse<Post>> {
        const {
            searchValues,
            location,
            radius,
            size,
            from
        } = params;

        const query = new QueryBuilder();
        query.mustShouldMatch(searchValues.map((value) => [
                {key: 'title', value},
                {key: 'categories', value},
                {key: 'task', value}
            ]).flat());

        // query.from(from);
        query.size(size);

        const queryObject = query.build();

        if (location) {
            queryObject.sort.push({
                _geo_distance : {
                    geo_location : {
                        lat: location.lat,
                        lon: location.lon
                    },
                    order : 'asc',
                    unit : 'km',
                    mode : 'min',
                    distance_type : 'arc',
                    ignore_unmapped: true
                }
            });
        }

        if (location && radius) {
            // @ts-ignore
            queryObject.query.bool.filter = {
                geo_distance: {
                    distance: radius,
                    geo_location: {
                        lat: location.lat,
                        lon: location.lon
                    }
                }
            };
        }

        return this.performQuery<Post>(new QueryBuilder(queryObject));
    }

    private performQuery<T>(query: QueryBuilder): Promise<PaginatedResponse<T>> {
        return new Promise<PaginatedResponse<T>>((resolve, reject) => {
            axios.post(this.baseUrl, query.build())
              .then(({ data }) => {

                  const entities: T[] = data.hits.hits.map((elem: any) => {
                      return {
                          id: elem._id,
                          ...elem._source
                      };
                  });

                  const response: PaginatedResponse<T> = {
                      data: entities,
                      meta: {
                          total: data.hits.total.value,
                          size: entities.length
                      }
                  };
                  resolve(response);
              })
              .catch((error) => reject(error));
        });
    }
}

const dataServiceInstance = new DataService();

export default dataServiceInstance;

export {
    dataServiceInstance as DataService,
};

