<template>
  <v-container class="text-center" fill-height style="height: calc(70vh - 58px);">
    <v-row align="center">
      <v-col>
        <h1 class="display-3 indigo--text">Offers Page</h1>
        <h3 class="indigo--text">You searched for: {{$route.params.category}}</h3>
      </v-col>
    </v-row>
  </v-container>
</template>