<template>
    <div>
        <Header />
        <v-row no-gutters>
            <v-col cols="6">
                <div style="height:75vh;overflow:auto">
                    <template v-for="(advertisement, i) in visiblePages">
                        <v-card class="mb-3" tile>
                            <v-list-item three-line @click="openAdvertisement(i)">
                                <v-list-item-content>
                                    <v-list-item-title class="headline mb-1">{{advertisement.title}}</v-list-item-title>
                                    <v-list-item-subtitle>{{advertisement.task}}</v-list-item-subtitle>
                                </v-list-item-content>

                                <v-img max-width="80px" height="80px" contain :src="advertisement.image"></v-img>
                            </v-list-item>
                        </v-card>
                    </template>
                </div>
                <!--pageination-->
                <div class="text-center" style="margin-top:2%">
                    <v-pagination
                            color="#054C66"
                            v-model="page"
                            :length="numberOfPages"
                    ></v-pagination>
                </div>
            </v-col>


            <v-col cols="6" v-if="!advertisementIsOpen">
                <v-card tile height='75vh' style="position: absolute">
                    <v-img src="https://media.wired.com/photos/59269cd37034dc5f91bec0f1/master/pass/GoogleMapTA.jpg"
                           height="100%" width="100%"></v-img>
                </v-card>
            </v-col>
            <v-col cols="6" v-if="advertisementIsOpen">
                <v-card tile height='75vh' width="50%" style="position: absolute;overflow:auto">
                    <v-list-item three-line>
                        <v-btn class="mr-3" text @click="closeAdvertisement()">
                            <v-icon>arrow_back</v-icon>
                        </v-btn>
                        <!--display title, subtitle and image on the left side-->
                        <v-list-item-content style="margin-top:2%">
                            <v-list-item-title class="headline mb-1">{{currentAdvertisement.title}}</v-list-item-title>
                            <v-list-item-subtitle>{{currentAdvertisement.task}}</v-list-item-subtitle>
                        </v-list-item-content>

                        <v-img style="margin-top:2%" max-width="80px" height="80px" contain
                               :src="currentAdvertisement.image"></v-img>
                    </v-list-item>

                    <!--display content on the right side-->
                    <v-card-text style="padding-left:5%; padding-right:5%">
                        <v-row>
                            <v-col cols="2">Einsatzort</v-col>
                            <v-col cols="8">{{currentAdvertisement.location}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">Zielgruppe</v-col>
                            <v-col cols="8">{{currentAdvertisement.target_group}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">Einstiegsdatum / Beginn</v-col>
                            <v-col cols="8">{{currentAdvertisement.timing}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">Zeitaufwand</v-col>
                            <v-col cols="8">{{currentAdvertisement.effort}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">Möglichkeiten</v-col>
                            <v-col cols="8">{{currentAdvertisement.opportunities}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">Organisation</v-col>
                            <v-col cols="8">{{currentAdvertisement.organization}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">Kontakt</v-col>
                            <v-col cols="8">{{currentAdvertisement.contact}}</v-col>
                        </v-row>
                    </v-card-text>

                    <v-card-actions>
                        <v-col>
                            <v-container style="margin-bottom: 10px">
                                <template v-for="(category, i) in currentAdvertisement.categories">
                                    <v-chip :key="i" class="mr-2">{{ category }}</v-chip>
                                </template>
                            </v-container>
                            <v-spacer></v-spacer>
                            <v-container style="display:flex;justify-content:center;">
                                <v-btn class="my-2" dark large color="#054C66" :href="currentAdvertisement.link"
                                       target="_blank">
                                    Zum Stellenangebot
                                    <!--<v-icon dark>arrow_forward</v-icon>-->
                                </v-btn>
                            </v-container>
                        </v-col>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>

<!-- test content -->
<script lang="ts">

  import Header from '@/components/layout/Header.vue';

  interface Advertisement {
    title: string;
    categories: string[];
    location: string;
    task: string;
    target_group: string;
    timing: string;
    effort: string;
    opportunities: string;
    organization: string;
    contact: string;
    link: string;
    image: string;
    map_address: [];
    lat: number;
    lon: number;
  }


  import Vue from 'vue';

  export default Vue.extend({
    components: {Header},
    data(): {
      advertisementIsOpen: boolean,
      currentAdvertisementId: number,
      advertisements: Advertisement[],
      page: number,
      perPage: number
    } {
      return {
        advertisementIsOpen: false,
        currentAdvertisementId: 0,
        advertisements: [
          {
            title: 'Einkaufen gehen 1',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: 'https://www.ehrenamtssuche-hessen.de/',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 2',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '28.06.2020',
            effort: '2 Tage pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: 'https://ehrenamt.bund.de/',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 3',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '26.06.2020',
            effort: '5 Tage pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 4',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 5',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 6',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 7',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 8',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 9',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 10',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 11',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 12',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 13',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 14',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
          {
            title: 'Einkaufen gehen 15',
            categories: ['MacherIn', 'DenkerIn'],
            location: 'Hessen, Frankfurt am Main, 65929',
            task: 'Gehe für abc einkaufen',
            target_group: 'Jugendliche',
            timing: '25.05.2020',
            effort: '1 Tag pro Woche',
            opportunities: 'Wir bieten Einkaufen zu gehen',
            organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
              'breitenausbildung@asb-frankfurt.de',
            contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
            link: '',
            image: 'https://www.hessen.de/sites/default/themes/hessen_web_omega/logo.svg',
            map_address: [],
            lat: 12.3,
            lon: 12.3
          },
        ],
        page: 1,
        perPage: 7
      };
    },
    computed: {
      visiblePages(): Advertisement[] {
        return this.advertisements.slice((this.page - 1) * this.perPage, this.page * this.perPage);
      },
      currentAdvertisement(): Advertisement|null {
        return this.advertisementIsOpen
            ? this.advertisements[this.currentAdvertisementId]
            : null;
      },
      numberOfPages(): number {
        return Math.ceil(this.advertisements.length / this.perPage);
      }
    },
    methods: {
      openAdvertisement(index: number): void {
        this.advertisementIsOpen = true;
        this.currentAdvertisementId = index;
      },
      closeAdvertisement(): void {
        this.currentAdvertisementId = 0;
        this.advertisementIsOpen = false;
      }
    }
  });

</script>


<style scoped>

</style>
