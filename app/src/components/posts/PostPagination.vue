<template>
  <div class="pagination-container text-center">
    <v-pagination
      v-model="page"
      :length="totalPages"
      total-visible="7"
      color="#054C66"
    />
    <span class="pl-2 mt-2 d-inline-block font-italic">
      {{ totalResultSize }} Ergebnisse
    </span>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";

export default Vue.extend({
  name: "PostPagination",
  data: function () {
    return {
      page: 1,
    };
  },
  computed: {
    ...mapState("postsModule", ["totalResultSize", "selectedPage"]),
    ...mapGetters("postsModule", ["totalPages"]),
  },
  watch: {
    // update page in store if this page change
    page(page: number): void {
      if (page != this.selectedPage) {
        this.setSelectedPage(page).then(() =>
          // update uri with new page
          this.updateURIFromState()
        );
      }
    },
    // update this page if page in store change
    selectedPage(page: number): void {
      this.page = page;
    },
  },
  mounted() {
    // Set page from uri from store
    this.page = this.selectedPage;
  },
  methods: {
    ...mapActions("postsModule", ["setSelectedPage"]),
    ...mapActions(["updateURIFromState"]),
  },
});
</script>

<style lang="scss" scoped>
.pagination-container {
  margin-top: 2%;
  margin-bottom: 1%;
}
</style>
