<template>
  <v-btn class="mx-2" fab dark large color="primary" @click="handleSearchEvent">
    <v-icon dark>search</v-icon>
  </v-btn>
</template>

<script lang="ts">
import Vue from 'vue';
import { createNamespacedHelpers, mapActions as mapStateActions } from 'vuex';
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
    ...mapStateActions(['updateURIFromState', 'findPosts']),
    handleSearchEvent(): void {
       {
        this.addSearchValue(this.searchInput);
        this.updateURIFromState();
        this.findPosts();
      }
    }
  }
});
</script>

<style scoped></style>
