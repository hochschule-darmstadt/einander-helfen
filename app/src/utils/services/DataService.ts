import axios from 'axios';
import QueryBuilder, { QueryObject } from 'es-query-builder';
import Location from '@/models/location';

class DataService {
    private baseUrl = searchURI;

    public findById<T>(id: string): Promise<T> {
        const queryData = new QueryBuilder()
            .mustTerm('_id', id);
        return this.performQuery<T>(queryData);
    }

    public findByCategory<T>(category: string): Promise<T> {
        const queryData = new QueryBuilder()
            .mustMatch('categories', `${category}`);
        return this.performQuery<T>(queryData);
    }

    public findByTitle<T>(title: string): Promise<T> {
        const queryData = new QueryBuilder()
            // TODO Matching both if string contains the keyword für
            .mustWildcard('title', `${title}`);
        return this.performQuery<T>(queryData);
    }

    public findByWildcard<T>(object: string): Promise<T> {
        const queryData = new QueryBuilder()
            // TODO Matching both if string contains the keyword für
            .size(15)
            .shouldWildcard('title', `${object}`)
            .shouldMatch('categories', `${object}`)
            .shouldWildcard('organization', `${object.toLowerCase()}`);
        return this.performQuery<T>(queryData);
    }

    public findAll<T>(): Promise<T> {
        const queryData = new QueryBuilder();
        return this.performQuery<T>(queryData);
    }

    public findBySelection({searchValues,
                               location,
                               radius
                            }: {searchValues: string[],
                                location: Location|undefined,
                                radius: string
                            }): Promise<any> {
        const query = new QueryBuilder();
        query.mustShouldMatch(searchValues.map((value) => [{key: 'title', value}, {key: 'categories', value}]).flat());

        query.size(100);
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

        return this.performQuery(new QueryBuilder(queryObject));
    }

    private performQuery<T>(query: QueryBuilder): Promise<T> {
        return new Promise<T>((resolve, reject) => {
            axios.post(this.baseUrl, query.build())
                    .then(({ data }) => {
                    resolve(data.hits.hits.map((elem: any) => {
                        return {
                            id: elem._id,
                            ...elem._source
                        };
                    }));
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

