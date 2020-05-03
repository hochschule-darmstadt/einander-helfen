import axiosConstructor, {AxiosInstance} from 'axios';

class API {

    constructor(private axios: AxiosInstance) {
        this.axios = axios;
    }

    public list<T>(resource: string, options: object): Promise<PaginatedResponse<T>> {
        return new Promise<PaginatedResponse<T>>((resolve, reject) => {
            this.axios.get(resource + '?' + this.buildQueryString(options)).then((data) => {
                resolve(data.data);
            });
        });
    }

    public get<T>(resource: string, options: object): Promise<T> {
        return new Promise<T>((resolve, reject) => {
            this.axios.get(resource + '?' + this.buildQueryString(options)).then(({data}) => {
                return resolve(data.data);
            });
        });
    }


    private buildQueryString(options: object): string {
        // @ts-ignore
        return Object.keys(options).map((key) => key + '=' + options[key]).join('&');
    }

}

interface PaginatedResponse<T> {
    data: T[];
    links: {
        first: URL,
        last: URL,
        prev: URL,
        next: URL
    };
    meta: {
        current_page: number,
        from: number,
        last_page: number,
        path: URL,
        per_page: number,
        to: number,
        total: number
    };
}

const apiInstance = new API(axiosConstructor.create({
    baseURL: 'https://einander-helfen.de/api/'
}));


export default apiInstance;

export {
    apiInstance as API,
    PaginatedResponse
};

