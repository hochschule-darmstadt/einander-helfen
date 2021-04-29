<template>
  <div class="searchBar">
    <v-combobox
      style="background: white"
      rounded
      color="black"
      placeholder="z. B. Jugendarbeit"
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
              Drücken Sie
              <kbd>Enter</kbd> für eine Freitextsuche mit Ihrer Eingabe
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
import TagService from "@/utils/services/TagService";
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
    searchProposals(): string[] {
      if (!this.searchValue || this.searchValue.length < 1) {
        return [];
      }
      const listOfMatchingTerms = this.filterProposals(
        this.allSearchProposals.filter((el) => "label" in el),
        this.searchValue
      );
      const rankedListOfOrderedTerms = this.rankTerms(
        listOfMatchingTerms,
        this.searchValue
      );

      return rankedListOfOrderedTerms;
    },
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
     * Filters Tags by searchTerm and return list of proposals
     */
    filterProposals(proposals: Tag[], searchTerm: string): string[] {
      const stringArray: string[] = [];
      searchTerm = searchTerm.toLowerCase();

      proposals
        // remove already defined tagas
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
     * Rank terms by a searchterm
     */
    rankTerms(terms: string[], searchTerm: string): string[] {
      return terms
        .map((term) => {
          // 2x on start; 1x on end, 0.5x in the middle
          const rank = term.toLowerCase().startsWith(searchTerm.toLowerCase())
            ? 2
            : this.isSuccessiveMatch(
                term.toLowerCase(),
                searchTerm.toLowerCase()
              )
            ? 1
            : 0.5;
          return {
            label: term,
            rank,
          };
        })
        .sort((a, b) => Math.sign(b.rank - a.rank))
        .map((obj) => obj.label);
    },
    isSuccessiveMatch(term: string, searchTerm: string): boolean {
      const sucArr = term.split(" ");
      if (sucArr.length < 2) return false;

      // Remove the first term we only want to match successive terms
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
     * On searchbar enter
     */
    onEnter(): void {
      this.$emit("input", this.searchValue);
      this.$emit("enter");
    },
    removeTag(tag: string): void {
      this.$emit("remove", tag);
    },
  },
});
</script>

<style lang="scss" scoped>
.searchBar {
  background: white;
  border-radius: 28px;
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
