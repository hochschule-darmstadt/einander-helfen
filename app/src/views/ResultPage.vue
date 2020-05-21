<template>
<<<<<<< HEAD

<div class="home">
    <v-row no-gutters>
        <v-col cols="6">
            <div style="height: 525px;overflow:auto">
                <template v-for="(volunteer, i) in volunteers">  
                    <v-card class="mb-3 listItem" tile>
                    <v-list-item three-line @click="isMap = false; volNum = i;">
=======
    <v-row no-gutters>
        <v-col cols="6">
            <template v-for="(volunteer, i) in volunteers">
                <v-card class="mb-3" tile>
                    <v-list-item three-line>
>>>>>>> 325cca51d0cb6366aae66c99f7773bbd78e6b77b
                        <v-list-item-content>
                            <v-list-item-title class="headline mb-1">{{volunteer.title}}</v-list-item-title>
                            <v-list-item-subtitle>{{volunteer.task}}</v-list-item-subtitle>
                        </v-list-item-content>
<<<<<<< HEAD
                        <v-img max-width="80px" height="80px" contain :src="volunteer.image"></v-img>
                    </v-list-item>
                    </v-card>
                </template>
            </div>
            <!--pageination-->
          <div class="text-center" style="margin-top:2%">
            <v-pagination
=======

                        <v-img max-width="80px" height="80px" contain :src="volunteer.image"></v-img>
                    </v-list-item>
                </v-card>
            </template>
            <div class="text-center">
                <v-pagination
>>>>>>> 325cca51d0cb6366aae66c99f7773bbd78e6b77b
                    v-model="page"
                    :length="6"
                    :total-visible="5"
                    circle
                ></v-pagination>
            </div>
