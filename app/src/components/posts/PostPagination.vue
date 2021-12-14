<!-- Pagination of the list of posts. -->

<template>
  <div class="pagination-container text-center">
    <v-pagination
      v-model="page"
      :length="totalPages"
      :total-visible="buttonsCount"
      color="#054C66"
    />
    <span class="pl-2 mt-2 d-inline-block font-italic">
      {{ totalResultSize }} Ergebnisse
    </span>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { mapActions, mapGetters, mapState } from "vuex";

export default Vue.extend({
  name: "PostPagination",
  data: function () {
    return {
      page: 1,
      buttonsCount: 7,
    };
  },
  computed: {
    ...mapState("postsModule", ["totalResultSize", "selectedPage"]),
    ...mapGetters("postsModule", ["totalPages"]),
  },
  watch: {
    // update page in store if this page change
    async page(page: number): Promise<void> {
      if (page != this.selectedPage) {
        await this.setSelectedPage(page);
        this.updateURIFromState();
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
  margin-top: 1%;
  margin-bottom: 1%;
}
</style>
