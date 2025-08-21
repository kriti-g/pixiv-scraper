from api_wrapper import ApiWrapper
from time import sleep
import os
import logging_utils
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

logger = logging_utils.setup_logging()

# Login
api_wrapper = ApiWrapper(refresh_token=TOKEN, illust_dl_size=DL_SIZE, logger=logger)

# Init
if not os.path.exists(DL_PATH):
    logger.info(f"Setting up core download path at {DL_PATH}.")
    os.makedirs(DL_PATH)

# Init BookmarkScraper
bookmark_scraper = BookmarkScraper(api_wrapper, USER_ID, DL_PATH, logger, INTERVAL)

# Download
search_word = input("Choose bookmark type 'illust' or 'novel'\n")
max_bookmark_id = input("Specify a max bookmark id or hit enter for none.\n")

if search_word.upper() == 'NOVEL':
    bookmark_scraper.download_novels(max_bookmark_id=max_bookmark_id.strip())
if search_word.upper() == 'ILLUST':
    bookmark_scraper.download_illusts(max_bookmark_id=max_bookmark_id.strip())