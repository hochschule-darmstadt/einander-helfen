import axios from 'axios';
import QueryBuilder, { QueryObject } from 'es-query-builder/dist';

class DataService {
    private baseUrl = 'https://cai-einander-helfen.fbi.h-da.de/api/_search/';

    public findById<T>(id: string): Promise<T> {
        const queryData = new QueryBuilder()
            .mustTerm('_id', id);
        return this.performQuery<T>(queryData);
    }

    public findByCategories<T>(categories: string[]): Promise<T> {
        const queryData = new QueryBuilder();
        // TODO
        categories.forEach((category) => {
            queryData.shouldWildcard('categories', `${category}`);
        });
        return this.performQuery<T>(queryData);
    }

    public findByTitle<T>(title: string): Promise<T> {
        const queryData = new QueryBuilder()
            // TODO Matching both if string contains the keyword für
            .mustMatch('title', `${title}`);
        return this.performQuery<T>(queryData);
    }

    public findAll<T>(): Promise<T> {
        const queryData = new QueryBuilder();
        return this.performQuery<T>(queryData);
    }


    public findByWildcard<T>(title: string, location: string, task: string): Promise<T> {
        const queryData = new QueryBuilder()
            // TODO Matching both if string contains the keyword für
            .shouldWildcard('title', `${title}`)
            .shouldWildcard('location', `${location}`)
            .shouldWildcard('task', `${task}`);
        return this.performQuery<T>(queryData);
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
