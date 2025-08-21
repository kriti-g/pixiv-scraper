import backoff
import os
from pixivpy3 import AppPixivAPI
from logging import Logger
from datetime import datetime
from time import sleep
from http.client import RemoteDisconnected
from urllib3.exceptions import IncompleteRead
from pixivpy3 import PixivError
from tqdm import tqdm

class ApiWrapper:
    def __init__(self, refresh_token: str,  illust_dl_size: str, logger: Logger):
        self.refresh_token = refresh_token
        self.illust_dl_size = illust_dl_size
        self.logger = logger

        logger.info("Initialising Pixiv API.")
        self.api = AppPixivAPI()
        self.api.auth(refresh_token=refresh_token)
        logger.info("Starting timer.")
        self.last_refresh = datetime.now()

    @backoff.on_exception(backoff.expo, (RemoteDisconnected, PixivError), max_time=300)    
    def refresh_auth_if_needed(self): 
        seconds_since_last_refresh = (datetime.now() - self.last_refresh).total_seconds()
        if seconds_since_last_refresh > 3400:
            self.logger.info(f"{seconds_since_last_refresh} seconds passed, refreshing API auth and resetting timer.")
            self.api.auth(refresh_token=self.refresh_token)
            self.last_refresh = datetime.now()
    
    def download_illust(self, illust, illusts_dl_path, sleep_interval):
        str_id = str(illust.id)
        illust_dl_path = illusts_dl_path + "/" + str_id + "/"
        skipped_count = 0
        if len(illust.meta_pages) > 0:
            pages = illust.meta_pages
        else:
            if illust.title:
                illust.image_urls['original'] = illust.meta_single_page.original_image_url
            pages = [illust]
        for page in tqdm(pages, desc=f"Downloading pages from {str_id}", leave=True):
            if not self.download_img(page, path=illust_dl_path, sleep_interval=sleep_interval):
                skipped_count += 1
        if skipped_count > 0:
            self.logger.info(f"Skipped {skipped_count}/{len(pages)} pages for {str_id}.")
        self.logger.info(f"Completed {str_id}.")

    @backoff.on_exception(backoff.expo, (RemoteDisconnected, PixivError), max_time=300)       
    def download_img(self, img, path, sleep_interval: 1):
        url = None
        if self.illust_dl_size in img.image_urls.keys():
            url = img.image_urls[self.illust_dl_size]

        if not url:
            self.logger.info(f"Can't find URL for: {str(img.id)}")
            return False
        
        self.mk_dir_if_needed(path)
        for _ in range(2):
            try:
                self.refresh_auth_if_needed()
                if self.api.download(url=url, path=path, replace=False):
                    self.logger.info(f"Downloaded image at {url}")
                    sleep(sleep_interval)
                    return True
            except IncompleteRead:
                self.logger.error("IncompleteRead exception while trying to download.")
                self.delete_half_completed(url, path)
        return False
        
    def delete_half_completed(self, url, path):
        name = str(os.path.basename(url))
        file_path = os.path.join(path, name)
        self.logger.info(f"Attempting to remove path {file_path}")
        if os.path.exists(file_path):
            os.remove(file_path)
            self.logger.info(f"Removed path {file_path}")
    
    def mk_dir_if_needed(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def user_bookmarks_novel(self, user_id, max_bookmark_id):
        self.refresh_auth_if_needed()
        return self.api.user_bookmarks_novel(user_id=user_id, max_bookmark_id=max_bookmark_id)
    
    def user_bookmarks_illust(self, user_id, max_bookmark_id):
        self.refresh_auth_if_needed()
        return self.api.user_bookmarks_illust(user_id=user_id, max_bookmark_id=max_bookmark_id)
    
    def parse_qs(self, url):
        return self.api.parse_qs(url)
    
    def webview_novel(self, novel_id):
        self.refresh_auth_if_needed()
        return self.api.webview_novel(novel_id=novel_id)