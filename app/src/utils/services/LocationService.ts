import Location from '@/models/location';

class LocationService {
    private locations: Location[] = [];

    constructor() {
        for (let i = 0; i < 15; i++) {
            this.locations.push({
                plz: '6502' + i,
                name: 'Frank ' + i,
                lat: i * 3,
                lon: i * 2,
                rank: i % 15
            });
        }
    }

    public findLocationByPlzOrName(searchValue: string): Location[] {



        // TODO
        return this.locations;
    }
}

const locationServiceInstance = new LocationService();

export default locationServiceInstance;

export {
    locationServiceInstance as LocationService,
};
