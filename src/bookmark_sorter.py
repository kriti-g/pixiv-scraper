from tag_config import TagConfig
import os
import json
from logging import getLogger

NOVEL_METADATA_FILE_NAME = "__novel_metadata.json"
ILLUST_METADATA_FILE_NAME = "__illust_metadata.json"

class BookmarkSorter:
    def __init__(self, dl_path: str):
        self.dl_path = dl_path
        self.logger = getLogger(__name__)

    def all_tag_names_for(self, path):
        all_tags_names = []
        if os.path.exists(path):
            with(open(path, "r")) as f:
                taggables_to_sort = json.load(f)
                for taggable in taggables_to_sort:
                    for tag in taggable["tags"]:
                        all_tags_names.append(tag["name"])
        return all_tags_names

    def sort_all_tags(self):
        tag_config = TagConfig()
        novel_metadata_path = self.dl_path + "/" + NOVEL_METADATA_FILE_NAME
        illust_metadata_path = self.dl_path + "/" + ILLUST_METADATA_FILE_NAME
        tags_to_sort = self.all_tag_names_for(novel_metadata_path) + self.all_tag_names_for(illust_metadata_path)

        print(f"{len(tag_config.ignored_tags) + len(tag_config.sorted_tags.keys())}/{len(set(tags_to_sort))} sorted so far.")
        for tag in tags_to_sort:
            tag_config.read_tag(tag)

        tag_config.save()