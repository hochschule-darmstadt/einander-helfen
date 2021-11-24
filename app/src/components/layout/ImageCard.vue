<template>
  <v-hover v-slot:default="{ hover }">
    <v-card
      class="mx-auto"
      :elevation="hover ? 12 : 2"
      :class="{ 'on-hover': hover }"
    >
      <router-link
        style="text-decoration: none; color: inherit"
        :to="{
          name: 'posts',
          path: card.post.id,
          query: { q: query },
        }"
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
</template>

<script lang="ts">
import Post from "@/models/post";
import Vue from "vue";

export interface Card {
  title: string;
  search: Array<string>;
  img: string;
  post: Post | undefined;
}

export default Vue.extend({
  name: "ImageCard.Vue",
  props: {
    card: {
      type: Object as () => Card,
      required: true,
    },
  },
  computed: {
    query(): string {
      if (this.card.search.length > 1) {
        return "";
      }
      if (this.card.search.length === 1) {
        return this.card.search[0];
      }
      return this.card.search.reduce(
        (previousValue, currentValue) => `${previousValue},${currentValue}`
      );
    },
  },
});
</script>

<style scoped></style>
