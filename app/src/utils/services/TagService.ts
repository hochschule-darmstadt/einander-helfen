import tags from '@/utils/tags/index';
import Tag from '@/models/tag';

class TagService {
    public csvFile = '@/utils/tags/index';
    public tags: Tag[] = [];

    /**
     * The constructor initializes the `Location` list.
     */
    constructor() {
        this.loadTagCsv('s');
    }

    private loadTagCsv(csvFile): void {
        tags.forEach((tag) => {
            this.tags.push({
                label: tag.label,
                synonyms: tag.synonyms,
            });
        });
    }
}

const tagServiceInstance = new TagService();

export default tagServiceInstance;

export {
    tagServiceInstance as TagService,
};
