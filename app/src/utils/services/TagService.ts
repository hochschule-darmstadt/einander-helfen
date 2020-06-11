import importedTags from '@/utils/tags/index';
import Tag from '@/models/tag';
import store from '@/store/store';

class TagService {
    public csvFile = '@/utils/tags/index';
    public tags: Tag[] = [];

    /**
     * The constructor initializes the `Tag` list.
     */
    constructor() {
        this.loadTagCsv('s');
        this.splitSynonyms(importedTags);
        importedTags.forEach((tag) => {
            store.commit('addTag', tag.label);
            store.commit('addTag', tag.synonyms);
        });
    }

    private loadTagCsv(csvFile): void {

        importedTags.forEach((tag) => {
            this.tags.push({
                label: tag.label,
                synonyms: tag.synonyms,
            });
        });
    }
    private splitSynonyms(tags): void {
        tags.forEach((tag) => {
            if (tag.synonyms) {
                const splittedSynonyms = tag.synonyms.split(',');
                if (splittedSynonyms.length > 1) {
                    splittedSynonyms.forEach((element) => {
                        this.tags.push({
                            label: tag.label,
                            synonyms: element
                        });
                    });
                }
            }
        });
        console.log(tags);
    }
}

const tagServiceInstance = new TagService();

export default tagServiceInstance;

export {
    tagServiceInstance as TagService,
};
