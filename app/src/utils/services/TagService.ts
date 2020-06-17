import importedTags from '@/utils/tags/index';
import Tag from '@/models/tag';
import store from '@/store/store';

class TagService {
    private tags: Tag[] = [];
    public getTags(): Tag[] {
        if (!this.tags.length) {
            this.tags = this.changeSynonymsToStringArray();
        }
        return this.tags;
    }


    private changeSynonymsToStringArray(): Tag[] {
        console.log(importedTags);
        return importedTags.map((tag) => {
            const synonyms = tag.synonyms
                ? tag.synonyms.split(',').map((synonym) => synonym.trim())
                : [];

            return {
                label: tag.label,
                synonyms
            };
        });
    }
}

const tagServiceInstance = new TagService();

export default tagServiceInstance;

export { tagServiceInstance as TagService };
