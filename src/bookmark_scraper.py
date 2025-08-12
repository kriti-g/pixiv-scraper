from pixivpy3 import AppPixivAPI
from time import sleep
import os

class BookmarkScraper:
    def __init__(self, api: AppPixivAPI, user_id: int, dl_path: str, sleep_interval: 1):
        self.user_id = user_id
        self.dl_path = dl_path + "/bookmarks"
        self.api = api
        self.sleep_interval = sleep_interval
        if not os.path.exists(self.dl_path):
            os.makedirs(self.dl_path)

    def download_novels(self):
        print("Downloading bookmarked novels for user " + str(self.user_id))
        json_result = self.api.user_bookmarks_novel(self.user_id)

        if json_result:
            print('Found novel bookmarks.')
            novel_dl_path = self.dl_path + "/novels"
            if not os.path.exists(novel_dl_path):
                    os.makedirs(novel_dl_path)
            for novel in json_result.novels:
                str_id = str(novel.id)
                print("Saving novel: " + str_id)
                novel_result = self.api.webview_novel(novel.id)
                if novel_result:
                    with open(novel_dl_path + "/" + str_id + ".txt", "a", encoding="utf-8") as f:
                        f.write(str(novel_result) + "\n\n")
                sleep(self.sleep_interval)

    def download_illusts(self):
        print("Downloading bookmarked images for user " + str(self.user_id))
        json_result = self.api.user_bookmarks_illust(self.user_id)

        if json_result:
            print('Found illust bookmarks.')
            for illust in json_result.illusts:
                str_id = str(illust.id)
                illust_dl_path = self.dl_path + "/" + str_id
                if not os.path.exists(illust_dl_path):
                    os.makedirs(illust_dl_path)
                    print("%s %s" % ("Downloading all for", illust.id))
                    
                    if len(illust.meta_pages) > 1:
                        for page in illust.meta_pages:
                            print("Downloading" + page.image_urls[self.img_dl_size])
                            self.api.download(page.image_urls[self.img_dl_size], path=illust_dl_path)
                            sleep(self.sleep_interval)
                        else:
                            print("Downloading" + illust.image_urls[self.img_dl_size])
                            self.api.download(illust.image_urls[self.img_dl_size], path=illust_dl_path)
                    sleep(self.sleep_interval)
                else:
                    print("Skipping illust " + str_id)
            print("Finished.")
            json_result = None
