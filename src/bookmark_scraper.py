from api_wrapper import ApiWrapper
from time import sleep
from tqdm import tqdm
import os
from logging import Logger

class BookmarkScraper:
    def __init__(self, api_wrapper: ApiWrapper, user_id: int, dl_path: str, logger: Logger,  sleep_interval: 1):
        self.user_id = user_id
        self.dl_path = dl_path + "/bookmarks"
        self.api_wrapper = api_wrapper
        self.sleep_interval = sleep_interval
        self.logger = logger

    def download_novels(self, max_bookmark_id: str | None):
        json_result = self.api_wrapper.user_bookmarks_novel(self.user_id, max_bookmark_id=max_bookmark_id)
        self.logger.info(f"Found novel bookmarks for user {str(self.user_id)} (Max bookmark id: {max_bookmark_id})")
        novel_dl_path = self.dl_path + "/novels"
        self.mk_dir_if_needed(novel_dl_path)
        for novel in tqdm(json_result.novels, desc=f"Downloading next page of novels", leave=True):
            str_id = str(novel.id)
            fname = novel_dl_path + "/" + str_id + ".txt"
            if not novel.title:
                self.logger.info(f"Novel {str_id} may have been deleted or access restricted.")
            elif os.path.exists(fname):
                self.logger.info('Skipping already downloaded novel: ' + str_id)
            else:
                print("Saving novel: " + str_id)
                self.logger.info("Saving novel: " + str_id)
                novel_result = self.api_wrapper.webview_novel(novel.id)
                if novel_result:
                    with open(fname, "a", encoding="utf-8") as f:
                        f.write(str(novel_result))
                sleep(self.sleep_interval)
        if json_result.next_url:
            parsed_qs = self.api_wrapper.parse_qs(json_result.next_url)
            max_bookmark_id = parsed_qs['max_bookmark_id']
            self.download_novels(max_bookmark_id=max_bookmark_id)
        else:
            self.logger.info("Finished downloading all novels.")
            print("Finished.")

    def download_illusts(self, max_bookmark_id: str | None):
        json_result = self.api_wrapper.user_bookmarks_illust(self.user_id, max_bookmark_id=max_bookmark_id)
        illusts_dl_path = self.dl_path + "/illusts"
        self.logger.info(f"Found illust bookmarks for user {str(self.user_id)} (Max bookmark id: {max_bookmark_id})")
        for illust in json_result.illusts:
            self.api_wrapper.download_illust(illust, illusts_dl_path, self.sleep_interval)
        if json_result.next_url:
            self.logger.info("Looking for next page.")
            parsed_qs = self.api_wrapper.parse_qs(json_result.next_url)
            return self.download_illusts(max_bookmark_id=parsed_qs['max_bookmark_id'])
        else:
            print("Finished.")
            return True
