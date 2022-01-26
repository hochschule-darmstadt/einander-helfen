<!-- Component to define keywords/tags for the search. -->

<template>
  <div class="searchBar">
    <v-combobox
      style="background: white"
      rounded
      color="black"
      :placeholder="$t('searchBar.searchBarPlaceholder')"
      item-text="tag"
      autocomplete="off"
      append-icon=""
      :items="searchProposals"
      :search-input.sync="searchValue"
      @change="onInputChange"
      @keyup.enter="onEnter"
      attach=".searchBar"
    >
      <template v-slot:no-data v-if="showNoData">
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>
              {{ $t("searchBar.searchBarText1") }}
              <kbd>{{ $t("searchBar.searchBarEnter") }}</kbd>
              {{ $t("searchBar.searchBarText2") }}
              <v-chip>"{{ searchValue }}"</v-chip>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-combobox>
    <v-spacer />
    <v-chip-group
      active-class="primary-text"
      column
      class="tags"
      v-if="tags.length"
    >
      <v-chip
        v-for="tag in tags"
        :key="tag"
        close
        @click:close="removeTag(tag)"
      >
        {{ tag }}
      </v-chip>
    </v-chip-group>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import TagService from "@/services/TagService";
import Tag from "@/models/tag";

/**
 * Use v-model for input value
 * Emits @remove for remove tag
 * Emits @input for v-model
 */
export default Vue.extend({
  name: "SearchBar",
  props: {
    value: {
      type: String,
      required: true,
    },
    enableNoDataMessage: {
      type: Boolean,
      default: false,
    },
    tags: {
      type: Array as () => string[],
      default: () => [],
    },
  },
  data: function () {
    return {
      searchValue: "",
      allSearchProposals: [] as Tag[],
    };
  },
  mounted(): void {
    this.searchValue = this.value;
    this.allSearchProposals = TagService.getTags();
  },
  watch: {
    /** change searchValue on value change */
    value(): void {
      this.searchValue = this.value;
    },
  },
  computed: {
    /**
     * Gets all proposed tags (ranked) that match the user input.
     *
     * @return {string[]}: An array of all tags that are suitable for the user input.
     */
    searchProposals(): string[] {
      if (!this.searchValue || this.searchValue.length < 1) {
        return [];
      }
      const listOfMatchingTerms = this.filterProposals(
        this.allSearchProposals.filter((el) => "label" in el),
        this.searchValue
      );
      return this.rankTags(listOfMatchingTerms, this.searchValue);
    },
    /** Don't show a list of proposals for tags based on the given user input. */
    showNoData(): boolean {
      return (
        this.enableNoDataMessage &&
        this.searchValue !== null &&
        this.searchValue.length > 0
      );
    },
  },
  methods: {
    /**
     * Filters Tags by searchTerm.
     *
     * @param tags
     * @param {string} searchTerm: The searchTerm used to filter the proposals to be suitable to the user input.
     * @return {string[]}: An array of all suitable proposals.
     */
    filterProposals(tags: Tag[], searchTerm: string): string[] {
      const stringArray: string[] = [];
      searchTerm = searchTerm.toLowerCase();

      tags
        // remove already defined tags
        .filter((tag) => !this.tags.includes(tag.label))
        // filter proposals by tag label or one synonym matches the searchTerm
        .forEach((tag) => {
          if (tag.label.toLowerCase().match(searchTerm)) {
            stringArray.push(tag.label);
          } else {
            tag.synonyms.forEach((element) => {
              if (element.toLowerCase().match(searchTerm)) {
                stringArray.push(tag.label + " (" + element + ")");
              }
            });
          }
        });
      return stringArray;
    },
    /**
     * Rank tags based on how they match searchTerm. Tags that start with searchTerm get rank 2. Tags that end with searchTerm get rank 1.
     * All other Tags (with the searchTerm in the middle) get rank 0.5.
     *
     * @param {string[]} tags: Tags that had a match with the searchTerm.
     *                         Don't use the complete tag list here because then not matching tags would get the rank 0.5.
     * @param {string[]} searchTerm: The given user input to search for.
     * @return {string[]}: A list of all given tags sorted by their tags.
     */
    rankTags(tags: string[], searchTerm: string): string[] {
      return tags
        .map((tag) => {
          // 2x on start; 1x on end, 0.5x in the middle
          const rank = tag.toLowerCase().startsWith(searchTerm.toLowerCase())
            ? 2
            : this.isSuccessiveMatch(
                tag.toLowerCase(),
                searchTerm.toLowerCase()
              )
            ? 1
            : 0.5;
          return {
            label: tag,
            rank,
          };
        })
        .sort((a, b) => Math.sign(b.rank - a.rank))
        .map((obj) => obj.label);
    },
    isSuccessiveMatch(tags: string, searchTerm: string): boolean {
      const sucArr = tags.split(" ");
      if (sucArr.length < 2) return false;

      // Remove the first tag we only want to match successive tags.
      sucArr.shift();
      return !!sucArr.find((element) => {
        return element.startsWith(searchTerm);
      });
    },
    /**
     * The Input text changed
     */
    onInputChange(input: string): void {
      // remove "(" icon from input
      this.searchValue = input.includes(" (")
        ? input.substr(0, input.indexOf(" ("))
        : input;
      // update v-model value
      this.$emit("input", this.searchValue);
    },
    /**
     * Fires an 'enter' event after searchbar enter.
     */
    onEnter(): void {
      this.$emit("enter", this.searchValue);
    },
    /**
     * Fires a 'remove' event when removing a tag.
     */
    removeTag(tag: string): void {
      this.$emit("remove", tag);
    },
  },
});
</script>

<style lang="scss" scoped>
.searchBar {
  background: white;
  border-radius: 25px;
  margin-right: 2%;
  width: inherit;
  display: flex;
  flex-direction: column;
}
.tags {
  margin-left: 10px;
  margin-right: 10px;
  margin-top: -20px;
}
</style>

<style lang="scss">
/** global style */
.searchBar .v-autocomplete__content.v-menu__content {
  top: auto !important;
  left: auto !important;
  margin-top: 50px;
}
</style>
