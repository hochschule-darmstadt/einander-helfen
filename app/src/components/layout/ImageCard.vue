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
          params: { id: card.post.id },
          query: { q: query },
        }"
      >
        <v-img
          class="white--text align-end mt-10"
          height="300px"
          :key="card.title"
          :src="card.img"
        >
          <v-card
            class="no-radius"
            style="border-bottom-right-radius: 0; border-bottom-left-radius: 0"
          >
            <v-card-title
              style="padding-bottom: 0"
              class="justify-center black--text"
            >
              <h2 style="color: #2f3640" v-html="card.title"></h2>
            </v-card-title>
          </v-card>
        </v-img>
        <v-card-subtitle>
          <h3
            style="padding-bottom: 0.7rem; text-align: center"
            v-html="card.post.title"
          />
          <strong v-html="removeHtmlTags(card.post.location)" />
          <br />
          <span class="text--primary" v-html="makePostShort(card.post.task)" />
        </v-card-subtitle>
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
  data: function () {
    return {
      postLoaded: false,
    };
  },
  methods: {
    makePostShort(post: string): string {
      if (post.length > 400) {
        post = post.replace(/<\/?[^>]+(>|$)/g, "");
        return post.substring(0, 400) + "...";
      }
      return post;
    },
    removeHtmlTags(post: string): string {
      post = post.replace(/<\/?[^>]+(>|$)/g, "");
      post = post.replace("Adresse", "");
      post = post.replace("PLZ:", "");
      post = post.replace("Straße:", "");
      post = post.replace("Ort:", "");
      post = post.replace("Internet:", "");
      return post;
    },
  },
  computed: {
    query(): string {
      console.log(this.card.search);
      if (this.card.search.length < 1) {
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
