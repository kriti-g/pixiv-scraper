from pixivpy3 import AppPixivAPI
from time import sleep
import os

from config import Config
from bookmark_scraper import BookmarkScraper

# Parameters
config = Config()
if os.path.exists("config.json"):
    config.load("config.json")
else:
    config.input_refresh_token()
    config.input_user_id()
    config.save("config.json")

TOKEN = config.refresh_token
DL_PATH = config.download_path
INTERVAL = config.interval
DL_SIZE = config.download_size
USER_ID = config.user_id

# Login
api = AppPixivAPI()
api.auth(refresh_token=TOKEN)

# Init
if not os.path.exists(DL_PATH):
    os.makedirs(DL_PATH)

# Init BookmarkScraper
bookmark_scraper = BookmarkScraper(api, USER_ID, DL_PATH, sleep_interval=INTERVAL)

# Download
search_word = input("Choose bookmark type 'illust' or 'novel'\n")

if search_word.upper() == 'NOVEL':
    bookmark_scraper.download_novels()
if search_word.upper() == 'ILLUST':
    bookmark_scraper.download_illusts()