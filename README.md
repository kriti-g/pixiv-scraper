# pixiv-scraper

## Includes
- Scraping and downloading of illust and novel bookmarks for a given user
- Manual sorting program for all collected tags
  - Program asks for a tag parent (for parent folder) and a user-decided consistency tag.

## Usage
1. Install requirements with `pip install -r requirements.txt`
2. Get your pixiv refresh token with [OAuth with Selenium/ChromeDriver]( https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde) - make sure to scroll to the bottom and use latest recommendations.
3. Run main.py and follow instructions.

**Note**: Edit `config_example.json` and change the name to `config.json`.