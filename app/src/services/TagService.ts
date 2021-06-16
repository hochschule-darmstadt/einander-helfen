/**
 * This service provides the methods to find tags in the database with Elastic Search.
 */

import importedTags from "@/resources/tags/index";
import Tag from "@/models/tag";

/**
 * this service manage all static tags from resources
 */
class TagService {
  private tags: Tag[] = [];

  public getTags(): Tag[] {
    if (!this.tags.length) {
      this.tags = this.changeSynonymsToStringArray();
    }
    return this.tags;
  }

  private changeSynonymsToStringArray(): Tag[] {
    return importedTags.map((tag) => {
      const synonyms = tag.synonyms
        ? tag.synonyms.split(",").map((synonym) => synonym.trim())
        : [];

      return {
        label: tag.label,
        synonyms,
      };
    });
  }
}

const tagServiceInstance = new TagService();

export default tagServiceInstance;
