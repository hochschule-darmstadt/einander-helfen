<template>
  <div class="home">
    <v-img
      dark
      max-height="30vh"
      src="https://images.unsplash.com/photo-1581093581417-60b6c94a7945?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1951&q=80"
    ></v-img>

  <v-container>
    <v-form class="mt-12 mb-12">
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-autocomplete filled rounded color="white" label="z.B. MacherIn" append-icon="search" :items="volunteerTags"></v-autocomplete>
        </v-col>
      </v-row>

      <v-row justify="center">
        <v-col cols="12" md="6">
          <v-autocomplete label="Standort" :items="cities" v-model="cities[0]" prepend-inner-icon="place">Mein Standort</v-autocomplete>
        </v-col>

        <v-col cols="12" md="2">
          <v-autocomplete label="Umkreis" :items="kms" v-model="kms[0]">Überall</v-autocomplete>
        </v-col>
      </v-row>
    </v-form>

    <v-row justify="center">
      <template v-for="(tag, i) in volunteerTags">
        <v-col cols="12" md="2" :key="i">
          <v-card height="20vh">
            <v-card-title>
              {{ tag }}
            </v-card-title>
          </v-card>
        </v-col>
      </template>
    </v-row>
  </v-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
export default {
  data: () => ({
    kms: ['Überall', '5 km', '10 km', '25 km', '50 km'],
    volunteerTags: [
      'MacherIn',
      'DenkerIn',
      'Jugend Arbeit',
      'Soziales'
    ],
    cities: [
      'Main Standort',
      'Darmstadt',
      'Frankfurt am Main',
      'Wiesbaden',
      'Mainz'
    ],
  })
};
</script>
