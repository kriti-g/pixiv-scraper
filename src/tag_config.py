import os
import json
from logging import getLogger
from collections.abc import MutableSequence

class TagConfig:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.config_path = "tag_config.json"

        if os.path.exists(self.config_path):
            with(open(self.config_path, "r")) as f:
                config = json.load(f)
        else:
            with(open(self.config_path, "w")) as f:
                config = { "sorted_tags": {}, "ignored_tags": [], "parents": []}
                json.dump(config, f, indent=4)
        self.sorted_tags: dict = config["sorted_tags"]
        self.ignored_tags: MutableSequence[str] = config["ignored_tags"]
        self.parents: MutableSequence[str] = config["parents"]

    def save(self):
        with(open(self.config_path, "w")) as f:
            json.dump({ "sorted_tags": self.sorted_tags, "ignored_tags": self.ignored_tags, "parents": self.parents }, f, indent=4)

    def read_tag(self, tag: str):
        if tag in self.sorted_tags.keys() or tag in self.ignored_tags or len(tag.strip()) < 1:
            return False
        translated = input(f"Tag: {tag}\nWrite your preferred translation for this tag or hit enter if you'd like to skip\n").strip()

        if len(translated) < 1:
            self.ignored_tags.append(tag)
            self.save()
            return True

        parent_prompt = "Select a parent for this tag to be sorted into, write a new parent name, or hit enter to skip.\n"
        for ind in range(len(self.parents)):
            parent_prompt += f"{ind}. {self.parents[ind]}\n"

        parent = input(parent_prompt).strip()
        if parent.isnumeric() and int(parent) < len(self.parents):
            parent = self.parents[int(parent)]
        elif len(parent) > 0 and parent not in self.parents:
            self.parents.append(parent)

        self.sorted_tags[tag] = { "translated": translated, "parent": parent }
        self.save()
        return True


