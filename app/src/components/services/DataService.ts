import axios from 'axios';
import QueryBuilder from 'es-query-builder/dist';

class DataService {
    private baseUrl = 'http://localhost:8080/api/_search';

    public findById<T>(id: string): Promise<T> {
        return new Promise<T>((resolve, reject) => {
            let log: [];
            axios.get(this.baseUrl + '?q=id:' + id)
                .then((result) => resolve((log = result.data.hits.hits)))
                .catch((error) => reject(error))
                .finally(() => console.log(log));
        });
    }
    private performQuery<T>(query: QueryBuilder): void {
        let entities;
        const req = axios
            .post(
                'http://localhost:8080/api/_search',
                query.build()
            )
            .then(
                (response) =>
                    (entities = response.data.hits.hits.map(
                        (elem: any) => elem._source
                    ))
            )
            .catch((error) => console.log(error));
        // .finally(() => console.log(entities));
    }
}

const dataServiceInstance = new DataService();

export default dataServiceInstance;

export {
    dataServiceInstance as DataService,
};

