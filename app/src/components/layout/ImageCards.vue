<template>
  <v-row justify="center">
    <v-col xs="12" sm="6" md="6" lg="3" v-for="card in cards" :key="card.title">
      <v-hover v-slot:default="{ hover }">
        <v-card
          class="mx-auto"
          :elevation="hover ? 12 : 2"
          :class="{ 'on-hover': hover }"
        >
          <router-link
            style="text-decoration: none; color: inherit"
            :to="{ name: 'posts', query: { q: card.to } }"
          >
            <v-img
              class="white--text align-end mt-10"
              height="300px"
              :key="card.title"
              :src="card.img"
            >
              <v-card class="no-radius">
                <v-card-title
                  class="justify-center black--text"
                  v-html="card.title"
                />
              </v-card>
            </v-img>
          </router-link>
        </v-card>
      </v-hover>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";

export interface Card {
  title: string;
  to: string;
  img: string;
}

export default Vue.extend({
  name: "ImageCard",
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
