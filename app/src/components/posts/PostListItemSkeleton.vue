<template>
  <v-card class="post mb-3">
    <v-skeleton-loader
      v-bind="$attrs"
      type="card-heading,  list-item-two-line"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "PostListItemSkeleton",
});
</script>
