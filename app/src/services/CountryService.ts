import axios from "axios";
import Location from "@/models/location";

class CountryService {
  public countries: Location[] = [];
  private baseUrl = searchURI;

  /**
   * The constructor initializes the `country` list.
   */
  constructor() {
    this.findCountries();
  }

  /**
   * This method finds all unique countries.
   */
  public findCountries(): void {
    const query = {
      size: 0,
      aggs: {
        country: {
          terms: {
            field: "post_struct.location.country.keyword",
            size: 1000,
          },
        },
      },
    };

    this.performQuery(query);
  }

  /**
   * This method performs the elasticsearch query
   * @param query The elasticsearch querystring
   */
  private performQuery(query: any): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      axios
        .post(this.baseUrl, query)
        .then(({ data }) => {
          data.aggregations.country.buckets.map((elem: any) => {
            if (elem.key !== "Deutschland") {
              this.countries.push({
                name: "",
                plz: "",
                title: elem.key,
                state: "",
                lat: 0,
                lon: 0,
                rank: 0,
                country: elem.key,
              });
            }
          });
        })
        .catch((error) => reject(error));
    });
  }
}

const countryServiceInstance = new CountryService();

export default countryServiceInstance;

export { countryServiceInstance as CountryService };
