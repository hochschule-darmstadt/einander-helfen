import importedTags from '@/utils/tags/index';
import Tag from '@/models/tag';
import store from '@/store/store';

class TagService {
    private tags: Tag[] = [];
    // private tagsAsStringArr: string[] = [];
    // private filteredTagsAsStringArr: any;

    /**
     * The constructor initializes the `Tag` list.
     */
    constructor() {
        this.generateTags();

        // this.removeDuplicateTags(this.tagsAsStringArr);
        this.tags.forEach((tag) => {
            store.commit('addTag', { tag });
        });
    }

    private generateTags(): void {
        // this.splitSynonyms();
        // this.getTagsAsStringArray();
        this.changeSynonymsToStringArray();
    }


    private changeSynonymsToStringArray(): void {
        importedTags.forEach((tag) => {
            if (tag.synonyms) {
                const splittedSynonyms = tag.synonyms.split(',');
                // TODO: Trimming for whitespace element's
                this.tags.push({
                    label: tag.label,
                    synonyms: splittedSynonyms
                });
            } else {
                this.tags.push({
                    label: tag.label,
                    synonyms: []
                });
            }
        });
    }

    private splitSynonyms(): void {
        importedTags.forEach((tag) => {
            if (tag.synonyms) {
                const splittedSynonyms = tag.synonyms.split(',');
                splittedSynonyms.forEach((element) => {
                    this.tags.push({
                        label: tag.label,
                        synonyms: element.trim()
                    });
                });
            } else {
                this.tags.push({
                    label: tag.label,
                    synonyms: []
                });
            }
        });
    }
    private getTagsAsStringArray(): void {
        this.tags.forEach((element) => {
            // this.tagsAsStringArr.push(element.label);
            if (element.synonyms) {
                // this.tagsAsStringArr.push(element.synonyms);
            }
        });
    }

    private removeDuplicateTags(tagsAsStringArr): void {
        // this.filteredTagsAsStringArr = [...new Set(tagsAsStringArr)];
    }
}

const tagServiceInstance = new TagService();

export default tagServiceInstance;

export { tagServiceInstance as TagService };
