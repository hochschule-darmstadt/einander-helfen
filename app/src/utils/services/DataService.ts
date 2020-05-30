import axios from 'axios';
import QueryBuilder, { QueryObject } from 'es-query-builder';

class DataService {
    private baseUrl = 'https://cai-einander-helfen.fbi.h-da.de/api/_search/';

    public findById<T>(id: string): Promise<T> {
        const queryData = new QueryBuilder()
            .mustTerm('_id', id);
        return this.performQuery<T>(queryData);
    }

    public findByCategories<T>(categories: string): Promise<T> {
        const queryData = new QueryBuilder();
        const categorieArray = categories.split(/(\s+)/).filter( (e) => e.trim().length > 0);
        console.log(categorieArray);
        let catCounter = 1;
        categorieArray.forEach((category) => {
           queryData.shouldWildcard('categories.Cat' + catCounter, `${category}`);
           catCounter = catCounter + 1;
           console.log('categories.Cat' + catCounter);
           console.log(category);
        });
        return this.performQuery<T>(queryData);
    }

    public findByTitle<T>(title: string): Promise<T> {
        const queryData = new QueryBuilder()
            // TODO Matching both if string contains the keyword für
            .mustWildcard('title', `${title}`);
        return this.performQuery<T>(queryData);
    }

    public findAll<T>(): Promise<T> {
        const queryData = new QueryBuilder();
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

