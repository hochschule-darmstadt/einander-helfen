import importedTags from '@/utils/tags/index';
import Tag from '@/models/tag';
import store from '@/store/store';

class TagService {
    private tags: Tag[] = [];
    private tagsAsStringArr: string[] = [];
    private filteredTagsAsStringArr: any;

    /**
     * The constructor initializes the `Tag` list.
     */
    constructor() {
        this.generateTags();
        this.removeDuplicateTags(this.tagsAsStringArr);
        this.filteredTagsAsStringArr.forEach((tag) => {
            store.commit('addTag', tag);
        });
    }

    private generateTags(): void {
        this.splitSynonyms();
        this.getTagsAsStringArray();
    }
    //TODO: I think this ignores tags without synonym. So we dont have those in our list!!
    private splitSynonyms(): void {
        importedTags.forEach((tag) => {
            if (tag.synonyms) {
                var splittedSynonyms = tag.synonyms.split(',');
                splittedSynonyms.forEach((element) => {
                    this.tags.push({
                        label: tag.label,
                        synonyms: element.trim(),
                    });
                });
            }
        });
    }
    private getTagsAsStringArray(): void {
        this.tags.forEach((element) => {
            this.tagsAsStringArr.push(element.label);
            this.tagsAsStringArr.push(element.synonyms);
        });
    }

    private removeDuplicateTags(tagsAsStringArr): void {
        this.filteredTagsAsStringArr = [...new Set(tagsAsStringArr)];
    }
}

const tagServiceInstance = new TagService();

export default tagServiceInstance;

export {
    tagServiceInstance as TagService,
};
