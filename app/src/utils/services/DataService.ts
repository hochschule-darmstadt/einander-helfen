import axios from 'axios';
import QueryBuilder, { QueryObject } from 'es-query-builder';

class DataService {
    private baseUrl = 'https://cai-einander-helfen.fbi.h-da.de/api/_search/';

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

    public findBySelection({searchValues, location, radius}:
                               {searchValues: string[], location: string, radius: string}): Promise<any> {
        const query = new QueryBuilder();
        searchValues.forEach((value) => {
            query.shouldMatch('categories', value)
                .shouldMatch('title', value)
                .size(100);
        });

        const queryObject = query.build();
        // @ts-ignore
        // queryObject.query.bool.filter = {
        //     geo_distance: {
        //         distance: "50km",
        //         posts: {
        //             lat: 49.878708,
        //             lon: 8.646927
        //         }
        //     }
        // };

        return this.performQuery(new QueryBuilder(queryObject));
    }

    private performQuery<T>(query: QueryBuilder): Promise<T> {
        return new Promise<T>((resolve, reject) => {
            axios.post(this.baseUrl, query.build())
                .then(({ data }) => { resolve(data.hits.hits.map((elem: any) => elem._source)); })
                .catch((error) => reject(error));
        });
    }
}

const dataServiceInstance = new DataService();

export default dataServiceInstance;

export {
    dataServiceInstance as DataService,
};

