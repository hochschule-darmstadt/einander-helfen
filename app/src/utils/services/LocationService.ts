import Location from '@/models/location';
import locationArray from '@/resources/locations/index';
import CountryService from "@/utils/services/CountryService";

class LocationService {
    public locations: Location[] = [];
    public countries: Location[] = [];
    public selectedLocationAmount = 10;
    public diversityValue = 5;

    /**
     * The constructor initializes the `Location` list.
     */
    constructor() {
        this.loadLocationCsv();
        this.countries = CountryService.countries;
    }

    /**
     * This method finds a specified location by the title.
     * @param title The title of the searched location.
     */
    public findByTitle(title: string): Location|undefined {
        return this.locations.find((location) => location.title === title);
    }

    /**
     * This method executes a query on the locations specified by a string.
     * If there is no input an empty array is returned.
     * Otherwise it searches for `Location`s where the name or plz starts with the input string.
     * @param searchValue   The input string for the query.
     * @returns A list of the top `this.selectedLocationAmount` `Location`s
     *          which have a diversity of `this.diversityValue` ordered by rank and name.
     */
    public findLocationByPlzOrName(searchValue: string): Location[] {
        // return empty on null
        if (!searchValue) {
            return [];
        }

        // get locations which start with the searchValue string
        const selectedLocations = [] as Location[];
        this.locations.forEach((location) => {
            if (location.title === searchValue ||
                location.name.toLowerCase().startsWith(searchValue.toLowerCase()) ||
                location.plz.startsWith(searchValue)) {
                selectedLocations.push(location);
            }
        });
        selectedLocations.sort(this.dynamicSort('-rank'));

        return this.diversitySplice(selectedLocations);
    }

    /**
     * This method executes a query on the countries specified by a string.
     * If there is no input an empty array is returned.
     * Otherwise it searches for countries where the name starts with the input string.
     * @param searchValue   The input string for the query.
     * @returns A list of the top `this.selectedLocationAmount` `Location`s
     *          which have a diversity of `this.diversityValue` ordered by country.
     */
    public findCountryByName(searchValue: string): Location[] {
        // return empty on null
        if (!searchValue) {
            return [];
        }

        // get countries which start with the searchValue string
        const selectedCounties = [] as Location[];

        this.countries.forEach((location) => {
            if (location.country.toLowerCase().startsWith(searchValue.toLowerCase())) {
                selectedCounties.push(location);
            }
        });

        selectedCounties.sort(this.dynamicSort('country'));

        return this.diversitySplice(selectedCounties);
    }

    /**
     * This method executes a wildcard query on the locations.
     * @returns A list of the top `this.selectedLocationAmount` `Location`s
     *          which have a diversity of `this.diversityValue` ordered by rank and name.
     */
    private findLocationWildcard(): Location[] {
        const selectedLocations = [] as Location[];
        this.locations.forEach((location) => {
            selectedLocations.push(location);
        });
        selectedLocations.sort(this.dynamicSort('-rank'));

        return this.diversitySplice(selectedLocations);
    }

    /**
     * This method helps to sort any list of object by a specific property.
     * The method needs to be call inside of a `<T>.sort(dynamicSort('abc'))` method.
     * @param property  The property the object should be sorted by.
     *                  If the property starts with '-' the result is inversed.
     * @returns A number between -1 - 1:
     *          - -1:   b comes before a.
     *          - 0:    a and b are equal.
     *          - 1:    a comes before b.
     */
    private dynamicSort(property): any {
        let sortOrder = 1;
        if (property[0] === '-') {
            sortOrder = -1;
            property = property.substr(1);
        }
        return (a, b) => {
            return (a[property] < b[property] ? -1 :
                (a[property] > b[property]) ? 1 : 0)
                * sortOrder;
        };
    }

    /**
     * This method creates a subset of a `Location` array.
     * The subset has the size of `this.selectedLocationAmount` and
     * contains a maximum of `this.diversityValue` `Location`s with the same name.
     * @param locations Array of `Location`s
     * @returns The subset of `Location`s
     */
    private diversitySplice(locations: Location[]): Location[] {
        if (!locations || locations.length === 0) {
            return [];
        }
        if (locations.length < this.selectedLocationAmount) {
            return locations;
        }

        // add locations only if they do not exceed the diversity value
        const diverseLocations = [] as Location[];
        let newSize = this.selectedLocationAmount;
        const unusedIndices = [] as number [];
        for (let i = 0; i < newSize && i < locations.length; i++) {
            if (this.diversityNameOccurrence(diverseLocations, locations[i].name) < this.diversityValue) {
                diverseLocations.push(locations[i]);
            } else {
                unusedIndices.push(i);
                newSize++;
            }
        }

        // if the diverse locations have free space, add unused diverse locations
        const fillEmptySpace = this.selectedLocationAmount - diverseLocations.length;
        if (fillEmptySpace > 0 && unusedIndices.length > 0) {
            for (let i = 0; i < fillEmptySpace && i < unusedIndices.length; i++) {
                diverseLocations.push(locations[unusedIndices[i]]);
            }
        }

        return diverseLocations;
    }

    /**
     * This method counts the occurrence of a name in a location array.
     * @param locations Array of `Location`s
     * @param name      Name of a `Location`
     * @returns The number of how many `Location`s in `locations` have the name `name`.
     */
    private diversityNameOccurrence(locations: Location[], name): number {
        let count = 0;
        locations.forEach((v) => (v.name === name && count++));
        return count;
    }

    /**
     * This method loads a CSV file and stores the content as `Location` in locations.
     */
    private loadLocationCsv(): void {
        locationArray.forEach((location) => {
            this.locations.push({
                name: location.name,
                plz: location.plz,
                state: location.state,
                lat: +location.lat,
                lon: +location.lon,
                rank: +location.rank,
                title: location.plz + ' ' + location.name,
                country: 'Deutschland'
            });
        });
    }
}

const locationServiceInstance = new LocationService();

export default locationServiceInstance;

export {
    locationServiceInstance as LocationService,
};