<<<<<<< HEAD
       </v-col>


        <v-col cols="6" v-if="isMap">
            <v-card tile height='66%' width="48%" style="position: absolute" >
                <v-img src="https://media.wired.com/photos/59269cd37034dc5f91bec0f1/master/pass/GoogleMapTA.jpg"  height="100%" width="100%"></v-img>
            </v-card>
        </v-col>
            <v-col cols="6" v-if="!isMap">
                <v-card tile height='66%' width="48%" style="position: absolute;overflow:auto">
                    <v-list-item three-line >
                        <v-btn class="mr-3" text @click="isMap = !isMap">
                            <v-icon>arrow_back</v-icon>
                        </v-btn>
                    <!--display title, subtitle and image on the left side-->
                        <v-list-item-content style="margin-top:2%"> 
                            <v-list-item-title  class="headline mb-1">{{volunteers[volNum].title}}</v-list-item-title>
                            <v-list-item-subtitle>{{volunteers[volNum].task}}</v-list-item-subtitle>
                        </v-list-item-content >

                        <v-img style="margin-top:2%" max-width="80px" height="80px" contain :src="volunteers[volNum].image"></v-img>
                    </v-list-item>

                    <!--display content on the right side-->
                    <v-card-text style="padding-left:5%; padding-right:5%">
                        <v-row>
                            <v-col cols="2">Einsatzort</v-col>
                            <v-col cols="8">{{volunteers[volNum].location}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">Zielgruppe</v-col>
                            <v-col cols="8">{{volunteers[volNum].target_group}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">Einstiegsdatum / Beginn</v-col>
                            <v-col cols="8">{{volunteers[volNum].timing}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">Zeitaufwand</v-col>
                            <v-col cols="8">{{volunteers[volNum].effort}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">Möglichkeiten</v-col>
                            <v-col cols="8">{{volunteers[volNum].opportunities}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">Organisation</v-col>
                            <v-col cols="8">{{volunteers[volNum].organization}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">Kontakt</v-col>
                            <v-col cols="8">{{volunteers[volNum].contact}}</v-col>
                        </v-row>
                    </v-card-text>

                    <v-card-actions>
                        <v-col>
                            <v-container style="margin-bottom: 10px">
                                <template v-for="(category, i) in volunteers[0].categories">
                                    <v-chip :key="i" class="mr-2">{{ category }}</v-chip>
                                </template>
                            </v-container>
                            <v-spacer></v-spacer>
                            <v-container style="display:flex;justify-content:center;">
                                <v-btn class="my-2" dark large color="#F29472" :href="volunteers[volNum].link" target="_blank" >
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
<script>
    export default {
        data: () => ({
            isMap: true,
            volNum: 0,
=======
        </v-col>

        <v-col cols="6" v-if="isMap">
            <v-card tile height='100%' width="100%" style="position: absolute">
                <v-img src="https://media.wired.com/photos/59269cd37034dc5f91bec0f1/master/pass/GoogleMapTA.jpg" width="50%" height="100%"></v-img>
            </v-card>
        </v-col>
        <v-col cols="6" v-if="!isMap">
            <v-card tile height='100%' width="50%" style="position: absolute">
                <v-list-item three-line>
                    <v-btn class="mr-3" text @click="isMap = !isMap">
                        <v-icon>arrow_back</v-icon>
                    </v-btn>
                    <v-list-item-content>
                        <v-list-item-title class="headline mb-1">{{volunteers[0].title}}</v-list-item-title>
                        <v-list-item-subtitle>{{volunteers[0].task}}</v-list-item-subtitle>
                    </v-list-item-content>

                    <v-img max-width="80px" height="80px" contain :src="volunteers[0].image"></v-img>
                </v-list-item>

                <v-card-text>
                    <v-row>
                        <v-col cols="2">Einsatzort</v-col>
                        <v-col cols="8">{{volunteers[0].location}}</v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="2">Zielgruppe</v-col>
                        <v-col cols="8">{{volunteers[0].target_group}}</v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="2">Einstiegsdatum / Beginn</v-col>
                        <v-col cols="8">{{volunteers[0].timing}}</v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="2">Zeitaufwand</v-col>
                        <v-col cols="8">{{volunteers[0].effort}}</v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="2">Möglichkeiten</v-col>
                        <v-col cols="8">{{volunteers[0].opportunities}}</v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="2">Organisation</v-col>
                        <v-col cols="8">{{volunteers[0].organization}}</v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="2">Kontakt</v-col>
                        <v-col cols="8">{{volunteers[0].contact}}</v-col>
                    </v-row>
                </v-card-text>

                <v-card-actions>
                    <v-col cols="10">
                        <template v-for="(category, i) in volunteers[0].categories">
                            <v-chip :key="i" class="mr-2">{{ category }}</v-chip>
                        </template>

                        <v-spacer></v-spacer>

                        <v-btn class="mr-4" fab dark large color="#F29472">
                            <v-icon dark>arrow_forward</v-icon>
                        </v-btn>
                    </v-col>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
    export default {
        data: () => ({
            isMap: false,
>>>>>>> 325cca51d0cb6366aae66c99f7773bbd78e6b77b
            volunteers: [
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
<<<<<<< HEAD
                    link: 'https://www.ehrenamtssuche-hessen.de/',
=======
                    link: '',
>>>>>>> 325cca51d0cb6366aae66c99f7773bbd78e6b77b
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
<<<<<<< HEAD
                    timing: '28.06.2020',
                    effort: '2 Tage pro Woche',
=======
                    timing: '25.05.2020',
                    effort: '1 Tag pro Woche',
>>>>>>> 325cca51d0cb6366aae66c99f7773bbd78e6b77b
                    opportunities: 'Wir bieten Einkaufen zu gehen',
                    organization: 'ASB Regionalverband, Frankfurt am Main, 069-314072-13, 65929, -, ' +
                        'breitenausbildung@asb-frankfurt.de',
                    contact: 'Heinz Müller, Frankfurt am Main, 069-314072-13, 65929, -, breitenausbildung@asb-frankfurt.de',
<<<<<<< HEAD
                    link: 'https://ehrenamt.bund.de/',
=======
                    link: '',
>>>>>>> 325cca51d0cb6366aae66c99f7773bbd78e6b77b
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
<<<<<<< HEAD
                    timing: '26.06.2020',
                    effort: '5 Tage pro Woche',
=======
                    timing: '25.05.2020',
                    effort: '1 Tag pro Woche',
>>>>>>> 325cca51d0cb6366aae66c99f7773bbd78e6b77b
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
            ]
        }),
    };
<<<<<<< HEAD

</script>


=======
</script>

>>>>>>> 325cca51d0cb6366aae66c99f7773bbd78e6b77b
<style scoped>

</style>