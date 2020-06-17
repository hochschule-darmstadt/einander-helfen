<template>
    <v-combobox
            style="background: white"
            rounded
            color="white"
            label="z.B. Macher/in"
            append-icon="search"
            item-text="tag"
            autocomplete="off"
            :items="mySearchProposals"
            @input="addSearchTag"
            :search-input.sync="currentSearchValue"
    ></v-combobox>
</template>

<script lang="ts">
import Vue from 'vue';
import TagService from '@/utils/services/TagService';
import Tag from '@/models/tag';
import {mapActions, mapState} from 'vuex';

export default Vue.extend({
    data(): {
        currentSearchValue: string
    } {
        return {
            currentSearchValue: ''
        };
    },
    created(): void {
        this.initializeSearchProposals(TagService.getTags());
    },
    watch: {
        selectedTag(newValue): void {
            this.setSelectedTag(newValue);
        },
    },
    computed: {
        ...mapState(['searchProposals', 'selectedLocation', 'radiusSearchValue']),
        mySearchProposals(): string[] {
            if (!this.currentSearchValue || this.currentSearchValue.length < 1) {
                return [];
            }
            const searchTerm = this.currentSearchValue;
            const listOfMatchingTerms = this.matchSearchInput(searchTerm, this.searchProposals
                    .filter((element) => 'label' in element));
            const rankedListOfOrderedTerms = this.rankTerms(searchTerm, listOfMatchingTerms);

            return rankedListOfOrderedTerms;
        }
    },
    methods: {
        ...mapActions(['initializeSearchProposals', 'setSelectedTag']),
        matchSearchInput(searchTerm: string, proposals: Tag[]): string[] {
            const stringArray: string[] = [];
            searchTerm = searchTerm.toLowerCase();

            proposals.forEach((tag) => {
                if (tag.label.toLowerCase().match(searchTerm)) {
                    stringArray.push(tag.label);
                } else {
                    tag.synonyms.forEach((element) => {
                        if (element.toLowerCase().match(searchTerm)) {
                            stringArray.push(tag.label + ' (' + element + ')');
                        }
                    });
                }
            });
            stringArray.length = 10;
            return stringArray;
        },
        rankTerms(searchTerm: string, terms: string[]): string[] {
            return terms.map((term) => {
                // 2x on start; 1x on end, 0.5x in the middle
                const rank = term.toLowerCase().startsWith(searchTerm.toLowerCase())
                        ? 2
                        : this.isSuccessiveMatch(term.toLowerCase(), searchTerm.toLowerCase())
                                ? 1
                                : 0.5;
                return {
                    label: term,
                    rank
                };
            })
                    .sort((a, b) => Math.sign(b.rank - a.rank))
                    .map((obj) => obj.label);
        },
        addSearchTag(tag: string): void {

            const tagName = tag.includes(' (')
                    ? tag.substr(0, tag.indexOf(' ('))
                    : tag;

            this.$emit('input', tagName);
        },
        isSuccessiveMatch(term: string, searchTerm: string): boolean {
            var isSuccessive: boolean = false;
            const sucArr = term.split(" ");
            if (sucArr.length < 2) {
                return false;
            }
            sucArr.forEach(element => {
                if (element.startsWith(searchTerm)) {
                    isSuccessive = true;
                }
            });
            return isSuccessive;
        }
    }
});
</script>

<style scoped>

</style>
