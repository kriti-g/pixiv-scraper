from api_wrapper import ApiWrapper
import logging_utils
from config import Config
from bookmark_scraper import BookmarkScraper
from bookmark_sorter import BookmarkSorter

POSSIBLE_ACTIONS = {
    "1": "Download",
    "2": "Scrape",
    "3": "Sort and TL tags",
    "4": "Sort and tag all downloads"
}

def get_bookmark_scraper() -> BookmarkScraper:
    config = Config()
    config.load_and_fill("config.json", for_downloads=True)
    api_wrapper = ApiWrapper(refresh_token=config.refresh_token, illust_dl_size=config.download_size)
    return BookmarkScraper(api_wrapper, config.user_id, config.download_path + "/bookmarks", config.interval)

def get_bookmark_sorter() -> BookmarkSorter:
    config = Config()
    config.load_and_fill("config.json", for_downloads=False)
    return BookmarkSorter(config.download_path + "/bookmarks")

def main():
    logger = logging_utils.setup_logging()
    try:
        action_prompt = "What would you like to do?\n"
        for key, action in POSSIBLE_ACTIONS.items():
            action_prompt += f"{key} - {action}\n"

        chosen_action = input(action_prompt).strip()
        search_word = input("Choose bookmark type 'illust' or 'novel'\n").strip().upper() if chosen_action in ["1", "2"] else None
        max_bookmark_id = input("Specify a max bookmark id or hit enter for none.\n").strip() if chosen_action in ["1", "2"] else None

        match([chosen_action, search_word]):
            case ['1', 'NOVEL']:
                get_bookmark_scraper().download_novels(max_bookmark_id=max_bookmark_id)
            case ['2', 'NOVEL',]:
                get_bookmark_scraper().scrape_novels(max_bookmark_id=max_bookmark_id)
            case ['1', 'ILLUST']:
                get_bookmark_scraper().download_illusts(max_bookmark_id=max_bookmark_id)
            case ['2', 'ILLUST']:
                get_bookmark_scraper().scrape_illusts(max_bookmark_id=max_bookmark_id)
            case ['3', None]:
                get_bookmark_sorter().sort_all_tags()

        logger.info(f"Finished action: {POSSIBLE_ACTIONS[chosen_action]}.")

        do_again = input("Finished. Do something else? Y/N\n").strip().upper()
        if do_again == "Y":
            return main()
    except KeyboardInterrupt:
        logger.info("User closing program.\n")
        exit(0)


if __name__ == "__main__":
    main()
