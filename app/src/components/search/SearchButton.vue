<!-- Button inside of the SearchComponent to start the search. -->

<template>
  <v-btn class="mx-2" fab large color="primary" @click="$emit('click')">
    <v-icon>search</v-icon>
  </v-btn>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({});
</script>
