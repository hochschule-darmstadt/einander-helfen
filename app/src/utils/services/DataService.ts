import axios from 'axios';
import QueryBuilder, {QueryObject} from 'es-query-builder';
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
    location: Location|null;
    radius: string;
    from: number;
    size: number;
    international: boolean;
}

class DataService {
    private baseUrl = searchURI;

    public findBySelection(params: SearchParameters): Promise<PaginatedResponse<Post>> {
        const {
            searchValues,
            size,
            from,
            international
        } = params;

        const query = new QueryBuilder();
        query.from(from);
        query.size(size);

        const queryObject = query.build();

        queryObject.query.bool.must.push({ bool: { should: [] } });

        queryObject.query.bool.must[0].bool.should = searchValues
            .map((value) => value + '*')
            .map((value) => {
                return {
                    query_string: {
                        query: value,
                        fields: ['title', 'categories', 'task']
                    }
                };
            });

        if (international) {
            DataService.findInternationalBySelection(queryObject, params.location);
        } else {
            DataService.findNationalBySelection(queryObject, params.location, params.radius);
        }

        return this.performQuery<Post>(new QueryBuilder(queryObject));
    }

    private static findNationalBySelection(queryObject: QueryObject, location: Location|null, radius: string) : void {
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

        // only national posts
        // @ts-ignore
        queryObject.query.bool.must_not = [{
            'term': {
                'categories': 'international'
            }
        }];
    }

    private static findInternationalBySelection(queryObject: QueryObject, location: Location|null) : void {
        // only international posts (default)
        queryObject.query.bool.must = [{
                'term': {
                    'categories': 'international'
                }
            }
        ];

        if (location) {
            if (location.country && location.country !== 'Deutschland') {
                queryObject.query.bool.must.push({
                    match: {
                        'post_struct.location.country': location.country
                    }
                });
            }
        }
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

