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
              :items="volunteerTags"
            ></v-autocomplete>
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-col cols="12" md="6">
            <v-autocomplete
              label="Standort"
              :items="cities"
              v-model="cities[0]"
              prepend-inner-icon="place"
            >Mein Standort</v-autocomplete>
          </v-col>

          <v-col cols="12" md="2">
            <v-autocomplete label="Umkreis" :items="kms" v-model="kms[0]">Überall</v-autocomplete>
          </v-col>
        </v-row>
      </v-form>

      <v-row justify="center">
        <template v-for="(item, i) in volunteerTags">
          <v-col cols="12" md="2" :key="i">
            <v-card height="200px" class="mx-auto">
              <v-img class="white--text align-end" height="200px" :key="i" :src="item.img">
                <v-card-title>{{ item.title }}</v-card-title>
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
export default {
  data: () => ({
    kms: ['Überall', '5 km', '10 km', '25 km', '50 km'],
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
    cities: [
      'Main Standort',
      'Darmstadt',
      'Frankfurt am Main',
      'Wiesbaden',
      'Mainz'
    ]
  })
};
</script>
