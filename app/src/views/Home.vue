<template>
    <div class="home">
        <v-img
                dark
                max-height="250px"
                :src="require('../../public/images/senior-mother_crop.jpg')"
        ></v-img>

        <v-container>
            <v-form class="mt-12 mb-12">
                <v-row justify="center">
                    <v-col cols="12" md="8">
                        <v-autocomplete
                                filled
                                rounded
                                color="white"
                                label="z.B. MacherIn"
                                append-icon="search"
                                item-text="title"
                                :items="volunteerTags"
                                v-model="selectedTag"
                        ></v-autocomplete>
                    </v-col>
                </v-row>

                <v-row justify="center">
                    <v-col cols="12" md="6">
                        <v-autocomplete
                                label="Standort"
                                :items="volunteerCities"
                                v-model="selectedCity"
                                prepend-inner-icon="place"
                        >Mein Standort
                        </v-autocomplete>
                    </v-col>

                    <v-col cols="12" md="2">
                        <v-autocomplete label="Umkreis" :items="volunteerRadius" v-model="selectedRadius">Überall
                        </v-autocomplete>
                    </v-col>
                </v-row>
            </v-form>

            <v-row justify="center">
                <template v-for="tag in volunteerTags">
                    <v-col cols="12" md="2" :key="tag.title">
                        <v-card height="200px" class="mx-auto">
                            <v-img class="white--text align-end" height="200px" :key="tag.title" :src="tag.img">
                                <v-card-title v-html="tag.title"></v-card-title>
                            </v-img>
                        </v-card>
                    </v-col>
                </template>
            </v-row>
        </v-container>
    </div>
</template>

<script lang="ts">
  declare var require: any;
  import Vue from 'vue';

  import QueryBuilder from 'es-query-builder/dist';
  import axios from 'axios';

  export default Vue.extend({
    data: () => ({
      volunteerTags: [
        {
          title: 'MacherIn',
          img: require('../../public/images/macherIN.jpg')
        },
        {
          title: 'DenkerIN',
          img: require('../../public/images/denkerIN.jpeg')
        },
        {
          title: 'Jugendarbeit',
          img: require('../../public/images/jugend.jpeg')
        },
        {
          title: 'Soziales',
          img: require('../../public/images/sozial.jpeg')
        },
      ],
      volunteerCities: [
        'Main Standort',
        'Darmstadt',
        'Frankfurt am Main',
        'Wiesbaden',
        'Mainz'
      ],
      volunteerRadius: [
        'Überall',
        '5 km',
        '10 km',
        '25 km',
        '50 km'
      ],
      selectedTag: '',
      selectedCity: '',
      selectedRadius: '',
    }),

    created(): void {
      this.findArtworksByLabel('mona');
    },

    methods: {
      performQuery(query: QueryBuilder): void {
        axios.post('https://openartbrowser.org/api/de/_search', query.build()).then((result) => console.log(result));
      },

      findArtworksByLabel(label: string): void {
        const query = new QueryBuilder()
          .size(20)
          .sort()
          .mustMatch('type', 'artwork')
          .shouldMatch('label', `${label}`);
        this.performQuery(query);
      }
    }
  });
</script>
