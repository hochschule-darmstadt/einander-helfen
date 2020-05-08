<template>
  <v-container>
    <v-form class="mt-12">
      <v-col cols="12">
        <v-row justify="center">
          <v-col cols="12" md="4">
            <v-text-field
              label="Suche nach einer passenden Tätigkeit..."
              prepend-inner-icon="mdi-magnify"
              filled
              rounded
              dense
              flat
            ></v-text-field>
          </v-col>
        </v-row>
      </v-col>

      <v-col cols="12">
        <v-row justify="center">
          <v-col cols="6" md="2">
            <v-text-field label="Standort" prepend-inner-icon="mdi-map-marker"></v-text-field>
          </v-col>

          <v-col cols="6" md="2">
            <v-select :items="kms" label="Umkreis"></v-select>
          </v-col>
        </v-row>
      </v-col>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
export default {
  data: () => ({
    kms: ['5 km', '10 km', '25 km', '50 km']
  })
};
</script>
