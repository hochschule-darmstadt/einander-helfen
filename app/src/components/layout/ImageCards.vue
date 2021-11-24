<template>
  <v-row justify="center">
    <v-col xs="12" sm="6" md="6" lg="3" v-for="card in cards" :key="card.title">
      <ImageCard :card="card"></ImageCard>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import ImageCard, { Card } from "@/components/layout/ImageCard.vue";

export default Vue.extend({
  name: "ImageCards",
  components: {
    ImageCard,
  },
  props: {
    cards: {
      type: Array as () => Card[],
      required: true,
    },
  },
});
</script>

<style lang="scss" scoped></style>
