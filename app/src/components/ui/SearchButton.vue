<template>
  <v-btn icon outlined fab color="#00254f" @click="handleSearchEvent">
    <v-icon>search</v-icon>
  </v-btn>
</template>

<script lang="ts">
import Vue from 'vue';
import { createNamespacedHelpers, mapActions } from 'vuex';
const { mapMutations } = createNamespacedHelpers('textSearchModule');

export default Vue.extend({
  props: {
    searchInput: String
  },
  data(): {
    mySearchValue: string
  } {
    return {
      mySearchValue: this.searchInput || ''
    };
  },
  watch: {
    mySearchValue(value): void {
      this.$emit('update:searchInput', value);
    }
  },
  methods: {
    ...mapMutations(['addSearchValue']),
    ...mapActions(['updateURIFromState']),
    handleSearchEvent(): void {
       {
        this.addSearchValue(this.searchInput);
        this.updateURIFromState();
      }
    }
  }
});
</script>

<style scoped></style>
