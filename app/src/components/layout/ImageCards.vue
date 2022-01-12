<template>
  <div>
    <v-row justify="center" style="text-align: center" class="pb-5 pt-10">
      <h1 style="font-size: 2.5em; color: rgb(47, 54, 64)">
        Freiwilligenarbeit in vielen Bereichen!
      </h1>
    </v-row>

    <v-row justify="center">
      <v-col
        xs="12"
        sm="6"
        md="6"
        lg="3"
        v-for="card in cards"
        :key="card.title"
      >
        <ImageCard :card="card"></ImageCard>
      </v-col>
    </v-row>
  </div>
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

<style lang="scss" scoped>
.mx-auto {
  .v-image {
    border-radius: 4px;
  }
}
</style>
