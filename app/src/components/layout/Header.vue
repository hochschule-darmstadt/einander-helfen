<template>
  <v-header color="grey lighten-4" padless style="margin:10px 10px">
   <!--<v-container style="margin:0px;padding:0px">-->
     <v-row no-gutters>
        <v-btn justify="left" style="margin:0 10px"
          v-for="(link, index) in links"
          :key="index"
          color="grey"
          text
          rounded
          class="my-2"
          router
          :to="link.route"
         >{{ link.text }}</v-btn>
   
        <v-col cols="4" md="4" style=" margin-left:10%; margin-top:1%; margin-right:2%">
          <v-autocomplete
            filled
            rounded
            color="black"
            label="z.B. MacherIn"
            append-icon="search"
            item-text="title"
            :items="volunteerTags"
            v-model="selectedTag"
          ></v-autocomplete>
        </v-col>
         
        <v-col cols="2" md="2" style="margin-top:1%; margin-right:1%; margin-left:1%">
          <v-autocomplete
            label="Standort"
            :items="volunteerCities"
            v-model="selectedCity"
            prepend-inner-icon="place"
          >Mein Standort</v-autocomplete>
        </v-col>

        <v-col  cols="1" md ="1" style="margin-top:1%; margin-right:1%">
          <v-autocomplete
            label="Umkreis"
            :items="volunteerRadius"
             v-model="selectedRadius"
          >Überall</v-autocomplete>
         </v-col> 
        </v-row>
   <!--</v-container>-->
  </v-header>
</template>

<script>
export default {
  data: () => ({
    links: [
      { text: 'Logo', route: '/' },

    ],
        volunteerTags: [
      {
        title: 'Macher/in',
      },
      {
        title: 'Denker/in',
      },
      {
        title: 'Jugendarbeit',
      },
      {
        title: 'Soziales',
      }
    ],
    volunteerCities: [
      'Main Standort',
      'Darmstadt',
      'Frankfurt am Main',
      'Wiesbaden',
      'Mainz'
    ],
    volunteerRadius: ['Überall', '5 km', '10 km', '25 km', '50 km'],
    selectedTag: '',
    selectedCity: '',
    selectedRadius: '',
    dummyData: null
  })
};
</script>