from api_wrapper import ApiWrapper
from time import sleep
from tqdm import tqdm
import os
import json
from logging import getLogger

NOVEL_METADATA_FILE_NAME = "__novel_metadata.json"
ILLUST_METADATA_FILE_NAME = "__illust_metadata.json"

class BookmarkScraper:
    def __init__(self, api_wrapper: ApiWrapper, user_id: int, dl_path: str, sleep_interval: 1):
        self.user_id = user_id
        self.dl_path = dl_path
        self.api_wrapper = api_wrapper
        self.sleep_interval = sleep_interval
        self.logger = getLogger(__name__)

    def scrape_novels(self, max_bookmark_id: str | None):
        metadata_path = self.dl_path + "/" + NOVEL_METADATA_FILE_NAME
        novels_to_dump = []
        if os.path.exists(metadata_path):
            with(open(metadata_path, "r")) as f:
                novels_to_dump = json.load(f)

        all_novel_ids = []
        for novel in novels_to_dump:
            all_novel_ids.append(novel["id"])

        json_result = self.api_wrapper.user_bookmarks_novel(self.user_id, max_bookmark_id=max_bookmark_id)

        for novel in json_result.novels:
            if novel.id not in all_novel_ids:
                novels_to_dump.append(novel)
        self.logger.info(f"Scraped {len(json_result.novels)} novel bookmarks for user {str(self.user_id)} (Max bookmark id: {max_bookmark_id})")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(novels_to_dump, f, indent=2)
        if json_result.next_url:
            self.logger.info("Looking for next page.")
            parsed_qs = self.api_wrapper.parse_qs(json_result.next_url)
            sleep(self.sleep_interval)
            self.scrape_novels(max_bookmark_id=parsed_qs['max_bookmark_id'])

    def download_novels(self, max_bookmark_id: str | None):
        json_result = self.api_wrapper.user_bookmarks_novel(self.user_id, max_bookmark_id=max_bookmark_id)
        self.logger.info(f"Found {len(json_result.novels)} novel bookmarks for user {str(self.user_id)} (Max bookmark id: {max_bookmark_id})")
        novel_dl_path = self.dl_path + "/novels"
        self.api_wrapper.mk_dir_if_needed(novel_dl_path)
        skipped_count = 0
        for novel in tqdm(json_result.novels, desc=f"Downloading next page of novels", leave=True):
            str_id = str(novel.id)
            fname = novel_dl_path + "/" + str_id + ".txt"
            if not novel.title:
                self.logger.info(f"Novel {str_id} may have been deleted or access restricted.")
            elif os.path.exists(fname):
                skipped_count += 1
            else:
                self.logger.info("Saving novel: " + str_id)
                novel_result = self.api_wrapper.webview_novel(novel.id)
                if novel_result:
                    with open(fname, "a", encoding="utf-8") as f:
                        f.write(str(novel_result))
                sleep(self.sleep_interval)
        self.logger.info(f"{skipped_count}/{len(json_result.novels)} novels on this page were skipped - already downloaded.")
        if json_result.next_url:
            parsed_qs = self.api_wrapper.parse_qs(json_result.next_url)
            max_bookmark_id = parsed_qs['max_bookmark_id']
            self.download_novels(max_bookmark_id=max_bookmark_id)

    def scrape_illusts(self, max_bookmark_id: str | None):
        metadata_path = self.dl_path + "/" + ILLUST_METADATA_FILE_NAME
        illusts_to_dump = []
        if os.path.exists(metadata_path):
            with(open(metadata_path, "r")) as f:
                illusts_to_dump = json.load(f)

        all_illust_ids = []
        for illust in illusts_to_dump:
            all_illust_ids.append(illust["id"])

        json_result = self.api_wrapper.user_bookmarks_illust(self.user_id, max_bookmark_id=max_bookmark_id)

        for illust in json_result.illusts:
            if illust.id not in all_illust_ids:
                illusts_to_dump.append(illust)

        self.logger.info(f"Scraped {len(json_result.illusts)} illust bookmarks for user {str(self.user_id)} (Max bookmark id: {max_bookmark_id})")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(illusts_to_dump, f, indent=2)
        if json_result.next_url:
            self.logger.info("Looking for next page.")
            parsed_qs = self.api_wrapper.parse_qs(json_result.next_url)
            sleep(self.sleep_interval)
            self.scrape_illusts(max_bookmark_id=parsed_qs['max_bookmark_id'])

    def download_illusts(self, max_bookmark_id: str | None):
        json_result = self.api_wrapper.user_bookmarks_illust(self.user_id, max_bookmark_id=max_bookmark_id)
        illusts_dl_path = self.dl_path + "/illusts"
        self.logger.info(f"Found {len(json_result.illusts)} illust bookmarks for user {str(self.user_id)} (Max bookmark id: {max_bookmark_id})")
        for illust in json_result.illusts:
            self.api_wrapper.download_illust(illust, illusts_dl_path, self.sleep_interval)
        if json_result.next_url:
            self.logger.info("Looking for next page.")
            parsed_qs = self.api_wrapper.parse_qs(json_result.next_url)
            self.download_illusts(max_bookmark_id=parsed_qs['max_bookmark_id'])