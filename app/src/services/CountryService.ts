/**
 * This service provides the countries of the database with Elastic Search queries.
 */

import axios from "axios";
import Location from "@/models/location";
import Bodybuilder from "bodybuilder";

class CountryService {
  public countries: Location[] = [];
  private baseUrl = process.env.VUE_APP_SEARCH_URI;

  /**
   * The constructor initializes the `country` list.
   */
  constructor() {
    this.findCountries();
  }

  /**
   * This query finds all unique countries.
   * @return The elasticsearch querystring
   */
  private createQuery(): any {
    return Bodybuilder()
      .size(0)
      .agg(
        "terms",
        "post_struct.location.country.keyword",
        { size: 1000 },
        "country"
      )
      .build();
  }

  /**
   * This method performs the elasticsearch query
   */
  private async findCountries(): Promise<any> {
    const query = this.createQuery();

    const { data } = await axios.post(this.baseUrl, query);

    return data.aggregations.country.buckets.map((elem: any) => {
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
  }
}

const countryServiceInstance = new CountryService();

export default countryServiceInstance;
