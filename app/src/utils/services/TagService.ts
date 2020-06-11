import importedTags from '@/utils/tags/index';
import Tag from '@/models/tag';
import store from '@/store/store';

class TagService {
    public csvFile = '@/utils/tags/index';
    public tags: Tag[] = [];
    public tagsAndSynonyms: string[] = [];
    public filteredtagAndSysnonyms: any;

    /**
     * The constructor initializes the `Tag` list.
     */
    constructor() {
        this.loadTagCsv(importedTags);
        // this.splitSynonyms(importedTags);
        this.removeDuplicatedEntries(this.tagsAndSynonyms);
        this.filteredtagAndSysnonyms.forEach((tag) => {
            store.commit('addTag', tag);
        });
    }

    private loadTagCsv(importedTags): void {
        this.splitSynonyms(importedTags);
        this.getLabelAndSynonymAsStringArray(this.tags);
        // importedTags.forEach((tag) => {
        //    this.tags.push({
        //        label: tag.label,
        //        synonyms: tag.synonyms
        //    });
        //    this.getLabelAndSynonymAsStringArray(tag);
        // });
    }
    private splitSynonyms(tags): void {
        tags.forEach((tag) => {
            if (tag.synonyms) {
                var splittedSynonyms = tag.synonyms.split(',');
                //splittedSynonyms = this.removeWhiteSpaceFromArray(splittedSynonyms);
                // console.log(splittedSynonyms);
                // if (splittedSynonyms.length > 1) {
                splittedSynonyms.forEach((element) => {
                    this.tags.push({
                        label: tag.label,
                        synonyms: element.trim(),
                    });
                });
                // }
            }
        });
    }
    private getLabelAndSynonymAsStringArray(tags): void {
        tags.forEach((element) => {
            this.tagsAndSynonyms.push(element.label);
            this.tagsAndSynonyms.push(element.synonyms);
        });
    }
    private removeWhiteSpaceFromArray(array: string[]) {
        return array.filter((item) => item.charAt(0) !== ' ');
    }
    private removeDuplicatedEntries(duplicatedArray): void {
        this.filteredtagAndSysnonyms = [...new Set(duplicatedArray)];
        this.removeWhiteSpaceFromArray(this.filteredtagAndSysnonyms);
    }
}

const tagServiceInstance = new TagService();

export default tagServiceInstance;

export {
    tagServiceInstance as TagService,
};
