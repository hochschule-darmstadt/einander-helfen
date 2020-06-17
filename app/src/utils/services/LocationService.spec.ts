import { shallowMount } from '@vue/test-utils';
import LocationService from '@/utils/services/LocationService';

describe('LocationService.vue', () => {

    beforeEach(() => {
        LocationService.locations = [
            {
                name: 'Frankfurt',
                plz: '65929',
                title: '65929 Frankfurt',
                state: 'Hessen',
                lat: 1,
                lon: 2,
                rank: 3
            },
            {
                name: 'Darmstadt',
                plz: '64283',
                title: '64283 Darmstadt',
                state: 'Hessen',
                lat: 3,
                lon: 1,
                rank: 2
            },
            {
                name: 'Berlin',
                plz: '10115',
                title: '10115 Berlin',
                state: 'Berlin',
                lat: 2,
                lon: 3,
                rank: 1
            },
            {
                name: 'Berlin',
                plz: '10178',
                title: '10178 Berlin',
                state: 'Berlin',
                lat: 2,
                lon: 3,
                rank: 4
            },
            {
                name: 'Berlin',
                plz: '10247',
                title: '10247 Berlin',
                state: 'Berlin',
                lat: 2,
                lon: 3,
                rank: 5
            },
            {
                name: 'Bochum',
                plz: '44787',
                title: '44787 Bochum',
                state: 'Nordrhein-Westfalen',
                lat: 2,
                lon: 3,
                rank: 6
            }];
        LocationService.selectedLocationAmount = 2;
    });

    it('wildcard query is executed if search value is empty', () => {
        const locationArray = LocationService.findLocationByPlzOrName('');
        expect(locationArray).toEqual([
            {
                name: 'Berlin',
                plz: '10115',
                title: '10115 Berlin',
                state: 'Berlin',
                lat: 2,
                lon: 3,
                rank: 1
            },
            {
                name: 'Darmstadt',
                plz: '64283',
                title: '64283 Darmstadt',
                state: 'Hessen',
                lat: 3,
                lon: 1,
                rank: 2
            }
        ]);
    });
    it('wildcard query is executed if search value is a star', () => {
        const locationArray = LocationService.findLocationByPlzOrName('*');
        expect(locationArray).toEqual([
            {
                name: 'Berlin',
                plz: '10115',
                title: '10115 Berlin',
                state: 'Berlin',
                lat: 2,
                lon: 3,
                rank: 1
            },
            {
                name: 'Darmstadt',
                plz: '64283',
                title: '64283 Darmstadt',
                state: 'Hessen',
                lat: 3,
                lon: 1,
                rank: 2
            }
        ]);
    });
    it('query is executed with first number of plz', () => {
        const locationArray = LocationService.findLocationByPlzOrName('6');
        expect(locationArray).toEqual([
            {
                name: 'Darmstadt',
                plz: '64283',
                title: '64283 Darmstadt',
                state: 'Hessen',
                lat: 3,
                lon: 1,
                rank: 2
            },
            {
                name: 'Frankfurt',
                plz: '65929',
                title: '65929 Frankfurt',
                state: 'Hessen',
                lat: 1,
                lon: 2,
                rank: 3
            }
        ]);
    });
    it('query is executed with wrong first number of plz', () => {
        const locationArray = LocationService.findLocationByPlzOrName('5');
        expect(locationArray).toEqual([]);
    });
    it('query is executed with full plz', () => {
        const locationArray = LocationService.findLocationByPlzOrName('65929');
        expect(locationArray).toEqual([
            {
                name: 'Frankfurt',
                plz: '65929',
                title: '65929 Frankfurt',
                state: 'Hessen',
                lat: 1,
                lon: 2,
                rank: 3
            }
        ]);
    });
    it('query is executed with first letter of name', () => {
        const locationArray = LocationService.findLocationByPlzOrName('B');
        expect(locationArray).toEqual([
            {
                name: 'Berlin',
                plz: '10115',
                title: '10115 Berlin',
                state: 'Berlin',
                lat: 2,
                lon: 3,
                rank: 1
            },
            {
                name: 'Berlin',
                plz: '10178',
                title: '10178 Berlin',
                state: 'Berlin',
                lat: 2,
                lon: 3,
                rank: 4
            }
        ]);
    });
    it('query is executed with wrong first letter of name', () => {
        const locationArray = LocationService.findLocationByPlzOrName('Z');
        expect(locationArray).toEqual([]);
    });
    it('query is executed with full name', () => {
        const locationArray = LocationService.findLocationByPlzOrName('Darmstadt');
        expect(locationArray).toEqual([
            {
                name: 'Darmstadt',
                plz: '64283',
                title: '64283 Darmstadt',
                state: 'Hessen',
                lat: 3,
                lon: 1,
                rank: 2
            }
        ]);
    });
    it('query is executed and uses diversity with overhead', () => {
        LocationService.diversityValue = 1;
        LocationService.selectedLocationAmount = 3;
        const locationArray = LocationService.findLocationByPlzOrName('B');
        expect(locationArray).toEqual([
            {
                name: 'Berlin',
                plz: '10115',
                title: '10115 Berlin',
                state: 'Berlin',
                lat: 2,
                lon: 3,
                rank: 1
            },
            {
                name: 'Bochum',
                plz: '44787',
                title: '44787 Bochum',
                state: 'Nordrhein-Westfalen',
                lat: 2,
                lon: 3,
                rank: 6
            },
            {
                name: 'Berlin',
                plz: '10178',
                title: '10178 Berlin',
                state: 'Berlin',
                lat: 2,
                lon: 3,
                rank: 4
            }
        ]);
    });
    it('query is executed and uses diversity without overhead', () => {
        LocationService.diversityValue = 1;
        LocationService.selectedLocationAmount = 4;
        const locationArray = LocationService.findLocationByPlzOrName('B');
        expect(locationArray).toEqual([
            {
                name: 'Berlin',
                plz: '10115',
                title: '10115 Berlin',
                state: 'Berlin',
                lat: 2,
                lon: 3,
                rank: 1
            },
            {
                name: 'Bochum',
                plz: '44787',
                title: '44787 Bochum',
                state: 'Nordrhein-Westfalen',
                lat: 2,
                lon: 3,
                rank: 6
            },
            {
                name: 'Berlin',
                plz: '10178',
                title: '10178 Berlin',
                state: 'Berlin',
                lat: 2,
                lon: 3,
                rank: 4
            },
            {
                name: 'Berlin',
                plz: '10247',
                title: '10247 Berlin',
                state: 'Berlin',
                lat: 2,
                lon: 3,
                rank: 5
            }
        ]);
    });
});
