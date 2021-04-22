<template>
  <v-combobox
    style="background: white"
    rounded
    color="black"
    placeholder="z. B. Jugendarbeit"
    item-text="tag"
    autocomplete="off"
    :items="mySearchProposals"
    @input="addSearchTag"
    append-icon=""
    :search-input.sync="mySearchValue"
    @keydown.enter="$emit('enter')"
    :attach="attachTo"
  >
    <template v-slot:no-data v-if="showNoData">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>
            Drücken Sie
            <kbd>Enter</kbd> für eine Freitextsuche mit Ihrer Eingabe
            <v-chip>"{{ mySearchValue }}"</v-chip>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </template>
  </v-combobox>
</template>

<script lang="ts">
import Vue from "vue";
import TagService from "@/utils/services/TagService";
import Tag from "@/models/tag";
import { createNamespacedHelpers } from "vuex";
const { mapState, mapActions } = createNamespacedHelpers("textSearchModule");

export default Vue.extend({
  props: {
    searchInput: String,
    enableNoDataMessage: {
      type: Boolean,
      default: false,
    },
    attachTo: {
      type: String,
      default: "",
    },
  },
  data: function () {
    return {
      mySearchValue: this.searchInput || "",
    };
  },
  created(): void {
    this.initializeSearchProposals(TagService.getTags());
  },
  watch: {
    selectedTag(newValue): void {
      this.setSelectedTag(newValue);
    },
    mySearchValue(value): void {
      this.$emit("update:searchInput", value);
    },
  },
  computed: {
    ...mapState(["searchProposals", "searchValues"]),
    mySearchProposals(): string[] {
      if (!this.mySearchValue || this.mySearchValue.length < 1) {
        return [];
      }
      const searchTerm = this.mySearchValue;
      const listOfMatchingTerms = this.matchSearchInput(
        searchTerm,
        this.searchProposals.filter((element) => "label" in element)
      );
      const rankedListOfOrderedTerms = this.rankTerms(
        searchTerm,
        listOfMatchingTerms
      );

      return rankedListOfOrderedTerms;
    },
    showNoData(): boolean {
      return (
        this.enableNoDataMessage &&
        this.mySearchValue !== null &&
        this.mySearchValue.length > 0
      );
    },
  },
  methods: {
    ...mapActions(["initializeSearchProposals", "setSelectedTag"]),
    matchSearchInput(searchTerm: string, proposals: Tag[]): string[] {
      const stringArray: string[] = [];
      searchTerm = searchTerm.toLowerCase();

      proposals
        .filter((tag) => !this.searchValues.includes(tag.label))
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
    rankTerms(searchTerm: string, terms: string[]): string[] {
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
    addSearchTag(tag: string): void {
      // No empty tags!
      if (!tag) return;

      const tagName = tag.includes(" (")
        ? tag.substr(0, tag.indexOf(" ("))
        : tag;
      this.$emit("input", tagName);
    },
    clearInput(): void {
      this.$nextTick(() => (this.mySearchValue = ""));
    },
  },
});
</script>
